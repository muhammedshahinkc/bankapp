from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages, auth
from .forms import PersonForm
from .models import Person, Branch


def home(request):
    return render(request, 'home.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('info')
        else:
            messages.info(request, "Incorrect Password")

    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, "User already exists")
            user = User.objects.create_user(username=username, password=password)
            user.save();
            return redirect('login')
        else:
            messages.info(request, 'Passwords does not match')
    return render(request, 'register.html')


def logout(request):
    auth.logout(request)
    return redirect('/')


def personDetail(request):
    form = PersonForm()
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            form.save();
            messages.info(request, 'Application accepted ')
            return redirect("/")
    return render(request, 'person_detail.html', {'form': form})


def person_update_view(request, pk):
    person = get_object_or_404(Person, pk=pk)
    form = PersonForm(instance=person)
    if request.method == 'POST':
        form = PersonForm(request.POST, instance=person)
        if form.is_valid():
            form.save()
            return redirect('person_change', pk=pk)
    return render(request, 'person_detail.html', {'form': form})


def load_branches(request):
    district_id = request.GET.get('district_id')
    branches = Branch.objects.filter(district_id=district_id).all()
    return render(request, 'branch_dropdown.html', {'branches': branches})


def infodata(request):
    return render(request, 'info.html')