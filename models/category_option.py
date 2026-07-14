"""
Model representing an organization category option.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class CategoryOption:
    """
    Represents a selectable organization category.

    Attributes:
        name:
            Category name.

        count:
            Number of files in this category.

        checked:
            Whether this category is selected.

        icon:
            Display icon.
    """

    name: str
    count: int
    checked: bool = True
    icon: str = "📁"

    @property
    def display_name(self) -> str:
        """
        Return display text.
        """
        return f"{self.icon} {self.name} ({self.count})"