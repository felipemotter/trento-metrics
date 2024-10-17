import altair as alt
import streamlit as st
from data_processing.classic_revenue_report import (
    format_brazilian_currency,
    format_display_df,
    get_anual_invoice_move_lines_df,
    get_unique_product_families,
    process_classic_revenue_report_df,
)


def create_chart(df_plot):
    df_plot["formatted_sale_value"] = df_plot["sale_value"].apply(
        format_brazilian_currency
    )
    chart = (
        alt.Chart(df_plot)
        .mark_line(point=True)
        .encode(
            x=alt.X("Mês_num:O", title="Mês", axis=alt.Axis(labelAngle=0)),
            y=alt.Y("sale_value:Q", title="Valor de Venda"),
            color=alt.Color("Ano:N", title="Ano"),
            tooltip=[
                alt.Tooltip("Ano:N", title="Ano"),
                alt.Tooltip("Mês_num:O", title="Mês"),
                alt.Tooltip("formatted_sale_value:N", title="Valor de Venda"),
            ],
        )
        .properties(width=400, height=300)
        .configure_axis(labelFontSize=12, titleFontSize=14)
        .configure_legend(titleFontSize=14, labelFontSize=12)
    )

    return chart


def view_revenue():
    st.title("FATURAMENTO")

    df = get_anual_invoice_move_lines_df()

    if not df.empty:
        families = get_unique_product_families(df)

        for family in families:
            if family != "TOTAL":
                df_family = df[df["product_family"] == family].copy()
            else:
                df_family = df.copy()

            report_df, warning_message = process_classic_revenue_report_df(df_family)

            if warning_message:
                st.warning(warning_message)
                continue

            df_display = format_display_df(report_df).set_index("Mês")

            st.subheader(f"{family}")

            col_table, col_chart = st.columns([2, 1])

            with col_table:
                st.table(df_display)

            with col_chart:
                df_plot = (
                    df_family.groupby(["Ano", "Mês_num", "Mês"])
                    .agg({"sale_value": "sum"})
                    .reset_index()
                )
                sorted_years = sorted(df_plot["Ano"].unique(), reverse=True)
                if len(sorted_years) < 2:
                    st.info("Not enough years to compare in the chart.")
                    continue
                chart = create_chart(df_plot)
                st.altair_chart(chart, use_container_width=True)

    else:
        st.info("No revenue data found.")
