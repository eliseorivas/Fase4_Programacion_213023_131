# Cómo publicar TODA la Fase 4 en tu GitHub

Repositorio de destino:

https://github.com/wilmeradrianrh/Software_FJ_Fase4_Programacion

**El proyecto contiene los cinco aportes**: Cliente, Servicio abstracto, tres servicios especializados, Reserva, excepciones y logs, además de menú, 16 operaciones de demostración, 22 tests y PDF.

## Subida manual (sin comandos)
1. Descarga `Tarea_Completa_Fase4_SoftwareFJ.zip` y **extráelo**.
2. Abre el repositorio de destino en tu navegador e inicia sesión como `wilmeradrianrh`.
3. Si está vacío, elige `uploading an existing file`. Si tiene archivos, usa **Add file → Upload files**.
4. Arrastra el contenido de la carpeta `Software_FJ_Fase4` o selecciona los archivos. Incluye los `.py`, `README.md`, `EVIDENCIA_EJECUCION.txt` y el `Informe_Fase4_Software_FJ.pdf`. Para conservar subcarpetas como `logs/`, puedes arrastrar la carpeta en un navegador de escritorio, o crear la ruta manualmente. No subas `__pycache__`.
5. Escribe como mensaje del commit: `Proyecto completo Fase 4 - Software FJ (5 aportes)`.
6. Pulsa **Commit changes** y actualiza la página.
7. Comprueba que se visualicen `entidades.py`, `servicios.py`, `reservas.py`, `excepciones.py`, `validaciones.py`, `sistema.py`, `main.py`, `demostracion.py`, `test_sistema.py` y `README.md`.
8. Abre `servicios.py` o `reservas.py` desde GitHub para comprobar que el código se puede visualizar.

## Pruebas en Visual Studio Code
En la carpeta del proyecto, abre la terminal y ejecuta:

```bash
python demostracion.py
python -m unittest test_sistema.py -v
python main.py
```

La demostración ejecuta 16 operaciones, el conjunto de pruebas realiza 22 comprobaciones y el menú te permite interactuar con la aplicación. Puedes usar `py` en Windows si `python` no funciona.

## Entrega final
La guía pide un único documento PDF con portada, introducción, enlace del repositorio, conclusiones y referencias APA. Se incluye un informe modelo que hace referencia al repositorio de destino; **la URL no demuestra la subida** hasta que los archivos realmente estén publicados. Solicita la aprobación del tutor para una entrega individual, porque la guía exige trabajo colaborativo.
