from rest_framework import serializers
from .models import Polls, Questions, Options, Votes
import uuid
from datetime import datetime, timezone

class PollsSerializer(serializers.ModelSerializer):
    """
    Handles serialization and creation logic for polls,
    including automatic assignment of the creator.
    """
    class Meta:
        model = Polls
        fields = ['poll_id', 'title', 'description', 'created_by', 'expires_at', 'is_closed', 'created_at', 'is_public']
        read_only_fields = ['created_by', 'created_at']

    def create(self, validated_data):
        # Sets the logged-in user as the poll creator before saving.
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)
    
class OptionSerializer(serializers.ModelSerializer):
    """
    Serializes poll options (used within questions),
    allowing only basic fields.
    """
    class Meta:
        model = Options
        fields = ['option_id', 'option_text']

class QuestionsSerializer(serializers.ModelSerializer):
    """
    Serializes questions along with their options
    and manages nested creation of options.
    """
    options = OptionSerializer(many=True)

    class Meta:
        model = Questions
        fields = ['question_id', 'poll_id', 'question_text', 'question_type', 'options']
        read_only_fields = ['poll_id', 'created_at']

    def create(self, validated_data):
        # Creates a new question under a specified poll and saves its options.
        options_data = validated_data.pop('options')
        poll_id = self.context['view'].kwargs.get('poll_pk')

        try:
            poll = Polls.objects.get(pk=poll_id)
        except Polls.DoesNotExist:
            raise serializers.ValidationError("Invalid poll ID")

        question = Questions.objects.create(poll_id=poll, **validated_data)
        # creates option nested in the options list
        for option_data in options_data:
            Options.objects.create(question_id=question, **option_data)
        return question

class VotesSerializer(serializers.ModelSerializer):
    """
    Handles validation and creation of votes,
    enforcing voting rules and poll status.
    """
    class Meta:
        model = Votes
        fields = ['vote_id', 'option_id', 'user_id', 'created_at']
        read_only_fields = ['vote_id', 'created_at', 'user_id']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Restrict the options to those under the current question
        question = self.context.get("question")
        if question:
            self.fields['option_id'].queryset = question.options.all()

    def validate_option_id(self, option):
        # Ensures the selected option belongs to the current question.
        question = self.context['question']
        if option.question_id != question:
            raise serializers.ValidationError("This option doesn't belong to the question.")
        return option

    def validate(self, attrs):
        # Prevents multiple votes on single-choice questions and 
        # blocks voting on closed or expired polls.
        user = self.context['request'].user
        option = attrs['option_id']
        question = option.question_id
        poll = question.poll_id

        # Check if user already voted (single choice)
        if question.question_type == Questions.SINGLE:
            if Votes.objects.filter(user_id=user, option_id__question_id=question).exists():
                raise serializers.ValidationError("You have already voted on this question.")
            
        
        has_expired = poll.expires_at is not None and datetime.now(timezone.utc) > poll.expires_at
        # Check if poll is active
        if poll.is_closed or has_expired :
            raise serializers.ValidationError("Voting is closed or expired for this poll.")

        return attrs
    
    def create(self, validated_data):
        # Creates and saves a vote with a unique ID and the authenticated user.
        return Votes.objects.create(
            vote_id=uuid.uuid4(),
            option_id=validated_data['option_id'],
            user_id=self.context['request'].user
        )
    
class ClosePollSerializer(serializers.Serializer):
    """
    Empty serializer for closing a poll.
    Can be extended later to accept confirmation or comments.
    """
    pass

