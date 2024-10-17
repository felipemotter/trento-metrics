# database/external.py
import os
from urllib.parse import quote_plus

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker


def get_external_database_url():
    # Obter as configurações do banco de dados a partir das variáveis de ambiente
    db_user = os.getenv("EXTERNAL_DB_USER")
    db_password = os.getenv("EXTERNAL_DB_PASSWORD")
    db_host = os.getenv("EXTERNAL_DB_HOST")
    db_port = os.getenv("EXTERNAL_DB_PORT", "5432")
    db_name = os.getenv("EXTERNAL_DB_NAME")

    # Codificar a senha para lidar com caracteres especiais
    db_password_encoded = quote_plus(db_password)

    # Construir a URL de conexão com a senha codificada
    return f"postgresql://{db_user}:{db_password_encoded}@{db_host}:{db_port}/{db_name}"


def get_external_session():
    external_database_url = get_external_database_url()
    external_engine = create_engine(external_database_url)
    ExternalSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=external_engine
    )
    return ExternalSessionLocal()


def get_invoice_move_lines_data():
    session = get_external_session()
    try:
        query = text("""
            SELECT
                aml.part_confirm_date AS confirm_date,
                aml.sale_value AS sale_value,
                aml.product_family AS product_family
            FROM
                account_move_line aml
            JOIN
                account_move am ON aml.move_id = am.id
            WHERE
                aml.parent_state = 'posted'
                AND am.move_type = 'out_invoice'
                AND aml.part_confirm_date IS NOT NULL
                AND aml.exclude_from_invoice_tab = false
                AND EXTRACT(YEAR FROM aml.part_confirm_date) IN (
                    EXTRACT(YEAR FROM CURRENT_DATE),
                    EXTRACT(YEAR FROM CURRENT_DATE) - 1
                )
        """)
        result = session.execute(query)
        data = result.fetchall()
        return data
    except Exception as e:
        print(f"Erro ao obter dados de faturamento: {e}")
        return []
    finally:
        session.close()
