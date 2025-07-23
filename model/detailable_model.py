from model.generic_model import ExplorableModel
from ui.details_windows.generic_detail_window import GenericDetailWindow

class DetailableModel(ExplorableModel):
    details_window_class = GenericDetailWindow
    
    @classmethod
    def get_detail_windowclass(cls):
        return cls.details_window_class