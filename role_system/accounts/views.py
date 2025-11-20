# accounts/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login,authenticate 
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import SignupForm, UserUpdateForm
from .models import CustomUser
from django.contrib.auth import logout
# --- 1. Signup View ---
def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
        else:
            # --- ADD THIS TEMPORARY DEBUGGING LINE ---
            print("FORM ERRORS:", form.errors) 

    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})
# --- Login Logic &  Redirection Logic ---
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # REDIRECTION LOGIC 
            if user.role == 'admin':
                return redirect('admin_dashboard')
            else:
                return redirect('customer_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# ---  Dashboard Interfaces ---

@login_required
def customer_dashboard(request):
    # Security Check: Prevent Admin from accidentally landing here
    if request.user.role == 'admin':
        return redirect('admin_dashboard')
        
    return render(request, 'customer_dashboard.html')

@login_required
def admin_dashboard(request):
    # Security Check: Prevent Customer from seeing Admin Dash
    if request.user.role != 'admin':
        return redirect('customer_dashboard')
    
    # Fetch all users for the table
    users = CustomUser.objects.all()
    return render(request, 'admin_dashboard.html', {'users': users})

# ---  CRUD Operations ---

@login_required
def delete_user(request, user_id):
    # Security: Only admin can delete
    if request.user.role != 'admin': 
        return redirect('customer_dashboard')
        
    user_to_delete = get_object_or_404(CustomUser, id=user_id)
    user_to_delete.delete()
    return redirect('admin_dashboard')

@login_required
def update_user(request, user_id):
    # Security: Only admin can update
    if request.user.role != 'admin':
        return redirect('customer_dashboard')
        
    user_to_update = get_object_or_404(CustomUser, id=user_id)
    
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user_to_update)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = UserUpdateForm(instance=user_to_update)
        
    return render(request, 'update_user.html', {'form': form, 'target_user': user_to_update})

# --- Logout Logic &  Redirection Logic ---
def logout_view(request):
    logout(request)
    return redirect('login')