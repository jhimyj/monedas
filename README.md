Para levantar el front y el back:

```
docker compose up (--build) -d
```

(Utilizar la opción `--build` cuando se necesite rebuildear los containers)

El front se encuentra en:

```
localhost:5173
```

Y el back se encuentra en:

```
localhost:8000
```

Para el backend, se necesita un archivo .env en la carpeta 'back' que contenga lo siguiente:

```
CURRENCY_API_API_KEY = "(api key para CurrencyAPI)"
```

El API de Frankfurter no requiere API key, pero tiene menos información, mientras que el de CurrencyAPI contiene más info pero requiere de un API key.