import json, urllib.request, urllib.parse
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime

TOPICS = {
    "Überfälle": "Überfall OR Raubüberfall",
    "Unfälle": "Unfall OR Verkehrsunfall",
    "Einbrüche": "Einbruch OR Diebstahl",
    "Polizei": "Polizeieinsatz OR Festnahme",
    "Feuer": "Brand OR Feuerwehreinsatz",
}

items, seen = [], set()
for topic, q in TOPICS.items():
    url = ("https://news.google.com/rss/search?q="
           + urllib.parse.quote(f"({q}) when:2d")
           + "&hl=de&gl=DE&ceid=DE:de")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        xml = urllib.request.urlopen(req, timeout=30).read()
        for it in ET.fromstring(xml).iter("item"):
            link = it.findtext("link", "")
            if not link or link in seen:
                continue
            seen.add(link)
            items.append({
                "topic": topic,
                "title": it.findtext("title", ""),
                "link": link,
                "source": it.findtext("source", ""),
                "date": parsedate_to_datetime(it.findtext("pubDate")).isoformat(),
            })
    except Exception as e:
        print("Fehler bei", topic, e)

items.sort(key=lambda x: x["date"], reverse=True)
json.dump({"items": items[:150]}, open("news.json", "w", encoding="utf-8"), ensure_ascii=False)
print(len(items), "Meldungen")
