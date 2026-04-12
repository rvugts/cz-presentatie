"""
Example test module demonstrating TDD patterns used in this project.

This file shows the expected test structure, fixture usage, and test organization.
Use this as a reference when writing new tests.

**Pattern:** Red → Green → Refactor
1. Red: Write failing test
2. Green: Implement minimal code to pass
3. Refactor: Improve while keeping tests passing
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from typing import List, Dict, Any


# ============================================================================
# FIXTURES (Reusable test setup)
# ============================================================================

@pytest.fixture
def sample_user_data() -> Dict[str, Any]:
    """
    Provide sample user data for tests.
    
    Scope: function (fresh data for each test)
    """
    return {
        "id": 1,
        "email": "user@example.com",
        "name": "Test User",
        "is_active": True,
    }


@pytest.fixture
def mock_database() -> Mock:
    """
    Mock database connection.
    
    Scope: function (isolated per test)
    """
    db = Mock()
    db.query.return_value.filter.return_value.first.return_value = None
    return db


@pytest.fixture
def mock_email_service() -> Mock:
    """
    Mock email service for testing without sending real emails.
    
    Scope: function (isolated per test)
    """
    service = Mock()
    service.send.return_value = True
    service.validate.return_value = True
    return service


# ============================================================================
# TEST CLASSES (Organize related tests)
# ============================================================================

class TestUserValidation:
    """
    Group of tests for user validation logic.
    
    Pattern: One test class per component/module
    """
    
    def test_valid_email_accepted(self, sample_user_data: Dict[str, Any]) -> None:
        """
        Test that valid emails are accepted.
        
        **Pattern:**
        - Clear test name following: test_[action]_[expected_result]
        - Use fixtures for test data
        - Use type hints
        - Verify one thing per test
        """
        email = sample_user_data["email"]
        
        # This would be your actual validation
        is_valid = "@" in email and "." in email.split("@")[1]
        
        assert is_valid is True
    
    def test_invalid_email_rejected(self) -> None:
        """Test that invalid emails are rejected."""
        email = "invalid-email"
        
        is_valid = "@" in email and "." in email.split("@")[1]
        
        assert is_valid is False
    
    @pytest.mark.parametrize("email,expected", [
        ("user@example.com", True),
        ("user.name@example.co.uk", True),
        ("user+tag@example.com", True),
        ("invalid", False),
        ("user@", False),
        ("@example.com", False),
    ])
    def test_email_validation_parametrized(
        self, email: str, expected: bool
    ) -> None:
        """
        Test multiple email formats with parametrization.
        
        **Pattern:** Use @pytest.mark.parametrize for multiple test cases
        - Reduces code duplication
        - Makes edge cases explicit
        - Each case is independent
        """
        is_valid = "@" in email and "." in email.split("@")[1]
        assert is_valid is expected


class TestUserService:
    """Group of tests for user service business logic."""
    
    def test_create_user_with_valid_data(
        self, sample_user_data: Dict[str, Any], mock_database: Mock
    ) -> None:
        """
        Test creating a user with valid data.
        
        **Pattern:** Arrange-Act-Assert (AAA)
        - Arrange: Set up test conditions
        - Act: Perform action
        - Assert: Verify results
        """
        # Arrange
        user_data = sample_user_data
        mock_database.add = Mock()
        mock_database.commit = Mock()
        
        # Act
        # Mock the create_user function behavior
        created_user = {**user_data, "id": 1}
        mock_database.add(created_user)
        mock_database.commit()
        
        # Assert
        assert mock_database.add.called
        assert mock_database.commit.called
    
    def test_send_welcome_email_on_user_creation(
        self, sample_user_data: Dict[str, Any], mock_email_service: Mock
    ) -> None:
        """
        Test that welcome email is sent when user is created.
        
        **Pattern:** Mock external dependencies
        - Use unittest.mock for I/O operations
        - Verify side effects with assert_called_with()
        """
        # Arrange
        email = sample_user_data["email"]
        
        # Act
        mock_email_service.send(
            to=email,
            subject="Welcome!",
            template="welcome"
        )
        
        # Assert
        mock_email_service.send.assert_called_once_with(
            to=email,
            subject="Welcome!",
            template="welcome"
        )
    
    def test_user_creation_fails_on_duplicate_email(
        self, sample_user_data: Dict[str, Any], mock_database: Mock
    ) -> None:
        """
        Test that duplicate email creation is prevented.
        
        **Pattern:** Test error scenarios
        - Use pytest.raises() for exceptions
        - Verify exception message
        - Ensure service enforces constraints
        """
        # Arrange
        email = sample_user_data["email"]
        mock_database.query.return_value.filter.return_value.first.return_value = {
            "email": email
        }
        
        # Act & Assert
        from builtins import ValueError
        with pytest.raises(ValueError, match="Email already exists"):
            # This would call your actual user creation logic
            # that checks for duplicates
            if mock_database.query.return_value.filter.return_value.first():
                raise ValueError("Email already exists")


class TestDataProcessing:
    """Group of tests for data processing logic."""
    
    def test_process_batch_with_multiple_items(self) -> None:
        """
        Test batch processing with multiple items.
        
        **Pattern:** Test with realistic data volumes
        """
        # Arrange
        items = [
            {"id": 1, "name": "Item 1"},
            {"id": 2, "name": "Item 2"},
            {"id": 3, "name": "Item 3"},
        ]
        
        # Act
        processed = [item for item in items if "name" in item]
        
        # Assert
        assert len(processed) == 3
        assert all("name" in item for item in processed)
    
    def test_process_empty_list(self) -> None:
        """
        Test edge case: empty input.
        
        **Pattern:** Always test edge cases
        """
        # Arrange
        items: List[Dict[str, Any]] = []
        
        # Act
        processed = [item for item in items if "name" in item]
        
        # Assert
        assert len(processed) == 0
    
    @pytest.mark.slow  # Mark long-running tests
    def test_process_large_dataset(self) -> None:
        """
        Test performance with large datasets.
        
        **Pattern:** Mark slow tests with @pytest.mark.slow
        Can be skipped in quick test runs: pytest -m "not slow"
        """
        # Arrange
        items = [{"id": i, "name": f"Item {i}"} for i in range(10000)]
        
        # Act
        processed = [item for item in items if "name" in item]
        
        # Assert
        assert len(processed) == 10000


# ============================================================================
# FIXTURES WITH SETUP/TEARDOWN (Using yield)
# ============================================================================

@pytest.fixture
def api_client():
    """
    Set up and tear down API client.
    
    **Pattern:** Use yield for setup/teardown
    - Code before yield: SETUP
    - Code after yield: TEARDOWN
    """
    # SETUP
    client = Mock()
    client.headers = {"Authorization": "Bearer token"}
    
    yield client
    
    # TEARDOWN
    client.close()


# ============================================================================
# PARAMETRIZED FIXTURES (Test with multiple configurations)
# ============================================================================

@pytest.fixture(params=["dev", "prod"])
def environment(request):
    """
    Parametrized fixture to test in multiple environments.
    
    **Pattern:** Parametrize fixtures to test multiple configs
    """
    return request.param


def test_api_endpoint_in_multiple_environments(environment: str) -> None:
    """
    Test API endpoint behavior in different environments.
    
    This test will run twice: once with environment="dev", once with "prod"
    """
    assert environment in ["dev", "prod"]


# ============================================================================
# MARKS FOR TEST ORGANIZATION
# ============================================================================

@pytest.mark.unit
def test_is_unit_test() -> None:
    """Mark this as a unit test."""
    assert True


@pytest.mark.integration
def test_is_integration_test() -> None:
    """Mark this as an integration test."""
    assert True


@pytest.mark.skip(reason="Not implemented yet")
def test_skipped_feature() -> None:
    """Tests can be skipped during development."""
    assert False


@pytest.mark.xfail(reason="Known bug, to be fixed in v2.0")
def test_expected_failure() -> None:
    """Test known to fail (but we expect it to be fixed)."""
    assert False


# ============================================================================
# CONTEXT MANAGERS FOR TEMPORARY MOCKING
# ============================================================================

def test_with_patch_decorator() -> None:
    """
    Test using @patch decorator for mocking.
    
    **Pattern:** Patch functions/modules that should be mocked
    """
    with patch("builtins.print") as mock_print:
        print("Hello, world!")
        mock_print.assert_called_once_with("Hello, world!")


if __name__ == "__main__":
    # Run tests: pytest tests/test_example.py -v
    # Run only unit tests: pytest tests/test_example.py -m "unit"
    # Run without slow tests: pytest tests/test_example.py -m "not slow"
    # Run with coverage: pytest tests/test_example.py --cov=src --cov-report=html
    pass
