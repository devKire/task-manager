from django.contrib import admin
from .models import Tarefa

@admin.register(Tarefa)
class TarefaAdmin(admin.ModelAdmin):
    list_display = ['descricao', 'prioridade', 'data_vencimento', 'concluida', 'usuario']
    list_filter = ['prioridade', 'concluida', 'data_vencimento']
    search_fields = ['descricao']