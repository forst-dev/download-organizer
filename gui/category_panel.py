"""
Category selection panel.
"""

from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from models.category_option import CategoryOption
from qfluentwidgets import PrimaryPushButton

class CategoryPanel(QScrollArea):
    """
    Scrollable category selection panel.
    """

    selection_changed = Signal(list)

    def __init__(self) -> None:
        super().__init__()

        self._checkboxes: dict[str, QCheckBox] = {}

        self._container = QWidget()

        self._layout = QVBoxLayout(self._container)
        self._button_widget = QWidget()

        self._button_layout = QVBoxLayout(self._button_widget)
        self._button_layout.setContentsMargins(0, 0, 0, 10)
        self._button_layout.setSpacing(5)

        self.select_all_button = PrimaryPushButton("전체 선택")
        self.clear_all_button = PrimaryPushButton("전체 해제")

        self._button_layout.addWidget(self.select_all_button)
        self._button_layout.addWidget(self.clear_all_button)

        self._layout.addWidget(self._button_widget)

        self.select_all_button.clicked.connect(
            self.select_all
        )

        self.clear_all_button.clicked.connect(
            self.clear_all
        )

        self._layout.setContentsMargins(
            10,
            10,
            10,
            10,
        )

        self._layout.setSpacing(8)

        self.setWidget(self._container)
        self.setWidgetResizable(True)

    def set_categories(
        self,
        categories: list[CategoryOption],
    ) -> None:
        """
        Display categories.

        Args:
            categories:
                Categories to display.
        """
        self.clear()

        for category in categories:
            checkbox = QCheckBox(
                category.display_name
            )

            checkbox.setChecked(
                category.checked
            )

            checkbox.toggled.connect(
                self._emit_selection_changed
            )

            self._layout.addWidget(
                checkbox
            )

            self._checkboxes[
                category.name
            ] = checkbox

        self._layout.addStretch()

        self._emit_selection_changed()

    def selected_categories(
        self,
    ) -> list[str]:
        """
        Return selected category names.
        """
        return [
            name
            for name, checkbox
            in self._checkboxes.items()
            if checkbox.isChecked()
        ]

    def clear(self) -> None:
        """
        Remove all category checkboxes.
        """
        while self._layout.count() > 1:
            item = self._layout.takeAt(1)

            widget = item.widget()

            if widget is not None:
                widget.deleteLater()

        self._checkboxes.clear()

    def _emit_selection_changed(
        self,
    ) -> None:
        """
        Emit selected categories.
        """
        self.selection_changed.emit(
            self.selected_categories()
        )

    def select_all(self) -> None:
        """
        Select all categories.
        """
        for checkbox in self._checkboxes.values():
            checkbox.setChecked(True)

        self._emit_selection_changed()

    def clear_all(self) -> None:
        """
        Deselect all categories.
        """
        for checkbox in self._checkboxes.values():
            checkbox.setChecked(False)

        self._emit_selection_changed()