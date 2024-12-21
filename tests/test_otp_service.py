import pytest
from unittest.mock import MagicMock
from datetime import datetime, timedelta, timezone
from app.Services.otp_service import OTPService


@pytest.fixture(scope="function")
def otp_service():
    """
    Fixture to initialize the OTPService with mocked notifier and repositories.
    """
    notifier = MagicMock()
    otp_service = OTPService(notifier)
    otp_service.otp_repo = MagicMock()
    otp_service.order_repo = MagicMock()
    return otp_service


def test_verify_otp_success(otp_service):
    """
    Test the verify_otp method for a successful OTP verification.
    """
    # Arrange
    customer_email = "test@example.com"
    otp_code = "123456"
    otp_entry = MagicMock()
    otp_entry.expiry_time = datetime.now(timezone.utc) + timedelta(minutes=5)
    otp_entry.is_used = False

    otp_service.otp_repo.get_otp.return_value = otp_entry

    # Act
    result = otp_service.verify_otp(customer_email, otp_code)

    # Assert
    otp_service.otp_repo.get_otp.assert_called_once_with(customer_email, otp_code)
    otp_service.otp_repo.mark_otp_used.assert_called_once_with(otp_entry)
    assert result == {"message": "OTP verified successfully"}


def test_verify_otp_expired(otp_service):
    """
    Test the verify_otp method for an expired OTP.
    """
    # Arrange
    customer_email = "test@example.com"
    otp_code = "123456"
    otp_entry = MagicMock()
    otp_entry.expiry_time = datetime.now(timezone.utc) - timedelta(minutes=5)
    otp_entry.is_used = False

    otp_service.otp_repo.get_otp.return_value = otp_entry

    # Act
    result = otp_service.verify_otp(customer_email, otp_code)

    # Assert
    otp_service.otp_repo.get_otp.assert_called_once_with(customer_email, otp_code)
    assert result == {"error": "OTP has expired"}


def test_verify_otp_already_used(otp_service):
    """
    Test the verify_otp method for an OTP that has already been used.
    """
    # Arrange
    customer_email = "test@example.com"
    otp_code = "123456"
    otp_entry = MagicMock()
    otp_entry.expiry_time = datetime.now(timezone.utc) + timedelta(minutes=5)
    otp_entry.is_used = True

    otp_service.otp_repo.get_otp.return_value = otp_entry

    # Act
    result = otp_service.verify_otp(customer_email, otp_code)

    # Assert
    otp_service.otp_repo.get_otp.assert_called_once_with(customer_email, otp_code)
    assert result == {"error": "OTP has already been used"}


def test_verify_otp_invalid(otp_service):
    """
    Test the verify_otp method for an invalid OTP.
    """
    # Arrange
    customer_email = "test@example.com"
    otp_code = "123456"
    otp_service.otp_repo.get_otp.return_value = None

    # Act
    result = otp_service.verify_otp(customer_email, otp_code)

    # Assert
    otp_service.otp_repo.get_otp.assert_called_once_with(customer_email, otp_code)
    assert result == {"error": "Invalid OTP"}
