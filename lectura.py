import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from datetime import datetime
from pathlib import Path

ruta_csv = Path(__file__).parent/"datos"/"ventas.csv"
ruta_parquet = Path(__file__).parent/"datos"/"consultas.parquet"

def calcular_total_ventas():
    total_ventas_df = pd.read_csv(ruta_csv,usecols=['unidades','precio_unitario'])

    total_ventas = 0

    for index,row in total_ventas_df.iterrows():
        total_por_producto = int(row['unidades']) * float(row['precio_unitario'])
        total_ventas += total_por_producto
        total_formateado = "{:,}".format(total_ventas)

    print(f'Importe total de ventas: {total_formateado}€')

    registrar_consulta(tipo_consulta='Total de ventas')

def calcular_unidades_categoria(nombre_categoria):
    unidades_df = pd.read_csv(ruta_csv,usecols=['categoria','unidades'])

    total_unidades = 0

    for index, row in unidades_df.iterrows():
        if row['categoria'] == nombre_categoria:
            total_unidades += int(row['unidades'])
        else:
            pass
    print(f'Número de unidades en la categoria {nombre_categoria}: {total_unidades}')

    registrar_consulta(tipo_consulta='Unidades por categoria')

def calcular_ventas_categoria(nombre_categoria):
    ventas_categoria_df = pd.read_csv(ruta_csv, usecols=['categoria','unidades','precio_unitario'])

    total_ventas_categoria = 0

    for index, row in ventas_categoria_df.iterrows():
        if row['categoria'] == nombre_categoria:
            total_ventas_categoria += int(row['unidades']) * float(row['precio_unitario'])
            total_ventas_categoria = round(total_ventas_categoria,2)
            ventas_categoria_formateado = "{:,}".format(total_ventas_categoria)
        else:
            pass
    print(f'Total de ventas de la categoria {nombre_categoria}: {ventas_categoria_formateado}€')

    registrar_consulta(tipo_consulta='Ventas por categoria')

def registrar_consulta(tipo_consulta):

    from funciones import nombre_usuario, continuar_sesion
    today = datetime.now()

    consulta = pd.DataFrame({
        "fecha": [today],
        "usuario": [nombre_usuario[0]],
        "tipo de consulta": [tipo_consulta],
    })

    tabla_existente = pq.read_table(ruta_parquet)
    tabla_nueva = pa.Table.from_pandas(consulta)

    tabla_combinada = pa.concat_tables([tabla_existente, tabla_nueva])

    pq.write_table(tabla_combinada, ruta_parquet)
    continuar_sesion()
