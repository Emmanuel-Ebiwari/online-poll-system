from polls.models import Options, Questions
from .serializers import VotesSerializer
from rest_framework.exceptions import PermissionDenied
from django.db.models import Count, Prefetch

def handle_vote(request, question):
    """
    Handles the logic for casting a vote on a given question.

    - Validates the incoming vote data using `VotesSerializer`
    - Associates the vote with the currently authenticated user
    - Saves the vote to the database
    - Returns the serialized vote data
    """
    serializer = VotesSerializer(
        data=request.data,
        context={
            "request": request,
            "question": question
        }
    )

    serializer.is_valid(raise_exception=True)
    serializer.save(user_id=request.user)

    return serializer

def close_poll(poll, user):
    """
    Closes a poll if the requesting user is the creator.

    - Checks if the user is authorized to close the poll
    - Prevents re-closing an already closed poll
    - Invokes the model’s `.close()` method to update the poll state
    - Returns a success or info message
    """
    if poll.created_by != user:
        raise PermissionDenied("Not allowed to close this poll.")
    if poll.is_closed:
        return "Poll already closed."

    poll.close()
    return "Poll closed successfully."

def handle_result(poll):
    """
    Generates a structured result summary for a poll.
    
    - Prefetches all questions and their related options and votes using optimized queries
    - Annotates each option with its total vote count
    - Builds a response containing:
        - Each question's details
        - Total votes per question
        - All options with their vote counts and percentages
    - Returns the full result as a nested dictionary
    """
    results = {
        "poll_id": poll.poll_id,
        "poll_title": poll.title,
        "questions": []
    }

    # Prefetch votes for each option
    option_qs = Options.objects.annotate(vote_count=Count('votes')).prefetch_related('votes')
    # Prefetch options for each question (and their votes)
    question_qs = Questions.objects.filter(poll_id=poll).order_by('-created_at').prefetch_related(
        Prefetch('options', queryset=option_qs, to_attr='prefetched_options')
    )
    
    for question in question_qs:
        options = question.prefetched_options
        total_votes = sum(opt.vote_count for opt in options)
        question_result = {
            "question_id": question.question_id,
            "question_text": question.question_text,
            "total_votes": total_votes,
            "options": [
                {
                    "option_id": str(opt.option_id),
                    "option_text": opt.option_text,
                    "vote_count": opt.vote_count,
                    "percentage": round((opt.vote_count / total_votes) * 100, 2) if total_votes > 0 else 0
                }
                for opt in options
            ]
        }

        results['questions'].append(question_result)

    return results

