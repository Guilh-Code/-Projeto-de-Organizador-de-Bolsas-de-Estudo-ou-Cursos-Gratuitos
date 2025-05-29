from datetime import datetime
import json

# -----------------------------------------------------------
# Utilitários

def formatar_data_brasileira(data_iso):
    try:
        data = datetime.strptime(data_iso, "%Y-%m-%d")
        return data.strftime("%d/%m/%Y")
    except ValueError:
        return data_iso

def formatar_valor(valor):
    return "Gratuito" if valor == 0 else f"R${valor:.2f}"

def normalizar_texto(texto):
    return texto.strip().lower()

# -----------------------------------------------------------
# Arquivos

def salvar_bolsas_em_arquivos(nome_arquivo='bolsas.json'):
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        json.dump(bolsas, f, indent=4, ensure_ascii=False)
    print('📁 Dados salvos com sucesso!')

def carregar_bolsas_de_arquivo(nome_arquivo='bolsas.json'):
    global bolsas
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as f:
            bolsas = json.load(f)
        print('📂 Dados carregados com sucesso!')
    except FileNotFoundError:
        bolsas = []
        print('⚠️ Arquivo não encontrado. Nenhuma bolsa carregada.')

# -----------------------------------------------------------
# Programa

bolsas = []

def exibir_menu():
    print('\n--- Organizador de Bolsas de Estudo ---')
    print('1. Cadastrar nova bolsa')
    print('2. Listar todas as bolsas')
    print('3. Listar bolsas ordenadas por nome')
    print('4. Buscar bolsa por nome')
    print('5. Filtrar bolsas gratuitas')
    print('6. Filtrar por prazo de inscrição')
    print('7. Filtrar por instituição')
    print('8. Filtrar por modalidade')
    print('9. Sair')

def cadastrar_bolsa():
    nome = input('Nome da bolsa ou curso: ').strip()
    instituicao = input('Instituição: ').strip().title()
    modalidade = input('Modalidade (Online/Presencial): ').strip().title()
    valor = float(input('Valor (0 para gratuita): '))
    prazo = input('Prazo de inscrição (YYYY-MM-DD): ').strip()

    nova_bolsa = {
        "nome": nome,
        "instituicao": instituicao,
        "modalidade": modalidade,
        "valor": valor,
        "prazo_inscricao": prazo
    }

    bolsas.append(nova_bolsa)
    salvar_bolsas_em_arquivos()
    print('✅ Bolsa cadastrada com sucesso!')

def listar_bolsas():
    if not bolsas:
        print('Nenhuma bolsa cadastrada.')
        return
    print('\n--- Lista de Bolsas ---')
    for bolsa in bolsas:
        print(f'{bolsa["nome"]} | {bolsa["instituicao"]} | {bolsa["modalidade"]} | {formatar_valor(bolsa["valor"])} | Prazo: {formatar_data_brasileira(bolsa["prazo_inscricao"])}')

# -----------------------------------------------------------
# Algoritmos

def quicksort(lista, chave):
    if len(lista) <= 1:
        return lista
    pivo = lista[0]
    menores = [item for item in lista[1:] if normalizar_texto(item[chave]) <= normalizar_texto(pivo[chave])]
    maiores = [item for item in lista[1:] if normalizar_texto(item[chave]) > normalizar_texto(pivo[chave])]
    return quicksort(menores, chave) + [pivo] + quicksort(maiores, chave)

# Busca por nome parcial (linear)
def buscar_bolsas_por_nome_parcial(lista, termo_busca):
    termo_busca = termo_busca.lower()
    resultados = [bolsa for bolsa in lista if termo_busca in bolsa['nome'].lower()]
    return resultados


# -----------------------------------------------------------
# Filtros

def filtrar_bolsas_gratuitas(lista):
    return [bolsa for bolsa in lista if bolsa['valor'] == 0]

def filtrar_por_prazo(lista, data_limite):
    try:
        data_limite = datetime.strptime(data_limite, '%Y-%m-%d')
    except ValueError:
        print('⚠️ Data inválida. Use o formato YYYY-MM-DD.')
        return []
    resultado = []
    for bolsa in lista:
        try:
            prazo = datetime.strptime(bolsa['prazo_inscricao'], '%Y-%m-%d')
            if prazo <= data_limite:
                resultado.append(bolsa)
        except ValueError:
            continue
    return resultado

def filtrar_por_instuicao(lista, instituicao):
    inst_normalizado = normalizar_texto(instituicao)
    return [bolsa for bolsa in lista if normalizar_texto(bolsa['instituicao']) == inst_normalizado]

def filtrar_por_modalidade(lista, modalidade):
    mod_normalizada = normalizar_texto(modalidade)
    return [bolsa for bolsa in lista if normalizar_texto(bolsa['modalidade']) == mod_normalizada]

# -----------------------------------------------------------
# Execução

carregar_bolsas_de_arquivo()

while True:
    exibir_menu()
    opcao = input('Escolha uma opção: ').strip()

    if opcao == '1':
        cadastrar_bolsa()

    elif opcao == '2':
        listar_bolsas()

    elif opcao == '3':
        bolsas_ordenadas = quicksort(bolsas, 'nome')
        print('\n--- Bolsas ordenadas por nome ---')
        for bolsa in bolsas_ordenadas:
            print(f'{bolsa["nome"]} | {bolsa["instituicao"]} | {bolsa["modalidade"]} | {formatar_valor(bolsa["valor"])} | Prazo: {formatar_data_brasileira(bolsa["prazo_inscricao"])}')

    elif opcao == '4':
        nome_busca = input('Digite parte do nome da bolsa para buscar: ').strip()
        bolsas_ordenadas = quicksort(bolsas, 'nome')
        resultados = buscar_bolsas_por_nome_parcial(bolsas_ordenadas, nome_busca)

        if resultados:
            print('\n🎯 Bolsas encontradas:')
            for bolsa in resultados:
                valor_formatado = "Gratuito" if bolsa["valor"] == 0 or bolsa["valor"] == "Gratuito" else f'R${float(bolsa["valor"]):.2f}'
                print(f'{bolsa["nome"]} | {bolsa["instituicao"]} | {bolsa["modalidade"]} | {valor_formatado} | Prazo: {formatar_data_brasileira(bolsa["prazo_inscricao"])}')
        else:
            print('❌ Nenhuma bolsa encontrada com esse nome.')


    elif opcao == '5':
        gratuitas = filtrar_bolsas_gratuitas(bolsas)
        print('\n--- Bolsas Gratuitas ---')
        for bolsa in gratuitas:
            print(f'{bolsa["nome"]} | {bolsa["instituicao"]} | {bolsa["modalidade"]} | {formatar_valor(bolsa["valor"])} | Prazo: {formatar_data_brasileira(bolsa["prazo_inscricao"])}')

    elif opcao == '6':
        data_input = input("Filtrar bolsas com inscrição até qual data? (YYYY-MM-DD): ").strip()
        filtradas = filtrar_por_prazo(bolsas, data_input)
        print(f"\n--- Bolsas com prazo até {formatar_data_brasileira(data_input)} ---")
        for bolsa in filtradas:
            print(f"{bolsa['nome']} | {bolsa['instituicao']} | {bolsa['modalidade']} | {formatar_valor(bolsa['valor'])} | Prazo: {formatar_data_brasileira(bolsa['prazo_inscricao'])}")

    elif opcao == '7':
        inst = input('Digite o nome da instituição para filtrar: ').strip()
        filtradas = filtrar_por_instuicao(bolsas, inst)
        print(f'\n--- Bolsas da instituição: {inst.title()} ---')
        for bolsa in filtradas:
            print(f"{bolsa['nome']} | {bolsa['instituicao']} | {bolsa['modalidade']} | {formatar_valor(bolsa['valor'])} | Prazo: {formatar_data_brasileira(bolsa['prazo_inscricao'])}")

    elif opcao == '8':
        mod = input('Digite a modalidade (Online/Presencial) para filtrar: ').strip()
        filtradas = filtrar_por_modalidade(bolsas, mod)
        print(f'\n--- Bolsas com modalidade: {mod.title()} ---')
        for bolsa in filtradas:
            print(f"{bolsa['nome']} | {bolsa['instituicao']} | {bolsa['modalidade']} | {formatar_valor(bolsa['valor'])} | Prazo: {formatar_data_brasileira(bolsa['prazo_inscricao'])}")

    elif opcao == '9':
        print('👋 Encerrando programa.')
        break

    else:
        print('❌ Opção inválida.')
