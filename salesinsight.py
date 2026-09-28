"""
SalesInsight PY - Analise de Dados de Vendas

Modulo principal do projeto academico.
Responsavel pela leitura, limpeza, transformacao,
analise e exportacao dos dados de vendas.
"""

import csv
import json
import os
import random
import re
from datetime import datetime, timedelta


def gerar_dataset_vendas(caminho_csv="vendas.csv", n_registros=200, seed=42):
    """Gera um dataset sintético de vendas com algumas inconsistências propositalmente."""
    random.seed(seed)
    produtos = ["Notebook", "Smartphone", "Tablet", "Monitor",
                "Teclado", "Mouse", "Headset"]
    categorias = {
        "Notebook": "Computadores", "Smartphone": "Celulares",
        "Tablet": "Celulares", "Monitor": "Computadores",
        "Teclado": "Perifericos", "Mouse": "Perifericos",
        "Headset": "Perifericos"
    }
    precos = {
        "Notebook": 3500, "Smartphone": 2200, "Tablet": 1800,
        "Monitor": 1200, "Teclado": 250, "Mouse": 120,
        "Headset": 350
    }
    regioes = ["Sudeste", "Sul", "Nordeste", "Centro-Oeste", "Norte"]
    data_inicio = datetime(2025, 1, 1)
    colunas = [
        "id_venda", "data_venda", "cliente", "produto", "categoria",
        "regiao", "quantidade", "preco_unitario"
    ]

    with open(caminho_csv, "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=colunas)
        escritor.writeheader()

        for i in range(n_registros):
            produto = random.choice(produtos)
            categoria = categorias[produto]
            quantidade = random.randint(1, 10)
            preco = round(precos[produto] * random.uniform(0.85, 1.15), 2)
            data = data_inicio + timedelta(days=random.randint(0, 364))
            data_txt = data.strftime("%Y-%m-%d")
            cliente = f"Cliente_{random.randint(1, 50):03d}"

            if random.random() < 0.05:
                quantidade = ""
            if random.random() < 0.04:
                preco = ""
            if random.random() < 0.06:
                produto = " " + produto + " "
            if random.random() < 0.03:
                data_txt = "DATA INVALIDA"
            if random.random() < 0.10:
                cliente = random.choice([
                    cliente.upper().replace("_", "-"),
                    cliente + "!!",
                    " " + cliente,
                    cliente.replace("Cliente_", "cliente#"),
                ])

            escritor.writerow({
                "id_venda": i + 1,
                "data_venda": data_txt,
                "cliente": cliente,
                "produto": produto,
                "categoria": categoria,
                "regiao": random.choice(regioes),
                "quantidade": quantidade,
                "preco_unitario": preco,
            })

    print(f"Dataset gerado com {n_registros} registros em {caminho_csv}.")


def carregar_dataset(caminho_csv):
    """Lê o CSV e retorna uma lista de dicionários."""
    with open(caminho_csv, "r", encoding="utf-8") as arquivo:
        return list(csv.DictReader(arquivo))


def inspecionar_dados(registros):
    """Exibe informações estruturais do dataset."""
    total = len(registros)
    colunas = list(registros[0].keys()) if registros else []
    nulos = {coluna: 0 for coluna in colunas}

    for linha in registros:
        for coluna in colunas:
            if linha.get(coluna, "").strip() == "":
                nulos[coluna] += 1

    print("\n=== INSPEÇÃO INICIAL DO DATASET ===")
    print(f"Total de registros: {total}")
    print(f"Colunas: {colunas}")
    print(f"Valores ausentes por coluna: {nulos}")
    print("Primeiros registros:")
    for linha in registros[:5]:
        print(linha)


def limpar_dados(registros):
    """Limpa dados e retorna (registros_limpos, relatório)."""
    relatorio = {
        "iniciais": len(registros),
        "removidos_data": 0,
        "removidos_nulos": 0,
        "finais": 0,
    }
    padrao_cliente = re.compile(r"^Cliente_\d{3}$", flags=re.IGNORECASE)
    limpos = []

    for linha_original in registros:
        linha = linha_original.copy()

        for chave in ("cliente", "produto", "categoria", "regiao"):
            linha[chave] = linha[chave].strip()

        try:
            linha["data_venda"] = datetime.strptime(
                linha["data_venda"], "%Y-%m-%d"
            )
        except ValueError:
            relatorio["removidos_data"] += 1
            continue

        if linha["quantidade"] == "" or linha["preco_unitario"] == "":
            relatorio["removidos_nulos"] += 1
            continue

        linha["quantidade"] = int(float(linha["quantidade"]))
        linha["preco_unitario"] = float(linha["preco_unitario"])

        nome_limpo = re.sub(r"[^A-Za-z0-9_]", "", linha["cliente"])
        linha["cliente"] = nome_limpo
        linha["cliente_fora_do_padrao"] = padrao_cliente.match(nome_limpo) is None
        limpos.append(linha)

    relatorio["finais"] = len(limpos)

    print("\n=== RELATÓRIO DE LIMPEZA ===")
    print(f"Registros iniciais: {relatorio['iniciais']}")
    print(f"Removidos por data inválida: {relatorio['removidos_data']}")
    print(f"Removidos por valores ausentes: {relatorio['removidos_nulos']}")
    print(f"Registros finais: {relatorio['finais']}")

    return limpos, relatorio


def criar_colunas_derivadas(registros):
    """Cria receita, mês, trimestre, ano e faixa de receita."""
    nomes_meses = {
        1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
        5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
        9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
    }

    for linha in registros:
        data = linha["data_venda"]
        receita = linha["quantidade"] * linha["preco_unitario"]
        mes = data.month

        if mes <= 3:
            trimestre = "Q1"
        elif mes <= 6:
            trimestre = "Q2"
        elif mes <= 9:
            trimestre = "Q3"
        else:
            trimestre = "Q4"

        if receita < 500:
            faixa = "Baixo Valor"
        elif receita < 5000:
            faixa = "Medio Valor"
        else:
            faixa = "Alto Valor"

        linha["receita_total"] = round(receita, 2)
        linha["mes"] = mes
        linha["mes_nome"] = nomes_meses[mes]
        linha["trimestre"] = trimestre
        linha["ano"] = data.year
        linha["faixa_receita_item"] = faixa

    return registros


def calcular_metricas(registros):
    """Calcula métricas agregadas por mês, produto, categoria e região."""
    por_mes = {}
    por_produto = {}
    por_categoria = {}
    por_regiao = {}

    for linha in registros:
        mes = linha["mes"]
        produto = linha["produto"]
        categoria = linha["categoria"]
        regiao = linha["regiao"]
        receita = linha["receita_total"]
        quantidade = linha["quantidade"]

        if mes not in por_mes:
            por_mes[mes] = {"mes": mes, "receita_total": 0.0,
                            "quantidade": 0, "n_vendas": 0}
        por_mes[mes]["receita_total"] += receita
        por_mes[mes]["quantidade"] += quantidade
        por_mes[mes]["n_vendas"] += 1

        if produto not in por_produto:
            por_produto[produto] = {"produto": produto, "receita_total": 0.0}
        por_produto[produto]["receita_total"] += receita

        if categoria not in por_categoria:
            por_categoria[categoria] = {
                "categoria": categoria, "receita_total": 0.0
            }
        por_categoria[categoria]["receita_total"] += receita

        if regiao not in por_regiao:
            por_regiao[regiao] = {
                "regiao": regiao, "receita_total": 0.0, "n_vendas": 0
            }
        por_regiao[regiao]["receita_total"] += receita
        por_regiao[regiao]["n_vendas"] += 1

    lista_mes = list(por_mes.values())
    lista_produto = list(por_produto.values())
    lista_categoria = list(por_categoria.values())
    lista_regiao = list(por_regiao.values())

    for item in lista_mes:
        item["receita_total"] = round(item["receita_total"], 2)

    for item in lista_produto:
        item["receita_total"] = round(item["receita_total"], 2)

    for item in lista_categoria:
        item["receita_total"] = round(item["receita_total"], 2)

    for item in lista_regiao:
        item["receita_total"] = round(item["receita_total"], 2)
        item["ticket_medio"] = round(
            item["receita_total"] / item["n_vendas"], 2
        )

    lista_mes.sort(key=lambda x: x["mes"])
    lista_produto.sort(key=lambda x: x["receita_total"], reverse=True)
    lista_categoria.sort(key=lambda x: x["receita_total"], reverse=True)
    lista_regiao.sort(key=lambda x: x["receita_total"], reverse=True)

    return {
        "por_mes": lista_mes,
        "top_produtos": lista_produto[:5],
        "por_categoria": lista_categoria,
        "por_regiao": lista_regiao,
    }


def segmentar_clientes(registros):
    """Agrupa clientes e classifica em Bronze, Prata ou Ouro usando lambda."""
    classificar = lambda total: (
        "Ouro" if total > 15000
        else "Prata" if total >= 5000
        else "Bronze"
    )

    total_por_cliente = {}
    for linha in registros:
        cliente = linha["cliente"]
        total_por_cliente[cliente] = (
            total_por_cliente.get(cliente, 0) + linha["receita_total"]
        )

    clientes = [
        {
            "cliente": nome,
            "total_gasto": round(total, 2),
            "segmento": classificar(total)
        }
        for nome, total in total_por_cliente.items()
    ]

    clientes.sort(key=lambda x: x["total_gasto"], reverse=True)
    return clientes


def processar_coluna(registros, coluna, funcao_transformacao, nome_saida=None):
    """Aplica uma função recebida como argumento a uma coluna."""
    nome_saida = nome_saida or f"{coluna}_transformado"
    for linha in registros:
        linha[nome_saida] = funcao_transformacao(linha[coluna])
    return registros


def calcular_estatisticas_gerais(registros, clientes):
    """Calcula estatísticas gerais solicitadas no desafio."""
    receitas = [linha["receita_total"] for linha in registros]
    total_receita = sum(receitas)
    media_receita = total_receita / len(receitas) if receitas else 0

    acima_media = sum(
        1 for linha in registros if linha["receita_total"] > media_receita
    )

    distribuicao = {"Bronze": 0, "Prata": 0, "Ouro": 0}
    for cliente in clientes:
        distribuicao[cliente["segmento"]] += 1

    return {
        "total_registros_validos": len(registros),
        "receita_total_geral": round(total_receita, 2),
        "receita_media_por_venda": round(media_receita, 2),
        "vendas_acima_da_media": acima_media,
        "clientes_unicos": len(clientes),
        "clientes_bronze": distribuicao["Bronze"],
        "clientes_prata": distribuicao["Prata"],
        "clientes_ouro": distribuicao["Ouro"],
    }


def imprimir_metricas(metricas, clientes, estatisticas):
    """Exibe os principais resultados no console."""
    print("\n=== POR MÊS ===")
    print("Mês | Receita | Quantidade | Vendas")
    for item in metricas["por_mes"]:
        print(
            f"{item['mes']:02d} | R$ {item['receita_total']:,.2f} | "
            f"{item['quantidade']} | {item['n_vendas']}"
        )

    print("\n=== TOP 5 PRODUTOS ===")
    for item in metricas["top_produtos"]:
        print(f"{item['produto']}: R$ {item['receita_total']:,.2f}")

    print("\n=== POR CATEGORIA ===")
    for item in metricas["por_categoria"]:
        print(f"{item['categoria']}: R$ {item['receita_total']:,.2f}")

    print("\n=== POR REGIÃO ===")
    for item in metricas["por_regiao"]:
        print(
            f"{item['regiao']}: R$ {item['receita_total']:,.2f} | "
            f"Ticket médio: R$ {item['ticket_medio']:,.2f}"
        )

    print("\n=== TOP 10 CLIENTES ===")
    for item in clientes[:10]:
        print(
            f"{item['cliente']}: R$ {item['total_gasto']:,.2f} "
            f"({item['segmento']})"
        )

    print("\n=== ESTATÍSTICAS GERAIS ===")
    for chave, valor in estatisticas.items():
        print(f"{chave}: {valor}")


def exportar_resultados(metricas, clientes, estatisticas):
    """Exporta métricas e segmentação em CSV e estatísticas em JSON."""
    os.makedirs("outputs", exist_ok=True)

    with open("outputs/metricas_por_mes.csv", "w", newline="",
              encoding="utf-8-sig") as arquivo:
        escritor = csv.DictWriter(
            arquivo, fieldnames=metricas["por_mes"][0].keys()
        )
        escritor.writeheader()
        escritor.writerows(metricas["por_mes"])

    with open("outputs/segmentacao_clientes.csv", "w", newline="",
              encoding="utf-8-sig") as arquivo:
        escritor = csv.DictWriter(
            arquivo, fieldnames=clientes[0].keys()
        )
        escritor.writeheader()
        escritor.writerows(clientes)

    caminho_json = "outputs/estatisticas_gerais.json"
    with open(caminho_json, "w", encoding="utf-8") as arquivo:
        json.dump(estatisticas, arquivo, indent=4, ensure_ascii=False)

    with open(caminho_json, "r", encoding="utf-8") as arquivo:
        conferencia = json.load(arquivo)

    print(f"\nJSON gravado e lido com sucesso: {conferencia}")


def main():
    """Executa o fluxo completo do SalesInsight PY."""
    print("=" * 60)
    print(" SALESINSIGHT PY - ANÁLISE DE DADOS DE VENDAS")
    print("=" * 60)

    if not os.path.exists("vendas.csv"):
        gerar_dataset_vendas("vendas.csv")

    registros = carregar_dataset("vendas.csv")
    inspecionar_dados(registros)

    registros_limpos, relatorio = limpar_dados(registros)
    registros_limpos = criar_colunas_derivadas(registros_limpos)

    # Dois usos distintos de lambda.
    registros_limpos = processar_coluna(
        registros_limpos, "receita_total",
        lambda x: round(x / 1000, 2),
        "receita_em_milhares"
    )
    registros_limpos = processar_coluna(
        registros_limpos, "quantidade",
        lambda q: "Alto Volume" if q > 5 else "Baixo Volume",
        "perfil_volume"
    )

    metricas = calcular_metricas(registros_limpos)
    clientes = segmentar_clientes(registros_limpos)
    estatisticas = calcular_estatisticas_gerais(
        registros_limpos, clientes
    )

    imprimir_metricas(metricas, clientes, estatisticas)
    exportar_resultados(metricas, clientes, estatisticas)

    print("\n[CONCLUÍDO] Fluxo finalizado com sucesso.")


if __name__ == "__main__":
    main()
