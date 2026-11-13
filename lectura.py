import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

import streamlit as st

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

    st.write(f'Importe total de ventas: {total_formateado}€')

    registrar_consulta(tipo_consulta='Total de ventas', categoria='Todas', resultado_calculado=total_ventas)

def calcular_unidades_categoria():

    unidades_df = pd.read_csv(ruta_csv,usecols=['categoria','unidades'])
    total_unidades = 0

    for index, row in unidades_df.iterrows():
        if row['categoria'] == st.session_state['categoria_elegida']:
            total_unidades += int(row['unidades'])

    if total_unidades > 0:

        st.write(f'Número de unidades en la categoría {st.session_state['categoria_elegida']}: {total_unidades}')

        registrar_consulta(tipo_consulta='Unidades por categoría', categoria=st.session_state['categoria_elegida'], resultado_calculado=float(total_unidades))

def calcular_ventas_categoria():
    ventas_categoria_df = pd.read_csv(ruta_csv, usecols=['categoria','unidades','precio_unitario'])

    total_ventas_categoria = 0
    for index, row in ventas_categoria_df.iterrows():
        if row['categoria'] == st.session_state['categoria_elegida']:
            total_ventas_categoria += int(row['unidades']) * float(row['precio_unitario'])
            total_ventas_categoria = round(total_ventas_categoria,2)
            ventas_categoria_formateado = locale.format_string("%.2f", total_ventas_categoria, grouping=True)

    if total_ventas_categoria > 0:
        st.write(f'Total de ventas de la categoria {st.session_state['categoria_elegida']}: {ventas_categoria_formateado}€')

        registrar_consulta(tipo_consulta='Ventas por categoria',categoria=st.session_state['categoria_elegida'], resultado_calculado=total_ventas_categoria)

def mostrar_registro_consultas():
    df = pd.read_parquet('datos/consultas.parquet')

    if st.session_state['tipo_consulta_registro'] == 'Todas las consultas registradas':
        st.write('Mostrando todas las consultas registradas')
        st.dataframe(df)

    if st.session_state['tipo_consulta_registro'] == 'Últimas cinco consultas realizadas':
        st.write('Mostrando las últimas 5 consultas registradas')
        df_tail = df.tail()
        st.dataframe(df_tail)

    if st.session_state['tipo_consulta_registro'] == 'Consultas por usuario':

        if 'usuario_elegido' not in st.session_state:

            usuario_elegido = st.text_input('Escribe el nombre del usuario para recoger sus consultas: ')
            if st.button('Confirmar usuario', key='confirmar_usuario'):
                if usuario_elegido.strip():
                    st.session_state['usuario_elegido'] = usuario_elegido.title().strip()
                    st.rerun()

        else:
            usuario_df = df[df['usuario'] == st.session_state['usuario_elegido']]

            if usuario_df.empty:
                 st.write(f"No hay registros con el nombre {st.session_state['usuario_elegido']}")

            else:
                st.write(f"Mostrando todos los registros del usuario {st.session_state['usuario_elegido']}")
                st.dataframe(usuario_df)

            if st.button('Buscar otro usuario'):
                del st.session_state['usuario_elegido']
                st.rerun()

    registrar_consulta(tipo_consulta='Registro de consultas', categoria='N/A', resultado_calculado=0.0)

def registrar_consulta(tipo_consulta, categoria, resultado_calculado):

    today = datetime.now()
    today_truncated = today.replace(microsecond=0)

    consulta = pd.DataFrame({
        "fecha": [today_truncated],
        "usuario": [st.session_state['nombre_usuario']],
        "tipo de consulta": [tipo_consulta],
        "categoría": [categoria],
        "resultado" : [resultado_calculado]

    })

    tabla_existente = pq.read_table(ruta_parquet)
    tabla_nueva = pa.Table.from_pandas(consulta)

    tabla_combinada = pa.concat_tables([tabla_existente, tabla_nueva])

    pq.write_table(tabla_combinada, ruta_parquet)