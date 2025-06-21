# core/services/news_service.py
import requests
from bs4 import BeautifulSoup
import time

async def fetch_latest_news():
    news_sources = [
        ("Deutschlandfunk", "https://www.deutschlandfunk.de/nachrichten"),
        ("tagesschau", "https://www.tagesschau.de"),
        ("WELT", "https://www.welt.de"),
        ("n-tv", "https://www.n-tv.de")
    ]
    headlines = []
    for source, url in news_sources[:3]:
        try:
            response = requests.get(url, timeout=5)
            soup = BeautifulSoup(response.text, 'html.parser')
            if "tagesschau" in url:
                headlines += [h.text for h in soup.select(".teaser__headline")]
            elif "welt" in url:
                headlines += [h.text for h in soup.select(".most-read__item")]
            else:
                headlines += [h.text for h in soup.select(".headline")]
        except Exception as e:
            continue
    return headlines[:5]

async def send_hourly_news(bot):
    headlines = await fetch_latest_news()
    if headlines:
        message = (
                f"Aktuelle Nachrichten ({time.strftime('%d.%m.%Y %H:%M')}):\n\n"
                + "\n".join(headlines)
        )
        for user_id in default_model_dict.keys():
            try:
                await bot.send_message(user_id, message)
            except Exception as e:
                print(f"Fehler beim Senden an {user_id}: {e}")