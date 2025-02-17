import requests
from bs4 import BeautifulSoup

def Scraper(url):
    headers = {"User-Agent": "Mozilla/5.0", "Referer": "https://google.com", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    title = soup.find("h1") or soup.find("title") or soup.find("div", class_="header")
    
    if title:
        title = title.text
    else:
        title = "Not Available"

    og_image = soup.find("meta", property="og:image")

    if og_image and og_image.get("content"):
        thumbnail_url = og_image["content"]
    else:
        thumbnail_url = "No thumbnail found"

    paragraphs = soup.find_all("p") or soup.find("text") or soup.find("div", class_="")
    article_text = []
    
    if paragraphs:
        for p in paragraphs:
            article_text.append(p.text)
        article_text = " ".join(article_text)
    else: 
        article_text = "Not Available"

    return title, thumbnail_url, article_text



