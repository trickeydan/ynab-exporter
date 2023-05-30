from datetime import date, datetime
from pydantic import BaseModel
from typing import Optional

from uuid import UUID


class Account(BaseModel):
    id: UUID
    name: str
    type: str  # TODO
    on_budget: bool
    closed: bool
    deleted: bool
    cleared_balance: int
    uncleared_balance: int
    last_reconciled_at: Optional[datetime]


class Budget(BaseModel):
    id: UUID
    name: str
    last_modified_on: datetime
    first_month: date
    last_month: date
    accounts: list[Account]

    @property
    def active_accounts(self):
        return [account for account in self.accounts if not account.deleted]


class Category(BaseModel):
    id: UUID
    name: str
    budgeted: int
    activity: int
    balance: int


class CategoryGroup(BaseModel):
    id: UUID
    name: str
    hidden: bool
    categories: list[Category]
