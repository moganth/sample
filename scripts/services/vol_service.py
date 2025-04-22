from fastapi import APIRouter, status, Depends, HTTPException
from scripts.constants.api_endpoints import Endpoints
from scripts.handlers.vol_handler import (
    create_volume_with_params,
    remove_volume_with_params
)
from scripts.models.volume_model import VolumeCreateRequest, VolumeRemoveRequest
from scripts.logging.logger import logger
from scripts.utils.jwt_utils import get_current_user_from_token
from scripts.models.jwt_model import TokenData
from fastapi.security import OAuth2PasswordBearer
from scripts.constants.api_endpoints import Endpoints

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=Endpoints.AUTH_LOGIN)

volume_router = APIRouter()

def get_current_user(token: str = Depends(oauth2_scheme)):
    user = get_current_user_from_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return user

@volume_router.post(Endpoints.VOLUME_CREATE, status_code=status.HTTP_201_CREATED)
def create_volume_view(data: VolumeCreateRequest, current_user: TokenData = Depends(get_current_user)):
    try:
        logger.info(f"Authenticated user '{current_user.username}' is requesting to create a volume with data: {data}")
        return create_volume_with_params(data, current_user)
    except Exception as e:
        logger.error(f"Error creating volume: {e}")
        raise HTTPException(status_code=500, detail="Error creating volume")

@volume_router.delete(Endpoints.VOLUME_DELETE, status_code=status.HTTP_200_OK)
def remove_volume_view(name: str, params: VolumeRemoveRequest, current_user: TokenData = Depends(get_current_user)):
    try:
        logger.info(f"Authenticated user '{current_user.username}' is requesting to remove volume '{name}' with parameters: {params}")
        return remove_volume_with_params(name, params, current_user)
    except Exception as e:
        logger.error(f"Error removing volume '{name}': {e}")
        raise HTTPException(status_code=500, detail="Error removing volume")
