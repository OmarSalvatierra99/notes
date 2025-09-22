## 🔹 Movimientos del cursor

```
h      ← mover un carácter a la izquierda
l      → mover un carácter a la derecha
0      ↑ inicio de línea
^      ↑ inicio de línea sin espacios
$      → fin de línea
w      → siguiente palabra
e      → final de palabra
b      ← palabra anterior
gg     ↑ inicio del archivo
G      ↓ final del archivo
3G     → ir a la línea 3
{ }    → bloque anterior / siguiente
%      → paréntesis, corchete o llave coincidente
```

---

## 🔹 Modos de inserción

```
i  → insertar antes del cursor
I  → inicio de línea
a  → insertar después del cursor
A  → final de línea
o  → nueva línea debajo
O  → nueva línea arriba
```

---

## 🔹 Edición rápida

```
x      → borrar carácter
dd     → borrar línea
d$     → borrar hasta fin de línea
cw     → cambiar palabra
c$     → cambiar hasta fin de línea
u      → deshacer
Ctrl+r → rehacer
.      → repetir última acción
```

---

## 🔹 Navegación entre archivos / definiciones

```
gd     → ir a definición
gD     → ir a declaración
gf     → abrir archivo bajo cursor
Ctrl+o → regresar al archivo anterior
Ctrl+i → ir al siguiente archivo
```

---

## 🔹 Búsqueda / reemplazo

```
/texto         → buscar hacia adelante
?texto         → buscar hacia atrás
n              → siguiente resultado
N              → resultado anterior
:%s/viejo/nuevo/g → reemplazo global
```

---

## 🔹 Marcadores / saltos rápidos

```
ma     → marcar posición 'a'
'a     → saltar al marcador 'a (inicio línea)
`a     → saltar exacto al marcador 'a'
```

---

## 🔹 Ventanas / pestañas

```
:sp / :split      → dividir ventana horizontal
:vsp / :vsplit    → dividir ventana vertical
Ctrl+w h/j/k/l    → moverse entre ventanas
:tabnew           → nueva pestaña
gt / gT           → siguiente / anterior pestaña
```

---

## 🔹 Tips rápidos

- Combina operadores con movimientos:
    
    - `daw` → borrar palabra completa
        
    - `y}` → copiar hasta fin de bloque
        
- Repetir acción compleja: `.`
    
- Usa marcadores y saltos para navegar rápido en proyectos grandes