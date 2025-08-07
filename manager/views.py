from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from users.models import TrackedLink  # import your link model
from django.contrib import messages
from django.shortcuts import get_object_or_404

from django.db.models.functions import TruncDate
from django.db.models import Count
from django.utils import timezone
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth
from django.db.models import Count
from datetime import timedelta

from users.models import *


from users.models import TrackedLink
User = get_user_model()

@login_required(login_url='/login/')
def adminpanel(request):
    # Stats
    total_users = User.objects.count()
    total_links = TrackedLink.objects.count()

    # Users Data
    users_data = []
    for i, user in enumerate(User.objects.all(), start=1):
        users_data.append({
            "id": user.id,
            "sl_no": i,
            "name": user.get_full_name() or user.username,
            "email": user.email,
            "password": "********",
            "link_count": TrackedLink.objects.filter(user=user).count(),
        })

    # Links Data
    links_data = []
    for i, link in enumerate(TrackedLink.objects.all(), start=1):
        links_data.append({
            "id": link.id,
            "sl_no": i,
            "email": link.user.email,
            "category": link.category if link.category != "other" else link.other_category_name,
            "created_link": request.build_absolute_uri(f"/track/{link.id}/"),
        })

    return render(request, 'adminpanel.html', {
        "total_users": total_users,
        "total_links": total_links,
        "users_data": users_data,
        "links_data": links_data,
    })   

@login_required(login_url='/login/')
def manager_logout(request):
    logout(request)
    return redirect('users:login') 



@login_required(login_url='/login/')
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    # Prevent deleting superusers or yourself
    if user.is_superuser or user == request.user:
        return redirect('manager:adminpanel')
    user.delete()
    return redirect('manager:adminpanel')





@login_required(login_url='/login/')
def delete_link(request, link_id):
    link = get_object_or_404(TrackedLink, id=link_id)
    link.delete()
    return redirect('manager:adminpanel')

@login_required(login_url='/login/')
def view_link_details(request, link_id):
    link = get_object_or_404(TrackedLink, id=link_id)
    return render(request, 'adminsingle.html', {"link": link})




@login_required
def view_link_details(request, link_id):
    link = get_object_or_404(TrackedLink, id=link_id)

    # Get all clicks for this link
    clicks = TrackedClick.objects.filter(link=link)

    # Time calculations
    now = timezone.now()
    last_7_days = now - timedelta(days=7)
    last_4_weeks = now - timedelta(weeks=4)
    last_6_months = now - timedelta(days=180)

    # Clicks per Day (last 7 days)
    clicks_per_day = clicks.filter(timestamp__gte=last_7_days) \
        .annotate(day=TruncDay('timestamp')) \
        .values('day') \
        .annotate(count=Count('id')) \
        .order_by('day')

    # Clicks per Week (last 4 weeks)
    clicks_per_week = clicks.filter(timestamp__gte=last_4_weeks) \
        .annotate(week=TruncWeek('timestamp')) \
        .values('week') \
        .annotate(count=Count('id')) \
        .order_by('week')

    # Clicks per Month (last 6 months)
    clicks_per_month = clicks.filter(timestamp__gte=last_6_months) \
        .annotate(month=TruncMonth('timestamp')) \
        .values('month') \
        .annotate(count=Count('id')) \
        .order_by('month')

    return render(request, 'adminsingle.html', {
        'link': link,
        'clicks_per_day': list(clicks_per_day),
        'clicks_per_week': list(clicks_per_week),
        'clicks_per_month': list(clicks_per_month),
    })