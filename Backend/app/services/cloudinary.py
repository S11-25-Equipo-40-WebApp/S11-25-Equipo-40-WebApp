import cloudinary
import cloudinary.uploader
from fastapi import HTTPException, UploadFile, status

from app.core.config import settings

# Configure Cloudinary
cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
)


class CloudinaryService:
    @staticmethod
    def upload_images(files: list[UploadFile], folder: str = "testimonials") -> list[str]:
        """
        Upload multiple images to Cloudinary.

        Args:
            files: List of UploadFile objects to upload
            folder: Cloudinary folder to store the images

        Returns:
            List of secure URLs of uploaded images

        Raises:
            HTTPException: If upload fails or file type is invalid
        """
        if not files:
            return []

        uploaded_urls = []

        for file in files:
            # Validate file type
            if not file.content_type or not file.content_type.startswith("image/"):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"File {file.filename} is not a valid image",
                )

            try:
                # Upload to Cloudinary
                result = cloudinary.uploader.upload(
                    file.file,
                    folder=folder,
                    resource_type="image",
                    allowed_formats=["jpg", "jpeg", "png", "gif", "webp"],
                )
                uploaded_urls.append(result["secure_url"])

            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Failed to upload image {file.filename}: {str(e)}",
                ) from e

        return uploaded_urls
