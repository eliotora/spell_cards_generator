from pathlib import Path

from src.models.repositories.base_repository import BaseRepository, T

class DataRepository(BaseRepository[T]):
    data_path: Path = None

    @classmethod
    def set_data_path(cls, path: Path|str) -> None:
        if isinstance(path, str):
            path = Path(path)

        if not path.exists():
            raise ValueError(f"The data path: {path} doesn't exist")
        cls.data_path = path

    @classmethod
    def load_all(cls, model_cls: type[T]) -> list[T]:
        if not cls.data_path or not cls.data_path.exists():
            raise ValueError("Data folder not found")

        result = []

        model_folder : Path = getattr(model_cls, "DATA_FOLDER")

        for source_folder in cls.data_path.iterdir():
            if not source_folder.is_dir():
                continue

            folder = source_folder / model_folder

            if not folder.exists():
                continue

            for file in folder.glob("*.json"):
                item = cls.get_instance_from_file(file, model_cls)

                setattr(item, "source", source_folder.name)

                result.append(item)

        return result