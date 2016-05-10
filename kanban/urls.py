from kanban import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)
router.register(r'api/card', views.KanbanCardAPI, 'api-card')

urlpatterns = router.urls
