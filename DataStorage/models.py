
from datetime import timedelta
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils.timezone import now


ROLE=(
    ("Customer" , 'Customer'),
    ('Admin' , 'Admin')
)

class MyUserManager(BaseUserManager):
    def create_user(self, email,user_role, user_id,user_name,contact, password=None,password2=None):
        
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            user_role=user_role,
            user_id=user_id,
            user_name=user_name,
            contact=contact,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,user_role, user_id,user_name,contact, password=None,password2=None):
       
        user = self.create_user(
            email,
            user_role,
            user_id,
            user_name,
            contact,
            password=password,
            password2=password2
            
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class Users(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )

    user_id=models.IntegerField(max_length=6,unique=True)
    user_role=models.CharField(choices=ROLE,max_length=10)
    user_name=models.CharField(max_length=100)
    contact=models.BigIntegerField(max_length=10)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_role','user_id','user_name','contact',]

    def __str__(self):
        self.user_id=str(self.user_id)
        return self.user_id

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Vehicle(models.Model):
    vehicle_id=models.BigIntegerField(unique=True)
    vehicle_name=models.CharField(max_length=100)
    from_location=models.CharField(max_length=100)
    destination=models.CharField(max_length=100)
    date=models.DateField()
    time=models.TimeField()
    ticket_price=models.IntegerField()

    def __str__(self):
        self.id=str(self.vehicle_id)
        return self.id

class OTP(models.Model):
    contact=models.IntegerField()
    otp=models.IntegerField()


class Booking(models.Model):
    booking_id=models.BigIntegerField(unique=True)
    booking_date=models.DateTimeField()
    onboarding_date=models.DateField(null=True)
    total_passengers=models.IntegerField()
    total_price=models.IntegerField()
    user=models.ForeignKey(Users,on_delete=models.CASCADE)
    vehicle=models.ForeignKey(Vehicle,on_delete=models.CASCADE)

    def __str__(self):
        self.id=str(self.booking_id)
        return self.id


class Passenger(models.Model):
    passenger_id=models.IntegerField(unique=True)
    passenger_name=models.CharField(max_length=100)
    age=models.IntegerField()
    gender=models.CharField(max_length=10)
    booking_id=models.ForeignKey(Booking ,on_delete=models.CASCADE)


class PaymentsStatus(models.Model):
    order_id=models.CharField(unique=True,max_length=20)
    payment_id=models.CharField(max_length=50,unique=True,null=True)
    payment_amount=models.IntegerField()
    receipt=models.CharField(max_length=50)
    status=models.CharField(max_length=10,null=True)
    time=models.DateTimeField(auto_now_add=True,null=True)
    booking=models.ForeignKey(Booking,on_delete=models.CASCADE)

    @property
    def deletes_in_ten_seconds(self):
        time = self.time + timedelta(seconds=120)
        query = PaymentsStatus.objects.get(pk=self.pk)
        if time > now():
            query.delete()