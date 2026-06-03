import time
import os
import statistics
from corte_barras import forca_bruta, pd_memoizacao, pd_iterativo, gerar_tabela_de_precos
from plots import gerar_grafico_crescimento_comparativo, gerar_imagem_da_tabela, gerar_grafico_tempo_medio_linear

PASTA_RESULTADOS = "resultados"
LIMITE_TEMPO_FB = 3.0  # Limite máximo em segundos para a Força Bruta
REPETICOES = 5

# A MESMA ESCALA GIGANTE PARA OS DOIS GRÁFICOS:
TAMANHOS = list(range(2, 25, 2)) + list(range(50, 1001, 50))

# Tamanhos específicos para a nossa Tabela de Dados Visuais
TAMANHOS_TABELA = [2, 4, 6, 8, 10]

def calcular_tempo(func, n, precos):
    tempos = []
    for _ in range(REPETICOES):
        t0 = time.perf_counter()
        func(n, precos)
        tempos.append(time.perf_counter() - t0)
    return statistics.mean(tempos)

def main():
    os.makedirs(PASTA_RESULTADOS, exist_ok=True)

    # =========================================================================
    # EXPERIMENTO 1: TABELA DE DADOS
    # =========================================================================
    print("Gerando dados para a Tabela de Corretude...")
    dados_tabela = []
    
    for n in TAMANHOS_TABELA:
        precos = gerar_tabela_de_precos(n, seed=n*10)
        
        lucro_fb, cortes_fb     = forca_bruta(n, precos)
        lucro_memo, cortes_memo = pd_memoizacao(n, precos)
        lucro_iter, cortes_iter = pd_iterativo(n, precos)
        
        dados_tabela.append({
            "n": n, 
            "precos": precos, 
            "fb": {"lucro": lucro_fb, "cortes": cortes_fb},
            "memo": {"lucro": lucro_memo, "cortes": cortes_memo},
            "iter": {"lucro": lucro_iter, "cortes": cortes_iter}
        })

    caminho_tabela = os.path.join(PASTA_RESULTADOS, "1_Tabela_Resultados_Completos.png")
    gerar_imagem_da_tabela(dados_tabela, caminho_tabela)
    print(f"Tabela gerada com sucesso em: {caminho_tabela}\n")


    # =========================================================================
    # COLETA GERAL DE TEMPOS EM ALTA ESCALA
    # =========================================================================
    print("Coletando tempos de execução...")
    tempos_fb, tempos_memo, tempos_iter = [], [], []
    
    for n in TAMANHOS:
        precos = gerar_tabela_de_precos(n, seed=42)
        
        # 1. FORÇA BRUTA (Com trava de segurança)
        if len(tempos_fb) > 0 and tempos_fb[-1] is None:
            tempos_fb.append(None)
        else:
            t_fb = calcular_tempo(forca_bruta, n, precos)
            if t_fb > LIMITE_TEMPO_FB:
                print(f"[FB: TIMEOUT no limite de {LIMITE_TEMPO_FB}s para n={n}]" + " " * 20)
                tempos_fb.append(None)
            else:
                tempos_fb.append(t_fb)
                
        # 2 e 3. PROGRAMAÇÃO DINÂMICA
        t_memo = calcular_tempo(lambda t, p: pd_memoizacao(t, p, {}), n, precos)
        tempos_memo.append(t_memo)
        
        t_iter = calcular_tempo(pd_iterativo, n, precos)
        tempos_iter.append(t_iter)
        
    print("\nColeta concluída! Gerando gráficos...")
    
    # Identificando o momento exato da quebra da Força Bruta
    n_timeout = None
    for n, t in zip(TAMANHOS, tempos_fb):
        if t is None:
            n_timeout = n
            break

    # =========================================================================
    # EXPERIMENTO 2: GRÁFICO COMPARATIVO DE CRESCIMENTO (Escala Logarítmica)
    # =========================================================================
    caminho_imagem_log = os.path.join(PASTA_RESULTADOS, "2_Grafico_Comparativo_Logaritmico.png")
    gerar_grafico_crescimento_comparativo(TAMANHOS, tempos_fb, tempos_memo, tempos_iter, n_timeout, caminho_imagem_log)
    print(f"Gráfico comparativo de crescimento gerado em: {caminho_imagem_log}")

    # =========================================================================
    # EXPERIMENTO 3: MEDIÇÃO DO TEMPO MÉDIO (Escala Linear)
    # =========================================================================
    caminho_imagem_linear = os.path.join(PASTA_RESULTADOS, "3_Grafico_Tempo_Medio_Linear.png")
    gerar_grafico_tempo_medio_linear(TAMANHOS, tempos_fb, tempos_memo, tempos_iter, n_timeout, caminho_imagem_linear)
    print(f"Gráfico de tempo médio linear gerado em: {caminho_imagem_linear}")

if __name__ == "__main__":
    main()