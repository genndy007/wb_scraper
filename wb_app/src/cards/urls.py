from django.urls import path
from .views import AllCardsView

urlpatterns = [
    path('', AllCardsView.as_view()),
    # path('/<int:pk>',),
    # path('/<int:pk>/stats',),
]