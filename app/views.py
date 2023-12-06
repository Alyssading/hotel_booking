# 用户视图

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse

from app.forms.user_forms import RegisterForm, LoginForm, UserInfoForm, ChangePwdForm
from app.models import User


@login_required(login_url='/login')
def register(
        request: WSGIRequest
):
    """
    Registration, limited to administrator user assignments only
    """

    if request.method == 'GET':
        register_form = RegisterForm()
        return render(request, 'user/register.html', {'register_form': register_form})
    elif request.method == 'POST':
        data = request.POST
        register_form = RegisterForm(data)
        if register_form.is_valid():
            user_obj = register_form.cleaned_data
            if user_obj.get('password') == user_obj.get('re_password'):
                # 这个create_user就是继承的AbstractUser里的方法
                new_user = User.objects.create_user(
                    username=user_obj.get('username'),
                    email=user_obj.get('email'),
                    password=user_obj.get('password'),
                    first_name=user_obj.get('first_name'),
                    last_name=user_obj.get('last_name')
                )
                return redirect('/user_list/')

            else:
                register_form.add_error(
                    field='re_password',
                    error='The passwords entered twice are inconsistent'
                )
        return render(request, 'user/register.html', {'register_form': register_form})


def user_register(
        request: WSGIRequest
):
    """
    registration
    """
    if request.method == 'GET':
        register_form = RegisterForm()
        return render(request, 'user/register.html', {'register_form': register_form})
    elif request.method == 'POST':
        data = request.POST
        register_form = RegisterForm(data)
        if register_form.is_valid():
            user_obj = register_form.cleaned_data
            if user_obj.get('password') == user_obj.get('re_password'):
                # Register a new user through the auth module and create a new user using the User table (create.use regular user, create.superuser super user)
                new_user = User.objects.create_user(
                    username=user_obj.get('username'),
                    email=user_obj.get('email'),
                    password=user_obj.get('password'),
                    nickname=user_obj.get('nickname'),
                    first_name=user_obj.get('first_name')
                )
                return redirect('/login')

            else:
                register_form.add_error(
                    field='re_password',
                    error='The passwords entered twice are inconsistent'
                )
        return redirect('/login')


def user_login(
        request: WSGIRequest
):
    """
    login
    """
    if request.method == 'GET':
        login_form = LoginForm()

        return render(
            request=request,
            template_name='user/login.html',
            context={
                'login_form': login_form
            }
        )
    elif request.method == 'POST':
        data = request.POST
        login_form = LoginForm(data)
        if login_form.is_valid():
            login_data = login_form.cleaned_data
            user = authenticate(
                **login_data
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, 'Login Successful')
                    return redirect(request.GET.get('next') or '/')
                else:
                    login_form.add_error(
                        field='username',
                        error='User not activate'
                    )
                    return render(request, 'user/login.html', {'login_form': login_form})
            else:
                login_form.add_error(
                    field='password',
                    error='Password invalid'
                )
                return render(request, 'user/login.html', {'login_form': login_form})
        else:
            return render(request, 'user/login.html', {'login_form': login_form})
    else:
        return HttpResponse('Request types not allowed')


def user_logout(
        request: WSGIRequest
):
    """logout"""
    logout(request)
    return redirect('/')


@login_required(login_url='/login')
def user_info(
        request: WSGIRequest
):
    user = request.user
    if request.method == 'GET':
        form = UserInfoForm(
            instance=user
        )
        return render(request, 'user/user_info.html', {'form': form})
    elif request.method == 'POST':
        print(request.POST)
        form = UserInfoForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            User.objects.filter(id=user.id).update(**form.cleaned_data)
            return redirect('/')
        else:
            return render(request, 'user/user_info.html', {'form': form})


@login_required(login_url='/login')
def change_pwd(
        request: WSGIRequest
):
    if request.method == 'GET':
        form = ChangePwdForm()
        return render(
            request=request,
            template_name='user/change_pwd.html',
            context={
                'form': form
            }
        )
    elif request.method == 'POST':
        data = request.POST
        form = ChangePwdForm(data)
        if form.is_valid():
            login_data = form.cleaned_data
            if login_data.get('password') == login_data.get('re_password'):
                user = request.user
                if user.check_password(login_data.get('password')):
                    user.set_password(login_data.get('new_password'))
                    user.save()
                    messages.add_message(request, level=messages.SUCCESS,
                                         message='Password modification successful, please log in again')
                    return redirect(to=reverse('login'))
                else:
                    form.add_error(
                        field='password',
                        error='Old password error'
                    )
            else:
                form.add_error(
                    field='password',
                    error='The passwords entered twice are inconsistent'
                )
        return render(request, 'user/change_pwd.html', {'form': form})
    else:
        return HttpResponse('Request not allowed')
