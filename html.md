## 🔹 Estructura básica de un HTML

```
<!DOCTYPE html>         → define el tipo de documento
<html lang="es">        → etiqueta raíz con idioma
<head>                  → metadatos, título, links a CSS/JS
  <meta charset="UTF-8"> → codificación de caracteres
  <title>Título de la página</title> → título en la pestaña
</head>
<body>                  → contenido visible de la página
  <!-- Aquí va el contenido -->
</body>
</html>
```

---

## 🔹 Encabezados

```
<h1>Encabezado 1</h1>   → el más importante
<h2>Encabezado 2</h2>   → subencabezado
<h3>Encabezado 3</h3>   → sub-subencabezado
...
<h6>Encabezado 6</h6>
```

---

## 🔹 Párrafos y texto

```
<p>Esto es un párrafo</p>           → texto normal
<strong>Texto fuerte</strong>       → negrita
<em>Texto enfatizado</em>           → cursiva
<br>                                → salto de línea
```

---

## 🔹 Listas

```
<ul>                                 → lista desordenada
  <li>Elemento 1</li>
  <li>Elemento 2</li>
</ul>

<ol>                                 → lista ordenada
  <li>Elemento 1</li>
  <li>Elemento 2</li>
</ol>
```

---

## 🔹 Enlaces e imágenes

```
<a href="https://ejemplo.com">Enlace</a> → link a otra página
<img src="imagen.jpg" alt="Descripción">  → imagen con descripción
```

---

## 🔹 Tablas

```
<table>
  <tr>
    <th>Encabezado 1</th>
    <th>Encabezado 2</th>
  </tr>
  <tr>
    <td>Dato 1</td>
    <td>Dato 2</td>
  </tr>
</table>
```

---

## 🔹 Formularios básicos

```
<form action="/enviar" method="post">
  <label>Nombre:</label>
  <input type="text" name="nombre">
  <input type="submit" value="Enviar">
</form>
```

---

## 🔹 Tips rápidos

- `<!-- comentario -->` → agregar comentarios
    
- `<div>` → contenedor genérico
    
- `<span>` → contenedor en línea

- [[URL]]
- [[Xpath]]