from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib import messages
from .forms import CustomUserCreationForm, ForgotPasswordForm
from .models import CustomUser
from django.contrib.auth import get_backends 
from django.contrib.auth.tokens import default_token_generator
from .tasks import send_password_reset_email
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.conf import settings

# Home view (requires user login)
def home_view(request):
    return render(request, 'users/login.html')

# Register view
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            
            # Check if the role is 'Admin' or 'Moderator'
            if user.role in ['Admin', 'Moderator']:
                # Send an email to all Superadmins for approval
                superadmins = CustomUser.objects.filter(role='Superadmin')
                if superadmins.exists():
                    for superadmin in superadmins:
                        send_mail(
                            subject='Approval Request for New Registration',
                            message=(
                                f'A new user {user.username} has registered as {user.role} and needs your approval.'
                            ),
                            from_email=settings.EMAIL_HOST_USER,
                            recipient_list=[superadmin.email],
                            fail_silently=False,
                        )
                
                messages.info(
                    request, f'Registration submitted for {user.role}. Awaiting Superadmin approval.'
                )
                
                # Set the user as inactive until approved
                user.is_active = False

            user.save()

            # Set the backend explicitly
            backend = get_backends()[0]  # Use the first backend by default
            user.backend = f'{backend.__module__}.{backend.__class__.__name__}'

            login(request, user, backend=user.backend)
            return redirect('product_list')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'users/register.html', {'form': form})

def approve_user(request, user_id):
    if request.user.role == 'Superadmin':
        user = CustomUser.objects.get(id=user_id)
        user.is_active = True
        user.save()
        messages.success(request, f'{user.username} has been approved and can now log in.')
        return redirect('user_list')

def deny_user(request, user_id):
    if request.user.role == 'Superadmin':
        user = CustomUser.objects.get(id=user_id)
        user.delete()
        messages.success(request, f'{user.username} has been denied and their account has been deleted.')
        return redirect('user_list')

# Login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('product_list')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

# Logout view
def logout_view(request):
    logout(request)
    return redirect('login')

# Forgot password view
def forgot_password_view(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            users = CustomUser.objects.filter(email=email)

            if users.exists():
                current_site = get_current_site(request)
                for user in users:
                    send_password_reset_email.delay(user.id, current_site.domain, email)

                messages.success(request, 'If an account exists with that email, a reset link will be sent.')
            else:
                messages.error(request, 'No account found with that email address.')

            return redirect('login')  
    else:
        form = ForgotPasswordForm()

    return render(request, 'users/forgot_password.html', {'form': form})

User = get_user_model()

def is_admin_or_superadmin(user):
    return user.is_authenticated and user.role in ['Admin', 'Superadmin']

@login_required
@user_passes_test(is_admin_or_superadmin)
def user_list(request):
    User = get_user_model()  
    users = User.objects.all()
    return render(request, 'users/user_list.html', {'users': users})

@login_required
@user_passes_test(is_admin_or_superadmin)
def delete_user(request, user_id):
    user_to_delete = get_object_or_404(User, id=user_id)
    current_user = request.user

    # Define role-based deletion rules
    if current_user.role == 'Admin':
        # Admins can only delete users and moderators
        if user_to_delete.role in ['Admin', 'Superadmin']:
            messages.error(request, "You do not have permission to delete this user.")
            return redirect('user_list')

    elif current_user.role == 'Superadmin':
        # Superadmins can delete any user but themselves
        if user_to_delete == current_user:
            messages.error(request, "You cannot delete yourself.")
            return redirect('user_list')

    # Proceed to delete the user if all conditions are met
    user_to_delete.delete()
    messages.success(request, 'User account deleted successfully.')
    return redirect('user_list')

@login_required
@user_passes_test(lambda u: u.role == 'Superadmin')
def approve_user(request, user_id):
    user_to_approve = get_object_or_404(CustomUser, id=user_id)
    user_to_approve.is_approved = True
    user_to_approve.is_active = True
    user_to_approve.save()
    messages.success(request, f'User {user_to_approve.username} has been approved.')
    return redirect('user_list')