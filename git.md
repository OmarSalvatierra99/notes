## 🔹 Configuración inicial

```
git config --global user.name "Tu Nombre"   → configurar nombre de usuario
git config --global user.email "tu@email.com" → configurar email
git config --list                           → listar configuración
```

---

## 🔹 Crear y clonar repositorios

```
git init           → inicializar un repositorio local
git clone URL      → clonar un repositorio remoto
```

---

## 🔹 Estado y seguimiento de archivos

```
git status         → ver estado de archivos
git add archivo    → añadir archivo al área de staging
git add .          → añadir todos los cambios
git rm archivo     → eliminar archivo del repositorio
git mv archivo1 archivo2 → renombrar archivo
```

---

## 🔹 Commits

```
git commit -m "mensaje"   → crear commit
git commit -a -m "mensaje" → añadir y commitear en un solo paso
git log                     → historial de commits
git log --oneline           → historial resumido
```

---

## 🔹 Ramas (Branches)

```
git branch                → listar ramas
git branch nombre_rama    → crear nueva rama
git checkout nombre_rama  → cambiar de rama
git checkout -b nombre_rama → crear y cambiar a la rama
git merge nombre_rama     → fusionar rama al branch actual
git branch -d nombre_rama → eliminar rama local
```

---

## 🔹 Trabajando con repositorios remotos

```
git remote -v           → listar remotos
git remote add origin URL → añadir repositorio remoto
git push -u origin rama  → subir rama al remoto
git push                 → subir cambios al remoto
git pull                 → traer cambios del remoto
```

---

## 🔹 Deshacer cambios

```
git checkout -- archivo         → descartar cambios en archivo
git reset HEAD archivo          → sacar del área de staging
git revert HASH_COMMIT          → revertir commit específico
git reset --hard HASH_COMMIT    → reset total a commit específico
```

---

## 🔹 Comparar cambios

```
git diff                 → ver cambios sin añadir
git diff --staged        → ver cambios añadidos al staging
```

---

## 🔹 Tips rápidos

- `git stash` → guardar cambios temporales

- `git stash pop` → recuperar cambios guardados

- `git log --graph --all --decorate` → ver historial de commits en árbol visual