import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Web de la que vamos a extraer titulares
URL = "https://www.xataka.com/tag/ciberseguridad"

# Hacemos la petición
response = requests.get(URL)
soup = BeautifulSoup(response.text, "html.parser")

# Lista para los items del RSS
items = []

# Extraemos los primeros 10 artículos
for article in soup.find_all("article")[:10]:
    a_tag = article.find("a")
    if a_tag:
        title = a_tag.get_text(strip=True)
        href = a_tag.get("href")
        if title and href:
            items.append(f"""
            <item>
                <title>{title}</title>
                <link>{href}</link>
                <pubDate>{datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>
                <guid>{href}</guid>
            </item>
            """)

# Creamos el contenido completo del RSS
rss_content = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
    <title>RSS Ciberseguridad Xataka</title>
    <link>{URL}</link>
    <description>Titulares automáticos de Xataka sobre ciberseguridad</description>
    {''.join(items)}
</channel>
</rss>
"""

# Guardamos en rss.xml
with open("../../rss.xml", "w", encoding="utf-8") as f:
    f.write(rss_content)

print("rss.xml generado correctamente")
