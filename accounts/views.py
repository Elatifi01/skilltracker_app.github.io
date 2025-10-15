from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import UserProfile
from .forms import CustomUserCreationForm


def logout_view(request):
    # log out the current user
    logout(request)
    return redirect('tracker:dashboard')


class RegisterView(CreateView):
    model = UserProfile
    form_class = CustomUserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('tracker:dashboard')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

class ProfileView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    
    fields = ['first_name', 'last_name', 'email', 'profile_picture', 'skill_level', 'bio']
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('accounts:profile')
    
    def get_object(self):        
        user = self.request.user
        return user
