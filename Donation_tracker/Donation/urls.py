from django.urls import path
from .views import DonationAPIView, DonationDetailAPIView, DonationFormAPIView, DonationFormDetailsAPIView

urlpatterns = [
    path('form', DonationFormAPIView.as_view(), name='blood_donation_form'),
    path('form/<int:pk>', DonationFormDetailsAPIView.as_view()),
    path('', DonationAPIView.as_view()),
    path('<int:pk>/', DonationDetailAPIView.as_view()),

]
