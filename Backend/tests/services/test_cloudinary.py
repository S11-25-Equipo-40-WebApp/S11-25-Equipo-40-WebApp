"""Tests for Cloudinary service."""

from unittest.mock import Mock, patch

import pytest
from fastapi import HTTPException, UploadFile, status

from app.services.cloudinary import CloudinaryService


class TestUploadImages:
    """Tests for upload_images method."""

    def test_upload_images_empty_list(self):
        """Test that empty list returns empty list."""
        result = CloudinaryService.upload_images([])
        assert result == []

    def test_upload_images_invalid_content_type(self):
        """Test that non-image file raises HTTPException."""
        mock_file = Mock(spec=UploadFile)
        mock_file.filename = "document.pdf"
        mock_file.content_type = "application/pdf"

        with pytest.raises(HTTPException) as exc_info:
            CloudinaryService.upload_images([mock_file])

        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert "not a valid image" in str(exc_info.value.detail)

    def test_upload_images_none_content_type(self):
        """Test that file with None content_type raises HTTPException."""
        mock_file = Mock(spec=UploadFile)
        mock_file.filename = "unknown.bin"
        mock_file.content_type = None

        with pytest.raises(HTTPException) as exc_info:
            CloudinaryService.upload_images([mock_file])

        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST

    @patch("app.services.cloudinary.cloudinary.uploader.upload")
    def test_upload_images_success_single_file(self, mock_upload):
        """Test successful upload of single image."""
        mock_file = Mock(spec=UploadFile)
        mock_file.filename = "test.jpg"
        mock_file.content_type = "image/jpeg"
        mock_file.file = Mock()

        mock_upload.return_value = {
            "secure_url": "https://res.cloudinary.com/test/image/upload/v1234/testimonials/test.jpg"
        }

        result = CloudinaryService.upload_images([mock_file])

        assert len(result) == 1
        assert (
            result[0] == "https://res.cloudinary.com/test/image/upload/v1234/testimonials/test.jpg"
        )
        mock_upload.assert_called_once_with(
            mock_file.file,
            folder="testimonials",
            resource_type="image",
            allowed_formats=["jpg", "jpeg", "png", "gif", "webp"],
        )

    @patch("app.services.cloudinary.cloudinary.uploader.upload")
    def test_upload_images_success_multiple_files(self, mock_upload):
        """Test successful upload of multiple images."""
        mock_file1 = Mock(spec=UploadFile)
        mock_file1.filename = "test1.jpg"
        mock_file1.content_type = "image/jpeg"
        mock_file1.file = Mock()

        mock_file2 = Mock(spec=UploadFile)
        mock_file2.filename = "test2.png"
        mock_file2.content_type = "image/png"
        mock_file2.file = Mock()

        mock_upload.side_effect = [
            {"secure_url": "https://res.cloudinary.com/test/image1.jpg"},
            {"secure_url": "https://res.cloudinary.com/test/image2.png"},
        ]

        result = CloudinaryService.upload_images([mock_file1, mock_file2])

        assert len(result) == 2
        assert result[0] == "https://res.cloudinary.com/test/image1.jpg"
        assert result[1] == "https://res.cloudinary.com/test/image2.png"
        assert mock_upload.call_count == 2

    @patch("app.services.cloudinary.cloudinary.uploader.upload")
    def test_upload_images_with_custom_folder(self, mock_upload):
        """Test upload with custom folder parameter."""
        mock_file = Mock(spec=UploadFile)
        mock_file.filename = "test.jpg"
        mock_file.content_type = "image/jpeg"
        mock_file.file = Mock()

        mock_upload.return_value = {"secure_url": "https://res.cloudinary.com/test/custom/test.jpg"}

        result = CloudinaryService.upload_images([mock_file], folder="custom")

        assert len(result) == 1
        mock_upload.assert_called_once_with(
            mock_file.file,
            folder="custom",
            resource_type="image",
            allowed_formats=["jpg", "jpeg", "png", "gif", "webp"],
        )

    @patch("app.services.cloudinary.cloudinary.uploader.upload")
    def test_upload_images_cloudinary_failure(self, mock_upload):
        """Test that Cloudinary upload failure raises HTTPException."""
        mock_file = Mock(spec=UploadFile)
        mock_file.filename = "test.jpg"
        mock_file.content_type = "image/jpeg"
        mock_file.file = Mock()

        mock_upload.side_effect = Exception("Cloudinary error")

        with pytest.raises(HTTPException) as exc_info:
            CloudinaryService.upload_images([mock_file])

        assert exc_info.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "Failed to upload image" in str(exc_info.value.detail)
        assert "Cloudinary error" in str(exc_info.value.detail)

    @patch("app.services.cloudinary.cloudinary.uploader.upload")
    def test_upload_images_partial_failure(self, mock_upload):
        """Test that failure on second file raises exception."""
        mock_file1 = Mock(spec=UploadFile)
        mock_file1.filename = "test1.jpg"
        mock_file1.content_type = "image/jpeg"
        mock_file1.file = Mock()

        mock_file2 = Mock(spec=UploadFile)
        mock_file2.filename = "test2.jpg"
        mock_file2.content_type = "image/jpeg"
        mock_file2.file = Mock()

        # First upload succeeds, second fails
        mock_upload.side_effect = [
            {"secure_url": "https://res.cloudinary.com/test/image1.jpg"},
            Exception("Upload failed"),
        ]

        with pytest.raises(HTTPException) as exc_info:
            CloudinaryService.upload_images([mock_file1, mock_file2])

        assert exc_info.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "test2.jpg" in str(exc_info.value.detail)

    @patch("app.services.cloudinary.cloudinary.uploader.upload")
    def test_upload_images_supports_various_image_types(self, mock_upload):
        """Test that various image content types are accepted."""
        image_types = [
            ("test.jpg", "image/jpeg"),
            ("test.png", "image/png"),
            ("test.gif", "image/gif"),
            ("test.webp", "image/webp"),
        ]

        for filename, content_type in image_types:
            mock_file = Mock(spec=UploadFile)
            mock_file.filename = filename
            mock_file.content_type = content_type
            mock_file.file = Mock()

            mock_upload.return_value = {"secure_url": f"https://res.cloudinary.com/test/{filename}"}

            result = CloudinaryService.upload_images([mock_file])
            assert len(result) == 1
            assert filename in result[0]

    @patch("app.services.cloudinary.cloudinary.uploader.upload")
    def test_upload_images_stops_on_invalid_file(self, mock_upload):
        """Test that invalid file stops the upload process."""
        mock_file1 = Mock(spec=UploadFile)
        mock_file1.filename = "test.jpg"
        mock_file1.content_type = "image/jpeg"
        mock_file1.file = Mock()

        mock_file2 = Mock(spec=UploadFile)
        mock_file2.filename = "document.pdf"
        mock_file2.content_type = "application/pdf"

        # First file succeeds
        mock_upload.return_value = {"secure_url": "https://res.cloudinary.com/test/image1.jpg"}

        with pytest.raises(HTTPException) as exc_info:
            CloudinaryService.upload_images([mock_file1, mock_file2])

        # Verify that validation failed on second file
        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert "document.pdf" in str(exc_info.value.detail)
