"""
Create move plans for organizing files.
"""

from __future__ import annotations

from pathlib import Path
from collections import Counter
from models.move_plan import MovePlan
from models.category_option import CategoryOption
from core.base_service import BaseService


class OrganizationService(BaseService):
    """
    Create file organization plans without moving files.
    """

    CATEGORY_RULES: dict[str, tuple[str, set[str]]] = {
        "Images": (
            "Image file",
            {
                ".jpg",
                ".jpeg",
                ".png",
                ".gif",
                ".bmp",
                ".webp",
                ".svg",
                ".ico",
            },
        ),
        "Videos": (
            "Video file",
            {
                ".mp4",
                ".avi",
                ".mkv",
                ".mov",
                ".wmv",
                ".flv",
                ".webm",
            },
        ),
        "Documents": (
            "Document file",
            {
                ".pdf",
                ".doc",
                ".docx",
                ".ppt",
                ".pptx",
                ".xls",
                ".xlsx",
                ".csv",
                ".txt",
                ".hwp",
                ".hwpx",
            },
        ),
        "Archives": (
            "Archive file",
            {
                ".zip",
                ".7z",
                ".rar",
                ".tar",
                ".gz",
            },
        ),
        "Installers": (
            "Installer file",
            {
                ".exe",
                ".msi",
            },
        ),
    }

    DEFAULT_CATEGORY = "Others"

    def execute(
        self,
        folder: Path,
    ) -> list[MovePlan]:
        """
        Create move plans for all files in the folder.

        Args:
            folder:
                Target folder.

        Returns:
            List of MovePlan.
        """
        if not folder.exists():
            raise FileNotFoundError(folder)

        if not folder.is_dir():
            raise NotADirectoryError(folder)

        self.logger.info(
            "Creating organization plan: %s",
            folder,
        )

        plans: list[MovePlan] = []

        for path in folder.iterdir():
            if not path.is_file():
                continue

            category, reason = self._classify(path)

            destination = (
                folder
                / category
                / path.name
            )

            plans.append(
                MovePlan(
                    source=path,
                    destination=destination,
                    category=category,
                    reason=f"{reason} ({path.suffix.lower()})",
                )
            )

        self.logger.info(
            "Created %d move plans.",
            len(plans),
        )

        return plans

    def _classify(
        self,
        file_path: Path,
    ) -> tuple[str, str]:
        """
        Classify a file.

        Args:
            file_path:
                File path.

        Returns:
            (category, reason)
        """
        extension = file_path.suffix.lower()

        for category, (
            reason,
            extensions,
        ) in self.CATEGORY_RULES.items():
            if extension in extensions:
                return category, reason

        return (
            self.DEFAULT_CATEGORY,
            "Unknown file type",
        )
    
    def create_categories(
        self,
        plans: list[MovePlan],
    ) -> list[CategoryOption]:
        """
        Create category options from move plans.

        Args:
            plans:
                Generated move plans.

        Returns:
            List of CategoryOption.
        """
        counter = Counter(
            plan.category
            for plan in plans
        )

        icons = {
            "Images": "🖼",
            "Videos": "🎬",
            "Documents": "📄",
            "Archives": "📦",
            "Installers": "💿",
            "Others": "📁",
        }

        categories: list[CategoryOption] = []

        for name in sorted(counter):
            categories.append(
                CategoryOption(
                    name=name,
                    count=counter[name],
                    checked=True,
                    icon=icons.get(name, "📁"),
                )
            )

        return categories