from src.ui.details_windows.generic_detail_window import GenericDetailWindow

class PopupFactory:
    _REGISTRY: dict[type, type[GenericDetailWindow]] = {
        # Model: DetailsWindow
    }

    @classmethod
    def show(cls, obj, parent=None) -> None:
        # MRO research: respect heritage
        for klass in type(obj).mro():
            if klass in cls._REGISTRY:
                dialog_class = cls._REGISTRY[klass]
                break

        else:
            dialog_class = GenericDetailWindow

        dialog = dialog_class(obj, parent)
        dialog.exec()

    @classmethod
    def register(cls, dataclass_type, dialog_class):
        """Registers new types"""
        cls._REGISTRY[dataclass_type] = dialog_class