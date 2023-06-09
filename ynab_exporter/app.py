from time import sleep

from prometheus_client import start_http_server, Gauge

from .client import YNABClient
from .settings import Settings

ACCOUNT_LABELS = [
    "budget_id",
    "budget_name",
    "account_id",
    "account_name",
    "account_type",
]

CATEGORY_LABELS = [
    "budget_id",
    "budget_name",
    "category_group_id",
    "category_group_name",
    "category_id",
    "category_name",
]


def main() -> None:
    settings = Settings()  # type: ignore[call-arg]

    budget_last_modified_g = Gauge(
        "ynab_budget_last_modified",
        "Last modification time of the budget",
        labelnames=["budget_id", "budget_name"],
    )
    account_cleared_balance_g = Gauge(
        "ynab_account_cleared_balance",
        "Cleared Balance of the Account",
        labelnames=ACCOUNT_LABELS,
    )
    account_uncleared_balance_g = Gauge(
        "ynab_account_uncleared_balance",
        "Uncleared Balance of the Account",
        labelnames=ACCOUNT_LABELS,
    )
    account_last_reconciled_g = Gauge(
        "ynab_account_last_reconciled",
        "Last reconciliation time of the budget",
        labelnames=ACCOUNT_LABELS,
    )
    category_activity_g = Gauge(
        "ynab_category_activity",
        "Current activity of the category",
        labelnames=CATEGORY_LABELS,
    )
    category_balance_g = Gauge(
        "ynab_category_balance",
        "Current balance of the category",
        labelnames=CATEGORY_LABELS,
    )
    category_budgeted_g = Gauge(
        "ynab_category_budgeted",
        "Current budgeted amount of the category",
        labelnames=CATEGORY_LABELS,
    )

    start_http_server(settings.port)
    client = YNABClient(settings.access_token)
    while True:
        budgets = client.get_budgets()
        for budget in budgets:
            budget_last_modified_g.labels(budget.id, budget.name).set(
                budget.last_modified_on.timestamp()
            )
            for account in budget.active_accounts:
                account_labels = (
                    budget.id,
                    budget.name,
                    account.id,
                    account.name,
                    account.type,
                )
                account_cleared_balance_g.labels(*account_labels).set(
                    account.cleared_balance / 1000
                )
                account_uncleared_balance_g.labels(*account_labels).set(
                    account.uncleared_balance / 1000
                )
                if account.last_reconciled_at is not None:
                    account_last_reconciled_g.labels(*account_labels).set(
                        account.last_reconciled_at.timestamp()
                    )

            category_groups = client.get_categories(budget.id)
            for group in category_groups:
                for category in group.categories:
                    category_labels = (
                        budget.id,
                        budget.name,
                        group.id,
                        group.name,
                        category.id,
                        category.name,
                    )
                    category_activity_g.labels(*category_labels).set(
                        category.activity / 1000
                    )
                    category_balance_g.labels(*category_labels).set(
                        category.balance / 1000
                    )
                    category_budgeted_g.labels(*category_labels).set(
                        category.budgeted / 1000
                    )
        sleep(60)
