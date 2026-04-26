import uuid
import pymongo
import pytest
from unittest.mock import patch

from src.util.dao import DAO


@pytest.fixture
def sut():
    """
    Fixture for integration testing DAO.create with MongoDB.

    A unique test collection is created for this test run.
    The collection is removed after the test, so production data is not disturbed.
    """

    test_collection_name = f"test_create_{uuid.uuid4().hex}"

    test_validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["name"],
            "properties": {
                "name": {"bsonType": "string"}
            }
        }
    }

    with patch("src.util.dao.getValidator") as mock_get_validator:
        mock_get_validator.return_value = test_validator

        dao = DAO(test_collection_name)

        yield dao

        dao.drop()


def test_create_valid_object(sut):
    """
    A valid object that follows the validator should be created successfully.
    """

    valid_data = {"name": "Levin"}

    result = sut.create(valid_data)

    assert "_id" in result
    assert result["name"] == "Levin"


def test_create_missing_required_property(sut):
    """
    An object without the required property 'name' should be rejected by MongoDB.
    """

    invalid_data = {"age": 25}

    with pytest.raises(pymongo.errors.WriteError):
        sut.create(invalid_data)


def test_create_wrong_data_type(sut):
    """
    An object where 'name' has the wrong data type should be rejected by MongoDB.
    """

    invalid_data = {"name": 12345}

    with pytest.raises(pymongo.errors.WriteError):
        sut.create(invalid_data)