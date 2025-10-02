import sys
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.encoding import force_str
from .models import Tarefa, Categoria
from .forms import TarefaForm, CategoriaForm, CustomUserCreationForm

@login_required
def lista_tarefas(request):
    filtro = request.GET.get('filtro', 'todas')
    
    tarefas = Tarefa.objects.filter(usuario=request.user)
    
    if filtro == 'pendentes':
        tarefas = tarefas.filter(concluida=False)
    elif filtro == 'concluidas':
        tarefas = tarefas.filter(concluida=True)
    elif filtro in ['alta', 'media', 'baixa']:
        tarefas = tarefas.filter(prioridade=filtro)
    
    # Inicializa o formulário vazio para nova tarefa
    form = TarefaForm(user=request.user)
    
    if request.method == 'POST':
        form = TarefaForm(request.POST, user=request.user)
        if form.is_valid():
            nova_tarefa = form.save(commit=False)
            nova_tarefa.usuario = request.user
            nova_tarefa.save()
            messages.success(request, '✅ Tarefa adicionada com sucesso!')
            return redirect('tasks:lista_tarefas')
    
    return render(request, 'tasks/lista_tarefas.html', {
        'tarefas': tarefas,
        'form': form,
        'filtro_atual': filtro
    })

@login_required
def editar_tarefa(request, tarefa_id):
    tarefa = get_object_or_404(Tarefa, id=tarefa_id, usuario=request.user)
    
    if request.method == 'POST':
        form = TarefaForm(request.POST, instance=tarefa, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Tarefa atualizada com sucesso!')
            return redirect('tasks:lista_tarefas')
    else:
        form = TarefaForm(instance=tarefa, user=request.user)
    
    return render(request, 'tasks/editar_tarefa.html', {
        'form': form,
        'tarefa': tarefa
    })

@login_required
def marcar_concluida(request, tarefa_id):
    try:
        tarefa = get_object_or_404(Tarefa, id=tarefa_id, usuario=request.user)
        tarefa.concluida = not tarefa.concluida
        tarefa.save()
        
        # Mensagem mais simples e segura
        if tarefa.concluida:
            messages.success(request, '✅ Tarefa marcada como concluída!')
        else:
            messages.success(request, '🔄 Tarefa marcada como pendente!')
        
    except Exception as e:
        messages.error(request, f'❌ Erro ao atualizar a tarefa.')
        # Log do erro para debug
        print(f"Erro ao marcar tarefa como concluída: {str(e)}")
    
    return redirect('tasks:lista_tarefas')

@login_required
def excluir_tarefa(request, tarefa_id):
    tarefa = get_object_or_404(Tarefa, id=tarefa_id, usuario=request.user)
    tarefa.delete()
    messages.success(request, '🗑️ Tarefa excluída com sucesso!')
    
    return redirect('tasks:lista_tarefas')

@login_required
def lista_categorias(request):
    categorias = Categoria.objects.filter(usuario=request.user)
    form = CategoriaForm()
    
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            nova_categoria = form.save(commit=False)
            nova_categoria.usuario = request.user
            nova_categoria.save()
            messages.success(request, '✅ Categoria criada com sucesso!')
            return redirect('tasks:lista_categorias')
    
    return render(request, 'tasks/lista_categorias.html', {
        'categorias': categorias,
        'form': form
    })

@login_required
def excluir_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id, usuario=request.user)
    
    # Verifica se há tarefas usando esta categoria
    tarefas_com_categoria = Tarefa.objects.filter(categoria=categoria, usuario=request.user)
    
    if tarefas_com_categoria.exists():
        messages.error(request, '❌ Não é possível excluir esta categoria pois existem tarefas vinculadas a ela.')
        return redirect('tasks:lista_categorias')
    
    categoria.delete()
    messages.success(request, '🗑️ Categoria excluída com sucesso!')
    return redirect('tasks:lista_categorias')

# View de Registro
def registrar(request):
    if request.user.is_authenticated:
        return redirect('tasks:lista_tarefas')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Cria algumas categorias padrão para o novo usuário
            categorias_padrao = [
                {'nome': 'Trabalho', 'cor': '#007bff'},
                {'nome': 'Pessoal', 'cor': '#28a745'},
                {'nome': 'Estudos', 'cor': '#ffc107'},
                {'nome': 'Urgente', 'cor': '#dc3545'},
            ]
            
            for cat in categorias_padrao:
                Categoria.objects.create(
                    nome=cat['nome'],
                    cor=cat['cor'],
                    usuario=user
                )
            
            # Loga o usuário automaticamente após o registro
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            
            messages.success(request, '🎉 Conta criada com sucesso! Bem-vindo ao Task Manager!')
            return redirect('tasks:lista_tarefas')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/registrar.html', {'form': form})

# View de Login Personalizada (opcional, para substituir a padrão)
def user_login(request):
    if request.user.is_authenticated:
        return redirect('tasks:lista_tarefas')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'👋 Bem-vindo de volta, {user.first_name or user.username}!')
            next_url = request.GET.get('next', 'tasks:lista_tarefas')
            return redirect(next_url)
        else:
            messages.error(request, '❌ Usuário ou senha incorretos.')
    
    return render(request, 'registration/login.html')

def user_logout(request):
    if request.method == 'POST':
        auth_logout(request)
        messages.success(request, '👋 Você saiu com sucesso!')
        return redirect('tasks:login')
    else:
        # Se for GET, mostra uma página de confirmação
        return render(request, 'registration/confirmar_logout.html')