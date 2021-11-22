from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth, messages
from receitas.models import Receita

def cadastro(request):
    """Realiza o cadastro de uma pessoa no sistema"""
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        senha = request.POST['password']
        senha2 = request.POST['password2']

        if campo_vazio(nome):
            messages.error(request, 'O nome não pode ser vazio')
            return redirect('cadastro')
        if campo_vazio(email):
            messages.error(request, 'O email não pode ser vazio')
            return redirect('cadastro')
        if campo_vazio(senha) or campo_vazio(senha2):
            messages.error(request, 'A senha não pode ser vazia')
            return redirect('cadastro')
        if senha_nao_iguais(senha, senha2):
            messages.error(request, 'As senhas não são iguais')
            return redirect('cadastro')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Usuário já cadastrado')
            return redirect('cadastro')
        if User.objects.filter(username=nome).exists():
            messages.error(request, 'Usuário já cadastrado')
            return redirect('cadastro')
        user = User.objects.create_user(username=nome, email=email, password=senha)
        user.save()
        messages.success(request, 'Cadastro realizado com sucesso')
        return redirect('login')
    else:
        return render(request, 'usuarios/cadastro.html')

def login(request):
    """Realiza o login de uma pessoa no sistema"""
    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['senha']
        if campo_vazio(email) or campo_vazio(senha):
            messages.error(request, 'Os campos email e senha não podem ficar em branco')
            return redirect('login')
        print(email, senha)
        if User.objects.filter(email=email).exists():
            nome = User.objects.filter(email=email).values_list('username', flat=True).get()
            user = auth.authenticate(request, username=nome, password=senha)
            if user is not None:
                auth.login(request, user)
                messages.success(request, 'Login realizado com sucesso')
                return redirect('dashboard')
            else:
                messages.error(request, 'Usuário ou senha incorreto, por favor tente novamente')
    return render(request, 'usuarios/login.html')

def logout(request):
    """Realiza o logout de uma pessoa no sistema"""
    auth.logout(request)
    return redirect('index')

def dashboard(request):
    """Verifica se a pessoa já tem uma conta no sistema e redireciona para o dashboard"""
    if request.user.is_authenticated:
        id = request.user.id
        receitas = Receita.objects.filter(pessoa=id).order_by('-date_receita')

        dados={
            'receitas' : receitas
        }

        return render(request, 'usuarios/dashboard.html', dados)
    return redirect('index')        

def campo_vazio(campo):
    return not campo.strip()

def senha_nao_iguais(senha, senha2):
    return senha != senha2