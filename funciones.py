import streamlit as st

from lectura import calcular_total_ventas, calcular_unidades_categoria, calcular_ventas_categoria, \
    mostrar_registro_consultas


def iniciar_consulta():
    st.title('CONSULTA DE VENTAS')

    if 'stage' not in st.session_state:
        st.session_state.stage = 0

    def set_state(i):
        st.session_state.stage = i

    if st.session_state.stage == 0:
        st.button('Empezar', on_click=set_state, args=[1])

    if st.session_state.stage == 1:
        with st.form("formulario_nombre"):
            nombre_introducido = st.text_input("¿Cuál es tu nombre?")
            guardado = st.form_submit_button("Guardar")

        if guardado and nombre_introducido:
            st.session_state["nombre_usuario"] = nombre_introducido.title()
            st.session_state.stage = 2
            st.rerun()

    if st.session_state.stage == 2:
        st.write(f"¡Hola, **{st.session_state['nombre_usuario']}**!")
        eleccion_consulta = st.menu_button("Elige una consulta", options=
            ['Importe total vendido',
             'Número de unidades por categoría',
             'Ventas por categoría',
             'Registro de consultas',
             ],
            key='menu_incial')

        if eleccion_consulta:
            if eleccion_consulta != st.session_state.get('consulta_activa'):
                st.session_state['eleccion_consulta'] = eleccion_consulta
                st.session_state['consulta_activa'] = eleccion_consulta
                st.session_state.pop('categoria_elegida', None)

        if st.session_state.get('eleccion_consulta'):
            confirmar_consulta()

    if st.session_state.stage == 3:
        st.button('Realizar otra consulta', on_click=set_state, args=[0])


def confirmar_consulta():

    if st.session_state.eleccion_consulta == 'Importe total vendido':
        calcular_total_ventas()

    elif st.session_state.eleccion_consulta == 'Registro de consultas':
        tipo_consulta_registro = st.selectbox('Registro de consultas', options=
                                               ['Últimas cinco consultas realizadas',
                                               'Consultas por usuario',
                                               'Todas las consultas registradas'],
                                              key="consulta_registro"
                                                )
        if st.button("Confirmar", key='confirmar_registro'):
            st.session_state['tipo_consulta_registro'] = tipo_consulta_registro

        if 'tipo_consulta_registro' in st.session_state:
            mostrar_registro_consultas()

    elif st.session_state.eleccion_consulta in ("Número de unidades por categoría","Ventas por categoría"):
        asignar_categoria()

def asignar_categoria():
    if 'categoria_elegida' not in st.session_state:
        categoria_elegida = st.selectbox('CATEGORÍAS:', options=[
            'Electrónica',
            'Hogar',
            'Alimentación',
            'Deportes',
            'Ropa'],
        index = None,
        key = 'categoría',
        placeholder = 'Selecciona una categoría...',
        )

        if st.button('Confirmar categoría', key='confirmar_categoria'):
            if categoria_elegida is not None:
                st.session_state['categoria_elegida'] = categoria_elegida
                st.rerun()

    if 'categoria_elegida' in st.session_state:
        if st.session_state['eleccion_consulta'] == 'Número de unidades por categoría':
            calcular_unidades_categoria()

        elif st.session_state['eleccion_consulta'] == 'Ventas por categoría':
            calcular_ventas_categoria()


