from fastapi import APIRouter, Depends, HTTPException
from typing import Optional

from scripts.models.image_model import ImageBuildRequest, ImageRemoveRequest, ImageGithubBuildRequest
from scripts.constants.api_endpoints import Endpoints
from scripts.handlers.image_handler import (
    build_image,
    build_image_from_github,
    remove_image,
    list_images,
    pull_image,
    push_image,
    dockerhub_login
)
from scripts.logging.logger import logger
from scripts.utils.jwt_utils import get_current_user_from_token
from scripts.models.jwt_model import TokenData
from scripts.constants.api_endpoints import Endpoints
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl=Endpoints.AUTH_LOGIN)

def get_current_user(token: str = Depends(oauth2_scheme)):
    user = get_current_user_from_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return user

image_router = APIRouter()

@image_router.post(Endpoints.IMAGE_BUILD_ADVANCED)
def build_image_service(data: ImageBuildRequest, current_user: TokenData = Depends(get_current_user)):
    try:
        logger.info(f"User '{current_user.username}' is attempting to build an image with tag: {data.tag}")
        return build_image(data, current_user.access_token)
    except Exception as e:
        logger.error(f"Error building image with tag {data.tag}: {e}")
        raise HTTPException(status_code=500, detail="Error building image")

@image_router.post(Endpoints.IMAGE_BUILD_FROM_GITHUB)
def build_image_from_github_service(data: ImageGithubBuildRequest, current_user: TokenData = Depends(get_current_user)):
    try:
        logger.info(f"User '{current_user.username}' is attempting to build an image from GitHub repository: {data.github_url}")
        return build_image_from_github(data, current_user.access_token)
    except Exception as e:
        logger.error(f"Error building image from GitHub repository {data.github_url}: {e}")
        raise HTTPException(status_code=500, detail="Error building image from GitHub repository")

@image_router.get(Endpoints.IMAGE_LIST)
def list_images_service(name: str = None, all: bool = False, filters: Optional[dict] = None, current_user: TokenData = Depends(get_current_user)):
    try:
        logger.info(f"User '{current_user.username}' is listing Docker images with filters: {filters}")
        return list_images(name, all, filters, current_user.access_token)
    except Exception as e:
        logger.error(f"Error listing Docker images with filters {filters}: {e}")
        raise HTTPException(status_code=500, detail="Error listing Docker images")

@image_router.post(Endpoints.DOCKER_REGISTRY_LOGIN)
def dockerhub_login_service(username: str, password: str, current_user: TokenData = Depends(get_current_user)):
    try:
        logger.info(f"User '{current_user.username}' is attempting to login to DockerHub with username: {username}")
        return dockerhub_login(username, password, current_user.access_token)
    except Exception as e:
        logger.error(f"Error logging into DockerHub with username {username}: {e}")
        raise HTTPException(status_code=500, detail="Error logging into DockerHub")

@image_router.post(Endpoints.IMAGE_PUSH)
def push_image_service(local_tag: str, remote_repo: str, current_user: TokenData = Depends(get_current_user)):
    try:
        logger.info(f"User '{current_user.username}' is attempting to push image with tag: {local_tag} to remote repository: {remote_repo}")
        return push_image(local_tag, remote_repo, current_user.access_token)
    except Exception as e:
        logger.error(f"Error pushing image with tag {local_tag} to repository {remote_repo}: {e}")
        raise HTTPException(status_code=500, detail="Error pushing image")

@image_router.post(Endpoints.IMAGE_PULL)
def pull_image_service(repository: str, local_tag: str = None, current_user: TokenData = Depends(get_current_user)):
    try:
        logger.info(f"User '{current_user.username}' is attempting to pull image from repository: {repository}")
        return pull_image(repository, local_tag, current_user.access_token)
    except Exception as e:
        logger.error(f"Error pulling image from repository {repository}: {e}")
        raise HTTPException(status_code=500, detail="Error pulling image")

@image_router.delete(Endpoints.IMAGE_DELETE)
def remove_image_service(image_name: str, params: ImageRemoveRequest, current_user: TokenData = Depends(get_current_user)):
    try:
        logger.info(f"User '{current_user.username}' is attempting to remove image with name: {image_name}")
        return remove_image(image_name, params, current_user.access_token)
    except Exception as e:
        logger.error(f"Error removing image with name {image_name}: {e}")
        raise HTTPException(status_code=500, detail="Error removing image")
