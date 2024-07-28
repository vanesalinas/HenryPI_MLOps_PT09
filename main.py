#importar las librerias
from fastapi import FastAPI
import pandas as pd
import re   

''' 
Instanciamos la clase
FastAPI es una clase de Python que provee toda la funcionalidad para tu API
'''
app = FastAPI()

'''
Cargamos los datos con los que se trabajaran
'''
df_actores = pd.read_csv('./Datasets/actores.csv')
df_directores = pd.read_csv('./Datasets/directores.csv')
df_fecha_estreno = pd.read_csv('./Datasets/fecha_estreno.csv')
df_score_votos = pd.read_csv('./Datasets/score_votos.csv')

''' 
Escribimos el decorador de path para cada funcion
Este decorador le dice a FastAPI que la funcion que esta por debajo corresponde al path / con una operacion GET
'''
@app.get("/A")
def cantidad_filmaciones_mes( Mes: str ):
    '''
    Recibe un mes en idioma Español y devuelve la cantidad de películas que fueron estrenadas en ese mes.

    Parametros
    ----------
    mes : str

    Retorno
    -------
    Cantidad de películas estrenadas en el mes consultado

    '''
    
    # Convertir 'release_date' a tipo datetime
    df_fecha_estreno['release_date'] = pd.to_datetime(df_fecha_estreno['release_date'], format='%Y-%m-%d', errors='coerce')

    # Creamos una diccionario con los nombres de los meses en ingles ya que se extraen del df en este idioma
    meses = {'enero': 'January', 'febrero': 'February', 'marzo': 'March', 'abril': 'April', 'mayo': 'May', 
            'junio': 'June', 'julio': 'July', 'agosto': 'August', 'septiembre': 'September', 'setiembre': 'September', 
            'octubre': 'October', 'noviembre': 'November', 'diciembre': 'December'}
    try:
        mes_ingles = meses[Mes.lower()]
    except KeyError:
        return f"El mes '{Mes}' no es un día válido. Verifica la ortografia."

    # Filtrar y contar
    cantidad_peliculas = df_fecha_estreno[df_fecha_estreno['release_date'].dt.month_name() == mes_ingles].shape[0]

    return f"{cantidad_peliculas} películas fueron estrenadas en el mes '{Mes}'"

@app.get("/B")
def cantidad_filmaciones_dia( Dia: str ):
    '''
    Recibe un dia en idioma Español y devuelve la cantidad de películas que fueron estrenadas en ese dia.

    Parametros
    ----------
    dia : str

    Retorno
    -------
    Cantidad de películas estrenadas en el dia consultado

    '''

    # Convertir 'release_date' a tipo datetime
    df_fecha_estreno['release_date'] = pd.to_datetime(df_fecha_estreno['release_date'], format='%Y-%m-%d', errors='coerce')

    # Creamos una diccionario con los nombres de los dias en ingles ya que se extraen del df en este idioma
    dias = {'lunes': 'Monday', 'martes': 'Tuesday', 'miercoles': 'Wednesday', 'jueves': 'Thursday',
            'viernes': 'Friday', 'sabado': 'Saturday', 'domingo': 'Sunday'}
    try:
        dia_ingles = dias[Dia.lower()]
    except KeyError:
        return f"El día '{Dia}' no es un día válido. Verifica la ortografia."

    # Filtrar y contar
    cantidad_peliculas = df_fecha_estreno[df_fecha_estreno['release_date'].dt.day_name() == dia_ingles].shape[0]

    return f"{cantidad_peliculas} películas fueron estrenadas un día {Dia}"

@app.get("/C")
def score_titulo( titulo_de_la_filmacion: str ):
    '''
    Recibe el título de una filmación y devuelve el título, año de estreno y score.

    Parametros
    ----------
    titulo_de_la_filmación : str

    Retorno
    -------
    Titulo, año de estreno y popularidad de cada pelicula que coincide con el parametro ingresado

    '''

    # Filtrar por el titulo buscado
    titulo_df = df_score_votos[df_score_votos['title'].str.contains(r'\b' + re.escape(titulo_de_la_filmacion) + r'\b', case=False, na=False)]

    if titulo_df.empty:
        return f"No se encuentran registros que  coincidan con '{titulo_de_la_filmacion}'."

    # Almacenar resultados en una lista
    resultados = []

    # Recorrer los titulos encontrados
    for index, row in titulo_df.iterrows():
        # Convertir la popularidad a float antes de redondear
        popularidad = float(row['popularity']) if row['popularity'] else 0.0  # Manejar posibles valores nulos
        resultados.append({
            'Titulo': row['title'],
            'Año de estreno': row['release_year'],
            'Popularidad': round(popularidad, 2)
        })

    return resultados

@app.get("/D")
def votos_titulo( titulo_de_la_filmacion: str ):
    '''
    Recibe el título de una filmación y devuelve el título, año de estreno, cantidad de votos
    y el valor promedio de las votaciones si la misma cuenta con al menos 2000 valoraciones.
    Caso contrario, devuelve un mensaje avisando que no cumple esta condición y no se devuelve ningun valor.

    Parametros
    ----------
    titulo_de_la_filmacion : str

    Retorno
    -------
    Título, año de estreno, cantidad de votos y el valor promedio de las votaciones

    '''

    # Filtrar por el titulo buscado
    titulo_df = df_score_votos[df_score_votos['title'].str.contains(r'\b' + re.escape(titulo_de_la_filmacion) + r'\b', case=False, na=False)]

    if titulo_df.empty:
        return f"No se encuentran registros que  coincidan con '{titulo_de_la_filmacion}'."

    #Filtrar los registros que tengan más de 2000 votos
    filtrado = titulo_df[titulo_df['vote_count'] >= 2000]

    # Almacenar resultados en una lista
    resultados = []

    # Recorrer los titulos encontrados
    for index, row in filtrado.iterrows():
        resultados.append({
            'Titulo': row['title'],
            'Año de estreno': row['release_year'],
            'Cantidad de valoraciones': row['vote_count'],
            'Puntaje promedio': row['vote_average']
        })

    return resultados

@app.get("/E")
def get_actor( nombre_actor: str ):
    '''
    Recibe el nombre de un actor y devuelve el nombre del actor, el éxito medido a través del retorno, 
    la cantidad de películas que en las que ha participado y el promedio de retorno.

    Parametros
    ----------
    nombre_actor : str

    Retorno
    -------
    Nombre del actor, cantidad de peliculas, retorno y promedio de retorno por pelicula

    '''

    # Filtrar por el actor buscado
    actor_df = df_actores[df_actores['actor_name'].str.contains(nombre_actor, case=False, na=False)]

    if actor_df.empty:
        return f"No se encuentran registros que  coincidan con '{nombre_actor}'."

    # Almacenar resultados en un diccionario
    resultados = {}

    # Recorrer los actores únicos encontrados
    for index, row in actor_df.iterrows():
        lista_actores = re.findall(r"'(.*?)'", row['actor_name'])  # Extraer lista de actores
        for actor_nombre in lista_actores:
            if re.search(r'\b' + re.escape(nombre_actor) + r'\b', actor_nombre, re.IGNORECASE):
                actor_unico = actor_df[actor_df['actor_name'].str.contains(re.escape(actor_nombre), case=False, na=False)]
                total_return = actor_unico['return'].sum()
                cantidad_peliculas = actor_unico.shape[0]
                promedio_return = round(actor_unico['return'].mean(), 2)

                resultados[actor_nombre] = {
                    'Nombre': actor_nombre,
                    'Cantidad de peliculas': cantidad_peliculas,
                    'Retorno (USD)': total_return,
                    'Promedio de retorno por pelicula (USD)': promedio_return
                }

    return list(resultados.values())

@app.get("/F")
def get_director( nombre_director: str ):
    '''
    Recibe el nombre de un director y devuelve el éxito del mismo medido a través del retorno.
    Además, crea una lista con el nombre de cada película dirigida por el mismo,
    con la fecha de lanzamiento, retorno individual, costo y ganancia de la misma.

    Parametros
    ----------
    nombre_director : str

    Retorno
    -------
    Nombre del director, retorno, lista de peliculas dirigidas por el mismo

    '''

    # Filtrar por el director buscado
    director_df = df_directores[df_directores['director_name'].str.contains(r'\b' + re.escape(nombre_director) + r'\b', case=False, na=False)]

    if director_df.empty:
        return f"No se encuentran registros que  coincidan con '{nombre_director}'."

    #Almacenar los resultados en un diccionario
    resultados = {}

    # Recorrer los directores únicos encontrados
    for index, row in director_df.iterrows():
        director_nombre = row['director_name']
    
        if director_nombre not in resultados:
            # Inicializar la información del director si es la primera vez que se encuentra
            resultados[director_nombre] = {
                'Nombre del director': director_nombre,
                'Retorno total(USD)': 0,
                'Películas': []
            }

        # Actualizar el retorno total del director
        resultados[director_nombre]['Retorno total(USD)'] += row['return']

        # Recopilar información detallada de cada película del director actual
        pelicula_info = {
            'Título': row['title'],
            'Fecha de lanzamiento': row['release_date'],
            'Retorno': row['return'],
            'Costo': row['budget'],
            'Ganancia': row['revenue']
        }

        # Agregar la información de la película a la lista de películas del director
        resultados[director_nombre]['Películas'].append(pelicula_info)

    # Convertir el diccionario de resultados a una lista y devolverla
    return list(resultados.values())