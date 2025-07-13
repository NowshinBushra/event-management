from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from users.forms import CustomRegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from users.forms import LoginForm, AssignRoleForm, CreateGroupForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Prefetch
from events.models import Event
from django.utils.timezone import now

# Create your views here.

# Test for users
def is_admin(user):
    return user.groups.filter(name='Admin').exists()


def sign_up(request):
    # if request.method == 'GET':
    form = CustomRegisterForm()

    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password'))
            user.is_active = False
            user.save()

            user_group = Group.objects.get(name='User')
            user.groups.add(user_group)
            
            messages.success(request, "A Confirmation mail sent. Please check your email")
            return redirect('sign-in')
    return render(request, 'registration/register.html', {"form" : form})



def sign_in(request):
    form = LoginForm()
    if request.method == "POST":
        form= LoginForm(data = request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    return render(request, 'registration/login.html', {'form':form})


@login_required
def sign_out(request):
    if request.method == 'POST':
        logout(request)
        return redirect('sign-in')
    

def activate_user(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('sign-in')
        else:
            return HttpResponse('Invalid Id or token')

    except User.DoesNotExist:
        return HttpResponse('User not found')
    

@user_passes_test(is_admin, login_url='no-permission')
def admin_dashboard(request):
    users = User.objects.prefetch_related(
        Prefetch('groups', queryset=Group.objects.all(), to_attr='all_groups')).all()
    events = Event.objects.select_related('category').prefetch_related('participants').all()
    groups = Group.objects.prefetch_related('permissions').all()
    today = now().date()
    todays_event = Event.objects.filter(date=today)

    for user in users:
        if user.all_groups:
            user.group_name = user.all_groups[0].name
        else:
            user.group_name = 'No Group Assigned'

    context = {
        "users": users,
        'events': events,
        "todays_event": todays_event,
        'groups': groups,
    }
    return render(request, 'admin/dashboard.html', context)


@user_passes_test(is_admin, login_url='no-permission')
def assign_role(request, user_id):
    user = User.objects.get(id=user_id)
    form = AssignRoleForm()

    if request.method == 'POST':
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user.groups.clear()   
            user.groups.add(role)
            messages.success(request, f"User {user.username} has been assigned to the {role.name} role")
            return redirect('admin-dashboard')

    return render(request, 'admin/assign_role.html', {"form": form})

@user_passes_test(is_admin, login_url='no-permission')
def create_group(request):
    form = CreateGroupForm()
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)

        if form.is_valid():
            group = form.save()
            messages.success(request, f"Group {group.name} has been created successfully")
            return redirect('create-group')

    return render(request, 'admin/create_group.html', {'form': form})


@user_passes_test(is_admin, login_url='no-permission')
def group_list(request):
    groups = Group.objects.prefetch_related('permissions').all()
    return render(request, 'admin/group_list.html', {'groups': groups})


@user_passes_test(is_admin, login_url='no-permission')
def delete_user(request, user_id):
    if request.method =="POST":
        user = User.objects.get(id=user_id)
        user.delete()
        messages.success(request, 'User deleted successfully')
        return redirect('admin-dashboard')
    else:
        messages.success(request, 'Something went wrong')
        return redirect('admin-dashboard')
    

@user_passes_test(is_admin, login_url='no-permission')
def delete_group(request, grp_id):
    if request.method =="POST":
        group = Group.objects.get(id=grp_id)
        group.delete()
        messages.success(request, 'Group deleted successfully')
        return redirect('group-list')
    else:
        messages.success(request, 'Something went wrong')
        return redirect('group-list')
