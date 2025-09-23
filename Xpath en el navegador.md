## 🔹 Qué es $x()

- Función integrada en la consola del navegador (DevTools)
    
- Evalúa una expresión XPath y devuelve los elementos que coinciden
    
- Retorna un array de nodos HTML
    

---

## 🔹 Sintaxis

```
$x("expresion_xpath")
```

- `expresion_xpath`: tu XPath como string
    

---

## 🔹 Ejemplos prácticos

- Seleccionar todos los div:
    

```
$x("//div")
```

- Seleccionar un enlace con texto exacto "Contacto":
    

```
$x("//a[text()='Contacto']")
```

- Seleccionar el primer li dentro de un ul:
    

```
$x("//ul/li[1]")
```

---

## 🔹 Acceder a resultados

```
let enlaces = $x("//a");
console.log(enlaces[0]);       // primer enlace encontrado
console.log(enlaces[0].textContent); // texto del enlace
```

---

## 🔹 Consejos y tips

- Para obtener solo el primer nodo:
    

```
$x("//div[@class='menu']")[0]
```

- Muy útil para pruebas rápidas, depuración o scraping en el navegador