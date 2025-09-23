## 🔹 Variables y Tipos

```python
x = 5       # int
y = 3.14    # float
s = "Hola" # str
b = True    # bool
l = [1,2,3] # list
t = (1,2,3) # tuple
st = {1,2,3} # set
d = {"a":1} # dict
```

- Tipos: int, float, str, bool, list, tuple, set, dict
    
- `type(x)` → tipo de variable
    

---

## 🔹 Operadores

- Aritméticos: `+ - * / // % **`
    
- Comparación: `== != > < >= <=`
    
- Lógicos: `and or not`
    
- Membresía: `in`, `not in`
    
- Identidad: `is`, `is not`
    

---

## 🔹 Estructuras de Control

```python
if x > 0:
    print("Positivo")
elif x == 0:
    print("Cero")
else:
    print("Negativo")

for i in range(5):
    print(i)

while x > 0:
    x -= 1
```

- Usar `:` y sangría (4 espacios)
    
- `break` → salir del bucle
    
- `continue` → saltar a la siguiente iteración
    

---

## 🔹 Funciones

```python
def suma(a, b=0):
    return a + b

resultado = suma(3,5)
f = lambda x: x*2
```

- Parámetros: posicionales, por defecto, `*args`, `**kwargs`
    
- Funciones lambda → funciones anónimas
    

---

## 🔹 Listas

```python
nums = [1,2,3]
nums.append(4)
nums.insert(1,99)
nums.extend([5,6])
nums.remove(99)
nums.pop()
nums[0], nums[-1]
nums[1:3]
len(nums)
sum(nums)
```

- Comprensión de listas: `[x**2 for x in nums]`
    

---

## 🔹 Tuplas

```python
t = (1,2,3)
t[0], t[-1]
t[1:3], t[::-1]
t.count(2), t.index(3)
t + (4,5), t*2
```

- Inmutables, rápido acceso
    

---

## 🔹 Sets

```python
s = {1,2,3}
s.add(4)
s.remove(2)
s.discard(2)
len(s)
3 in s
s1 | s2  # unión
s1 & s2  # intersección
s1 - s2  # diferencia
s1 ^ s2  # diferencia simétrica
```

- Colección de elementos únicos, eficiente para pertenencia y operaciones de conjuntos
    

---

## 🔹 Diccionarios

```python
d = {"a":1, "b":2}
d["a"]
d.get("c",0)
d["c"] = 3
del d["b"]
d.keys(), d.values(), d.items()
d.pop("a")
d.clear()
"a" in d, len(d)
```

- Colección de pares clave-valor, claves únicas, acceso rápido
    

---

## 🔹 Strings

```python
s = "Hola Mundo"
s.lower(), s.upper(), s.title(), s.strip()
s[0], s[-1], s[0:4], s[::-1]
s.find("Mun"), s.replace("Hola","Adiós"), 'Mun' in s
f"Texto: {s}", "{}".format("Hola","Mundo")
s.split(), ",".join(["a","b"])
s.isalpha(), s.isdigit(), s.isalnum(), s.isspace()
```

---

## 🔹 Entrada/Salida

```python
input_str = input("Escribe algo: ")
print("Resultado:", input_str)
```

---

## 🔹 Importar módulos

```python
import math
import math as m
from math import sqrt
from math import *   # no recomendado
```

- Siempre al inicio del archivo
    

---

# 🗂 Python - Lectura y Escritura de Archivos

## 🔹 Abrir y leer archivos

```python
# Abrir archivo en modo lectura (r)
with open('archivo.txt', 'r') as f:
    contenido = f.read()  # lee todo el contenido
    # o leer línea por línea
    for linea in f:
        print(linea.strip())
```

- `with` asegura que el archivo se cierre automáticamente
    

## 🔹 Leer líneas como lista

```python
with open('archivo.txt', 'r') as f:
    lineas = f.readlines()  # devuelve lista de líneas
```

## 🔹 Escribir archivos

```python
# Abrir en modo escritura (w) -> sobrescribe
with open('salida.txt', 'w') as f:
    f.write("Hola Mundo\n")

# Abrir en modo append (a) -> agrega al final
with open('salida.txt', 'a') as f:
    f.write("Otra línea\n")
```

## 🔹 Modos de apertura

- `'r'` → lectura
    
- `'w'` → escritura (sobrescribe)
    
- `'a'` → agregar al final
    
- `'rb'`, `'wb'` → lectura/escritura binaria
    
- `'r+'` → lectura y escritura
    

## 🔹 Tips

- `f.readline()` → leer una línea a la vez
    
- `f.read(size)` → leer un número específico de caracteres
    
- Usar `with` es recomendable para evitar errores de cierre de archivo

## ❗Importante
- [[errores y excepciones en python]]
- [[poo python]]

    
    