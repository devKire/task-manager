import os
import json
from tabulate import tabulate 

ARQUIVO = "tarefas.json"
tarefas = []

# Carrega tarefas salvas (se houver)
if os.path.exists(ARQUIVO):
    with open(ARQUIVO, "r", encoding="utf-8") as f:
        try:
            tarefas = json.load(f)
        except json.JSONDecodeError:
            tarefas = []

opcoes = [
    'Adicionar tarefa',
    'Listar tarefas',
    'Marcar tarefa como concluída',
    'Remover tarefa',
    'Sair e salvar'
]

def salvar_tarefas():
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(tarefas, f, ensure_ascii=False, indent=4)

def adicionar_tarefa(tarefa, prioridade, data):
    nova_tarefa = {
        "descricao": tarefa,
        "prioridade": prioridade.lower(),
        "data": data,
        "concluida": False
    }
    tarefas.append(nova_tarefa)
    print(f"\n✅ Tarefa '{tarefa}' adicionada com prioridade '{prioridade.upper()}' e data {data}.")


def mostrar_tarefas(filtro=None):
    if filtro:
        filtro = filtro.lower()
        if filtro in ['alta', 'média', 'media', 'baixa']:
            # Tratar 'media' e 'média' como o mesmo
            prioridade_filtrada = 'media' if filtro in ['media', 'média'] else filtro
            tarefas_filtradas = [t for t in tarefas if t["prioridade"] == prioridade_filtrada]
        elif filtro == 'concluidas':
            tarefas_filtradas = [t for t in tarefas if t["concluida"]]
        elif filtro == 'pendentes':
            tarefas_filtradas = [t for t in tarefas if not t["concluida"]]
        elif filtro == 'todas':
            tarefas_filtradas = tarefas
        else:
            tarefas_filtradas = tarefas
    else:
        tarefas_filtradas = tarefas

    if not tarefas_filtradas:
        print("\n⚠️ Nenhuma tarefa encontrada.")
        return

    tabela = []
    for i, t in enumerate(tarefas_filtradas, 1):
        status = "✅" if t["concluida"] else "⏳"
        tabela.append([i, t["descricao"], t["prioridade"].capitalize(), t["data"], status])

    print("\n" + tabulate(tabela, headers=["ID", "Descrição", "Prioridade", "Data", "Status"], tablefmt="grid"))


def marcar_tarefa_concluida(indice):
    if 0 <= indice < len(tarefas):
        if not tarefas[indice]["concluida"]:
            tarefas[indice]["concluida"] = True
            print("\n✅ Tarefa marcada como concluída.")
        else:
            print("\n⚠️ Essa tarefa já está concluída.")
    else:
        print("\n❌ Índice inválido.")


def remover_tarefa(indice):
    if 0 <= indice < len(tarefas):
        tarefa = tarefas.pop(indice)
        print(f"\n🗑️ Tarefa '{tarefa}' removida com sucesso!")
    else:
        print("\n❌ Índice inválido.")

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')
# Loop principal
while True:
    limpar_tela()
    print("=-=-=-=-=-=-=-=-=-=-=")
    print("GERENCIADOR DE TAREFAS")
    print("=-=-=-=-=-=-=-=-=-=-=")
    
    for i, opcao in enumerate(opcoes, start=1):
        print(f"{i}. {opcao}")

    escolha = input("\nEscolha uma opção (1-5): ")

    if escolha == '1':
            limpar_tela()
            tarefa = input("\nDigite a nova tarefa: ").strip()
            data = 'DD/MM/AAAA'
            prioridade = '' 
            while data == 'DD/MM/AAAA':
                data = input("Digite a data de vencimento (DD/MM/AAAA): ").strip()
                if len(data) != 10 or data[2] != '/' or data[5] != '/':
                    print("❌ Data inválida. Use o formato DD/MM/AAAA.")
                    data = 'DD/MM/AAAA'
            while prioridade not in ['alta', 'media', 'baixa']:
                prioridade = input("Digite a prioridade (alta, media, baixa): ").strip().lower()
                if prioridade not in ['alta', 'media', 'baixa']:
                    print("❌ Prioridade inválida. Use 'alta', 'media' ou 'baixa'.") 
            if tarefa:
                adicionar_tarefa(tarefa, prioridade, data)
            else:
                print("⚠️ Tarefa vazia não adicionada.")
    
    elif escolha == '2':
        limpar_tela()
        filtro = ''
        while filtro not in ['alta', 'media', 'baixa', 'todas']:
            filtro = input("\nDeseja filtrar por prioridade? (alta, media, baixa, todas): ").strip().lower()
            if filtro not in ['alta', 'media', 'baixa', 'todas']:
                print("❌ Opção inválida. Tente novamente.")
        mostrar_tarefas(filtro)
        input("\nPressione Enter para continuar...")

    elif escolha == '3':
        limpar_tela()
        mostrar_tarefas(filtro='todas')
        try:
            indice = int(input("\nDigite o número da tarefa para marcar como concluída: ")) - 1
            marcar_tarefa_concluida(indice)
        except ValueError:
            print("❌ Entrada inválida. Digite um número.")
        input("\nPressione Enter para continuar...")

    elif escolha == '4':
        limpar_tela()
        mostrar_tarefas(filtro='todas')
        try:
            indice = int(input("\nDigite o número da tarefa para remover: ")) - 1
            remover_tarefa(indice)
        except ValueError:
            print("❌ Entrada inválida. Digite um número.")
        input("\nPressione Enter para continuar...")

    elif escolha == '5':
        limpar_tela()
        mostrar_tarefas(filtro='todas')
        print("\n💾 Tarefas salvas. Até logo!")
        break

    else:
        print("❌ Opção inválida. Tente novamente.")
        input("\nPressione Enter para continuar...")
