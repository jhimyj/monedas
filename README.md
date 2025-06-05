# EC3 - Implementación monedas

## Integrantes
- Alejandro Joel Ore Garcia (100%)
- Jhimy Jhoel Delgado Bazan (100%)
- Aldair Adrián Seminario Sánchez (100%)
- Alair Jairo Catacora Tupa (100%)
- Estefano Mauricio Zarate Manosalva (100%)

## Indicaciones

Para levantar el front y el back:

```
docker compose up (--build) -d
```

(Utilizar la opción `--build` cuando se necesite rebuildear los containers)

El front se puede acceder en:

```
localhost:5173
```

Y el back se puede acceder en:

```
localhost:8000
```

Para que el backend corra correctamente, se necesita un archivo .env en la carpeta 'back' que contenga lo siguiente:

```
CURRENCY_API_API_KEY = "(api key para CurrencyAPI)"
```

El API de Frankfurter no requiere API key, pero tiene menos información, mientras que el de CurrencyAPI contiene más info pero requiere de un API key