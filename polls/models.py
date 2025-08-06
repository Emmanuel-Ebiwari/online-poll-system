from django.db import models
from user.models import User
import uuid

class Polls(models.Model):
    poll_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='polls_created')
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    is_closed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} by {self.created_by}"
    
    class Meta:
        db_table = 'polls'
        verbose_name = 'Poll'
        verbose_name_plural = 'Polls'
        ordering = ['-created_at']

class Questions(models.Model):
    SINGLE = 'single'
    MULTIPLE = 'multiple'
    QUESTION_TYPE_CHOICES = [
        (SINGLE, 'Single Choice'),
        (MULTIPLE, 'Multiple Choice'),
    ]
    question_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    poll_id = models.ForeignKey(Polls, related_name='questions', on_delete=models.CASCADE)
    question_text = models.CharField(max_length=255)
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPE_CHOICES, default=SINGLE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question_text
    
    class Meta:
        db_table = 'questions'
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'
        ordering = ['poll_id', 'question_id']

class Options(models.Model):
    option_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    question_id = models.ForeignKey(Questions, related_name='options', on_delete=models.CASCADE)
    option_text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.option_text
    
    class Meta:
        db_table = 'options'
        verbose_name = 'Option'
        verbose_name_plural = 'Options'
        ordering = ['question_id', 'option_id']

class Votes(models.Model):
    vote_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    option_id = models.ForeignKey(Options, related_name='votes', on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes_cast')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Vote by {self.user_id} for {self.option_id}"
    
    class Meta:
        db_table = 'votes'
        verbose_name = 'Vote'
        verbose_name_plural = 'Votes'
        ordering = ['option_id', 'vote_id']
