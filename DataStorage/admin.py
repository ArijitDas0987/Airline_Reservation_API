from django.contrib import admin
from .models import OTP, Users,Vehicle,Booking,Passenger,PaymentsStatus
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserAdmin(BaseUserAdmin):

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('user_id','email','user_role','user_name','contact', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        ('User Credentials', {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('user_id','user_name','contact',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('id','email', 'user_role','user_id','user_name','contact',),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

# Now register the new UserAdmin...
admin.site.register(Users, UserAdmin)


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display=['id','vehicle_id','vehicle_name','from_location','destination',
                    'date','time','ticket_price']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display=['booking_id','booking_date','onboarding_date','total_passengers',
                    'total_price','user','vehicle']

@admin.register(Passenger)
class PassengerAdmin(admin.ModelAdmin):
    list_display=['passenger_id','passenger_name','age','gender','booking_id']

@admin.register(OTP)
class OtpAdmin(admin.ModelAdmin):
    list_display=['contact','otp']

@admin.register(PaymentsStatus)
class PaymentAdmin(admin.ModelAdmin):
    list_display=['order_id','payment_id','booking','payment_amount','receipt','status','time']
