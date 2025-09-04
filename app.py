# app.py
# ================================================================
# Unificado: "Veterano - Pagante (DELTAS #2)" + "Veterano - Pagante (%)"
# Streamlit + Plotly • 2 abas, cada uma com 5 dispersões
# ================================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Veterano - Pagante • Dispersões", layout="wide")

# ========= Helpers =========
def to_float(x):
    """Converte '1,2 pp' ou '35,5%' -> float (1.2 / 35.5)."""
    if pd.isna(x) or x == "":
        return np.nan
    s = str(x).lower().replace("%","").replace("pp","").replace(",",".").strip()
    try:
        return float(s)
    except:
        return np.nan

def add_quadrants(fig, x0, x1, y0, y1):
    fig.add_hline(y=0, line_dash="dash", opacity=0.6)
    fig.add_vline(x=0, line_dash="dash", opacity=0.6)
    fig.update_xaxes(range=[x0, x1])
    fig.update_yaxes(range=[y0, y1])

def scatter(df, x_col, y_col, x_label, y_label, title):
    x = df[x_col]; y = df[y_col]
    # folga
    dx = (x.max() - x.min())*0.1 if np.isfinite(x.max()-x.min()) else 1
    dy = (y.max() - y.min())*0.1 if np.isfinite(y.max()-y.min()) else 1
    x0, x1 = x.min()-dx, x.max()+dx
    y0, y1 = y.min()-dy, y.max()+dy

    fig = px.scatter(
        df, x=x_col, y=y_col, text="MARCA",
        color="AUM", color_continuous_scale="Viridis_r",
        labels={x_col: x_label, y_col: y_label, "AUM":"Δ % AUM"},
        title=title
    )
    fig.update_traces(marker=dict(size=12, line=dict(width=0.6, color="black")),
                      textposition="top center")
    add_quadrants(fig, x0, x1, y0, y1)
    fig.update_layout(margin=dict(l=10, r=10, t=48, b=10))
    return fig

# ========= Base padrão DELTAS #2 =========
raw_deltas = [
 ["ÂNIMA BR","1,0 pp","0,5 pp","-0,3 pp","-0,9 pp","-17,5 pp","-4,1 pp","35,5%","-18,3 pp"],
 ["AGES","1,0 pp","-0,3 pp","-1,2 pp","0,0 pp","-18,9 pp","-2,2 pp","119,0%","-22,4 pp"],
 ["UNIFG - BA","1,5 pp","1,0 pp","-1,1 pp","-1,6 pp","-25,2 pp","-8,8 pp","102,5%","-26,5 pp"],
 ["UNF","1,2 pp","0,6 pp","-0,5 pp","-0,9 pp","-20,0 pp","-4,9 pp","98,6%","-18,4 pp"],
 ["UNP","1,5 pp","0,3 pp","-0,1 pp","-0,8 pp","-14,5 pp","-4,8 pp","95,2%","-13,5 pp"],
 ["FPB","0,3 pp","0,0 pp","-0,7 pp","-1,0 pp","-4,9 pp","-5,7 pp","70,8%","-7,8 pp"],
 ["UNIFG - PE","2,1 pp","1,3 pp","-0,8 pp","-2,2 pp","-20,3 pp","-4,7 pp","93,5%","-14,6 pp"],
 ["UAM","1,0 pp","-1,8 pp","0,9 pp","1,4 pp","-19,3 pp","-2,6 pp","16,4%","0,0 pp"],
 ["USJT","0,8 pp","-1,0 pp","0,0 pp","0,4 pp","-16,5 pp","-2,2 pp","23,7%","0,0 pp"],
 ["UNA","2,2 pp","0,1 pp","-0,1 pp","-0,7 pp","-12,8 pp","-6,2 pp","25,3%","0,0 pp"],
 ["UNIBH","-0,7 pp","-0,9 pp","0,2 pp","0,7 pp","-27,0 pp","-4,1 pp","21,0%","0,0 pp"],
 ["IBMR","-0,3 pp","6,2 pp","-1,7 pp","-6,3 pp","-31,6 pp","-2,2 pp","95,0%","-22,2 pp"],
 ["FASEH","3,1 pp","-0,2 pp","-0,3 pp","0,0 pp","-4,8 pp","-9,3 pp","46,1%","0,0 pp"],
 ["MIL. CAMPOS","-0,1 pp","-2,0 pp","-2,2 pp","1,7 pp","0,0 pp","0,6 pp","4,1%","0,0 pp"],
 ["UNISUL","0,5 pp","0,9 pp","-0,6 pp","-0,6 pp","-29,9 pp","-2,4 pp","14,4%","0,0 pp"],
 ["UNICURITIBA","-1,1 pp","-0,3 pp","0,2 pp","-0,1 pp","-23,3 pp","-3,6 pp","3,6%","0,0 pp"],
 ["UNISOCIESC","0,3 pp","1,4 pp","-0,3 pp","-2,2 pp","-16,1 pp","-1,4 pp","19,4%","0,0 pp"],
 ["UNR","0,3 pp","2,0 pp","-0,3 pp","-1,7 pp","-13,0 pp","-9,4 pp","117,3%","-23,7 pp"],
 ["FAD","2,9 pp","3,8 pp","-1,8 pp","-3,9 pp","-33,7 pp","-11,0 pp","94,5%","-16,1 pp"]
]
cols_deltas = ["MARCA","D_CONV","D_REND100","D_MENOR40","D_REPROV","D_NAO_AI","D_MIX_INAD","AUM","D_DEV_BOLSA"]
df_deltas = pd.DataFrame(raw_deltas, columns=cols_deltas)
for c in cols_deltas[1:]:
    df_deltas[c] = df_deltas[c].apply(to_float)

# ========= Base padrão Percentuais (Veterano) =========
raw_perc = [
 ["ÂNIMA BR","90,3%","86,1%","6,4%","13,2%","22,5%","12,0%","90,2%","-18,3 pp"],
 ["AGES","91,1%","90,3%","3,8%","9,2%","13,2%","12,2%","101,6%","-22,4 pp"],
 ["UNIFG - BA","90,5%","90,9%","3,8%","8,5%","15,2%","13,7%","91,1%","-26,5 pp"],
 ["UNF","88,6%","80,9%","8,9%","18,7%","16,4%","13,4%","112,4%","-18,4 pp"],
 ["UNP","90,5%","87,9%","5,5%","11,4%","19,5%","15,1%","119,9%","-13,5 pp"],
 ["FPB","87,7%","84,7%","7,3%","14,2%","25,5%","14,8%","98,7%","-7,8 pp"],
 ["UNIFG - PE","87,1%","82,7%","9,0%","16,3%","31,5%","10,7%","114,4%","-14,6 pp"],
 ["UAM","91,1%","86,9%","6,3%","12,3%","28,6%","9,6%","101,4%","0,0 pp"],
 ["USJT","90,6%","86,7%","6,4%","12,6%","30,0%","10,9%","67,2%","0,0 pp"],
 ["UNA","90,9%","87,5%","5,7%","11,8%","20,7%","14,1%","61,1%","0,0 pp"],
 ["UNIBH","88,6%","87,1%","5,9%","12,3%","16,1%","11,9%","81,8%","0,0 pp"],
 ["IBMR","89,1%","82,6%","7,3%","16,7%","26,7%","6,6%","149,7%","-22,2 pp"],
 ["FASEH","90,2%","91,6%","4,2%","8,2%","16,1%","15,5%","74,6%","0,0 pp"],
 ["MIL. CAMPOS","89,5%","61,8%","8,5%","37,9%","0,0%","14,7%","32,5%","0,0 pp"],
 ["UNISUL","92,5%","86,4%","7,3%","13,2%","19,5%","11,6%","82,7%","0,0 pp"],
 ["UNICURITIBA","89,0%","84,1%","6,6%","15,3%","26,7%","12,7%","68,4%","0,0 pp"],
 ["UNISOCIESC","91,7%","89,4%","5,1%","9,6%","22,8%","11,8%","67,9%","0,0 pp"],
 ["UNR","90,0%","82,7%","7,2%","16,8%","22,3%","10,9%","108,4%","-23,7 pp"],
 ["FAD","89,5%","82,1%","8,8%","17,5%","23,7%","8,5%","141,5%","-16,1 pp"]
]
cols_perc = ["MARCA","P_CONV","P_REND100","P_MENOR40","P_REPROV","P_NAO_AI","P_MIX_INAD","AUM","D_DEV_BOLSA"]
df_perc = pd.DataFrame(raw_perc, columns=cols_perc)
for c in cols_perc[1:]:
    df_perc[c] = df_perc[c].apply(to_float)

# ========= UI =========
st.title("Veterano - Pagante • Dispersões Unificadas")
st.caption("Duas abas: DELTAS #2 (pp) e Percentuais (%). Cores representam Δ % AUM.")

tab_deltas, tab_perc = st.tabs(["DELTAS #2 (5 dispersões)", "Percentuais (5 dispersões)"])

# ---- Aba DELTAS #2 ----
with tab_deltas:
    st.subheader("DELTAS #2 — X = Δ % Conversão (pp)")
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(
            scatter(df_deltas, "D_CONV", "D_MENOR40",
                    "Δ % Conversão vs AA (pp)", "Δ % Média < 40 (pp)",
                    "Δ Conversão (X) vs Δ % Média < 40 (Y)"),
            use_container_width=True
        )
    with c2:
        st.plotly_chart(
            scatter(df_deltas, "D_CONV", "D_REPROV",
                    "Δ % Conversão vs AA (pp)", "Δ % Reprovado (pp)",
                    "Δ Conversão (X) vs Δ % Reprovado (Y)"),
            use_container_width=True
        )

    c3, c4 = st.columns(2)
    with c3:
        st.plotly_chart(
            scatter(df_deltas, "D_CONV", "D_REND100",
                    "Δ % Conversão vs AA (pp)", "Δ % Rendimento 100% (pp)",
                    "Δ Conversão (X) vs Δ % Rendimento 100% (Y)"),
            use_container_width=True
        )
    with c4:
        st.plotly_chart(
            scatter(df_deltas, "D_CONV", "D_MIX_INAD",
                    "Δ % Conversão vs AA (pp)", "Δ % Mix Inadimplência (pp)",
                    "Δ Conversão (X) vs Δ % Mix Inadimplência (Y)"),
            use_container_width=True
        )

    st.plotly_chart(
        scatter(df_deltas, "D_CONV", "D_NAO_AI",
                "Δ % Conversão vs AA (pp)", "Δ % Não Realizou AI (pp)",
                "Δ Conversão (X) vs Δ % Não Realizou AI (Y)"),
        use_container_width=True
    )

# ---- Aba Percentuais ----
with tab_perc:
    st.subheader("Percentuais — X = % Conversão (nível atual)")
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(
            scatter(df_perc, "P_CONV", "P_MENOR40",
                    "% Conversão (nível atual)", "% com Média < 40",
                    "% Conversão (X) vs % Média < 40 (Y)"),
            use_container_width=True
        )
    with c2:
        st.plotly_chart(
            scatter(df_perc, "P_CONV", "P_REPROV",
                    "% Conversão (nível atual)", "% Reprovado",
                    "% Conversão (X) vs % Reprovado (Y)"),
            use_container_width=True
        )

    c3, c4 = st.columns(2)
    with c3:
        st.plotly_chart(
            scatter(df_perc, "P_CONV", "P_REND100",
                    "% Conversão (nível atual)", "% Rendimento 100%",
                    "% Conversão (X) vs % Rendimento 100% (Y)"),
            use_container_width=True
        )
    with c4:
        st.plotly_chart(
            scatter(df_perc, "P_CONV", "P_MIX_INAD",
                    "% Conversão (nível atual)", "% Mix Inadimplência",
                    "% Conversão (X) vs % Mix Inadimplência (Y)"),
            use_container_width=True
        )

    st.plotly_chart(
        scatter(df_perc, "P_CONV", "P_NAO_AI",
                "% Conversão (nível atual)", "% Não Realizou AI",
                "% Conversão (X) vs % Não Realizou AI (Y)"),
        use_container_width=True
    )

st.markdown("---")
st.caption("Observação: Quadrantes traçados em 0 (linhas tracejadas). Escala de cores: Viridis invertida (Δ % AUM).")
