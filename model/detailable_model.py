from model.generic_model import ExplorableModel, MODEL_NAME_MAPPING
from ui.details_windows.generic_detail_window import GenericDetailWindow

class DetailableModel(ExplorableModel):
    details_window_class = GenericDetailWindow

    @classmethod
    def get_detail_windowclass(cls):
        return cls.details_window_class

    def __init_subclass__(cls):
        super().__init_subclass__()
        MODEL_NAME_MAPPING[cls.__name__.lower()] = cls