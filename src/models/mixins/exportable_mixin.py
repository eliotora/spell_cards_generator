from typing import ClassVar
import enum

MODEL_EXPORT_MODE_HTML_FILES = {}

class ExportOption(enum.IntEnum):
    """Enum for export options."""
    RULES = 1
    GRIMOIRE = 2
    CARDS = 3

    @classmethod
    def from_string(cls, value: str) -> 'ExportOption':
        """Convert a string to an ExportOption enum."""
        return cls[value.upper()]

    def __str__(self) -> str:
        """String representation of the enum."""
        return self.name.lower()

class ExportableMixin:
    """Mixin for models that should be explortable to HTML"""
    METADATA_NAMESPACE = "export"

    template_file_path = ClassVar[str]
    export_options: ClassVar[list[ExportOption]] = [ExportOption.RULES]

    def get_html_dict(self) -> dict[str, str|bool|int]:
        """Has to be implemented by every class"""
        pass

    def __init_subclass__(cls):
        MODEL_EXPORT_MODE_HTML_FILES[(cls.__name__.lower(), ExportOption.RULES.value)] = "generic_rules.html"
        MODEL_EXPORT_MODE_HTML_FILES[(cls.__name__.lower(), ExportOption.CARDS.value)] = "generic_cards.html"
        super().__init_subclass__()