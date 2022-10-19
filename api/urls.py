from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('questions', views.QuestionViewSet)
router.register('courses', views.CourseViewSet)
router.register('comments', views.CommentCommentViewSet)
router.register('students', views.StudentViewSet)

questions_router = routers.NestedSimpleRouter(router, r'questions', lookup='question')
questions_router.register(r'comments', views.CommentViewSet, basename='comments')

questions_commments_router = routers.NestedSimpleRouter(questions_router, r'comments', lookup='comment')
questions_commments_router.register(r'ccs', views.CommentCommentViewSet, basename='cc')

urlpatterns = router.urls + questions_router.urls + questions_commments_router.urls