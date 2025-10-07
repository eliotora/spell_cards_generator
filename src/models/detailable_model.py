from models.generic_model import ExplorableModel, MODEL_NAME_MAPPING, ExportOption
from ui.details_windows.generic_detail_window import GenericDetailWindow

MODEL_EXPORT_MODE_HTML_FILES = {}

class DetailableModel(ExplorableModel):
    details_window_class = GenericDetailWindow
    color = None

    def to_html_dict(self):
        pass

    @classmethod
    def get_detail_windowclass(cls):
        return cls.details_window_class

    def __init_subclass__(cls):
        super().__init_subclass__()
        MODEL_NAME_MAPPING[cls.__name__.lower()] = cls
        MODEL_EXPORT_MODE_HTML_FILES[(cls.__name__.lower(), ExportOption.RULES.value)] = "generic_rules.html"
        MODEL_EXPORT_MODE_HTML_FILES[(cls.__name__.lower(), ExportOption.CARDS.value)] = "generic_cards.html"
