from django.shortcuts import render
from .forms import UploadCodonForm, UserLoginForm, UserRegForm
from Bio.Seq import Seq
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout


genome = Seq('TGACCCACTAATCAGCAACATAGCACTTTGAGCAAAGGCCTGTGTTGGAGCTATTGGCCCCAAAACTGCCTTTCCCTAAACAGTGTTCACCATTGTAGACCTCACCACTGTTCGCGTAACAACTGGCATGTCCTGGGGGTTAATACTCAC')

def form_view(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % ('/login/', request.path))
    if request.method == 'POST':
        form = UploadCodonForm(request.POST)
        if form.is_valid():
            reply=dict()
            codon = form.cleaned_data['form']
            if codon in genome:
                reply['result'] = f"Кодон - {codon} - найден"
            else:
                reply['result'] = f"Кодон - {codon} - не найден"
            return render(request, 'result.html', reply)
    else:
        form = UploadCodonForm()
        return render(request, 'start_page.html', {'form': form})


def login_view(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('/form/')
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/login/')

def register_view(request):
    form = UserRegForm(request.POST or None)
    if form.is_valid():
        new_user = form.save(commit=False)
        new_user.set_password(form.cleaned_data['password'])
        new_user.save()
        return redirect('/login/')
    return render(request, 'register.html', {'form': form})