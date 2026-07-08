# Comandos en GitHub

## cambiar de rama si existe
```bash
git switch develop
```

## Crear un nueva rama basada en la existente
```bash
git switch -c develop
```

## Borrar una rama del github
```bash
git push origin --delete develop
```

## Borrar la rama en local
```bash
git branch -d develop
```

## Forzar el borrar la rama en local
```bash
git branch -D develop
```

## Agregar la nueva rama que ya esta en local a la web
```bash
git push -u origin develop
```

