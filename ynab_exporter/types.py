from datetime import date, datetime
from pydantic import BaseModel

from uuid import UUID


class Account(BaseModel):
    id: UUID
    name: str
    type: str  # TODO
    on_budget: bool
    closed: bool
    cleared_balance: int
    uncleared_balance: int
    last_reconciled_at: datetime


class Budget(BaseModel):
    id: UUID
    name: str
    last_modified_on: datetime
    first_month: date
    last_month: date
    accounts: list[Account]


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
