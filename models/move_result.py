"""
Model representing the result of a file move operation.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class MoveResult:
    """
    Result of a file move operation.

    Attributes:
        source:
            Original file path.

        destination:
            Destination file path.

        success:
            Whether the move succeeded.

        message:
            Result message or error description.
    """

    source: Path
    destination: Path
    success: bool
    message: str = ""

    @property
    def file_name(self) -> str:
        """
        Return the file name.
        """
        return self.source.name

    @property
    def status(self) -> str:
        """
        Return a human-readable status.
        """
        return "완료" if self.success else "실패"

    def to_dict(self) -> dict[str, str | bool]:
        """
        Convert to a JSON-serializable dictionary.

        Returns:
            Dictionary representation.
        """
        return {
            "source": str(self.source),
            "destination": str(self.destination),
            "success": self.success,
            "message": self.message,
        }

    @classmethod
    def from_dict(
        cls,
        data: dict[str, str | bool],
    ) -> "MoveResult":
        """
        Create MoveResult from a dictionary.

        Args:
            data:
                Dictionary data.

        Returns:
            MoveResult instance.
        """
        return cls(
            source=Path(str(data["source"])),
            destination=Path(str(data["destination"])),
            success=bool(data["success"]),
            message=str(data["message"]),
        )