import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from datetime import datetime
import locale
from pathlib import Path

ruta_csv = Path(__file__).parent/"datos"/"ventas.csv"
ruta_parquet = Path(__file__).parent/"datos"/"consultas.parquet"

locale.setlocale(locale.LC_NUMERIC, "es_ES")

def calcular_total_ventas():
    total_ventas_df = pd.read_csv(ruta_csv,usecols=['unidades','precio_unitario'])

    total_ventas = 0

    for index,row in total_ventas_df.iterrows():
        total_por_producto = int(row['unidades']) * float(row['precio_unitario'])
        total_ventas += total_por_producto
        total_formateado = locale.format_string("%.2f", total_ventas, grouping=True)

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
            ventas_categoria_formateado = locale.format_string("%.2f", total_ventas_categoria, grouping=True)
        else:
            pass
    print(f'Total de ventas de la categoria {nombre_categoria}: {ventas_categoria_formateado}€')

    registrar_consulta(tipo_consulta='Ventas por categoria')

def mostrar_registro_consultas(tipo_consulta_registro):
    df = pd.read_parquet('datos/consultas.parquet')

    if tipo_consulta_registro == '1':
        print(df.tail())

    elif tipo_consulta_registro == '2':
        usuario_elegido = input('Escribe el nombre del usuario para recoger sus consultas: ').title()
        usuario_df = df[df['usuario']== usuario_elegido]

        if usuario_df.empty:
            print(f'No hay registros con el nombre {usuario_elegido}')
        else:
            print(f'Mostrando todos los registros del usuario {usuario_elegido}')
            print(usuario_df)

    elif tipo_consulta_registro == '3':
        print(df)
    else:
        print('ERROR: Elección inválida. Intenta de nuevo.\n\n')
        mostrar_registro_consultas()

    registrar_consulta(tipo_consulta='Registro de consultas')

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