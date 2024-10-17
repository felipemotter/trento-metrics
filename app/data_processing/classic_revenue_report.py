import pandas as pd
from data_processing.base import get_invoice_move_lines_df, handle_empty_families
from utils.constants import PRODUCT_FAMILY_OTHERS

# Dicionário de mapeamento dos meses
MONTH_DICT = {
    1: "Janeiro",
    2: "Fevereiro",
    3: "Março",
    4: "Abril",
    5: "Maio",
    6: "Junho",
    7: "Julho",
    8: "Agosto",
    9: "Setembro",
    10: "Outubro",
    11: "Novembro",
    12: "Dezembro",
}


def get_anual_invoice_move_lines_df():
    df = get_invoice_move_lines_df()

    if not df.empty:
        df = df[["confirm_date", "sale_value", "product_family"]]

        df["Ano"] = df["confirm_date"].dt.year
        df["Mês_num"] = df["confirm_date"].dt.month
        df["Mês"] = df["Mês_num"].map(MONTH_DICT)

        # Define a ordem dos meses
        df["Mês"] = pd.Categorical(
            df["Mês"], categories=list(MONTH_DICT.values()), ordered=True
        )

        df = process_anual_invoice_move_lines_df(df)

    return df


def process_anual_invoice_move_lines_df(df):
    df = clean_column(
        df,
        column="sale_value",
        patterns={"R\$": "", "\$": "", " ": ""},
        fill_na=0,
    )

    custom_values = {
        1: 10000,  # Janeiro
        2: 15000,  # Fevereiro
    }

    df = apply_custom_values(df, year=2023, custom_values=custom_values)

    df = clean_column(
        df,
        column="sale_value",
        patterns={"R\$": "", "\$": "", " ": ""},
        fill_na=0,
    )

    df = df.sort_values(["product_family", "Ano", "Mês_num"])
    handle_empty_families(df)
    return df


def format_brazilian_currency(value):
    s = f"{value:,.2f}"
    s = s.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {s}"


def clean_column(df, column, patterns=None, fill_na=0, new_column=None):
    if column not in df.columns:
        raise ValueError(f"The column '{column}' does not exist in the DataFrame.")

    if patterns:
        df[column] = df[column].replace(patterns, regex=True)

    df[column] = pd.to_numeric(df[column], errors="coerce")

    df[column] = df[column].fillna(fill_na)

    if new_column:
        df.rename(columns={column: new_column}, inplace=True)

    return df


def apply_custom_values(df, year, custom_values, product_family=PRODUCT_FAMILY_OTHERS):
    for month_num, value in custom_values.items():
        exists = ((df["Ano"] == year) & (df["Mês_num"] == month_num)).any()
        if exists:
            df.loc[(df["Ano"] == year) & (df["Mês_num"] == month_num), "sale_value"] = (
                value
            )
        else:
            new_record = {
                "confirm_date": pd.Timestamp(year, month_num, 1),
                "sale_value": value,
                "product_family": product_family,
                "Ano": year,
                "Mês_num": month_num,
                "Mês": MONTH_DICT[month_num],
            }
            df = pd.concat([df, pd.DataFrame([new_record])], ignore_index=True)
    return df


def get_unique_product_families(df):
    families = df["product_family"].unique().tolist()
    families = reorganize_families(families)
    return families


def reorganize_families(families):
    if "TOTAL" in families:
        families.remove("TOTAL")

    # Insere 'TOTAL' no início da lista
    families.insert(0, "TOTAL")

    # Move 'Outros' para o final da lista
    if PRODUCT_FAMILY_OTHERS in families:
        families.remove(PRODUCT_FAMILY_OTHERS)
        families.append(PRODUCT_FAMILY_OTHERS)

    return families


def process_classic_revenue_report_df(df):
    df_monthly = (
        df.groupby(["Ano", "Mês_num", "Mês"]).agg({"sale_value": "sum"}).reset_index()
    )
    df_monthly["Acumulado"] = df_monthly.groupby(["Ano"])["sale_value"].cumsum()

    years = sorted(df_monthly["Ano"].unique(), reverse=True)

    if len(years) < 2:
        return None, "Dados insuficientes para comparar os anos."

    current_year = years[0]
    previous_year = years[1]

    df_current = df_monthly[df_monthly["Ano"] == current_year][
        ["Mês_num", "Mês", "sale_value", "Acumulado"]
    ].copy()
    df_current.rename(
        columns={"sale_value": "Total", "Acumulado": "Acumulado"}, inplace=True
    )

    df_previous = df_monthly[df_monthly["Ano"] == previous_year][
        ["Mês_num", "Mês", "sale_value", "Acumulado"]
    ].copy()
    df_previous.rename(
        columns={"sale_value": "Total Anterior", "Acumulado": "Acumulado Anterior"},
        inplace=True,
    )

    df_merged = pd.merge(df_current, df_previous, on=["Mês_num", "Mês"], how="outer")

    df_merged.fillna(0, inplace=True)

    df_merged["Variação (%)"] = (
        (df_merged["Total"] - df_merged["Total Anterior"]) / df_merged["Total Anterior"]
    ) * 100

    df_merged["Variação Acumulada (%)"] = (
        (df_merged["Acumulado"] - df_merged["Acumulado Anterior"])
        / df_merged["Acumulado Anterior"]
    ) * 100

    df_merged.replace([float("inf"), -float("inf")], 0, inplace=True)
    df_merged["Variação (%)"] = df_merged["Variação (%)"].fillna(0)
    df_merged["Variação Acumulada (%)"] = df_merged["Variação Acumulada (%)"].fillna(0)

    # Ordena pelos números dos meses para manter a ordem correta
    df_merged = df_merged.sort_values("Mês_num")

    df_merged = df_merged[
        [
            "Mês",
            "Total",
            "Acumulado",
            "Variação (%)",
            "Variação Acumulada (%)",
            "Total Anterior",
            "Acumulado Anterior",
        ]
    ]

    return df_merged, None


def format_display_df(df):
    df_display = df.copy()
    df_display["Variação (%)"] = df_display["Variação (%)"].map("{:+.2f}%".format)
    df_display["Variação Acumulada (%)"] = df_display["Variação Acumulada (%)"].map(
        "{:+.2f}%".format
    )
    df_display["Total"] = df_display["Total"].apply(format_brazilian_currency)
    df_display["Acumulado"] = df_display["Acumulado"].apply(format_brazilian_currency)
    df_display["Total Anterior"] = df_display["Total Anterior"].apply(
        format_brazilian_currency
    )
    df_display["Acumulado Anterior"] = df_display["Acumulado Anterior"].apply(
        format_brazilian_currency
    )
    return df_display
