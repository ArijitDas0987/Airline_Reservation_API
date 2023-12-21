
from django.urls import path

from .views import *


urlpatterns = [
    path('User/Registration/',UserRegister.as_view(),name="user_regitration"),
    path('User/Login/',UserLogin.as_view(),name="user_login"),
    path('User/ChangePassword/',ChangePassword.as_view(),name="change_password"),
    path('User/ResetPassword/',ResetPassword.as_view(),name="reset_password"),
    path('User/UpdateData/<uid>/',UserDataUpdate.as_view(),name="update_user_data"),

    path('Admin/AddVehicle/',AddVehicle.as_view(),name="add_vehicle"),
    path('Admin/VehicleDataUpdate/<vid>/',VehicleDataUpdate.as_view(),name="vehicle_data_update"),
    path('Admin/DeleteVehicle/<vid>/',DeleteVehicle.as_view(),name="delete_vehicle"),
    path('Admin/ShowVehicles/',ShowVehicles.as_view(),name="show_vehicles"),
    path('Admin/ShowParticularVehicle/',ShowParticularVehicle.as_view(),name="show_particular_vehicle"),
    
    path('User/SearchFlights/',SearchFlights.as_view(),name="search_flights"),

    path('User/Booking/',Bookings.as_view(),name="booking"),
    path('User/DeleteBooking/<bid>/',DeleteBooking.as_view(),name="delete_booking"),
    path('User/ShowParticularBooking/',ShowParticularBooking.as_view(),name="show_particular_booking"),
    path('User/ShowBookings/',ShowBookings.as_view(),name="show_bookings"),

    path('User/Passenger/',Passengers.as_view(),name="Passenger"),

    path('User/GenerateOtp/',GenerateOtp.as_view(),name="generate_otp"),
    path('User/VerifyOtp/',VerifyOtp.as_view(),name="verify_otp"),

    path('User/PaymentOrder/<bid>',PaymentOrder.as_view(),name="payment_order"),
    path('User/PaymentStats/<order_id>',PaymentStats.as_view(),name="payment_stats"),

]