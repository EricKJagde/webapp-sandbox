from django.http import Http404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .models import CustomUser
from .forms import CustomUserCreationForm


def index(request):
    context = {
        'navbar_home_class': 'active'
    }
    return render(request, 'home/index.html', context)


def explore(request):
    user_list = CustomUser.objects.order_by('-username')
    if len(user_list) > 10:
        user_list = user_list[:10]
    context = {
        'navbar_explore_class': 'active',
        'user_list': user_list
    }
    return render(request, 'home/explore.html', context)


def post(request):
    context = {
        'navbar_post_class': 'active',
    }
    return render(request, 'home/post.html', context)


def roster(request):
    context = {
        'navbar_roster_class': 'active',
    }
    return render(request, 'home/roster.html', context)


def profile(request):
    """For user that is logged in."""
    context = {
        'navbar_profile_class': 'active',
        'user_specific': request.user
    }
    return render(request, 'home/profile.html', context)


def profile_spec(request, username):
    """For custom search of different user."""
    try:
        user_specific = CustomUser.objects.get(username=username)
    except CustomUser.DoesNotExist:
        raise Http404("CustomUser does not exist")

    context = {
        'user_specific': user_specific,
    }
    return render(request, 'home/profile.html', context)


def about(request):
    context = {
        'navbar_about_class': 'active',
    }
    return render(request, 'home/about.html', context)


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
