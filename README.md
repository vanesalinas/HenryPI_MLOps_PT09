# <h1 align=center> **Machine Learning Operations (MLOps)** </h1>
<p align="center"><img src='/src/img/portada.png'></p>

## <p align="center">PROYECTO INDIVIDUAL Nº1<br/>SOY HENRY DATA-PT09</p>

### Tabla de contenido
+	Contexto.
+	Tecnologías utilizadas
+	Transformaciones.
+	Análisis exploratorio de los datos.
+	Sistema de recomendación.
+	API.
+	Demo.
+	Estructura del repositorio.
+	Enlaces.

### Contexto

<p align="justify">En el rol de Data Scientist de una startup que provee servicios de agregación de plataformas de streaming, el objetivo de este proyecto  es diseñar un sistema de recomendación que aún no ha sido puesto en marcha.<br/>
Se trabajará en un MVP (Minimum Viable Product) realizando tareas de ETL (Extracción, Transformación y Carga de datos) en la base de datos de la start-up para luego realizar un Análisis Exploratorio de Datos (EDA) y así poder construir un modelo de aprendizaje automático para brindar recomendaciones de películas.<br/>
Los datos se pondrán a disposición de los usuarios para ser consumidos a través de una API utilizando el framework FASTAPI.<br/></p>

***Este proyecto fue desarrollado durante la etapa de Labs del Bootcamp de Henry.*** 

### Herramientas utilizadas
<style>
  img {
    max-height: 50px; 
    width: 50px; 
  }
</style>

<div style="display: flex;">
  <img src="./src/img/imagen1 - copia.png">
  <img src="./src/img/imagen2 - copia.png">
  <img src="./src/img/imagen3 - copia.png">
  <img src="./src/img/imagen4 - copia.png">
  <img src="./src/img/imagen5 - copia.png">
</div>

### Transformaciones

<p align="justify">Los datos iniciales presentan ciertas limitaciones por lo que se realizará un trabajo de Data Engineering para transformarlos y prepararlos adecuadamente.<br/> 
Se realizaron transformaciones en los datos tales como:</p>  

+	Desanidar campos que contenían listas de diccionarios.
+	Rellenar con 0 los valores nulos de las columnas "revenue" y "budget".
+	Eliminar registros que contengan valores nulos en el campo "release date".
+	Verificar el formato del campo "release_year" (AAAA-MM-DD) y generar una nueva columna con el año de estreno.
+	Crear un nuevo campo llamado "return" donde se calculara el retorno de inversión de cada película, dividiendo el valor del campo "revenue" entre el valor del campo "budget".
+	Eliminar los campos que no serán utilizados: "video", "imdb_id", "adult", "original_title", "poster_path" y "homepage".<br/>

<p align="justify">Por último, se crean dataframes filtrando solo la información requerida, para optimizar el funcionamiento de las funciones que serán desarrolladas para disponibilizar en la API.<br/>
Puedes visualizar estas transformaciones en el siguiente archivo link</p>  

### Análisis exploratorio de los datos. ###

<p align="justify"> Antes de construir nuestro modelo, realizamos un Analisis Exploratorio de Datos (EDA). Este paso es crucial para entender la distribucion, tendencias y relaciones dentro de los datos. Este analisis ayudo a tomar decisiones informadas sobre como construir nuestro sistema de recmendacion. </p>

### Sistema de recomendación ###

<p align="justify"> Se utilizaron tecnicas de aprendizaje automatico para sugerir peliculadas basadas en el contenido. El filtrado basado en contenido recomienda elementos similares a los que el usuario ha interactuado anteriormente, basandose en las caracteristicas de estos elementos.<br/>

En este caso, el sistema recibe el titulo de una filmacion y utilizando K-Nearest Neighnors(KNN) encuentra los cinco elementos mas similares a ese titulo, recomendando los elementos mas populares entre esos vecinos. Por ello el dataframe que alimenta este modelo esta basado en las columnas de texto 'overview', 'title', 'genres', 'production_companies' en las que va a filtrar las coincidencias y tambien en la columna 'popularity' para poder ordenar segun la popularidad de las peliculas y recomendar las cinco mas populares.<br/>
</p>

### API ###
Se utilizó el framework FastAPI  para disponibilizar los datos de la empresa y se crearon las siguientes consultas:
+	def cantidad_filmaciones_mes( Mes ): Se ingresa un mes en idioma Español. Debe devolver la cantidad de películas que fueron estrenadas en el mes consultado en la totalidad del dataset.
+	def cantidad_filmaciones_dia( Dia ): Se ingresa un día en idioma Español. Debe devolver la cantidad de películas que fueron estrenadas en día consultado en la totalidad del dataset.
+	def score_titulo( titulo_de_la_filmación ): Se ingresa el título de una filmación esperando como respuesta el título, el año de estreno y el score.
+	def votos_titulo( titulo_de_la_filmación ): Se ingresa el título de una filmación esperando como respuesta el título, la cantidad de votos y el valor promedio de las votaciones. La misma variable deberá de contar con al menos 2000 valoraciones, caso contrario, debemos contar con un mensaje avisando que no cumple esta condición y que por ende, no se devuelve ningun valor.
+	def get_actor( nombre_actor ): Se ingresa el nombre de un actor que se encuentre dentro de un dataset debiendo devolver el éxito del mismo medido a través del retorno. Además, la cantidad de películas que en las que ha participado y el promedio de retorno. La definición no deberá considerar directores.
+	def get_director( nombre_director ): Se ingresa el nombre de un director que se encuentre dentro de un dataset debiendo devolver el éxito del mismo medido a través del retorno. Además, deberá devolver el nombre de cada película con la fecha de lanzamiento, retorno individual, costo y ganancia de la misma.
+	def recomendacion( titulo ): Se ingresa el nombre de una película y te recomienda las similares en una lista de 5 valores.
<p>Puedes visualizar el código en el siguiente archivo (link)<br/>
  
Esta API será consumida en la web a través de un service web de Render. Puedes acceder desde aquí https://vanessasalinas-henrypi-mlops-pt09.onrender.com/docs </p>  

### Demo ###
Resumen del funcionamiento de todo lo explicado en el siguiente video https://youtu.be/gYk_VJU9qBc

### Estructura del repositorio ###

<p> En este repositorio encontrarás los siguientes archivos:<br/></p>
+	_ pycache_: Carpeta donde se almacenan los datos cache de Python para mejorar su proceso de ejecución.
+   Datasets: carpeta donde se encuentran las fuentes de datos utilizadas.
+	Notebook: Carpeta que almacena los archivos para el ETL y el EDA.
+	src: carpeta que almacena imagenes que se encuentran en el repositorio.
+   .gitignore: archivo que indica lo que no debe ser rastreado por git
+	main.py: Archivo donde se almacenan las funciones que se ejecutarán en la API.
+	README.md: archivo con el readme del proyecto donde podras ver la presentacion del mismo.
+   requirements.txt: librerias requeridas para el deploy en Render
Tabla de contenido


### Enlaces (resumen)
+	Demo: https://youtu.be/gYk_VJU9qBc 
+	API: https://vanessasalinas-henrypi-mlops-pt09.onrender.com/docs 
+	Repositorio: https://github.com/vanesalinas/HenryPI_MLOps_PT09.git 
+	Fuente de datos: https://drive.google.com/drive/folders/1wWCFOjhQ-nLi_FRQ_zBIlr9CM5gjelCq?usp=drive_link

<hr> 

> `AUTOR`<br>
Este proyecto fue realizado por Vanessa Salinas. No dudes en contactarme! linked

<p align="center"><img src=https://d31uz8lwfmyn8g.cloudfront.net/Assets/logo-henry-white-lg.png></p>
