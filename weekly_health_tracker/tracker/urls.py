from django.urls import path, include
from .views import WeeklySummaryView
from .views import FriendshipListCreateView
from .views import FriendWeeklySummaryView


urlpatterns = [
    path('admin/', admin.site.urls),
    path("weekly-summary/", WeeklySummaryView.as_view(), name="weekly-summary"),
    path('api/tracker/', include('tracker.urls')),
    path('friends/', FriendshipListCreateView.as_view(), name='friend-list-create'),
    path('friends/<int:friend_id>/weekly-summary/', FriendWeeklySummaryView.as_view(), name='friend-weekly-summary'),

]
