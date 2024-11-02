import requests
import hashlib
import time
import pandas as pd

public_key = 'YOUR_PUBLIC_KEY_HERE'
private_key = 'YOUR_PRIVATE_KEY_HERE'
url = 'https://gateway.marvel.com/v1/public/characters'

def generate_hash(ts):
    return hashlib.md5((ts + private_key + public_key).encode()).hexdigest()
     

def getAllCharacters():
    limit = 100 
    offset = 0 
    all_characters = []
    ts = str(time.time())


    while True:
        hash_value = generate_hash(ts)
        params = {
            'apikey': public_key,
            'ts': ts,
            'hash': hash_value,
            'limit': 100,
            'offset': offset
        }
        # Hacemos el request
        response = requests.get(url, params=params)
        data = response.json()

        if 'code' in data and data['code'] != 200:
            print(f"Error {data['code']}: {data['message']}")
            break

        # El campo results es el que trae la información de los personajes
        characters = data['data']['results']
        
        # Rompemos el bucle si no trae personajes
        if not characters:
            break

        # Agregamos todos los personajes en una lista
        all_characters.extend(characters)

        # Actualizamos el offset para la siguiente petición
        offset += limit

    return all_characters

def formatDataFrame(all_characters):

    df_characters = pd.DataFrame(all_characters)
    df_characters = pd.DataFrame(df_characters[['id', 'name', 'description' ,'comics', 'series', 'stories', 'events']]) #Elejimos solo las columnas de interes

    #Con este ciclo obtenemos el número de items que está en cada diccionario de los campos comics, series, etc...
    for i in df_characters:
        df_characters[i] = df_characters[i].apply(
            lambda x: x['available'] if i in ('comics', 'series', 'stories', 'events') else x
            )
    
    return df_characters

characters = getAllCharacters()
characters_formatted = formatDataFrame(characters)
print(characters_formatted)