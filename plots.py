import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

COR_FB   = "#E63946" 
COR_MEMO = "#2A9D8F" 
COR_ITER = "#E9C46A" 
BG       = "#0F1117" 

def _aplicar_estilo_visual():
    plt.rcParams.update({
        "figure.facecolor": BG, "axes.facecolor": BG,
        "axes.edgecolor": "#3A3D45", "axes.labelcolor": "#C8D0E0",
        "xtick.color": "#8892A4", "ytick.color": "#8892A4",
        "text.color": "#C8D0E0", "grid.color": "#2A2D35",
        "grid.linestyle": "--", "font.family": "sans-serif",
    })

# =========================================================================
# FUNÇÃO 1: GERA A IMAGEM DA TABELA DE DADOS
# =========================================================================
def gerar_tabela_comparacao_resultados(dados_tabela: list, caminho_salvar: str) -> None:
    _aplicar_estilo_visual()
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.axis("off") 
    
    colunas = [
        "Tamanho\n(n)", 
        "Tabela de Preços\n(Gerada Automaticamente)",
        "Força Bruta\n(Lucro | Cortes)", 
        "PD Memoização\n(Lucro | Cortes)", 
        "PD Iterativo\n(Lucro | Cortes)"
    ]
    
    matriz_celulas = []
    for linha in dados_tabela:
        matriz_celulas.append([
            str(linha["n"]), 
            str(linha["precos"]), 
            f"${linha['fb']['lucro']} | {linha['fb']['cortes']}", 
            f"${linha['memo']['lucro']} | {linha['memo']['cortes']}",
            f"${linha['iter']['lucro']} | {linha['iter']['cortes']}"
        ])
        
    tabela = ax.table(
        cellText=matriz_celulas, colLabels=colunas, loc="center", cellLoc="center"
    )
    
    tabela.auto_set_font_size(False)
    tabela.set_fontsize(10)
    tabela.scale(1.1, 2.5) 
    
    for (row, col), cell in tabela.get_celld().items():
        if row == 0:
            cell.set_facecolor("#1D3557")
            cell.get_text().set_color("white")
            cell.get_text().set_fontweight("bold")
        else:
            cell.set_facecolor("#1A1D25")
            cell.get_text().set_color("#C8D0E0")
            
    plt.title("Resultados Detalhados por Algoritmo", color="white", fontweight="bold", pad=20)
    plt.tight_layout()
    fig.savefig(caminho_salvar, dpi=150, facecolor=BG)
    plt.close(fig)


# =========================================================================
# FUNÇÃO 2: GERA O GRÁFICO LOGARÍTMICO (Crescimento Estendido)
# =========================================================================
def gerar_grafico_crescimento_comparativo(tamanhos, tempos_fb, tempos_memo, tempos_iter, n_timeout, caminho):
    _aplicar_estilo_visual()
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Filtra os timeouts da Força Bruta para não quebrar a linha
    tamanhos_fb_validos = [tam for tam, t in zip(tamanhos, tempos_fb) if t is not None]
    tempos_fb_validos   = [t for t in tempos_fb if t is not None]

    ax.plot(tamanhos_fb_validos, tempos_fb_validos, color=COR_FB, lw=2.5, marker="^", label="Força Bruta O(2ⁿ)")
    ax.plot(tamanhos, tempos_memo, color=COR_MEMO, lw=2.5, marker="o", label="PD Memoização O(n²)")
    ax.plot(tamanhos, tempos_iter, color=COR_ITER, lw=2.5, marker="s", label="PD Iterativo O(n²)")
    
    # Escala Logarítmica no Eixo do Tempo
    ax.set_yscale("log")
    
    ax.set_title("Crescimento do Tempo de Execução (Escala Logarítmica)", color="white", fontweight="bold", fontsize=14)
    ax.set_xlabel("Tamanho da barra (n)", fontsize=12)
    ax.set_ylabel("Tempo de Execução em Segundos (Log)", fontsize=12)
    ax.grid(True, which="both", ls="--", alpha=0.3)
    ax.legend(loc="upper left", fontsize=11)
    
    # Adicionando a informação de timeout
    frase_timeout = f"\n* A Força Bruta estourou o limite de 3 segundos em n={n_timeout}." if n_timeout else ""
    
    texto_explicativo = (
            "Nota: O eixo Y está em escala logarítmica.\n"
            "A Força Bruta cresce exponencialmente (linha reta no log).\n"
            "A Programação Dinâmica se mantém eficiente (curva baixa)." + frase_timeout
        )
        
    ax.text(0.48, 0.03, texto_explicativo, transform=ax.transAxes, color="white", 
            fontsize=9, bbox=dict(facecolor='#1A1D25', alpha=0.8, edgecolor='#3A3D45'))

    plt.tight_layout()
    fig.savefig(caminho, dpi=150, bbox_inches="tight", facecolor=BG)
    plt.close(fig)


# =========================================================================
# FUNÇÃO 3: GERA O GRÁFICO LINEAR (Explosão da Força Bruta em Alta Escala)
# =========================================================================
def gerar_grafico_tempo_medio_linear(tamanhos, tempos_fb, tempos_memo, tempos_iter, n_timeout, caminho_salvar):
    _aplicar_estilo_visual()
    fig, ax = plt.subplots(figsize=(10, 6))
    
    tamanhos_fb_validos = [tam for tam, t in zip(tamanhos, tempos_fb) if t is not None]
    tempos_fb_validos   = [t for t in tempos_fb if t is not None]

    ax.plot(tamanhos_fb_validos, tempos_fb_validos, color=COR_FB, lw=2.5, marker="^", label="Força Bruta O(2ⁿ)")
    ax.plot(tamanhos, tempos_memo, color=COR_MEMO, lw=2.5, marker="o", label="PD Memoização O(n²)")
    ax.plot(tamanhos, tempos_iter, color=COR_ITER, lw=2.5, marker="s", label="PD Iterativo O(n²)")
    
    ax.set_title("Medição do Tempo Médio de Execução (Escala Linear)", color="white", fontweight="bold", fontsize=14)
    ax.set_xlabel("Tamanho da barra (n)", fontsize=12)
    ax.set_ylabel("Tempo Médio (segundos)", fontsize=12)
    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper left", fontsize=11)
    
    # Adicionando a informação de timeout
    frase_timeout = f"\n* A Força Bruta estourou o limite de 3 segundos em n={n_timeout}." if n_timeout else ""
    
    texto_explicativo = (
        "Nota: A Força Bruta 'explode' logo no início, formando uma\n"
        "parede vertical à esquerda. Isso permite ver os algoritmos de\n"
        "Programação Dinâmica formando sua curva suave ao longo do eixo X." + frase_timeout
    )
    ax.text(0.35, 0.15, texto_explicativo, transform=ax.transAxes, color="white", 
            fontsize=10, bbox=dict(facecolor='#1A1D25', alpha=0.8, edgecolor='#3A3D45'))

    plt.tight_layout()
    fig.savefig(caminho_salvar, dpi=150, facecolor=BG)
    plt.close(fig)