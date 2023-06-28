import re, requests
from bs4 import BeautifulSoup
from fastapi import Request, APIRouter, Form, Query, Depends
from fastapi.responses import JSONResponse
from src.routes.error import http_error
from src.config import network
from src.helper.musicmap_helper import find_similar_music_helper


api_router = APIRouter()
limiter = network.limiter


@api_router.get('/api/v1/connection')
@api_router.get('/api/v1/connection/', include_in_schema=False)
@api_router.get('/api/v2/connection')
@api_router.get('/api/v2/connection/', include_in_schema=False)
@limiter.limit("2/second")
async def musicmap_connection(request: Request):
    """
    Get the status of the grid connection.

    Returns:
        A dictionary with the status of the grid connection.
    """

    content = { "status": "online" }
    return JSONResponse(content=content, status_code=200)


@api_router.get('/api/v1/find-similar-music')
@api_router.get('/api/v1/find-similar-music/', include_in_schema=False)
@limiter.limit("2/second")
async def find_similar_music_v1(request: Request, band: str = Query(None, description="Band you want to find similar music for")):
    content = await find_similar_music_helper(band)
    if not content or type(content) != list:
        raise content
    return JSONResponse(content=content, status_code=200)


@api_router.post('/api/v2/find-similar-music')
@api_router.post('/api/v2/find-similar-music/', include_in_schema=False)
@limiter.limit("2/second")
async def find_similar_music_v2(request: Request, band: str = Form(None, description="Band you want to find similar music for")):
    content = await find_similar_music_helper(band)
    if not content or type(content) != list:
        raise content
    
    return JSONResponse(content=content, status_code=200)
