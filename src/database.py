import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT, connection


def create_database(db_name: str, user: str, password: str, host: str, port: str) -> None:
    """Создает базу данных PostgreSQL с заданными параметрами подключения."""
    conn = psycopg2.connect(dbname="postgres", user=user, password=password, host=host, port=port)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute(f"CREATE DATABASE {db_name};")
    cur.close()
    conn.close()


def create_tables(conn: connection) -> None:
    """Создает таблицы компаний и вакансий в базе данных PostgreSQL."""
    with conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS companies (
                company_id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                industry VARCHAR(255),
                city VARCHAR(255),
                url VARCHAR(255)
            );
        """
        )

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS vacancies (
                vacancy_id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                salary_from NUMERIC,
                salary_to NUMERIC,
                currency VARCHAR(10),
                company_id INT REFERENCES companies(company_id),
                url VARCHAR(255)
            );
        """
        )
        conn.commit()
