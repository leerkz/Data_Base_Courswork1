from typing import Any, Optional

import psycopg2


class DBManager:
    """Класс для выполнения запросов к базе данных PostgreSQL по вакансиям и компаниям."""

    def __init__(self, db_name: str, user: str, password: str, host: str, port: str) -> None:
        """Инициализирует подключение к базе данных PostgreSQL."""
        self.conn = psycopg2.connect(dbname=db_name, user=user, password=password, host=host, port=port)

    def get_companies_and_vacancies_count(self) -> list[tuple[Any, ...]]:
        """Возвращает список компаний и количество вакансий у каждой компании."""
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT c.name, COUNT(v.vacancy_id) AS vacancies_count
                FROM companies c
                LEFT JOIN vacancies v ON c.company_id = v.company_id
                GROUP BY c.company_id;
            """
            )
            return cur.fetchall()

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
                SELECT v.title, c.name, v.salary_from, v.salary_to, v.currency, v.url
                FROM vacancies v
                JOIN companies c ON v.company_id = c.company_id
                WHERE (v.salary_from + v.salary_to) / 2 > (
                    SELECT AVG((salary_from + salary_to) / 2) FROM vacancies
                );
            """
            )
            return cur.fetchall()

    def get_vacancies_with_keyword(self, keyword: str) -> list[tuple[Any, ...]]:
        """Возвращает вакансии, содержащие заданное ключевое слово в названии."""
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT v.title, c.name, v.salary_from, v.salary_to, v.currency, v.url
                FROM vacancies v
                JOIN companies c ON v.company_id = c.company_id
                WHERE v.title ILIKE %s;
            """,
                (f"%{keyword}%",),
            )
            return cur.fetchall()

    def close(self) -> None:
        """Закрывает подключение к базе данных."""
        self.conn.close()
