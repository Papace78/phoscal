class PhoscalException(Exception):
    """Base exception for Phoscal module."""


class FileExtensionNotFound(PhoscalException):
    """Raise when extension is not found."""
