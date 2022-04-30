from django.urls import path
from .views import AllCardsView, SingleCardView, CardStatsView, UpdateInfoView

urlpatterns = [
    path('', AllCardsView.as_view()),
    path('<int:pk>', SingleCardView.as_view()),
    path('<int:pk>/stats', CardStatsView.as_view()),
    path('update', UpdateInfoView.as_view()),
]