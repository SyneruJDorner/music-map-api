import re, requests
from bs4 import BeautifulSoup
from src.routes.error import http_error

async def find_similar_music_helper(band: str):
    if not band or band.strip() == "":
        http_error(400, "Field 'band' is missing")

    url = f"https://www.music-map.com/{band}"
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Host": "www.music-map.com",
        "Referer": "https://www.music-map.com/",
        "Sec-Ch-Ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Sec-Gpc": "1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        http_error(400, "Failed to find similar music")

    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the <div id="gnodMap"> element
    div_element = soup.find('div', {'id': 'gnodMap'})

    # Extract the content within the <div id="gnodMap"> element
    content_str = div_element.get_text()

    # Split the content into an array
    content = re.split(r'\n\s*', content_str)

    # Remove empty strings ("") and the band name
    content = [item for item in content if item.lower().strip() != "" and item.lower().strip() != band.lower().strip()]

    return content