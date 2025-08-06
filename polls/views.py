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

