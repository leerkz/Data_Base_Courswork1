import psycopg2
from psycopg2.extensions import connection

from src.database import create_database, create_tables
from src.db_manager import DBManager
from config.cofig import config

DB_CONFIG = config()


def main() -> None:
    """Основная функция для выполнения этапов проекта: создания базы, таблиц, получения данных и их анализа."""
    # Создание базы данных и таблиц, получение данных и работа с запросами.
    create_database(
        "lera", **DB_CONFIG
    )
    conn: connection = psycopg2.connect(
        dbname="lera",
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
    )
    create_tables(conn)
    companies_ids = ["1455", "4740", "678", "3935"]
    db_manager = DBManager("lera", DB_CONFIG)
    print(db_manager.get_companies_and_vacancies_count())
    print(db_manager.get_all_vacancies())
    print(db_manager.get_avg_salary())
    print(db_manager.get_vacancies_with_higher_salary())
    print(db_manager.get_vacancies_with_keyword("a"))
    db_manager.close()


if __name__ == "__main__":
    main()
