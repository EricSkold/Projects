from bs4 import BeautifulSoup
from requests import get
import re
import json

BASE_URL = "https://avgangstavla.vasttrafik.se/?source=vasttrafikse-stopareadetailspage&stopAreaGid="
TRAMNETWORK = "lab3/static/tramnetwork.json"

with open(TRAMNETWORK, "r", encoding="utf-8") as stop_data:
    stop_dict = json.load(stop_data)["stops"]

västtrafik_page = get("https://www.vasttrafik.se/reseplanering/hallplatslista/")
soup = BeautifulSoup(västtrafik_page.text, "lxml")
pattern = re.compile(r".*Zon A.*")
html_data = soup.find_all("a", text=pattern)

url_dict = {}


for link in html_data:
    url_dict[link.text.split(",")[0].strip()] = (
        BASE_URL + link.get("href").split("hallplatser/")[1][:-1]
    )


for stop in url_dict.copy():
    if stop not in stop_dict:
        url_dict.pop(stop)


with open("stop_url_dictionary.json", "w", encoding="utf-8") as data:
    json.dump(url_dict, data, ensure_ascii=False, indent=4)
