from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Donation, BloodDonationForm
from Donor.models import Donor
from .serializers import BloodDonationSerializer
from django.db import transaction


class DonationFormAPIView(APIView):
    def get(self, request):
        form = BloodDonationForm.objects.all()
        serializer = BloodDonationSerializer(form, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Get donor data from request
        donor_data = request.data

        # Check if donor exists by email
        try:
            donor = Donor.objects.get(email=donor_data["email"])
        except Donor.DoesNotExist:
            # Create a new donor if not found
            donor = Donor.objects.create(
                first_name=donor_data.get("first_name"),
                second_name=donor_data.get("second_name"),
                email=donor_data.get("email"),
                phone_number=donor_data.get("phone_number"),
                town=donor_data.get("town"),
                date_of_birth=donor_data.get("date_of_birth"),
                blood_type=donor_data.get("blood_type"),
                gender=donor_data.get("gender"),
                last_donation=donor_data.get("last_donation"),
            )

        # Save the donation form with donor linked
        donation_data = request.data
        donation_data["donor"] = donor.id  # Link donor to the form

        # Serialize and save the donation form data
        serializer = BloodDonationSerializer(data=donation_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DonationFormDetailsAPIView(APIView):
    def get(self, request, pk):
        form = BloodDonationForm.objects.get(pk=pk)
        serializer = BloodDonationSerializer(form)
        return Response(serializer.data)
    
    def put(self, request, pk):
        form = BloodDonationForm.objects.get(pk=pk)
        serializer = BloodDonationSerializer(form, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        form = BloodDonationForm.objects.get(pk=pk)
        form.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class DonationAPIView(APIView):
    # Creates a donation entry
    def get(self, request):
        donations = Donation.objects.all()
        serializer = DonationSerializer(donations, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DonationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DonationDetailAPIView(APIView):
    # Gets a single instance of a donation with the primary key
    def get(self, request, pk):
        try:
            donation = Donation.objects.get(pk=pk)
        except Donation.DoesNotExist:
            return Response({'message': 'Donation not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = DonationSerializer(donation)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            donation = Donation.objects.get(pk=pk)
        except Donation.DoesNotExist:
            return Response({'message': 'Donation not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = DonationSerializer(donation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            donation = Donation.objects.get(pk=pk)
        except Donation.DoesNotExist:
            return Response({'message': 'Donation not found'}, status=status.HTTP_404_NOT_FOUND)
        donation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
