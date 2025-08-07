from polls.models import Options, Questions
from .serializers import VotesSerializer
from rest_framework.exceptions import PermissionDenied
from django.db.models import Count

def handle_vote(request, question):
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
    if poll.created_by != user:
        raise PermissionDenied("Not allowed to close this poll.")
    if poll.is_closed:
        return "Poll already closed."

    poll.close()
    return "Poll closed successfully."

def handle_result(poll):
        results = {
            "poll_id": poll.poll_id,
            "poll_title": poll.title,
            "questions": []
        }

        questions = Questions.objects.filter(poll_id=poll).order_by('-created_at')
        
        for question in questions:
            options = Options.objects.filter(question_id=question.question_id).annotate(
                vote_count=Count('votes')
            ) # get all options under the specified question in the loop and joins and aggregate the total votes

            total_votes = sum(opt.vote_count for opt in options) # get the total votes in a question

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

