## 🔹 Captura errores previsibles
```python
try:
    x = int(input("Número: "))
except ValueError:
    print("Debes ingresar un número válido")
```

- Captura errores que esperas que ocurran.

## 🔹 Captura errores específicos
```python
try:
    resultado = 10 / 0
except ZeroDivisionError:
    print("No se puede dividir entre cero")
```

- Mejora la claridad y depuración.

## 🔹 Usa `else` y `finally`
```python
try:
    f = open("archivo.txt")
except FileNotFoundError:
    print("Archivo no encontrado")
else:
    print(f.read())
finally:
    f.close()
```

- `else` → se ejecuta si no hay error.
- `finally` → siempre se ejecuta, útil para liberar recursos.

## 🔹 No ignores errores
```python
try:
    x = int("hola")
except:
    pass  # ❌ Evita esto
```

- Ignorar errores dificulta la depuración.

## 🔹 Mensajes claros
```python
except ValueError as e:
    print(f"Error: {e}")
```

- Ayuda a identificar la causa rápidamente.

## 🔹 Excepciones personalizadas
```python
class MiError(Exception): pass
raise MiError("Mensaje de error")
```

- Útil para reglas de negocio específicas.

**Resumen:**
- Captura solo lo necesario
- Mensajes claros
- `finally` para recursos
- Excepciones propias para lógica específica