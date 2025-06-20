import requests
from bs4 import BeautifulSoup
import re

def extraer_episodios_bleach():
    url = "https://bleach.fandom.com/es/wiki/Lista_de_Episodios"
    resp = requests.get(url)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    tablas = soup.find_all("table", class_="wikitable")

    episodios = []
    for tabla in tablas:
        for fila in tabla.find_all("tr")[1:]:
            celdas = fila.find_all(["th", "td"])
            if len(celdas) >= 2:
                num = celdas[0].get_text(strip=True)
                raw_title = celdas[1].get_text(strip=True)
                if num.isdigit():
                    # Extraer sólo el texto entre la primera pareja de « »
                    m = re.search(r'«([^»]+)»', raw_title)
                    title_es = m.group(1) if m else raw_title
                    episodios.append((int(num), title_es))

    episodios.sort(key=lambda x: x[0])
    return episodios

if __name__ == "__main__":
    eps = extraer_episodios_bleach()
    for num, titulo in eps:
        print(f"{num:02d} {titulo}")
