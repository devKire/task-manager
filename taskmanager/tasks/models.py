from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator

class Categoria(models.Model):
    nome = models.CharField(max_length=50)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    cor = models.CharField(max_length=7, default='#007bff')  
    
    def __str__(self):
        return self.nome

class Tarefa(models.Model):
    PRIORIDADE_CHOICES = [
        ('alta', 'Alta'),
        ('media', 'Média'),
        ('baixa', 'Baixa'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    descricao = models.CharField(max_length=200)
    prioridade = models.CharField(max_length=10, choices=PRIORIDADE_CHOICES, default='media')
    data_vencimento = models.DateField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    concluida = models.BooleanField(default=False)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    notas = models.TextField(blank=True)
    tempo_estimado = models.IntegerField(default=0,validators=[MinValueValidator(0)],help_text="Tempo estimado em minutos (mínimo: 0)")
    
    def __str__(self):
        return f"{self.descricao} - {self.get_prioridade_display()}"
    
    def esta_atrasada(self):
        return not self.concluida and self.data_vencimento < timezone.now().date()
    
    class Meta:
        ordering = ['-prioridade', 'data_vencimento']