import os
import json

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

def adicionar_tarefa(tarefa):
    tarefas.append(tarefa)
    print(f"\n✅ Tarefa '{tarefa}' adicionada com sucesso!")

def mostrar_tarefas():
    print("\n=-=-=-=-=-=-=-=-=-=-=")
    print("LISTA DE TAREFAS")
    print("=-=-=-=-=-=-=-=-=-=-=")
    if not tarefas:
        print("Nenhuma tarefa encontrada.")
    else:
        for i, tarefa in enumerate(tarefas, start=1):
            print(f"{i}. {tarefa}")

def marcar_tarefa_concluida(indice):
    if 0 <= indice < len(tarefas):
        if not tarefas[indice].startswith("✅"):
            tarefas[indice] = f"✅ {tarefas[indice]}"
            print(f"\n✅ Tarefa marcada como concluída!")
        else:
            print("\nEssa tarefa já está marcada como concluída.")
    else:
        print("\n❌ Índice inválido.")

def remover_tarefa(indice):
    if 0 <= indice < len(tarefas):
        tarefa = tarefas.pop(indice)
        print(f"\n🗑️ Tarefa '{tarefa}' removida com sucesso!")
    else:
        print("\n❌ Índice inválido.")

# Loop principal
while True:
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=-=-=-=-=-=-=-=-=-=-=")
    print("GERENCIADOR DE TAREFAS")
    print("=-=-=-=-=-=-=-=-=-=-=")
    
    for i, opcao in enumerate(opcoes, start=1):
        print(f"{i}. {opcao}")

    escolha = input("\nEscolha uma opção (1-5): ")

    if escolha == '1':
        tarefa = input("\nDigite a nova tarefa: ").strip()
        if tarefa:
            adicionar_tarefa(tarefa)
        else:
            print("⚠️ Tarefa vazia não adicionada.")
        input("\nPressione Enter para continuar...")

    elif escolha == '2':
        mostrar_tarefas()
        input("\nPressione Enter para continuar...")

    elif escolha == '3':
        mostrar_tarefas()
        try:
            indice = int(input("\nDigite o número da tarefa para marcar como concluída: ")) - 1
            marcar_tarefa_concluida(indice)
        except ValueError:
            print("❌ Entrada inválida. Digite um número.")
        input("\nPressione Enter para continuar...")

    elif escolha == '4':
        mostrar_tarefas()
        try:
            indice = int(input("\nDigite o número da tarefa para remover: ")) - 1
            remover_tarefa(indice)
        except ValueError:
            print("❌ Entrada inválida. Digite um número.")
        input("\nPressione Enter para continuar...")

    elif escolha == '5':
        salvar_tarefas()
        print("\n💾 Tarefas salvas. Até logo!")
        break

    else:
        print("❌ Opção inválida. Tente novamente.")
        input("\nPressione Enter para continuar...")
