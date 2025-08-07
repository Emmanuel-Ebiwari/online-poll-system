from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Polls, Questions
from .serializers import ClosePollSerializer, PollsSerializer, QuestionsSerializer, VotesSerializer
from .permissions import PollPermission, VotePermission, QuestionPermission
from .services import handle_result, handle_vote, close_poll

class PollsViewSet(viewsets.ModelViewSet):
    """
    Handles CRUD operations for polls, including listing,
    creation, closing, and viewing results.
    """
    queryset = Polls.objects.all()
    serializer_class = PollsSerializer
    permission_classes = [PollPermission]

    def get_queryset(self):
        """
        Returns polls that are public or owned by the
        authenticated user. Anonymous users see only public polls.
        """
        user = self.request.user

        if user.is_authenticated and user.is_superuser:
            # Superusers can see all polls
            return Polls.objects.all().order_by('-created_at')

        if user.is_authenticated:
            return Polls.objects.filter(Q(created_by=user) | Q(is_public=True))
        return Polls.objects.filter(is_public=True).order_by('-created_at').order_by('-created_at')

    def perform_create(self, serializer):
        # Sets the created_by field to the current user when creating a new poll.
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated], serializer_class=ClosePollSerializer)
    def close(self, request, pk=None):
        """
        Allows poll owners to manually close a poll.
        Returns an error if not the owner or already closed.
        """
        poll = self.get_object()
        message = close_poll(poll, request.user)
        return Response({'detail': message})
    
    @action(detail=True, methods=["get"], permission_classes=[PollPermission])
    def results(self, request, pk=None):
        """
        Returns the results of a specific poll, 
        including each question and its options with vote counts and percentages.
        """
        try:
            poll = self.get_object()
        except Polls.DoesNotExist:
            return Response({"detail": "Poll not found."}, status=404)

        results = handle_result(poll)

        return Response(results, status=200)

class QuestionsViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing poll questions with visibility rules:
    - Unauthenticated users see only questions from public polls.
    - Authenticated users see their own and public poll questions.
    - If a poll_id is provided, results are scoped to that poll.
    """
    queryset = Questions.objects.all()
    serializer_class = QuestionsSerializer
    permission_classes = [QuestionPermission]
    
    def get_queryset(self):
        user = self.request.user
        poll_id = self.kwargs.get('poll_pk') # Get the poll ID from the URL (if nested route)
    
        if user.is_superuser:
        # Superuser sees all questions, with optional filtering by poll
            if poll_id:
                return Questions.objects.filter(poll_id=poll_id)
            return Questions.objects.all()

        base_filter = Q() # Start with an empty filter
        if user.is_authenticated:
            # Show questions from polls they created OR polls that are public if authenticated
            base_filter &= Q(poll_id__created_by=user) | Q(poll_id__is_public=True)
        else:
            # Only show questions from public polls if anonymous
            base_filter &= Q(poll_id__is_public=True)

        if poll_id:
            # Filter questions under a specific poll (if nested route)
            base_filter &= Q(poll_id=poll_id)

        return Questions.objects.filter(base_filter)

    def perform_create(self, serializer):
        serializer.save()
    
    @action(detail=True, methods=["post"], permission_classes=[VotePermission], serializer_class=VotesSerializer )
    def vote(self, request, poll_pk=None, pk=None):
        """
        Allows authenticated users to vote on this question.
        Validates option, duplicates, and poll status via serializer.
        """

        question = self.get_object()
        handle_vote(request, question)
        return Response({"detail": "Vote recorded."})

