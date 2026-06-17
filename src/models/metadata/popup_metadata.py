from dataclasses import dataclass

@dataclass(frozen=True)
class PopupMetadata:
    label: str = ""
    tooltip: str = ""
    widget: str = "text"
    hidden: bool = False # If True, don't show field

    # Qt styles
    style: str = ""
    min_width: int = 0
