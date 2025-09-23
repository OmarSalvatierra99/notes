![[guiafinal.png]]

##  🔷 Ejemplos

### Extraer los idiomas de Wikipedia

```python
import requests
from lxml import html

# URL de Wikipedia
url = "https://www.wikipedia.org/"

# Encabezados HTTP para simular un navegador
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# Petición HTTP
response = requests.get(url, headers=headers)

# Parsear el HTML
tree = html.fromstring(response.text)

# Extraer todos los idiomas usando XPath
idiomas = tree.xpath("//div[contains(@class,'central-featured-lang')]/a/strong/text()")

# Mostrar resultados
for idioma in idiomas:
    print(idioma)
```