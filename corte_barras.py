"""
algoritmos.py
─────────────
Implementações dos algoritmos de Corte de Barras e geração de entradas
com nomenclatura descritiva para facilitar o entendimento.
"""

import random
import sys


def gerar_tabela_de_precos(tamanho_maximo: int, seed: int | None = None) -> list[int]:
    """
    Retorna uma tabela de preços onde o índice é o tamanho do pedaço.
    tabela[0] = 0 (barra de tamanho 0 não vale nada)
    """
    gerador = random.Random(seed)
    # Gera um preço aleatório para cada tamanho, proporcional ao tamanho do pedaço
    precos = [
        gerador.randint(1, 10 * tamanho) for tamanho in range(1, tamanho_maximo + 1)
    ]
    return [0] + precos


# ─────────────────────────────────────────────────────────────────────────────
# ALGORITMO 1 — FORÇA BRUTA
# ─────────────────────────────────────────────────────────────────────────────


def forca_bruta(tamanho_barra: int, tabela_precos: list[int]) -> tuple[int, list[int]]:
    """
    Testa absolutamente todas as combinações de cortes possíveis e escolhe a melhor.
    """
    if tamanho_barra == 0:
        return 0, []

    maior_lucro_encontrado = -1
    melhor_combinacao_de_cortes: list[int] = []

    def _testar_todas_combinacoes(
        tamanho_restante: int, cortes_em_teste: list[int]
    ) -> None:
        nonlocal maior_lucro_encontrado, melhor_combinacao_de_cortes

        # Se não sobrou barra, calculamos o lucro desta combinação específica
        if tamanho_restante == 0:
            lucro_desta_combinacao = sum(
                tabela_precos[corte] for corte in cortes_em_teste
            )

            if lucro_desta_combinacao > maior_lucro_encontrado:
                maior_lucro_encontrado = lucro_desta_combinacao
                melhor_combinacao_de_cortes = list(cortes_em_teste)
            return

        # Tenta fazer um corte de cada tamanho possível no pedaço que sobrou
        for tamanho_do_corte in range(1, tamanho_restante + 1):
            cortes_em_teste.append(tamanho_do_corte)
            _testar_todas_combinacoes(
                tamanho_restante - tamanho_do_corte, cortes_em_teste
            )
            cortes_em_teste.pop()  # Desfaz o corte para testar a próxima opção

    _testar_todas_combinacoes(tamanho_barra, [])
    return maior_lucro_encontrado, sorted(melhor_combinacao_de_cortes)


# ─────────────────────────────────────────────────────────────────────────────
# ALGORITMO 2 — PROGRAMAÇÃO DINÂMICA RECURSIVO COM MEMOIZAÇÃO
# ─────────────────────────────────────────────────────────────────────────────


def pd_memoizacao(
    tamanho_barra: int,
    tabela_precos: list[int],
    cache_lucros_conhecidos: dict | None = None,
) -> tuple[int, list[int]]:
    """
    Abordagem Top-Down: Resolve os problemas do maior para o menor e
    salva os resultados no cache (memo) para não calcular duas vezes.
    """
    sys.setrecursionlimit(max(10_000, tamanho_barra * 3))

    if cache_lucros_conhecidos is None:
        cache_lucros_conhecidos = {}

    def _descobrir_melhor_corte(tamanho_atual: int) -> tuple[int, list[int]]:
        # Casos base e consulta ao cache
        if tamanho_atual == 0:
            return 0, []
        if tamanho_atual in cache_lucros_conhecidos:
            return cache_lucros_conhecidos[tamanho_atual]

        maior_lucro_para_este_tamanho = -1
        melhor_primeiro_corte = -1

        # Simula fazer o primeiro corte de todos os tamanhos possíveis
        for tamanho_do_corte in range(1, tamanho_atual + 1):
            # Descobre o melhor lucro possível para o que sobrou da barra
            lucro_do_pedaco_restante, _ = _descobrir_melhor_corte(
                tamanho_atual - tamanho_do_corte
            )

            lucro_total_simulado = (
                tabela_precos[tamanho_do_corte] + lucro_do_pedaco_restante
            )

            # Se esse corte rendeu mais que os anteriores, vira o novo campeão
            if lucro_total_simulado > maior_lucro_para_este_tamanho:
                maior_lucro_para_este_tamanho = lucro_total_simulado
                melhor_primeiro_corte = tamanho_do_corte

        # Já sabemos o melhor primeiro corte. Agora pegamos os cortes do resto da barra.
        _, lista_cortes_do_pedaco_restante = _descobrir_melhor_corte(
            tamanho_atual - melhor_primeiro_corte
        )

        # Salva o recorde no dicionário e retorna
        lista_completa_ordenada = sorted(
            [melhor_primeiro_corte] + lista_cortes_do_pedaco_restante
        )
        cache_lucros_conhecidos[tamanho_atual] = (
            maior_lucro_para_este_tamanho,
            lista_completa_ordenada,
        )

        return cache_lucros_conhecidos[tamanho_atual]

    return _descobrir_melhor_corte(tamanho_barra)


# ─────────────────────────────────────────────────────────────────────────────
# ALGORITMO 3 — PROGRAMAÇÃO DINÂMICA ITERATIVO (BOTTOM-UP)
# ─────────────────────────────────────────────────────────────────────────────


def pd_iterativo(tamanho_barra: int, tabela_precos: list[int]) -> tuple[int, list[int]]:
    """
    Abordagem Bottom-Up: Resolve os problemas do menor (1) para o maior (n).
    Usa listas em vez de recursão para ir construindo a solução passo a passo.
    """
    # Cria listas preenchidas com zeros para guardar os resultados de cada tamanho
    lucro_maximo_por_tamanho = [0] * (tamanho_barra + 1)
    primeiro_corte_ideal_por_tamanho = [0] * (tamanho_barra + 1)

    # Resolve para uma barra de tamanho 1, depois 2, depois 3, até tamanho_barra
    for tamanho_subproblema in range(1, tamanho_barra + 1):
        # Testa todos os primeiros cortes possíveis para esse subproblema
        for tamanho_do_corte in range(1, tamanho_subproblema + 1):
            lucro_do_corte = tabela_precos[tamanho_do_corte]
            lucro_do_resto_ja_calculado = lucro_maximo_por_tamanho[
                tamanho_subproblema - tamanho_do_corte
            ]
            lucro_total = lucro_do_corte + lucro_do_resto_ja_calculado

            # Atualiza o placar se achou um lucro melhor para esse tamanho
            if lucro_total > lucro_maximo_por_tamanho[tamanho_subproblema]:
                lucro_maximo_por_tamanho[tamanho_subproblema] = lucro_total
                primeiro_corte_ideal_por_tamanho[tamanho_subproblema] = tamanho_do_corte

    # Etapa final: Reconstruir a lista de cortes baseada nas melhores escolhas salvas
    lista_final_de_cortes: list[int] = []
    pedaco_que_falta_cortar = tamanho_barra

    while pedaco_que_falta_cortar > 0:
        melhor_corte = primeiro_corte_ideal_por_tamanho[pedaco_que_falta_cortar]
        lista_final_de_cortes.append(melhor_corte)
        pedaco_que_falta_cortar -= melhor_corte

    lucro_final = lucro_maximo_por_tamanho[tamanho_barra]
    return lucro_final, sorted(lista_final_de_cortes)
