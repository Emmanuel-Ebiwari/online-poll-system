from django.contrib import admin
from .models import Polls, Questions, Options, Votes

admin.site.register(Polls)
admin.site.register(Questions)
admin.site.register(Options)
admin.site.register(Votes)
