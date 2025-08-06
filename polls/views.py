from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from django.db.models import Count
from .models import Polls, Questions, Options
from .serializers import PollsSerializer, QuestionsSerializer, VotesSerializer
from .permissions import PollPermission

class PollsViewSet(viewsets.ModelViewSet):
    queryset = Polls.objects.all()
    serializer_class = PollsSerializer
    permission_classes = [PollPermission]

    def get_queryset(self):
        # Optional: return only polls created by the user
        return self.queryset.filter(created_by=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def close(self, request, pk=None):
        poll = self.get_object()
        if poll.created_by != request.user:
            return Response({'detail': 'Not allowed to close this poll.'}, status=status.HTTP_403_FORBIDDEN)
        if poll.is_closed:
            return Response({'detail': 'Poll already closed.'}, status=status.HTTP_400_BAD_REQUEST)

        poll.close()
        return Response({'detail': 'Poll closed successfully.'})
    
    @action(detail=True, methods=["get"])
    def results(self, request, pk=None):
        """
        This function gets results of all questions in a poll
        """
        try:
            poll = self.get_object()
        except Polls.DoesNotExist:
            return Response({"detail": "Poll not found."}, status=404)
        
        results = {
            "poll_id": poll.poll_id,
            "poll_title": poll.title,
            "questions": []
        }

        questions = Questions.objects.filter(poll_id=poll).order_by('-created_at')
        
        for question in questions:
            options = Options.objects.filter(question_id=question.question_id).annotate(
                vote_count=Count('votes')
            )
            total_votes = sum([opt.vote_count for opt in options]) or 1  # avoid division by 0

            question_result = {
                "question_id": question.question_id,
                "question_text": question.question_text,
                "total_votes": total_votes if total_votes != 1 else 0,
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

        return Response(results, status=200)


class QuestionsViewSet(viewsets.ModelViewSet):
    """
    
    """
    queryset = Questions.objects.all()
    serializer_class = QuestionsSerializer
    permission_classes = [PollPermission]

    def get_queryset(self):
        # return only questions under a poll
        return self.queryset.filter(poll_id=self.kwargs['poll_pk'], poll_id__created_by=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save()

class VoteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, poll_id, question_id):
        try:
            question = Questions.objects.get(pk=question_id, poll_id=poll_id)
        except Questions.DoesNotExist:
            return Response({"detail": "Invalid question or poll."}, status=404)

        serializer = VotesSerializer(
            data=request.data,
            context={
                "request": request,
                "question": question
            }
        )

        if serializer.is_valid():
            serializer.save(user_id=request.user)
            return Response({"detail": "Vote recorded."}, status=201)

        return Response(serializer.errors, status=400)

