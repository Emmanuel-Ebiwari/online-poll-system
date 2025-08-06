from rest_framework import serializers
from .models import Polls, Questions, Options, Votes
import uuid
from datetime import datetime, timezone

class PollsSerializer(serializers.ModelSerializer):
    """
    Custom serializer for specific use cases.
    This can be extended with additional fields or methods as needed.
    """
    class Meta:
        model = Polls
        fields = ['poll_id', 'title', 'description', 'created_by', 'expires_at', 'is_closed', 'created_at']
        read_only_fields = ['created_by', 'created_at']

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)
    
class OptionSerializer(serializers.ModelSerializer):
    """
    Custom serializer for specific use cases.
    This can be extended with additional fields or methods as needed.
    """
    class Meta:
        model = Options
        fields = ['option_id', 'option_text']

class QuestionsSerializer(serializers.ModelSerializer):
    """
    Custom serializer for specific use cases.
    This can be extended with additional fields or methods as needed.
    """
    options = OptionSerializer(many=True)

    class Meta:
        model = Questions
        fields = ['question_id', 'poll_id', 'question_text', 'options', 'question_type']
        read_only_fields = ['poll_id', 'created_at']
        # fields = ['question_id', 'poll_id', 'text', 'question_type', 'options']

    def create(self, validated_data):
        options_data = validated_data.pop('options')
        poll_id = self.context['view'].kwargs.get('poll_pk')

        try:
            poll = Polls.objects.get(pk=poll_id)
        except Polls.DoesNotExist:
            raise serializers.ValidationError("Invalid poll ID")

        question = Questions.objects.create(poll_id=poll, **validated_data)
        for option_data in options_data:
            Options.objects.create(question_id=question, **option_data)
        return question

class VotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Votes
        fields = ['vote_id', 'option_id', 'user_id', 'created_at']
        read_only_fields = ['vote_id', 'created_at', 'user_id']

    def validate_option_id(self, option):
        question = self.context['question']
        if option.question_id != question:
            raise serializers.ValidationError("This option doesn't belong to the question.")
        return option

    def validate(self, attrs):
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
        return Votes.objects.create(
            vote_id=uuid.uuid4(),
            option_id=validated_data['option_id'],
            user_id=self.context['request'].user
        )

