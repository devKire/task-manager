from django import forms
from django.core.validators import MinValueValidator
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Tarefa, Categoria

class TarefaForm(forms.ModelForm):
    data_vencimento = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="Data de Vencimento"
    )
    
    tempo_estimado = forms.IntegerField(
        min_value=0,  # Não permite valores negativos
        widget=forms.NumberInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Minutos',
            'min': '0'  # Validação no HTML também
        }),
        help_text="Digite um valor maior ou igual a 0",
        initial=0  # Valor padrão
    )
    
    class Meta:
        model = Tarefa
        fields = ['descricao', 'prioridade', 'data_vencimento', 'categoria', 'notas', 'tempo_estimado', 'concluida']
        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite a tarefa...'}),
            'prioridade': forms.Select(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Notas adicionais...'}),
            'concluida': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['categoria'].queryset = Categoria.objects.filter(usuario=user)
            self.fields['categoria'].empty_label = "Selecione uma categoria"
    
    def clean_tempo_estimado(self):
        """Validação personalizada para tempo_estimado"""
        tempo_estimado = self.cleaned_data.get('tempo_estimado')
        
        if tempo_estimado is not None and tempo_estimado < 0:
            raise forms.ValidationError("O tempo estimado não pode ser negativo.")
        
        return tempo_estimado
    def clean_descricao(self):
        """Limpa e valida a descrição"""
        descricao = self.cleaned_data.get('descricao', '')
        
        # Remove espaços extras no início e fim
        descricao = descricao.strip()
        
        # Garante que a descrição não esteja vazia
        if not descricao:
            raise forms.ValidationError("A descrição da tarefa é obrigatória.")
        
        # Remove caracteres problemáticos (opcional)
        # descricao = descricao.encode('ascii', 'ignore').decode('ascii')
        
        return descricao
class CategoriaForm(forms.ModelForm):
    cor = forms.CharField(
        widget=forms.TextInput(attrs={'type': 'color', 'class': 'form-control form-control-color'}),
        label="Cor da Categoria"
    )
    
    class Meta:
        model = Categoria
        fields = ['nome', 'cor']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da categoria...'}),
        }

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Seu melhor email'})
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Seu nome'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Seu sobrenome'})
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome de usuário'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Senha'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirme a senha'})