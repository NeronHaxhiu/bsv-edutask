import pytest
from unittest.mock import MagicMock

from src.controllers.usercontroller import UserController


@pytest.fixture
def mocked_dao():
    return MagicMock()


@pytest.fixture
def controller(mocked_dao):
    return UserController(dao=mocked_dao)


def test_get_user_by_email_returns_registered_user(controller, mocked_dao):
    """
    Test case 1:
    A valid email that exists in the system should return the matching user.
    """

    expected_user = {
        "firstName": "Jane",
        "lastName": "Doe",
        "email": "jane.doe@example.com"
    }

    mocked_dao.find.return_value = [expected_user]

    result = controller.get_user_by_email("jane.doe@example.com")

    assert result == expected_user
    mocked_dao.find.assert_called_once()


def test_get_user_by_email_returns_none_when_user_does_not_exist(controller, mocked_dao):
    """
    Test case 2:
    A valid email that does not exist should return None.
    """

    mocked_dao.find.return_value = []

    result = controller.get_user_by_email("missing@example.com")

    assert result is None
    mocked_dao.find.assert_called_once()


def test_get_user_by_email_rejects_empty_email(controller, mocked_dao):
    """
    Test case 3:
    An empty email address should be rejected.
    The DAO should not be used because the input is invalid.
    """

    with pytest.raises(ValueError):
        controller.get_user_by_email("")

    mocked_dao.find.assert_not_called()


def test_get_user_by_email_rejects_email_without_domain(controller, mocked_dao):
    """
    Test case 4:
    An email without a domain should be rejected.
    """

    with pytest.raises(ValueError):
        controller.get_user_by_email("jane.doe")

    mocked_dao.find.assert_not_called()


def test_get_user_by_email_rejects_email_with_space(controller, mocked_dao):
    """
    Test case 5:
    An email containing whitespace should be rejected.
    """

    with pytest.raises(ValueError):
        controller.get_user_by_email("jane.doe example.com")

    mocked_dao.find.assert_not_called()


def test_get_user_by_email_rejects_none_input(controller, mocked_dao):
    """
    Test case 6:
    None is not a valid email input.
    """

    with pytest.raises(TypeError):
        controller.get_user_by_email(None)

    mocked_dao.find.assert_not_called()


def test_get_user_by_email_returns_first_user_when_multiple_users_exist(controller, mocked_dao):
    """
    Test case 7:
    If several users are connected to the same email, the method should return the first user.
    The method should also print a warning message.
    """

    user_1 = {
        "firstName": "Jane",
        "lastName": "Doe",
        "email": "duplicate@example.com"
    }

    user_2 = {
        "firstName": "John",
        "lastName": "Doe",
        "email": "duplicate@example.com"
    }

    mocked_dao.find.return_value = [user_1, user_2]

    result = controller.get_user_by_email("duplicate@example.com")

    assert result == user_1
    mocked_dao.find.assert_called_once()