"""
Model representing a file move history entry.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass(slots=True)
class MoveHistory:
    """
    Represents a completed file move operation.
    """

    source: Path
    destination: Path
    moved_at: datetime

    def to_dict(self) -> dict[str, str]:
        """
        Convert history to dictionary.
        """
        return {
            "source": str(self.source),
            "destination": str(self.destination),
            "moved_at": self.moved_at.isoformat(),
        }

    @classmethod
    def from_dict(
        cls,
        data: dict[str, str],
    ) -> "MoveHistory":
        """
        Create MoveHistory from dictionary.
        """
        return cls(
            source=Path(data["source"]),
            destination=Path(data["destination"]),
            moved_at=datetime.fromisoformat(
                data["moved_at"]
            ),
        )