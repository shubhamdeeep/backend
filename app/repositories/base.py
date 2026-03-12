"""
Base repository contract (Interface Segregation / Dependency Inversion).
Concrete repositories implement data access; services depend on these abstractions.
"""

from abc import ABC
from typing import Generic, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")


class BaseRepository(ABC, Generic[T]):
    """Abstract base for repositories. Defines contract, not implementation."""

    def __init__(self, session: AsyncSession):
        self._session = session

    @property
    def session(self) -> AsyncSession:
        return self._session
