import psycopg2
from psycopg2.extensions import connection

from database import create_database, create_tables
from db_manager import DBManager

DB_CONFIG = {
    "db_name": "hh_database",
    "user": "your_user",
    "password": "your_password",
    "host": "localhost",
    "port": "5432",
}


def main() -> None:
    """Основная функция для выполнения этапов проекта: создания базы, таблиц, получения данных и их анализа."""
    # Создание базы данных и таблиц, получение данных и работа с запросами.
    create_database(
        DB_CONFIG["db_name"], DB_CONFIG["user"], DB_CONFIG["password"], DB_CONFIG["host"], DB_CONFIG["port"]
    )
    conn: connection = psycopg2.connect(
        dbname=DB_CONFIG["db_name"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
    )
    create_tables(conn)
    companies_ids = ["1455", "4740", "678", "3935"]
    db_manager = DBManager(**DB_CONFIG)
    print(db_manager.get_companies_and_vacancies_count())
    db_manager.close()


if __name__ == "__main__":
    main()
