import pytest, os, tempfile
from pathlib import Path

from src.models.base.base_model import BaseModel
from src.models.mixins.json_mixin import JsonMixin
from src.models.repositories.data_repository import DataRepository

# === Fixtures ===
class MockModel(BaseModel, JsonMixin):
    """Mock model for tests"""
    DATA_FOLDER = "mock"

    def __init__(self, name:str = "test"):
        self.name = name

    def to_json(self) -> str:
        return f'{{"name": "{self.name}"}}'

    @classmethod
    def from_json(cls, json_str: str):
        import json
        data = json.loads(json_str)
        return cls(name=data.get("name", "test"))

# === Test DataRepository ===
class TestDataRepository:
    def setup_method(self):
        """Create a temp folder for each test"""
        self.temp_dir = tempfile.mkdtemp()

        # source1/mock/ and 2 files
        source1_mock = Path(self.temp_dir) / "source1" / "mock"
        source1_mock.mkdir(parents=True, exist_ok=True)
        (source1_mock / "file1.json").write_text('{"name": "spell1"}')
        (source1_mock / "file2.json").write_text('{"name": "spell2"}')

        # source2/mock/ and 2 files
        source2_mock = Path(self.temp_dir) / "source2" / "mock"
        source2_mock.mkdir(parents=True, exist_ok=True)
        (source2_mock / "file3.json").write_text('{"name": "spell3"}')
        (source2_mock / "file4.json").write_text('{"name": "spell4"}')

        # set data_path of repository
        DataRepository.set_data_path(Path(self.temp_dir))

    def teardown_method(self):
        """Cleanup after each test"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
        # Reset data_path
        DataRepository.data_path = None

    # Test set_data_path
    def test_set_data_path(self):
        """Test: change the data_path of the DataRepository"""
        # Arrange
        current_path = DataRepository.data_path
        new_path = Path(tempfile.mkdtemp())
        assert new_path != current_path

        # Act
        DataRepository.set_data_path(new_path)

        # Assert
        assert DataRepository.data_path == new_path

    def test_set_data_path_str(self):
        """Test: change the data_path with a str"""
        # Arrange
        current_path = DataRepository.data_path
        new_path = tempfile.mkdtemp()
        assert new_path != current_path

        # Act
        DataRepository.set_data_path(new_path)

        # Assert
        assert isinstance(DataRepository.data_path, Path)

    def test_set_data_path_not_exist(self):
        """Test: set_data_path raise an error if path doesn't exist"""
        # Arrange
        fake_path = Path("fake")

        # Act & Assert
        with pytest.raises(ValueError, match="doesn't exist"):
            DataRepository.set_data_path(fake_path)

    # Test load_all method
    def test_load_all(self):
        """Test: loads a few models"""
        # Arrange
        # / done in setup_method

        # Act
        models = DataRepository.load_all(MockModel)

        # Assert
        assert len(models) == 4
        assert models[0].name in ["spell1", "spell2", "spell3", "spell4"]

    def test_load_all_data_folder_none_raise(self):
        """Test: raises an error when data_path is None"""
        # Arrange
        DataRepository.data_path = None

        # Act & Assert
        with pytest.raises(ValueError, match="folder not found"):
            DataRepository.load_all(MockModel)

    def test_load_all_non_json_file(self):
        """Test: a non json file is ignored"""
        # Arrange
        (Path(self.temp_dir) / "source1" / "mock" / "ill_file.csv").write_text("col1,col2\nval1,val2\nval3,val4")

        # Act
        result: list[MockModel] = DataRepository.load_all(MockModel)

        # Assert
        assert len(result) == 4
        for i in result:
            assert i.name in ["spell1", "spell2", "spell3", "spell4"]