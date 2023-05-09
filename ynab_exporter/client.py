from uuid import UUID
import requests

from pydantic import parse_obj_as

from .types import Budget, CategoryGroup


class YNABClient:
    def __init__(self, access_token: str) -> None:
        self._access_token = access_token

    def get_budgets(self) -> list[Budget]:
        resp = requests.get(
            "https://api.ynab.com/v1/budgets?include_accounts=true",
            headers={"Authorization": f"Bearer {self._access_token}"},
        )
        resp.raise_for_status()
        return parse_obj_as(list[Budget], resp.json()["data"]["budgets"])

    def get_categories(self, budget_id: UUID) -> list[CategoryGroup]:
        resp = requests.get(
            f"https://api.ynab.com/v1/budgets/{budget_id}/categories",
            headers={"Authorization": f"Bearer {self._access_token}"},
        )
        resp.raise_for_status()
        return parse_obj_as(list[CategoryGroup], resp.json()["data"]["category_groups"])
