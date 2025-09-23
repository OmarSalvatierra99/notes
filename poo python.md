## 🔹 ¿Qué es `self` en Python?

- `self` es una referencia al objeto actual de la clase.
    
- Permite acceder a atributos y métodos del objeto desde dentro de la clase.
    
- Siempre debe ser el primer parámetro de los métodos de instancia.
    

```python
class Persona:
    def __init__(self, nombre):
        self.nombre = nombre  # self.nombre es atributo del objeto

    def saludar(self):
        print(f'Hola, mi nombre es {self.nombre}')

p = Persona('Omar')
p.saludar()  # Hola, mi nombre es Omar
```

---

## 🔹 ¿Qué es una clase en Python?

- Una clase es un molde o plantilla para crear objetos.
    
- Define atributos (propiedades) y métodos (funciones) que los objetos tendrán.
    
- Permite organizar y reutilizar código.
    

```python
class Coche:
    def __init__(self, marca, modelo):
        self.marca = marca
        self.modelo = modelo

    def descripcion(self):
        return f'{self.marca} {self.modelo}'

mi_coche = Coche('Toyota', 'Corolla')
print(mi_coche.descripcion())  # Toyota Corolla
```

---

## 🔹 ¿Qué es la herencia en Python?

- La herencia permite que una clase (clase hija) herede atributos y métodos de otra clase (clase padre).
    
- Facilita la reutilización de código y la creación de jerarquías de clases.
    

```python
class Vehiculo:
    def __init__(self, tipo):
        self.tipo = tipo

    def mostrar_tipo(self):
        print(f'Tipo: {self.tipo}')

class Moto(Vehiculo):  # Moto hereda de Vehiculo
    def __init__(self, tipo, cilindrada):
        super().__init__(tipo)  # llamar al constructor de la clase padre
        self.cilindrada = cilindrada

    def descripcion(self):
        print(f'Moto {self.tipo}, {self.cilindrada}cc')

m = Moto('Deportiva', 600)
m.mostrar_tipo()   # Tipo: Deportiva
m.descripcion()    # Moto Deportiva, 600cc
```

---

## 🔹 Tips rápidos

- `self` es obligatorio en los métodos de instancia.
    
- Las clases permiten encapsular datos y comportamientos.
    
- La herencia se usa con `class Hija(Padre):` y `super()` para acceder al constructor o métodos del padre.