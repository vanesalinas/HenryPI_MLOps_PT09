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
    Se ingresa un mes en idioma Español y devuelve la cantidad de películas que fueron estrenadas en ese mes.

    Parametros
    ----------
    mes : str

    Retorno
    -------
    Cantidad de películas estrenadas en el mes consultado

    '''
    # Convertir 'release_date' a tipo datetime
    df_fecha_estreno['release_date'] = pd.to_datetime(df_fecha_estreno['release_date'], format='%Y-%m-%d', errors='coerce')

    #Crea una lista con los meses en español
    meses = ['','Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio','Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    
    # Si mes es un número, convertir directamente a entero
    if Mes.isdigit():
        numero_mes = int(Mes)
        if numero_mes < 1 or numero_mes > 12:
            return "El número de mes debe estar entre 1 y 12"
    else:
        # Si es un string, convertir el nombre del mes a su número correspondiente
        try:
            numero_mes = list(meses).index(Mes.capitalize())
        except ValueError:
            return f"El mes '{Mes}' no está en la lista de meses válidos"
    
    # Contar cuántos registros contienen el mes especificado
    resultado = df_fecha_estreno[df_fecha_estreno['release_date'].dt.month == numero_mes].shape[0]

    return f"{resultado} películas fueron estrenadas en el mes {numero_mes}"

@app.get("/B")
def cantidad_filmaciones_dia( Dia: str ):
    '''
    Se ingresa un dia en idioma Español y devuelve la cantidad de películas que fueron estrenadas en ese dia.

    Parametros
    ----------
    dia : str

    Retorno
    -------
    Cantidad de películas estrenadas en el dia consultado

    '''

    

    return None

@app.get("/C")
def score_titulo( titulo_de_la_filmación ):
    '''
    Calcula cantidad de items y porcentaje de contenido Free por año según empresa desarrolladora

    Parametros
    ----------
    desarrollador : str

    Retorno
    -------
    Año, Cantidad de items, porcentaje contenido free

    '''

    # Filtrar por el titulo buscado
    titulo_df = df_score_votos[df_score_votos['title'].str.contains(titulo_de_la_filmación, case=False, na=False)]

    if titulo_df.empty:
        return f"No se encuentran registros que coincidan con '{titulo_de_la_filmación}'."

    #Seleccionamos solo las columnas con los datos a retornar
    resultado = titulo_df[['title','release_year','popularity']]
    resultado.rename(columns={
        'title': 'Titulo',
        'release_year': 'Año de estreno',
        'popularity': 'Popularidad'
        }, inplace=True)

    return {
        f"Peliculas que coinciden con {titulo_de_la_filmación}":
        {resultado.to_json(orient='records', lines=True)}
    }

@app.get("/D")
def votos_titulo( titulo_de_la_filmación ):
    '''
    Calcula cantidad de items y porcentaje de contenido Free por año según empresa desarrolladora

    Parametros
    ----------
    desarrollador : str

    Retorno
    -------
    Año, Cantidad de items, porcentaje contenido free

    '''

    # Filtrar por el titulo buscado
    titulo_df = df_score_votos[df_score_votos['title'].str.contains(titulo_de_la_filmación, case=False, na=False)]

    if titulo_df.empty:
        return f"No se encuentran registros que coincidan con '{titulo_de_la_filmación}'."

    #Seleccionamos solo las columnas con los datos a retornar
    resultado = titulo_df[['title','release_year','vote_count','vote_average']]

    #Filtrar los registros que tengan más de 2000 votos
    filtrado = resultado[resultado['vote_count'] >= 2000]

    filtrado.rename(columns={
        'title': 'Titulo',
        'release_year': 'Año de estreno',
        'vote_count': 'Cantidad de valoraciones',
        'vote_average': 'Puntaje promedio'
        }, inplace=True)

    if filtrado.empty:
        return "El título ingresado no cumple con el mínimo de votos necesarios para mostrar la información"

    return {
        f"Peliculas que coinciden con {titulo_de_la_filmación}":
        {filtrado.to_json(orient='records', lines=True)}
    }

@app.get("/E")
def get_actor( nombre_actor ):
    '''
    Calcula cantidad de items y porcentaje de contenido Free por año según empresa desarrolladora

    Parametros
    ----------
    desarrollador : str

    Retorno
    -------
    Año, Cantidad de items, porcentaje contenido free

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
def get_director( nombre_director ):
    '''
    Calcula cantidad de items y porcentaje de contenido Free por año según empresa desarrolladora

    Parametros
    ----------
    desarrollador : str

    Retorno
    -------
    Año, Cantidad de items, porcentaje contenido free

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