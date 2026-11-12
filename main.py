import pandas as pd
import os

import pyarrow as pa
import pyarrow.parquet as pq

from datetime import datetime
from funciones import iniciar_consulta
from lectura import ruta_parquet


if __name__ == "__main__":
    try:
        if not os.path.exists(ruta_parquet):
            datos_iniciales = {
                'fecha': [datetime.now()],
                'usuario': ['Administrador'],
                'tipo de consulta': ['Creación del archivo parquet'],
                'categoría' : ['ejemplo'],
                'resultado' : [123.456],
            }

            registro_consultas = pd.DataFrame(datos_iniciales)
            tabla = pa.Table.from_pandas(registro_consultas)

            pq.write_table(tabla, 'datos/consultas.parquet')

        iniciar_consulta()

    except FileNotFoundError:
        print('Puede que el archivo "consultas.parquet" no se haya creado.'
              'Si este archivo no se encuentra en la carpeta "datos", créalo y reinicia el programa.')
    except:
        print('Algo ha salido mal. Intenta de nuevo')

