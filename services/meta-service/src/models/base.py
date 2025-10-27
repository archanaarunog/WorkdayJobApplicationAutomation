"""
Base model configuration for Meta Portal.
"""

from src.config.database import Base

# Re-export Base for use in models
__all__ = ["Base"]