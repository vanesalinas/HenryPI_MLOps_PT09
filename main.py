#importar las librerias
from fastapi import FastAPI
import pandas as pd
import calendar   

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

    

    return None

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

    

    return None

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

    

    return None

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

    

    return None