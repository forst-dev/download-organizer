"""
Model representing a file move operation.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class MovePlan:
    """
    Represents a planned file move.

    Attributes:
        source:
            Original file path.

        destination:
            Destination file path.

        category:
            Target folder category.

        reason:
            Reason why this file will be moved.
    """

    source: Path
    destination: Path
    category: str
    reason: str

    @property
    def file_name(self) -> str:
        """
        Return the file name.
        """
        return self.source.name

    @property
    def destination_folder(self) -> str:
        """
        Return destination folder name.
        """
        return self.destination.parent.name

    def to_dict(self) -> dict[str, str]:
        """
        Convert to a JSON-serializable dictionary.

        Returns:
            Dictionary representation.
        """
        return {
            "source": str(self.source),
            "destination": str(self.destination),
            "category": self.category,
            "reason": self.reason,
        }

    @classmethod
    def from_dict(
        cls,
        data: dict[str, str],
    ) -> "MovePlan":
        """
        Create MovePlan from dictionary.

        Args:
            data:
                Dictionary data.

        Returns:
            MovePlan instance.
        """
        return cls(
            source=Path(data["source"]),
            destination=Path(data["destination"]),
            category=data["category"],
            reason=data["reason"],
        )