
import random
from rest_framework.views import APIView
from DataStorage.serializers import *
from .models import OTP, Booking, Users, Vehicle, PaymentsStatus
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from django.contrib.auth import authenticate,login
from rest_framework.generics import ListAPIView
from datetime import datetime
#import razorpay


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegister(APIView):
    def post(self,request):
        user_id=random.randint(1,10001)
        request.data['user_id']=user_id
        serializer=RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)


class UserLogin(APIView):
    def post(self,request):
        serializer=LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email=serializer.data.get('email')
        password=serializer.data.get('password')
        user=authenticate(email=email,password=password)
        if user is not None:
            login(request,user=user)
            token=get_tokens_for_user(user=user)
            return Response({'msg':'-- Login Successfull --','token':{'access_token':token['access']}},status=status.HTTP_202_ACCEPTED)
        return Response({'msg':'-- Invalid Credentials --'},status=status.HTTP_404_NOT_FOUND)


class UserDataUpdate(APIView):
    permission_classes=[IsAuthenticated]
    def put(self,request,uid):
        id=uid
        user=Users.objects.get(user_id=id)
        serializer=UserDataUpdateSerializer(user,data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ResetPassword(APIView):
    def post(self,request):
        email=request.data['email']
        if Users.objects.filter(email=email).exists():
            user=Users.objects.get(email=email)
            serializer=ChangePasswordSerializer(data=request.data,context={'user':user})
            serializer.is_valid(raise_exception=True)
            return Response({'msg':'Password Changed Successfully'},status=status.HTTP_202_ACCEPTED)
        return Response({'msg':'-- Email Not Found --'},status=status.HTTP_404_NOT_FOUND)

class ChangePassword(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer=ChangePasswordSerializer(data=request.data,context={'user':request.user})
        serializer.is_valid(raise_exception=True)
        return Response({'msg':'Password Changed Successfully'},status=status.HTTP_200_OK)

class AddVehicle(APIView):
    permission_classes=[IsAdminUser]
    def post(self,request):
        vehicle_id=random.randint(1,10001)
        request.data['vehicle_id']=vehicle_id
        serializer=VehicleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg':'Vehicle Added','data':serializer.data},status=status.HTTP_201_CREATED)


class VehicleDataUpdate(APIView):
    permission_classes=[IsAdminUser]
    def put(self,request,vid):
        id=vid
        vehicle=Vehicle.objects.get(vehicle_id=id)
        serializer=VehicleUpdateSerializer(vehicle,data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg':'-- Data Updated --','data':serializer.data},status=status.HTTP_202_ACCEPTED)

class DeleteVehicle(APIView):
    permission_classes=[IsAdminUser]
    def delete(self,request,vid):
        id=vid
        vehicle=Vehicle.objects.get(vehicle_id=id)
        vehicle.delete()
        return Response({"msg":"Vehicle Deleted"},status=status.HTTP_200_OK)

class ShowVehicles(ListAPIView):
    permission_classes=[IsAdminUser]
    queryset=Vehicle.objects.all()
    serializer_class=ShowVehicles

class ShowParticularVehicle(APIView):
    permission_classes=[IsAdminUser]
    def post(self,request):
        vehicle_id=request.data['vehicle_id']
        vehicle=Vehicle.objects.get(id=vehicle_id)
        serializer=ShowParticularVehicleSerializer(vehicle)
        return Response({"data":serializer.data},status=status.HTTP_200_OK)

class SearchFlights(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        startlocation=request.data['from_location']
        destination=request.data['destination']

        flights=Vehicle.objects.all().filter(from_location__contains=startlocation)
        flight_list=[]
        for i in flights:
            if i.destination==destination:
                serializer=VehicleSerializer(i)
                flight_list.append(serializer.data)
        return Response({"data":flight_list},status=status.HTTP_200_OK)


class Bookings(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        
        booking_id=random.randint(1,10001)
        id=request.user.id

        vehicle_id=request.data['vehicle']
        vehicle=Vehicle.objects.get(id=vehicle_id)
        ticket_price=vehicle.ticket_price
        total_passengers=int(request.data['total_passengers'])
        total_price=ticket_price*total_passengers
        onboarding_date=vehicle.date
        booking_date=datetime.now()

        request.data['booking_id']=booking_id
        request.data['user']=id
        request.data['total_price']=total_price
        request.data['onboarding_date']=onboarding_date
        request.data['booking_date']=booking_date

        serializer=BookingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg':'-- Booking Completed --','Booking_Data':serializer.data},status=status.HTTP_201_CREATED)

class DeleteBooking(APIView):
    permission_classes=[IsAuthenticated]
    def delete(self,request,bid):
        id=bid
        booking=Booking.objects.get(booking_id=id)
        booking.delete()
        return Response({"msg":"-- Booking Deleted --"})

class ShowParticularBooking(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        booking_id=request.data['booking_id']
        booking=Booking.objects.get(booking_id=booking_id)
        serializer=ShowBookingSerializer(booking)
        return Response(serializer.data)

class ShowBookings(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        user=request.user.id
        bookings=Booking.objects.all().filter(user=user)
        booking_list=[]
        for i in bookings:
            serializer=ShowBookingSerializer(i)
            booking_list.append(serializer.data)
        return Response(booking_list)

class Passengers(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        id=random.randint(1,10001)
        request.data['passenger_id']=id
        serializer=PassengerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg':'-- Passenger Created --','data':serializer.data},status=status.HTTP_201_CREATED)


class GenerateOtp(APIView):
    def post(self,request):
        contact=request.data['contact']
        if Users.objects.filter(contact=contact).exists():
            otp=random.randint(1000,10000)
            request.data['otp']=otp

            # send messege from twilio
            # account_sid = 'ACe9c59e14ca2cf8f8eb559bd225efebba'
            # auth_token = '333f2a1b2107b6abb35320267d203c89'
            # client = Client(account_sid, auth_token)

            # message = client.messages.create(
            #                             body=f'Your ccount has debited Rs.1000 - Here is the otp {otp}',
            #                             from_='+16184238369',
            #                             to=f'+91{contact}'
            #                         )

            # sending sms via 2factor.in
            Api_key='44824702-2b99-11ed-9c12-0200cd936042'
            url=f'https://2factor.in/API/V1/{Api_key}/SMS/{contact}/{otp}/'
            
            response=requests.get(url)
            serializer=OtpSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'msg' : '-- OTP Sent in your Mobile --','Details':response},status=status.HTTP_200_OK)

class VerifyOtp(APIView):
    def post(self,request):
        user=OTP.objects.get(contact=request.data['contact'])
        serializer=VerifyOtpSerializer(request.data)
        if serializer.data.get('otp')==user.otp:
            user.delete()
            return Response({'msg':'OTP VERIFIED'},status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

        # for i in user:
        #     serializer=VerifyOtpSerializer(request.data)
        #     print(serializer.data.get('otp'))
        #     if serializer.data.get('otp')==i.otp:
        #         user.delete()
        #         return Response({'msg':'OTP VERIFIED'},status=status.HTTP_200_OK)
        # return Response(status=status.HTTP_404_NOT_FOUND)


class PaymentOrder(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request,bid):
        key_id="rzp_live_8jv8Zh7ceNvMNA"
        key_secret="CYXvDa1mfDFXROIdbaSz2d1f"
        client = razorpay.Client(auth=(key_id, key_secret))
        try:
            booking=Booking.objects.get(booking_id=bid)
            amount=booking.total_price
            DATA={
                "amount": amount,
                "currency": "INR",
                "receipt": "Succeed"
            }
            payment_details=client.order.create(DATA)
        
            Data = {
                "payment_amount": payment_details.get('amount'),
                "order_id": payment_details.get('id'),
                "receipt": payment_details.get('receipt'),
                "booking" : booking.id,
                "status" : "Initiated",
            }
            serializer=PaymentSerializer(data=Data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            #order_time=datetime.now()+timedelta(minutes=2)
            #payment_object=PaymentsStatus.objects.get(order_id=serializer.data.get('order_id'))
            # while(True):
            #     if(now() == order_time):
            #         if(payment_object.__dict__.get('status')!='Completed'):
            #             print('inner if')
            #             payment_object.delete()
            #             break
            
            return Response({'messege': 'Payment has Initiated.','data':serializer.data},status=status.HTTP_201_CREATED)
        
        except:
            return Response({'messege': 'Problem Occured ! Try Again .','data':serializer.data},status=status.HTTP_400_BAD_REQUEST)

class PaymentStats(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request,order_id):
        id=order_id

        payment_details=PaymentsStatus.objects.get(order_id=id)

        payment_id=random.randint(1,10001)
        payment_details.status = "Completed"
        payment_details.payment_id=payment_id
        payment_details.save()

        return Response({'messege' : 'Payment has Completed.'},status=status.HTTP_202_ACCEPTED)
        
        #return Response({'messege' : 'Payment Failed ! Try Again.'},status=status.HTTP_400_BAD_REQUEST)
