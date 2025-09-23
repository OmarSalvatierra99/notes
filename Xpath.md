## 🔹 Definición de XPath

- XPath (XML Path Language) → lenguaje para localizar elementos dentro de documentos XML o HTML
    
- Se usa en automatización, web scraping, pruebas y navegación de DOM
    

---

## 🔹 Sintaxis básica

- `/` → selecciona desde la raíz
    
- `//` → selecciona en cualquier nivel del documento
    
- `.` → nodo actual
    
- `..` → nodo padre
    
- `@` → atributo del nodo
    

---

## 🔹 Ejemplos de selección

```
/html/body/div             → selecciona el div dentro del body desde la raíz
//div                      → selecciona todos los div en el documento
//div[@id='principal']     → div con atributo id='principal'
//a[@href]                → todos los enlaces con href
//input[@type='text']     → todos los inputs de tipo texto
```

---

## 🔹 Selección por posición

```
(//div)[1]                 → primer div encontrado
(//li)[last()]             → último li encontrado
(//tr)[position()<3]       → los primeros 2 tr
```

---

## 🔹 Funciones útiles

- `text()` → selecciona el contenido de texto del nodo
    
- `contains(@atributo, 'valor')` → filtra nodos que contienen cierto valor en atributo
    
- `starts-with(@atributo, 'valor')` → nodos cuyo atributo empieza con cierto valor
    
- `normalize-space()` → elimina espacios extra en texto
    

---

## 🔹 Ejemplos combinados

```
//div[contains(@class, 'menu')]          → div con clase que contiene 'menu'
//a[text()='Contacto']                    → enlace con texto exacto 'Contacto'
//ul/li[3]/a                              → enlace dentro del tercer li de una ul
```

---

## 🔹 Tips rápidos

- Siempre usar `//` si no estás seguro de la posición exacta
    
- Combinar funciones para filtrar nodos de manera precisa
    
- Probar expresiones XPath en la consola del navegador para depuración
- [Xpath cheatsheet](https://devhints.io/xpath)
- [[Xpath en el navegador]]