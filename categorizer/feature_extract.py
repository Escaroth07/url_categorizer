import aiohttp
from bs4 import BeautifulSoup

async def fetch_content(url):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, timeout=5) as resp:
                if resp.status == 200:
                    return await resp.text()
        except Exception:
            return ""

def extract_text_features(html):
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(separator=" ")
    return {"text": text[:5000]}  # Limit for simplicity
