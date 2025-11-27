import re

from unidecode import unidecode


def generate_slug(text: str) -> str:
    """
    Generate a URL-friendly slug from the given text.

    Args:
        text (str): The input text to convert into a slug.
    Returns:
        str: A URL-friendly slug.
    """
    # Normalize the text to remove accents
    text = unidecode(text)
    # Convert to lowercase
    text = text.lower()
    # Replace spaces and underscores with hyphens
    text = re.sub(r"[\s_]+", "-", text)
    # Remove all non-alphanumeric characters except hyphens
    text = re.sub(r"[^a-z0-9-]", "", text)
    # Remove leading and trailing hyphens
    text = text.strip("-")
    # Replace multiple hyphens with a single hyphen
    text = re.sub(r"-+", "-", text)
    return text
