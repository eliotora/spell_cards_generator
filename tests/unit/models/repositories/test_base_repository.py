import pytest, os, tempfile

from src.models.repositories.base_repository import BaseRepository
from src.models.base.base_model import BaseModel
from src.models.mixins.json_mixin import JsonMixin

# === Fixture ===
class MockModel(BaseModel, JsonMixin):
    """Mock model for tests"""
    def __init__(self, name:str = "test"):
        self.name = name

    def to_json(self) -> str:
        return f'{{"name": "{self.name}"}}'

    @classmethod
    def from_json(cls, json_str: str):
        import json
        data = json.loads(json_str)
        return cls(name=data.get("name", "test"))

# === TestBaseRepository ===
class TestBaseRepository:
    def setup_method(self):
        """Create a temp folder for each test"""
        self.temp_dir = tempfile.mkdtemp()

    def teardown_method(self):
        """Cleanup after each test"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    # Tests: get_instance_from_file
    def test_get_instance_from_file_success(self):
        """Test: load an instance from a file"""

        # Arrange
        file_path = os.path.join(self.temp_dir, "test.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('{"name": "my_test"}')

        # Act
        instance = BaseRepository.get_instance_from_file(file_path, MockModel)

        # Assert
        assert instance.name == "my_test"

    def test_get_instance_from_file_not_exists(self):
        """Test: raise error if the file doesn't exist"""
        # Arrange
        file_path = os.path.join(self.temp_dir, "fake.json")

        # Act & Assert
        with pytest.raises(ValueError, match="doesn't exist"):
            BaseRepository.get_instance_from_file(file_path, MockModel)

    # Tests: write_instance_to_file
    def test_write_instance_to_file(self):
        """Test : write an instance in a file"""
        # Arrange
        instance = MockModel(name="my_test")
        file_path = os.path.join(self.temp_dir, "output.json")

        assert issubclass(MockModel, JsonMixin)
        assert isinstance(instance, MockModel)

        # Act
        BaseRepository.write_instance_to_file(instance, file_path)

        # Assert
        assert os.path.exists(file_path)
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        assert '"my_test"' in content

    def test_write_instance_to_file_not_json_mixin(self):
        """Test: raise error if the instance is not a JsonMixin"""
        # Arrange
        class BadModel(BaseModel):
            pass

        instance = BadModel()
        file_path = os.path.join(self.temp_dir, "output.json")

        # Act & Assert
        with pytest.raises(TypeError, match="is not"):
            BaseRepository.write_instance_to_file(instance, file_path)

    def test_write_instance_to_file_empty_data(self):
        """Test: raise error if to_json() returns an empty string"""
        # Arrange
        class EmptyModel(BaseModel, JsonMixin):
            def to_json(self) -> str:
                return ""

            @classmethod
            def from_json(cls, json_str:str):
                return cls()

        instance = EmptyModel()
        file_path = os.path.join(self.temp_dir, "output.json")

        # Act & Assert
        with pytest.raises(ValueError, match="returns no data"):
            BaseRepository.write_instance_to_file(instance, file_path)