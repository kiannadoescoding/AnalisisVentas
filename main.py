import pandas as pd
import os
from pathlib import Path
import pyarrow as pa
import pyarrow.parquet as pq
from datetime import datetime
from funciones import iniciar_consulta

ruta_parquet = Path(__file__).parent/"datos"/"consultas.parquet"

if not os.path.exists(ruta_parquet):
        datos_iniciales = {
            'fecha': [datetime.now()],
            'usuario': ['Administrador'],
            'tipo de consulta': ['Creación del archivo parquet'],
        }

        registro_consultas = pd.DataFrame(datos_iniciales)
        tabla = pa.Table.from_pandas(registro_consultas)

        pq.write_table(tabla, 'datos/consultas.parquet')
        df = pd.read_parquet('datos/consultas.parquet')

else:
    pass


if __name__ == "__main__":
    iniciar_consulta()
    # df = pd.read_parquet('datos/consultas.parquet')
    # print(df)

