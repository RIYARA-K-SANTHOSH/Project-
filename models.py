from django.db import models
from django.core.mail import send_mail
from django.utils import timezone
import uuid

class Register(models.Model):
    reg_id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=15)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')])
    dob = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    password = models.CharField(max_length=128)
    confirm_password = models.CharField(max_length=128)
    reset_password_token = models.CharField(max_length=100, blank=True, null=True)
    token_expiry = models.DateTimeField(blank=True, null=True)
    blocked = models.BooleanField(default=False)  # New field for blocking users

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email

    def check_password(self, raw_password):
        return self.password == raw_password

    def generate_reset_token(self):
        self.reset_password_token = str(uuid.uuid4())
        self.token_expiry = timezone.now() + timezone.timedelta(hours=1)
        self.save()

    def block_user(self):
        self.blocked = True
        self.save()
        self.send_block_email()

    def unblock_user(self):
        self.blocked = False
        self.save()

    def send_block_email(self):
        subject = "Account Blocked"
        message = f"Dear {self.first_name},\n\nYour account has been blocked by the admin. Please contact support for more information."
        send_mail(subject, message, 'admin@yourdomain.com', [self.email])

class Profile(models.Model):
    personal_id = models.AutoField(primary_key=True)
    reg_id = models.OneToOneField(Register, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    height = models.CharField(max_length=10)
    weight = models.CharField(max_length=10, blank=True, null=True)
    marital_status = models.CharField(max_length=20)
    mother_tongue = models.CharField(max_length=50)
    religion = models.CharField(max_length=50)
    caste = models.CharField(max_length=50)
    physical_status = models.CharField(max_length=50, blank=True, null=True)
    about = models.TextField()
    spoken_language = models.CharField(max_length=255, blank=True, null=True)
    hobbies = models.TextField(blank=True, null=True)
    occupation = models.CharField(max_length=255, blank=True, null=True)
    annual_income = models.CharField(max_length=50, blank=True, null=True)
    more_about_me = models.TextField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    complexion = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return f"Profile for {self.reg_id.email}"
class Education(models.Model):
    education_id = models.AutoField(primary_key=True)  # Explicitly defining education_id as the primary key
    reg_id = models.ForeignKey(Register, on_delete=models.CASCADE)  # Reference to the user
    school_name = models.CharField(max_length=255)
    school_passout_year = models.IntegerField()
    school_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    plus_two_name = models.CharField(max_length=255)
    plus_two_passout_year = models.IntegerField()
    plus_two_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    degree_institution_name = models.CharField(max_length=255)
    degree_passout_year = models.IntegerField()
    degree_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    degree_name = models.CharField(max_length=255)
    field_of_study = models.CharField(max_length=255, blank=True, null=True)  # Optional field

    def __str__(self):
        return f"{self.reg_id.fullname}'s Education Details"
    from django.db import models
from django.db import models
from .models import Register  # Ensure this import is correct

class Family(models.Model):
    family_id = models.AutoField(primary_key=True)  # Primary key
    reg_id = models.ForeignKey(Register, on_delete=models.CASCADE)  # Reference to the Register model
    father_name = models.CharField(max_length=100)
    father_occupation = models.CharField(max_length=100, blank=True)
    mother_name = models.CharField(max_length=100)
    mother_occupation = models.CharField(max_length=100, blank=True)
    sibling_count = models.IntegerField(blank=True, null=True)
    sibling_details = models.TextField(blank=True)
    family_type = models.CharField(
        max_length=10,
        choices=[('Joint', 'Joint'), ('Nuclear', 'Nuclear'), ('Extended', 'Extended')]
    )
    family_status = models.CharField(
        max_length=20,
        choices=[('Middle Class', 'Middle Class'), ('Upper Middle Class', 'Upper Middle Class'), ('Rich', 'Rich')]
    )
    family_values = models.CharField(
        max_length=20,
        choices=[('Traditional', 'Traditional'), ('Moderate', 'Moderate'), ('Liberal', 'Liberal')]
    )
    native_place = models.CharField(max_length=100, blank=True)
    additional = models.TextField(blank=True)

    def __str__(self):
        return f"Family details of {self.reg_id.email}"

class ImageUpload(models.Model):
    reg_id = models.ForeignKey('Register', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='uploads/images/')
    compressed_image = models.ImageField(upload_to='uploads/compressed_images/', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.id} uploaded by User with reg_id {self.reg_id}"

        
from django.db import models
from .models import Register

class Login(models.Model):
    login_id = models.AutoField(primary_key=True)
    reg_id = models.ForeignKey(Register, on_delete=models.CASCADE)
    email = models.EmailField()
    password = models.CharField(max_length=128)  # Store hashed password

    def __str__(self):
        return f"Login record for {self.email}"

    
from django.db import models
from django.contrib.auth.models import User

class Blog(models.Model):
    blog_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)

    def __str__(self):
        return self.title


class Notification(models.Model):
    notification_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)  # Title of the notification
    message = models.TextField()  # Content of the notification
    date_created = models.DateTimeField(auto_now_add=True)  # Automatically set the date/time when created

    def __str__(self):
        return self.title


