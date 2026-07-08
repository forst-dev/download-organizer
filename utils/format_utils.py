"""
Utilities for formatting values for display.
"""

from __future__ import annotations


def format_size(size: int) -> str:
    """
    Convert a file size in bytes to a human-readable string.

    Args:
        size: File size in bytes.

    Returns:
        str: Formatted size (e.g. "1.25 MB", "3.42 GB").
    """
    if size < 0:
        raise ValueError("File size cannot be negative.")

    units = ["B", "KB", "MB", "GB", "TB"]

    value = float(size)

    for unit in units:
        if value < 1024 or unit == units[-1]:
            if unit == "B":
                return f"{int(value)} {unit}"

            return f"{value:.2f} {unit}"

        value /= 1024

    return f"{value:.2f} TB"