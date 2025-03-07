from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserEditForm
from django.contrib import messages
from .forms import UserRegistrationForm


@login_required  # Ensures only logged-in users can access this page
def dashboard(request):
    return render(request, 'accounts/dashboard.html')

@login_required
def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User created successfully!")
            return redirect('dashboard')  # Redirect after creating a user
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register_user.html', {'form': form})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES, instance=request.user)  # Handle image upload
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('dashboard')
    else:
        form = UserEditForm(instance=request.user)
    
    return render(request, 'accounts/edit_profile.html', {'form': form})


@login_required
def my_profile(request):
    return render(request, 'accounts/my_profile.html', {'user': request.user})
