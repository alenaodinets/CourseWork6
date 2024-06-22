from django.urls import path
from django.views.decorators.cache import cache_page

from main import apps
from main.views import HomeView, SendingListView, MessageListView, ClientListView, SendingDetailView, MessageDetailView, \
    ClientDetailView, SendingCreateView, MessageCreateView, ClientCreateView, SendingUpdateView, MessageUpdateView, \
    ClientUpdateView, SendingDeleteView, ClientDeleteView, MessageDeleteView, AttemptListView, SendingModerationView

app_name = apps.MainConfig.name

urlpatterns = [
    path('', cache_page(100)(HomeView.as_view()), name='home'),
    path('sending/', SendingListView.as_view(), name='sending_list'),
    path('messages/', MessageListView.as_view(), name='message_list'),
    path('clients/', ClientListView.as_view(), name='client_list'),
    path('sending/<int:pk>/', cache_page(100)(SendingDetailView.as_view()), name='sending_detail'),
    path('message/<int:pk>/', cache_page(100)(MessageDetailView.as_view()), name='message_detail'),
    path('client/<int:pk>/', cache_page(100)(ClientDetailView.as_view()), name='client_detail'),
    path('sending/create/', SendingCreateView.as_view(), name='sending_create'),
    path('message/create/', MessageCreateView.as_view(), name='message_create'),
    path('client/create/', ClientCreateView.as_view(), name='client_create'),
    path('sending/<int:pk>/update/', SendingUpdateView.as_view(), name='sending_update'),
    path('message/<int:pk>/update/', MessageUpdateView.as_view(), name='message_update'),
    path('client/<int:pk>/update/', ClientUpdateView.as_view(), name='client_update'),
    path('sending/<int:pk>/delete/', SendingDeleteView.as_view(), name='sending_delete'),
    path('message/<int:pk>/delete/', MessageDeleteView.as_view(), name='message_delete'),
    path('client/<int:pk>/delete/', ClientDeleteView.as_view(), name='client_delete'),
    path('sending/<int:pk>/attempts/', AttemptListView.as_view(), name='attempt_list'),
    path('sending/<int:pk>/moderate', SendingModerationView.as_view(), name='sending_moderation'),
]