
import sys
import os

# Add the parent directory of 'app' to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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


def test_validate_otp_success(otp_service):
    """
    Test the validate_otp method for a successful OTP verification.
    """
    # Arrange
    customer_email = "test@example.com"
    otp_code = "123456"
    otp_entry = MagicMock()
    otp_entry.expiry_time = datetime.now(timezone.utc) + timedelta(minutes=5)
    otp_entry.is_used = False
    otp_entry.order_id = 1

    otp_service.otp_repo.get_otp.return_value = otp_entry
    otp_service.order_repo.close_order.return_value = {"message": "Order closed successfully"}

    # Act
    result, status_code = otp_service.validate_otp(customer_email, otp_code)

    # Assert
    otp_service.otp_repo.get_otp.assert_called_once_with(customer_email, otp_code)
    otp_service.otp_repo.mark_otp_used.assert_called_once_with(otp_entry)
    otp_service.order_repo.close_order.assert_called_once_with(1)
    assert result == {"message": "OTP validated successfully"}
    assert status_code == 200




def test_validate_otp_expired(otp_service):
    """
    Test the validate_otp method for an expired OTP.
    """
    # Arrange
    customer_email = "test@example.com"
    otp_code = "123456"
    otp_entry = MagicMock()
    otp_entry.expiry_time = datetime.now(timezone.utc) - timedelta(minutes=5)
    otp_entry.is_used = False

    otp_service.otp_repo.get_otp.return_value = otp_entry

    # Act
    result, status_code = otp_service.validate_otp(customer_email, otp_code)

    # Assert
    otp_service.otp_repo.get_otp.assert_called_once_with(customer_email, otp_code)
    assert result == {"error": "OTP expired"}
    assert status_code == 400


def test_validate_otp_already_used(otp_service):
    """
    Test the validate_otp method for an OTP that has already been used.
    """
    # Arrange
    customer_email = "test@example.com"
    otp_code = "123456"
    otp_entry = MagicMock()
    otp_entry.expiry_time = datetime.now(timezone.utc) + timedelta(minutes=5)
    otp_entry.is_used = True

    otp_service.otp_repo.get_otp.return_value = otp_entry

    # Act
    result, status_code = otp_service.validate_otp(customer_email, otp_code)

    # Assert
    otp_service.otp_repo.get_otp.assert_called_once_with(customer_email, otp_code)
    assert result == {"error": "OTP has already been used"}
    assert status_code == 400


def test_validate_otp_invalid(otp_service):
    """
    Test the validate_otp method for an invalid OTP.
    """
    # Arrange
    customer_email = "test@example.com"
    otp_code = "123456"
    otp_service.otp_repo.get_otp.return_value = None

    # Act
    result, status_code = otp_service.validate_otp(customer_email, otp_code)

    # Assert
    otp_service.otp_repo.get_otp.assert_called_once_with(customer_email, otp_code)
    assert result == {"error": "Invalid OTP"}
    assert status_code == 400

