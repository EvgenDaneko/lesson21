from django.shortcuts import render, get_object_or_404, redirect
from .models import Profile, Skill
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import conf
from django.contrib import messages
from .forms import ProfileForm, SkillForm, CustomUserCreationForm


def registerUser(request):
    form = CustomUserCreationForm()
    page = 'register'
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'Аккаунт успешно создан')
            return redirect('edit-account')

        else:
            messages.success(request, 'Во время регистрации произошла ошибка')
    context = {'form':form, 'page':page}
    return render(request, 'users/login_register.html', context)


def LoginUser(request):
    page = 'login'
    if request.User.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Такого пользователя не существует')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request.user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')

        else:
            messages.error(request, 'Неверное имя пользователся или пароль')

    return render(request, 'users/login_register.html')


def LogoutUser(request):
    logout(request)
    messages.info(request, 'Вы вышли из учетной записи')
    return redirect('login')





def profiles(request):
    profiles = Profile.objects.all()
    context = {'profiles': profiles}
    return render(request, 'users/profiles.html', context)


def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    main_skills = profile.skills.all()[:2]
    extra_skills = profile.skills.all()[2:]
    context = {'profile': profile, 'main_skills': main_skills,
               'extra_skills': extra_skills}
    return render(request, "users/user_profile.html", context)


def profiles_by_skill(request, skill_slug):
    skill = get_object_or_404(Skill, slug=skill_slug)
    profiles = Profile.object.filter(skills__in=[skill])
    context = {'profiles': profiles}
    return render(request, "users/profiles.html", context)


@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile
    skills = profile.skills.all()
    projects = profile.projects_set.all()

    context = {'profile': profile, 'skills': skills,
               'projects': projects}

    return render(request, 'users/account.html', context)

@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect('account')

    context = {'form': form}
    return render(request, 'users/profile_form.html', context)


@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill_slug = request.POST.get('slug')
            skill_description = request.POST.get('description')
            profile.skill.get_or_create(name=skill, slug=skill_slug, description=skill_description)
            messages.success(request, 'Навык добавлен')
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def updateSkill(request, skill_slug):
    profile = request.user.profile
    skill = profile.skills.get(slug=skill_slug)
    form = SkillForm(instance=skill)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Навый успешно обновлен')
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def deleteSkill(request, skill_slug):
    profile = request.user.profile
    skill = profile.skills.get(slug=skill_slug)
    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Навык успешно удален')
        return redirect('account')

    context = {'object': skill}
    return render(request, 'delete_template.html', context)