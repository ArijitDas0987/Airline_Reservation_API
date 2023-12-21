
from rest_framework import serializers
from .models import OTP, Users,Vehicle,Booking,Passenger,PaymentsStatus

class RegistrationSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model=Users
        fields=['user_role','user_id','user_name','email','contact','password','password2']

    def validate(self, attrs):
        password=attrs.get('password')
        password2=attrs.get('password2')

        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        return attrs

    def create(self, validated_data):
        if validated_data.get('user_role')=='Admin':
            return Users.objects.create_superuser(**validated_data)
        return Users.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        model=Users
        fields=['email','password']
            
class UserDataUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Users
        fields=['user_name','email','contact']

class ChangePasswordSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type':'password'})
    class Meta:
        model=Users
        fields=['password','password2']
    
    def validate(self,attrs):
        password=attrs.get('password')
        password2=attrs.get('password2')

        if password != password2:
            raise serializers.ValidationError('Password and Confirm Password does not match')
        
        user=self.context.get('user')
        user.set_password(password)
        user.save()
        return attrs

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model=Vehicle
        fields=['vehicle_id','vehicle_name','from_location','destination','date','time','ticket_price']

class VehicleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Vehicle
        fields=['from_location','destination','date','time','ticket_price']

class SearchFlightSearializer(serializers.ModelSerializer):
    class Meta:
        model=Vehicle
        fields=['from_location','destination']

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model=Booking
        fields='__all__'

class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Passenger
        fields=['passenger_id','passenger_name','age','gender','booking_id']

class ShowBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model=Booking
        fields='__all__'


class ShowVehicles(serializers.ModelSerializer):
    class Meta:
        model=Vehicle
        fields=['vehicle_id','vehicle_name','from_location','destination','date','time','ticket_price']

class ShowParticularVehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model=Vehicle
        fields='__all__'

class OtpSerializer(serializers.ModelSerializer):
    class Meta:
        model=OTP
        fields='__all__'

class VerifyOtpSerializer(serializers.ModelSerializer):
    class Meta:
        model=OTP
        fields=['contact','otp']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model=PaymentsStatus
        fields=['payment_amount','payment_id','order_id','receipt','booking','status']


class PaymentStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model=PaymentsStatus
        fields=['status','payment_id']