from typing import Dict, List

import requests


class HHAPIClient:
    """Класс для получения информации о компаниях и вакансиях с API hh.ru."""

    BASE_URL = "https://api.hh.ru"

    @staticmethod
    def get_company_info(employer_id: str) -> Dict:
        """Возвращает информацию о компании по её ID."""
        response = requests.get(f"{HHAPIClient.BASE_URL}/employers/{employer_id}")
        response.raise_for_status()
        return response.json()

    @staticmethod
    def get_vacancies(employer_id: str, page: int = 0, per_page: int = 100) -> List[Dict]:
        """Возвращает список вакансий для компании с возможностью пагинации."""
        params = {"employer_id": employer_id, "page": page, "per_page": per_page}
        response = requests.get(f"{HHAPIClient.BASE_URL}/vacancies", params=params)
        response.raise_for_status()
        return response.json()["items"]
