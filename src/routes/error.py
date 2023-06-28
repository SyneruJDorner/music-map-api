from fastapi import APIRouter, HTTPException, Request
from src.config import logger

error_router = APIRouter()

# This function is used to raise an error
# Parameters:
#   request: The request object from FastAPI router
#   status_code: The status code to raise
#   msg: The message to raise
# Returns:
#   HTTPException: The exception to raise
def http_error(status_code: int, msg: str):
    headers = { "accept": "application/json", "x-header-error": msg.replace("\n", ", ") }

    # Navigates to existing error handlers:
    #   401: Unauthorized
    #   403: Forbidden
    #   404: Not Found
    if status_code == 401:
        return exception_unauthorized(headers, msg)

    if status_code == 403:
        return exception_forbidden(headers, msg)

    if status_code == 404:
        return exception_not_found(headers, msg)
    
    # Otherwise, raise a generic error
    logger.error("Status code: " + str(status_code) + ", Message: " + str(msg))
    raise HTTPException(status_code=status_code, detail=msg, headers=headers)


# Error Handlers for 401, 403, 404
# These function are exposed to the API
@error_router.get('/401')
@error_router.get('/401/', include_in_schema=False)
def exception_unauthorized(headers:str = None, msg: str = ""):
    msg = "Unauthorized" if msg == "" else msg
    headers = { "accept": "application/json", "x-header-error": msg.replace("\n", ", ") } if headers is None else headers
    logger.error("Status code: " + str(401) + ", Message: " + str(msg))
    raise HTTPException(status_code=401, detail=msg, headers=headers)

@error_router.get('/403')
@error_router.get('/403/', include_in_schema=False)
def exception_forbidden(headers:str = None, msg: str = ""):
    msg = "Unauthorized" if msg == "" else msg
    headers = { "accept": "application/json", "x-header-error": msg.replace("\n", ", ") } if headers is None else headers
    logger.error("Status code: " + str(403) + ", Message: " + str(msg))
    raise HTTPException(status_code=403, detail=msg, headers=headers)

@error_router.get('/404')
@error_router.get('/404/', include_in_schema=False)
def exception_not_found(headers:str = None, msg: str = ""):
    msg = "Unauthorized" if msg == "" else msg
    headers = { "accept": "application/json", "x-header-error": msg.replace("\n", ", ") } if headers is None else headers
    logger.error("Status code: " + str(404) + ", Message: " + str(msg))
    raise HTTPException(status_code=404, detail=msg, headers=headers)
