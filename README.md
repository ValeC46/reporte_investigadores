# Reportes Investigadores

## Descripcion
El script generara un el cual tendra una pagina para cada investigador proporcionado. En cada pagina estara el nombre del investigador y la tabla con los ultimos articulos del investigador.

### Librerias necesarias
Se necesitara la libreria de BeautifulSoup, SerpApi, FPDF

_Para instalar BeautifulSoup:_
 ```
 pip install beautifulsoup4
```

_Para instalar SerpAPI:_
```
pip install google-search-results
```

_Para instalar FPDF:_
```
pip install fpdf
```

_Para instalar openpyxl:_
```
pip install openpyxl
```

### Directorio de archivos
***main.py:*** script que obtiene la informacion y la imprime en un archivo _.pdf_ (actualmente falla la funcion de guardar el pdf)<br>
***test.py:*** script para correr pruebas de bloques de codigo (aqui si funciona la funcion de exportar a pdf)<br>
***toexcel.py:*** script que obtiene la informacion y la guarda en un archivo _.xlsx_ (guarda una hoja por investigador dentro del mismo archivo)<br>
***ScholarLink.csv:*** csv generado por el script _main.py_ o _toexcel.py_ si asi se desea (actualmente se necesita para correr _test.py_)<br>
