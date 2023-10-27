import requests
import pandas as pd
def catalogo_esios(token):
    """
    Descarga todos los identificadores y su descripcion de esios

    Parameters
    ----------
    token : str
        El token de esios necesario para realizar las llamadas al API

    Returns
    -------
    DataFrame
        Dataframe de pandas con el catalogo de los id de la API

    """

    headers = {'Accept': 'application/json; application/vnd.esios-api-v2+json',
               'Content-Type': 'application/json',
               'Host': 'api.esios.ree.es',
               'Cookie': '',
               'Authorization': 'Token token={}'.format(token),
               'Cache-Control': 'no-cache',
               'Pragma': 'no-cache'
               }
    end_point = 'https://api.esios.ree.es/indicators'
    response = requests.get(end_point, headers=headers).json()

    # del resultado en json bruto se convierte en pandas, y se eliminan los tags del campo description

    return response


print(catalogo_esios('27ac7b794ca773e7d1c6ea0f43adfd466abe7dbd6682b769ddd29cf25536c1d6'))