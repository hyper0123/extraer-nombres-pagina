import requests
from bs4 import BeautifulSoup

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
                titulo = celdas[1].get_text(strip=True)
                if num.isdigit():
                    episodios.append((int(num), titulo))

    episodios.sort(key=lambda x: x[0])
    return episodios

if __name__ == "__main__":
    eps = extraer_episodios_bleach()
    for num, titulo in eps:
        print(f"{num:03d} - {titulo}")
