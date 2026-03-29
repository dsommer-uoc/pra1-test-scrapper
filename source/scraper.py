import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# URL base del sitio de práctica
BASE_URL = "https://quotes.toscrape.com"

# Cabecera que identifica nuestro scraper
HEADERS = {
    "User-Agent": "Scraper-Practica-UOC/1.0 (uso academico)"
}


def extraer_frases(url):
    """
    Descarga una página y extrae todas las frases que contiene.
    Devuelve una lista de diccionarios y la URL de la siguiente página.
    """
    respuesta = requests.get(url, headers=HEADERS)

    if respuesta.status_code != 200:
        print(f"Error al acceder a {url}: {respuesta.status_code}")
        return [], None

    soup = BeautifulSoup(respuesta.text, "html.parser")

    frases = []
    for bloque in soup.find_all("div", class_="quote"):
        texto = bloque.find("span", class_="text").get_text()
        autor  = bloque.find("small", class_="author").get_text()
        tags   = [t.get_text() for t in bloque.find_all("a", class_="tag")]

        frases.append({
            "texto": texto,
            "autor": autor,
            "tags": ", ".join(tags)
        })

    # Buscar el enlace a la siguiente página
    siguiente = soup.find("li", class_="next")
    if siguiente:
        url_siguiente = BASE_URL + siguiente.find("a")["href"]
    else:
        url_siguiente = None

    return frases, url_siguiente


def main():
    """
    Navega por todas las páginas y guarda el dataset en CSV.
    """
    todas_las_frases = []
    url_actual = BASE_URL + "/page/1/"
    pagina = 1

    while url_actual:
        print(f"Scrapeando página {pagina}...")
        frases, url_siguiente = extraer_frases(url_actual)
        todas_las_frases.extend(frases)

        url_actual = url_siguiente
        pagina += 1
        time.sleep(1)  # pausa entre peticiones - scraping responsable

    # Guardar como CSV
    df = pd.DataFrame(todas_las_frases)
    df.to_csv("dataset/quotes.csv", index=False, encoding="utf-8-sig")
    print(f"\nListo. Dataset guardado con {len(df)} frases.")


if __name__ == "__main__":
    main()