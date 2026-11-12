import streamlit as st

from lectura import calcular_total_ventas, calcular_unidades_categoria, calcular_ventas_categoria, \
    mostrar_registro_consultas

nombre_usuario = []

def iniciar_consulta():
    st.write('CONSULTA DE VENTAS')
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

        if guardado and nombre_introducido.strip():
            nombre_usuario.append(nombre_introducido)
            st.session_state["nombre_usuario"] = nombre_introducido.strip()
            st.session_state.stage = 2
            st.rerun()

    if st.session_state.stage == 2:
        st.write(f"¡Hola, **{st.session_state['nombre_usuario']}**!")
        eleccion_consulta = st.menu_button("¿Qué tipo de consulta deseas realizar?", options=
        ['Importe total vendido',
         'Número de unidades por categoría',
         'Ventas por categoría',
         'Registro de consultas',
         ])
        if eleccion_consulta:
            confirmar_consulta(eleccion_consulta)

        if eleccion_consulta is None:
            set_state(2)

    if st.session_state.stage == 3:
        st.button('Realizar otra consulta', on_click=set_state, args=[0])


def confirmar_consulta(eleccion_consulta):
    if eleccion_consulta == 'Importe total vendido':
        calcular_total_ventas()

    elif eleccion_consulta == 'Registro de consultas':
        st.write('REGISTRO DE CONSULTAS')
        tipo_consulta_registro = st.selectbox('¿Qué tipo de consulta te gustaría hacer?', options=
                                               ['Últimas cinco consultas realizadas',
                                               'Consultas por usuario',
                                               'Todas las consultas']
                                                )

        mostrar_registro_consultas(tipo_consulta_registro)

    elif eleccion_consulta in ("Número de unidades por categoría","Ventas por categoría"):
        asignar_categoria(eleccion_consulta)


def continuar_sesion():
    while True:

        decision_usuario = input('\n\n¿Deseas realizar otra consulta? Escribe "sí" o "no": ')
        decision_usuario = decision_usuario.lower().strip()

        if decision_usuario in ('si','sí'):
            iniciar_consulta()

        if decision_usuario == 'no':
            print('¡Hasta luego!')
            break

        print('ERROR: Intenta de nuevo\n\n')

def asignar_categoria(eleccion_consulta):

    categoria_elegida = st.selectbox('CATEGORÍAS:', options=[
        'Electrónica',
        'Hogar',
        'Alimentación',
        'Deportes',
        'Ropa'],
    index = None,
    placeholder = 'Selecciona una categoría...'
    )
    if st.button('Confirmar categoría'):

        if categoria_elegida is None:
            st.warning('Por favor, selecciona una categoría.')

        elif eleccion_consulta == 'Número de unidades por categoría':
            calcular_unidades_categoria(categoria_elegida)

        elif eleccion_consulta == 'Ventas por categoría':
            calcular_ventas_categoria(categoria_elegida)

    if categoria_elegida is not None:
        st.write(f'Categoría elegida: {categoria_elegida}')
        if eleccion_consulta == 'Número de unidades por categoría':
            calcular_unidades_categoria(categoria_elegida)
        elif eleccion_consulta == 'Ventas por categoría':
            calcular_ventas_categoria(categoria_elegida)