from typing import Any, Optional, Tuple

import psycopg2


class DBManager:
    """Класс для выполнения запросов к базе данных PostgreSQL по вакансиям и компаниям."""

    def __init__(self, db_name: str, params: dict) -> None:
        """Инициализирует подключение к базе данных PostgreSQL."""
        self.db_name = db_name
        self.params = params
        self.conn = psycopg2.connect(dbname=db_name, **params)

    def get_companies_and_vacancies_count(self) -> tuple[Any, ...] | None:
        """Возвращает список компаний и количество вакансий у каждой компании."""
        conn = psycopg2.connect(dbname=self.db_name, **self.params)
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT name, COUNT(*) FROM vacancies
                INNER JOIN companies ON companies.company_id = vacancies.company_id
                GROUP BY name;
            """
            )
            return cur.fetchone()

    def get_all_vacancies(self) -> list[tuple[Any, ...]]:
        """Возвращает список всех вакансий с информацией о компании, зарплате и ссылке на вакансию."""
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT c.name AS company_name, v.title AS vacancy_title, v.salary_from, v.salary_to, v.currency, v.url
                FROM vacancies v
                JOIN companies c ON v.company_id = c.company_id;
            """
            )
            return cur.fetchall()

    def get_avg_salary(self) -> Optional[float]:
        """Возвращает среднюю зарплату по всем вакансиям."""
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT AVG((salary_from + salary_to)/2) AS avg_salary
                FROM vacancies
                WHERE salary_from IS NOT NULL AND salary_to IS NOT NULL;
            """
            )
            result = cur.fetchone()
            return result[0] if result else None

    def get_vacancies_with_higher_salary(self) -> list[tuple[Any, ...]]:
        """Возвращает вакансии с зарплатой выше средней по всем вакансиям."""
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT * FROM vacancies WHERE salary_to > (SELECT AVG(salary_to) FROM vacancies)
            """
            )
            return cur.fetchall()

    def get_vacancies_with_keyword(self, keyword: str) -> list[tuple[Any, ...]]:
        """Возвращает вакансии, содержащие заданное ключевое слово в названии."""
        with self.conn.cursor() as cur:
            cur.execute(
                f"""
                SELECT * FROM vacancies WHERE title LIKE '%{keyword}%'
            """
            )
            return cur.fetchall()

    def close(self) -> None:
        """Закрывает подключение к базе данных."""
        self.conn.close()
