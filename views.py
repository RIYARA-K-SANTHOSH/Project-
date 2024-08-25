from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from .models import Register,Login,MembershipPlan,Blog,Notification

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Register, Login

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Register, Profile, Login
import re

def index(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        profile_picture = request.FILES.get('profile_picture')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('index')

        if Register.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect('index')

        user = Register(
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            gender=gender,
            dob=dob,
            password=password,
            confirm_password=confirm_password,
            profile_picture=profile_picture
        )
        user.save()
        Login.objects.create(
            reg_id=user,
            email=email,
            password=password  # Store hashed password in practice
        )
        messages.success(request, "Registration successful.")
        return redirect('login')

    return render(request, 'index.html')


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Register

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if email == 'admin@gmail.com' and password == 'admin123':
            request.session['is_admin'] = True
            return redirect('adminmain_view')

        user = Register.objects.filter(email=email).first()

        if user and user.check_password(password):
            if user.blocked:
                messages.error(request, "Your account has been blocked by the administrator.")
                return redirect('login')

            messages.success(request, "Login successful.")
            request.session['user_email'] = email
            return redirect('profile')  # Ensure this is the correct pattern name

        else:
            messages.error(request, "Invalid email or password.")
            return redirect('login')

    return render(request, 'login.html')

def user_profile(request):
    email = request.session.get('user_email')
    if email:
        user = get_object_or_404(Register, email=email)
        return render(request, 'user_profile.html', {'user': user})
    else:
        return redirect('login')  # Redirect to login if user is not authenticated



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Register

def block_user(request, reg_id):
    user = get_object_or_404(Register, reg_id=reg_id)
    user.block_user()
    messages.success(request, f"User {user.email} has been blocked.")
    return redirect('review_users')

def unblock_user(request, reg_id):
    user = get_object_or_404(Register, reg_id=reg_id)
    user.unblock_user()
    messages.success(request, f"User {user.email} has been unblocked.")
    return redirect('review_users')


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Register, Profile

def profile(request):
    if request.method == 'POST':
        user_email = request.session.get('user_email')
        user = Register.objects.filter(email=user_email).first()
        
        if not user:
            messages.error(request, "User not found.")
            return redirect('login')

        # Create a new Profile or get the existing one
        profile, created = Profile.objects.get_or_create(reg_id=user)

        # Update the profile with POST data
        profile.address = request.POST.get('address')
        profile.height = request.POST.get('height')
        profile.weight = request.POST.get('weight')
        profile.marital_status = request.POST.get('marital_status')
        profile.mother_tongue = request.POST.get('mother_tongue')
        profile.religion = request.POST.get('religion')
        profile.caste = request.POST.get('caste')
        profile.physical_status = request.POST.get('physical_status')
        profile.about = request.POST.get('about')
        profile.spoken_language = request.POST.get('spoken_language')
        profile.hobbies = request.POST.get('hobbies')
        profile.occupation = request.POST.get('occupation')
        profile.annual_income = request.POST.get('annual_income')
        profile.more_about_me = request.POST.get('more_about_me')
        profile.save()

        messages.success(request, "Profile added successfully.")
        return redirect('education')

    return render(request, 'profile.html')



from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Education, Register

def education(request):
    if request.method == 'POST':
        user_email = request.session.get('user_email')
        user = Register.objects.filter(email=user_email).first()

        if not user:
            messages.error(request, "User not found.")
            return redirect('login')

        # Check if an Education record exists
        education = Education.objects.filter(reg_id=user).first()

        if not education:
            # Create a new Education record if it doesn't exist
            education = Education(reg_id=user)

        # Update the Education record with the provided form data
        education.school_name = request.POST.get('school_name')
        education.school_passout_year = request.POST.get('school_passout_year')
        education.school_percentage = request.POST.get('school_percentage')
        education.plus_two_name = request.POST.get('plus_two_name')
        education.plus_two_passout_year = request.POST.get('plus_two_passout_year')
        education.plus_two_percentage = request.POST.get('plus_two_percentage')
        education.degree_institution_name = request.POST.get('degree_institution_name')
        education.degree_passout_year = request.POST.get('degree_passout_year')
        education.degree_percentage = request.POST.get('degree_percentage')
        education.degree_name = request.POST.get('degree_name')
        education.field_of_study = request.POST.get('field_of_study')
        education.save()

        messages.success(request, "Education details added successfully.")
        return redirect('family')  # Redirect to the next step or wherever you want the user to go next

    return render(request, 'education.html')


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Family, Register


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Family, Register

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Family, Register

def family(request):
    if request.method == 'POST':
        user_email = request.session.get('user_email')
        if not user_email:
            messages.error(request, "User email not found in session.")
            return redirect('login')

        # Ensure you are using the correct model for fetching the user
        user = Register.objects.filter(email=user_email).first()
        if not user:
            messages.error(request, "User not found.")
            return redirect('login')

        # Extract form data
        father_name = request.POST.get('father_name')
        father_occupation = request.POST.get('father_occupation', '')
        mother_name = request.POST.get('mother_name')
        mother_occupation = request.POST.get('mother_occupation', '')
        sibling_count = request.POST.get('sibling_count', '')
        sibling_details = request.POST.get('sibling_details', '')
        family_type = request.POST.get('family_type')
        family_status = request.POST.get('family_status')
        family_values = request.POST.get('family_values')
        native_place = request.POST.get('native_place', '')
        additional = request.POST.get('additional', '')

        # Validate required fields
        if not father_name or not mother_name or not family_type or not family_status or not family_values:
            messages.error(request, "Please fill in all required fields.")
            return render(request, 'family.html')

        # Create a new Family record
        Family.objects.create(
            reg_id=user,  # Ensure `user` is the correct instance and matches the expected type
            father_name=father_name,
            father_occupation=father_occupation,
            mother_name=mother_name,
            mother_occupation=mother_occupation,
            sibling_count=int(sibling_count) if sibling_count.isdigit() else None,
            sibling_details=sibling_details,
            family_type=family_type,
            family_status=family_status,
            family_values=family_values,
            native_place=native_place,
            additional=additional
        )

        messages.success(request, "Family details added successfully.")
        return redirect('family')  # Redirect to the family detail page or another page after saving

    # Render form for GET request
    return render(request, 'family.html')





def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = Register.objects.get(email=email)
            user.generate_reset_token()

            current_site = get_current_site(request)
            subject = 'Password Reset Request'
            message = render_to_string('password_reset_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.reg_id)),
                'token': user.reset_password_token,
            })
            send_mail(subject, message, 'noreply@yourdomain.com', [user.email])

            return HttpResponse('Password reset link has been sent to your email.')
        except Register.DoesNotExist:
            return HttpResponse('Email not found', status=404)
    return render(request, 'forgot_password.html')

def reset_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Register.objects.get(reg_id=uid, reset_password_token=token, token_expiry__gte=timezone.now())
    except (TypeError, ValueError, OverflowError, Register.DoesNotExist):
        return HttpResponse('Invalid or expired reset link', status=400)

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if new_password == confirm_password:
            user.password = new_password  # Update plain text password
            user.reset_password_token = ''
            user.token_expiry = None
            user.save()

            try:
                login_record = Login.objects.get(reg_id=user)
                login_record.password = new_password  # Update plain text password
                login_record.save()
            except Login.DoesNotExist:
                return HttpResponse('Login record not found', status=404)

            return redirect('login')
        else:
            return HttpResponse('Passwords do not match', status=400)

    return render(request, 'reset_password.html', {'uidb64': uidb64, 'token': token})





def adminmain_view(request):
    if request.session.get('is_admin'):
        return render(request, 'adminmain.html')
    else:
        return redirect('login')
def logout(request):
    if 'is_admin' in request.session:
        del request.session['is_admin']
    return redirect('login')
def review_users(request):
    
    # Fetch all registered users
    users = Register.objects.all()
    # Pass the users to the template
    return render(request, 'review_users.html', {'users': users})
from django.shortcuts import get_object_or_404, redirect
def delete_user(request, reg_id):
    # Retrieve the user from the Register table
    user = get_object_or_404(Register, reg_id=reg_id)
    
    try:
        # Delete associated Login records
        Login.objects.filter(reg_id=user).delete()
        # Delete the user from the Register table
        user.delete()
        messages.success(request, 'User has been deleted successfully.')
    except Exception as e:
        messages.error(request, f'An error occurred: {e}')
    
    # Redirect to the review users page
    return redirect('review_users')

def add_plan(request):
    plan_choices = MembershipPlan.PLAN_CHOICES

    if request.method == 'POST':
        plan_name = request.POST.get('plan_name')
        plan_details = request.POST.get('plan_details')
        price = request.POST.get('price')
        duration_months = request.POST.get('duration_months')

        # Validate input fields
        if not plan_name or not plan_details or not price or not duration_months:
            messages.error(request, 'Please fill in all fields.')
            return render(request, 'add_plan.html', {'plan_choices': plan_choices})

        try:
            price = float(price)
            duration_months = int(duration_months)
        except ValueError:
            messages.error(request, 'Invalid price or duration.')
            return render(request, 'add_plan.html', {'plan_choices': plan_choices})

        # Create and save the new membership plan
        plan = MembershipPlan(
            plan_name=plan_name,
            plan_details=plan_details,
            price=price,
            duration_months=duration_months
        )
        plan.save()
        messages.success(request, 'Membership plan added successfully.')
        return redirect('view_plans')  # Redirect to view plans after adding

    return render(request, 'add_plan.html', {'plan_choices': plan_choices})

def view_plans(request):
    plans = MembershipPlan.objects.all()
    return render(request, 'view_plans.html', {'plans': plans})
def edit_plan(request, plan_id):
    plan = get_object_or_404(MembershipPlan, plan_id=plan_id)

    if request.method == 'POST':
        plan_name = request.POST.get('plan_name')
        plan_details = request.POST.get('plan_details')
        price = request.POST.get('price')
        duration_months = request.POST.get('duration_months')

        # Validate input fields
        if not plan_name or not plan_details or not price or not duration_months:
            messages.error(request, 'Please fill in all fields.')
            return render(request, 'edit_plan.html', {'plan': plan})

        try:
            price = float(price)
            duration_months = int(duration_months)
        except ValueError:
            messages.error(request, 'Invalid price or duration.')
            return render(request, 'edit_plan.html', {'plan': plan})

        # Update the membership plan
        plan.plan_name = plan_name
        plan.plan_details = plan_details
        plan.price = price
        plan.duration_months = duration_months
        plan.save()
        messages.success(request, 'Membership plan updated successfully.')
        return redirect('view_plans')

    return render(request, 'edit_plan.html', {'plan': plan})
def delete_plan(request, plan_id):
    plan = get_object_or_404(MembershipPlan, plan_id=plan_id)

    if request.method == 'POST':
        plan.delete()
        messages.success(request, 'Membership plan deleted successfully.')
        return redirect('view_plans')  # Redirect to view plans after deleting

    return render(request, 'confirm_delete.html', {'plan': plan})

from django.shortcuts import render, redirect
from .models import Blog
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import os
from django.shortcuts import render, redirect

def blog_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')

        # Ensure that required fields are provided
        if title and content:
            # Create a new Blog instance and save it
            blog = Blog(title=title, content=content, image=image)
            blog.save()  # Save the blog post to the database

            return redirect('blog_create')  # Redirect to the same page to display updated list

    # Fetch existing blogs to display
    blogs = Blog.objects.all()

    return render(request, 'blog_create.html', {'blogs': blogs})
def edit_blog(request, blog_id):
    blog = get_object_or_404(Blog, blog_id=blog_id)  # Ensure you're using the correct model and ID field

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')

        # Ensure that required fields are provided
        if title and content:
            blog.title = title
            blog.content = content
            if image:
                blog.image = image
            blog.save()  # Save the updated blog post to the database

            return redirect('blog_create')  # Redirect to the list of blog posts

    # Render the edit form with the current blog details
    return render(request, 'edit_blog.html', {'blog': blog})

def delete_blog(request, blog_id):
    if request.method == 'POST':
        blog = get_object_or_404(Blog, blog_id=blog_id)  # Use blog_id instead of id
        blog.delete()
        return redirect('blog_create')
def create_notification(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        message = request.POST.get('message')

        if title and message:  # Basic validation
            try:
                # Create a notification for all users or use specific logic
                Notification.objects.create(
                    title=title,
                    message=message
                )
                # Redirect to a confirmation page or notification list
                return redirect('create_notification')  # Adjust the redirect as needed
            except Exception as e:
                return HttpResponse(f"Error: {e}", status=400)
        else:
            return HttpResponse("Invalid input", status=400)
    notifications = Notification.objects.all().order_by('-date_created')
    
    return render(request, 'create_notification.html', {'notifications': notifications})

def delete_notification(request, notification_id):
    if request.method == 'POST':
        notification = get_object_or_404(Notification, notification_id=notification_id)
        try:
            notification.delete()
            return redirect('create_notification')  # Redirect back to the notifications list
        except Exception as e:
            return HttpResponse(f"Error: {e}", status=400)
    else:
        return HttpResponse("Invalid request method", status=405)

def home(request):
    return render(request, 'home.html')



