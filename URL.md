## 🔹 Definición de URL

- URL (Uniform Resource Locator) → dirección que localiza recursos en la web
    
- Formato general: `protocolo://dominio:puerto/ruta?query#fragmento`
    

---

## 🔹 Componentes de una URL

```
https://www.ejemplo.com:443/carpeta/pagina.html?busqueda=chatgpt#seccion1
```

- `https` → protocolo (HTTP, HTTPS, FTP, etc.)
    
- `www.ejemplo.com` → dominio o host
    
- `:443` → puerto (opcional, 443 es por defecto HTTPS)
    
- `/carpeta/pagina.html` → ruta del recurso
    
- `?busqueda=chatgpt` → query string (parámetros)
    
- `#seccion1` → fragmento o ancla dentro de la página
    

---

## 🔹 Tipos de URL

- **Absoluta** → contiene toda la ruta y dominio completo
    
    - Ej: `https://www.ejemplo.com/carpeta/pagina.html`
        
- **Relativa** → ruta relativa al documento actual
    
    - Ej: `carpeta/pagina.html` o `../otra_pagina.html`
        

---

## 🔹 Parámetros en la URL

- Se añaden con `?` y se separan con `&`
    
    - Ej: `?usuario=omar&edad=26`
        
- Útiles para pasar información a servidores o scripts
    

---

## 🔹 Fragmentos

- Se añaden con `#` al final de la URL
    
    - Ej: `#contacto`
        
- Sirven para ir a secciones internas de la página
    

---

## 🔹 Buenas prácticas

- Evitar caracteres especiales sin codificar (`espacio` → `%20`)
    
- Mantener URLs legibles y cortas
    
- Usar HTTPS para seguridad
    
- Nombrar rutas y archivos de manera consistente