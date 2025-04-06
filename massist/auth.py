import os

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from config import config
from massist.logger import Logger

# Initialize the security scheme
security = HTTPBearer(auto_error=False)
logger = Logger().get_logger(__name__)

# Get API key from config
MAI_LLMX_API_KEY = config.MAI_LLMX_API_KEY

if not MAI_LLMX_API_KEY:
    logger.warning(
        "MAI_LLMX_API_KEY environment variable is not set. API will be accessible without authentication!")


async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Verify the bearer token against the configured API key
    """
    # If no API key is configured, skip authentication
    if not MAI_LLMX_API_KEY:
        return True

    # If credentials weren't provided but API key is set, block access
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Bearer token missing.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if credentials.scheme != "Bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication scheme. Bearer token required.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if credentials.credentials != MAI_LLMX_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return True
