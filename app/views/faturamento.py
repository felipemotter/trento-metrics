# views/faturamento.py
import pandas as pd
import streamlit as st
from database.external import get_faturamento_data


def view_faturamento():
    st.title("Análise de Faturamento")

    # Obter os dados de faturamento
    data = get_faturamento_data()

    if data:
        # Criar um DataFrame a partir dos dados
        df = pd.DataFrame(data)
        df.columns = [
            "Data de Confirmação",
            "Nome",
            "Valor da Venda",
            "Família do Produto",
        ]

        # Exibir o DataFrame no Streamlit
        st.dataframe(df)

        # Análises Adicionais (Opcional)
        # Por exemplo, exibir métricas agregadas
        total_vendas = df["Valor da Venda"].sum()
        st.metric("Total de Vendas", f"R$ {total_vendas:,.2f}")

        # Gráfico de Barras por Família de Produto
        vendas_por_familia = (
            df.groupby("Família do Produto")["Valor da Venda"].sum().reset_index()
        )
        st.bar_chart(vendas_por_familia.set_index("Família do Produto"))
    else:
        st.info("Nenhum dado de faturamento encontrado.")
