from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from users.models import User, Customer 
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse
from .models import TrackedLink
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.db import IntegrityError





def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            auth_login(request, user)

           
            if user.is_superuser or getattr(user, 'is_manager', False):
                return redirect('manager:adminpanel')
            else:
                return redirect('users:index')
        else:
            context = {
                "error": True,
                "message": "Invalid Email or Password"
            }
            return render(request, 'login.html', context)

    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(email=email).exists():
            context = {
                "error": True,
                "message": "Email already exists"
            }
            return render(request, 'register.html', context)

        # Create user
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            is_customer=True
        )

        # Create related customer profile
        Customer.objects.create(user=user)

        return HttpResponseRedirect(reverse('users:login'))

    return render(request, 'register.html')


@login_required(login_url='/login/')
def logout_view(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('users:login'))


@login_required(login_url='/login/')
@login_required
def index(request):
    if request.method == "POST":
        url = request.POST.get("url")
        category = request.POST.get("category")
        other_category = request.POST.get("other_category") if category == "other" else ""
        custom_slug = request.POST.get("custom_slug") or None

        link = TrackedLink.objects.create(
            user=request.user,
            url=url,
            category=category,
            other_category_name=other_category,
            custom_slug=custom_slug
        )

        if custom_slug:
            tracking_url = request.build_absolute_uri(
                reverse("users:track_custom", args=[custom_slug])
            )
        else:
            tracking_url = request.build_absolute_uri(
                reverse("users:track_click", args=[link.id])
            )

        return JsonResponse({"tracking_url": tracking_url})

    links = TrackedLink.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "index.html", {"links": links})


def track_custom(request, slug):
    link = get_object_or_404(TrackedLink, custom_slug=slug)
    link.click_count += 1
    link.save()
    return redirect(link.url)


def track_click(request, link_id):
    link = get_object_or_404(TrackedLink, id=link_id)
    link.click_count += 1
    link.save()
    return redirect(link.url)

@login_required
def delete_link(request, link_id):
    link = get_object_or_404(TrackedLink, id=link_id, user=request.user)
    link.delete()
    messages.success(request, "Link deleted successfully.")
    return redirect("users:index")


