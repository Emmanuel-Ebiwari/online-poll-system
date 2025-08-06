from rest_framework import routers
from rest_framework_nested import routers as nested_routers
from django.urls import path, include
from .views import PollsViewSet, QuestionsViewSet, VoteAPIView

router = routers.DefaultRouter()
router.register(r'polls', PollsViewSet, basename='poll')

nested_router = nested_routers.NestedDefaultRouter(
    router, r'polls', lookup='poll')
nested_router.register(r'questions', QuestionsViewSet,
                       basename='poll-question')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(nested_router.urls)),
    path(
        'polls/<uuid:poll_id>/questions/<uuid:question_id>/vote/',
        VoteAPIView.as_view(),
        name='vote-on-question'
    ),
]
