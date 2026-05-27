from typing import ClassVar
from src.ui.details_windows.generic_detail_window import GenericDetailWindow


class PopupMixin:
    """Mixin for models that should display their data in a popup"""
    METADATA_NAMESPACE = "popup"

    popup_window_class : ClassVar[GenericDetailWindow] = GenericDetailWindow

    @classmethod
    def get_popup_window_class(self):
        return self.popup_window_class