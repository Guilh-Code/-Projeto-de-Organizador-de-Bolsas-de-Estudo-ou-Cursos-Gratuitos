from datetime import datetime
from time import sleep
import json
import csv

# ===========================================================
# Arquivos JSON
# ===========================================================

# Salva os dados da lista 'bolsas' no arquivo JSON
def salvar_bolsas_em_arquivos(nome_arquivo='bolsas.json'):
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        json.dump(bolsas, f, indent=4, ensure_ascii=False)
    print('📁 Dados salvos com sucesso!')

# Carrega os dados do arquivo JSON para a lista 'bolsas'
def carregar_bolsas_de_arquivo(nome_arquivo='bolsas.json'):
    global bolsas
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as f:
            bolsas = json.load(f)
        print('📂 Dados carregados com sucesso!')
    except FileNotFoundError:
        bolsas = []
        print('⚠️ Arquivo não encontrado. Nenhuma bolsa carregada.')

# ===========================================================
# Exportar para .CSV
# ===========================================================

# Exporta as bolsas para um arquivo CSV legível por Excel/Google Planilhas
def exportar_bolsas_para_csv(nome_arquivo='bolsas_exportadas.csv'):
    if not bolsas:
        print('⚠️ Nenhuma bolsa cadastrada para exportar.')
        return

    try:
        with open(nome_arquivo, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # Cabeçalho do CSV
            writer.writerow(['Nome', 'Instituição', 'Modalidade', 'Valor', 'Prazo de Inscrição'])
            # Escrevendo cada bolsa no CSV
            for bolsa in bolsas:
                writer.writerow([
                    bolsa['nome'],
                    bolsa['instituicao'],
                    bolsa['modalidade'],
                    formatar_valor(bolsa['valor']),
                    formatar_data_brasileira(bolsa['prazo_inscricao'])
                ])
        print(f'✅ Bolsas exportadas com sucesso para {nome_arquivo}')
    except Exception as e:
        print(f'❌ Erro ao exportar: {e}')

# ===========================================================
# Variável Principal
# ===========================================================

bolsas = []  # Lista que armazena todas as bolsas cadastradas

# ===========================================================
# Códigos de Cores ANSI (para terminal colorido)
# ===========================================================

RESET = "\033[0m"
VERDE = "\033[92m"
VERMELHO = "\033[91m"
AZUL = "\033[94m"
AMARELO = "\033[93m"
CIANO = "\033[96m"
NEGRITO = "\033[1m"

# ===========================================================
# Interface de Menu
# ===========================================================

# Mostra o menu principal com as opções disponíveis
def exibir_menu():
    print(f'\n{NEGRITO}{AZUL}{"="*44}{RESET}')
    print(f'{NEGRITO}{AZUL}{"🎓 Organizador de Bolsas de Estudo 🎓":^44}{RESET}')
    print(f'{NEGRITO}{AZUL}{"="*44}{RESET}')
    print(f'{CIANO}| {"Opção":<5} | {"Descrição":<28}     |{RESET}')
    print(f'{CIANO}|{"-"*7}|{"-"*34}|{RESET}')
    print(f'{CIANO}| {"1":<5} | {"Cadastrar nova bolsa":<28}     |{RESET}')
    print(f'{CIANO}| {"2":<5} | {"Listar bolsas ordenadas por nome":<28} |{RESET}')
    print(f'{CIANO}| {"3":<5} | {"Buscar bolsa por nome":<28}     |{RESET}')
    print(f'{CIANO}| {"4":<5} | {"Filtrar por instituição":<28}     |{RESET}')
    print(f'{CIANO}| {"5":<5} | {"Exportar bolsas para .CSV":<28}     |{RESET}')
    print(f'{CIANO}| {"6":<5} | {"Sair":<28}     |{RESET}')
    print(f'{CIANO}{"="*44}{RESET}')

# ===========================================================
# Cadastro de Bolsa
# ===========================================================

def cadastrar_bolsa():
    # Solicita os dados da nova bolsa ao usuário
    nome = input('Nome da bolsa ou curso: ').strip()
    instituicao = input('Instituição: ').strip().title()
    modalidade = input('Modalidade (Online/Presencial): ').strip().title()
    valor = float(input('Valor (0 para gratuita): '))
    prazo = input('Prazo de inscrição (YYYY-MM-DD): ').strip()

    # Cria um dicionário com os dados
    nova_bolsa = {
        "nome": nome,
        "instituicao": instituicao,
        "modalidade": modalidade,
        "valor": valor,
        "prazo_inscricao": prazo
    }

    bolsas.append(nova_bolsa)  # Adiciona à lista principal
    salvar_bolsas_em_arquivos()  # Salva no arquivo
    print('✅ Bolsa cadastrada com sucesso!')

# ===========================================================
# Menu de Continuação
# ===========================================================

# Pergunta ao usuário se deseja voltar ao menu ou sair
def continuar_ou_sair():
    while True:
        escolha = input('\nDeseja voltar ao menu (M) ou sair do programa (S)? [M/S]: ').strip().upper()
        if escolha == 'M':
            return True
        elif escolha == 'S':
            print('👋 Encerrando programa.')
            return False
        else:
            print('❌ Opção inválida. Digite M para menu ou S para sair.')

# ===========================================================
# Algoritmos de Ordenação e Busca
# ===========================================================

# Implementação do algoritmo QuickSort personalizado para ordenar bolsas por uma chave (ex: nome)
def quicksort(lista, chave):
    if len(lista) <= 1:
        return lista
    pivo = lista[0]
    menores = [item for item in lista[1:] if normalizar_texto(item[chave]) <= normalizar_texto(pivo[chave])]
    maiores = [item for item in lista[1:] if normalizar_texto(item[chave]) > normalizar_texto(pivo[chave])]
    return quicksort(menores, chave) + [pivo] + quicksort(maiores, chave)

# Busca bolsas cujo nome contenha o termo digitado (busca parcial, insensível a maiúsculas/minúsculas)
def buscar_bolsas_por_nome_parcial(lista, termo_busca):
    termo_busca = termo_busca.lower()
    return [bolsa for bolsa in lista if termo_busca in bolsa['nome'].lower()]

# ===========================================================
# Exibição de Bolsa com Formatação Colorida
# ===========================================================

# Exibe os dados de uma bolsa formatados com cores e alinhamento
def exibir_bolsa_formatada(bolsa):
    valor = bolsa.get("valor")

    if isinstance(valor, str):
        if valor.strip().lower() == "gratuito":
            valor_formatado = "Gratuito"
        else:
            try:
                valor_formatado = f'R${float(valor):.2f}'
            except ValueError:
                valor_formatado = valor
    else:
        valor_formatado = "Gratuito" if valor == 0 else f'R${float(valor):.2f}'

    # Monta e imprime a linha de dados com destaque e cor
    nome = f'{NEGRITO}Curso:{RESET} {bolsa["nome"]:<30}'
    instituicao = f'{NEGRITO}Instituição:{RESET} {AZUL}{bolsa["instituicao"]:<20}{RESET}'
    modalidade = f'{NEGRITO}Modalidade:{RESET} {AMARELO}{bolsa["modalidade"]:<20}{RESET}'
    valor_str = f'{NEGRITO}Valor:{RESET} {VERDE}{valor_formatado:<10}{RESET}'
    prazo = f'{NEGRITO}Prazo:{RESET} {CIANO}{formatar_data_brasileira(bolsa["prazo_inscricao"])}{RESET}'

    print(f'{AZUL}{"=" * 60}{RESET}')
    print(f'{nome}')
    print(f'{instituicao} | {modalidade}')
    print(f'{valor_str} | {prazo}')
    print(f'{AZUL}{"=" * 60}{RESET}')

# ===========================================================
# Funções Utilitárias
# ===========================================================

# Formata data ISO (AAAA-MM-DD) para o formato brasileiro (DD/MM/AAAA)
def formatar_data_brasileira(data_iso):
    try:
        data = datetime.strptime(data_iso, "%Y-%m-%d")
        return data.strftime("%d/%m/%Y")
    except ValueError:
        return data_iso

# Formata o valor da bolsa para "Gratuito" ou "R$XX.XX"
def formatar_valor(valor):
    try:
        valor_float = float(valor)
        return "Gratuito" if valor_float == 0 else f"R${valor_float:.2f}"
    except (ValueError, TypeError):
        return str(valor)

# Remove espaços extras e coloca tudo em minúsculo (para facilitar comparações)
def normalizar_texto(texto):
    return texto.strip().lower()

# ===========================================================
# Filtro por Instituição
# ===========================================================

# Filtra bolsas por nome exato da instituição (normalizado)
def filtrar_por_instituicao(lista, instituicao):
    inst_normalizado = normalizar_texto(instituicao)
    return [bolsa for bolsa in lista if normalizar_texto(bolsa['instituicao']) == inst_normalizado]

# ===========================================================
# Execução Principal do Programa
# ===========================================================

carregar_bolsas_de_arquivo()  # Carrega dados do arquivo JSON (se existir)

# Boas-vindas e tempo de carregamento
print(f'\n{NEGRITO}{VERDE}🎉 Bem-vindo ao Organizador de Bolsas de Estudo!{RESET}')
print(f'{AZUL}📊 Total de bolsas cadastradas:{RESET} {NEGRITO}{len(bolsas)}{RESET}')
print(f'{AMARELO}⏳ Carregando... O menu aparecerá em instantes.{RESET}')
sleep(5)

# Loop principal de execução do programa
while True:
    exibir_menu()
    opcao = input('Escolha uma opção: ').strip()

    if opcao == '1':
        cadastrar_bolsa()

    elif opcao == '2':
        bolsas_ordenadas = quicksort(bolsas, 'nome')
        print('\n--- Bolsas ordenadas por nome ---')
        for bolsa in bolsas_ordenadas:
            exibir_bolsa_formatada(bolsa)

    elif opcao == '3':
        nome_busca = input('Digite parte do nome da bolsa para buscar: ').strip()
        bolsas_ordenadas = quicksort(bolsas, 'nome')  # Ordena para exibir mais bonito
        resultados = buscar_bolsas_por_nome_parcial(bolsas_ordenadas, nome_busca)

        if resultados:
            print('\n🎯 Bolsas encontradas:')
            for bolsa in resultados:
                exibir_bolsa_formatada(bolsa)
        else:
            print('❌ Nenhuma bolsa encontrada com esse nome.')

    elif opcao == '4':
        if not bolsas:
            print("⚠️ Nenhuma bolsa cadastrada.")
            continue

        # Conta quantas bolsas existem por instituição
        from collections import defaultdict
        contador = defaultdict(int)
        for bolsa in bolsas:
            inst = bolsa["instituicao"].strip().title()
            contador[inst] += 1

        instituicoes = sorted(contador.items())

        if not instituicoes:
            print("⚠️ Nenhuma instituição encontrada.")
            continue

        # Exibe as instituições para o usuário escolher
        print("\n🏫 Instituições disponíveis:")
        for idx, (inst, qtd) in enumerate(instituicoes, start=1):
            print(f"{idx}. {inst} ({qtd} curso(s))")

        # Filtra bolsas da instituição escolhida
        try:
            escolha = int(input("Digite o número da instituição para filtrar: "))
            if 1 <= escolha <= len(instituicoes):
                inst_escolhida = instituicoes[escolha - 1][0]
                filtradas = filtrar_por_instituicao(bolsas, inst_escolhida)
                print(f'\n--- Bolsas da instituição: {inst_escolhida} ---')
                for bolsa in filtradas:
                    exibir_bolsa_formatada(bolsa)
            else:
                print("❌ Número inválido.")
        except ValueError:
            print("❌ Entrada inválida. Digite um número.")

    elif opcao == '5':
        exportar_bolsas_para_csv()

    elif opcao == '6':
        print('👋 Encerrando programa.')
        break

    else:
        print('❌ Opção inválida.')

    # Pergunta ao usuário se quer continuar ou sair
    if not continuar_ou_sair():
        break
