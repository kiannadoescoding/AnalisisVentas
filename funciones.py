from lectura import calcular_total_ventas, calcular_unidades_categoria, calcular_ventas_categoria, \
    mostrar_registro_consultas

nombre_usuario = []
numero_consultas = 0

def iniciar_consulta():
    global numero_consultas

    if numero_consultas == 0:
        nombre_usuario_actual = input('Introduce tu nombre: ').title()
        nombre_usuario.append(nombre_usuario_actual)
        print('Hola,', nombre_usuario[0])

    else:
        pass

    eleccion_consulta = str(input(
        f'¿Qué tipo de consulta deseas realizar?\n\n'
        f'Elige uno:\n'
        f'1. Importe total vendido\n'
        f'2. Número de unidades por categoria\n'
        f'3. Ventas por categoría\n'
        f'4. Registro de consultas\n\n'
        f'Introduce tu elección: '
        ))

    if eleccion_consulta == '1':
        numero_consultas += 1
        calcular_total_ventas()

    elif eleccion_consulta == '4':
        numero_consultas += 1
        mostrar_registro_consultas()

    elif eleccion_consulta == '2' or '3':
        numero_consultas += 1
        elegir_categoria(eleccion_consulta)

    else:
            print('ERROR: Elección inválida. Intenta de nuevo.\n\n')
            iniciar_consulta()

def continuar_sesion():
    while True:

        decision_usuario = input('\n\n¿Deseas realizar otra consulta? Escribe "sí" o "no" ')
        decision_usuario = decision_usuario.lower().strip()

        if decision_usuario in ('si','sí'):
            iniciar_consulta()
            continue

        elif decision_usuario == 'no':
            print('¡Hasta luego!')
            return False

    print('ERROR: Intenta de nuevo\n\n')

def elegir_categoria(eleccion_consulta):
    categoria_elegida = input('\nElige una categoria:\n\n'
                              '1. Electrónica\n'
                              '2. Hogar\n'
                              '3. Alimentación\n'
                              '4. Deportes\n'
                              '5. Ropa\n\n'
                              'Introduce el número: ')

    categorias = ['1','2','3','4','5']
    if categoria_elegida in categorias:
        asignar_categoria(categoria_elegida, eleccion_consulta)
    else:
        print('ERROR: Categoria no existe. Intenta de nuevo.')
        elegir_categoria(eleccion_consulta)

def asignar_categoria(categoria_elegida,eleccion_consulta):
    categorias_dict = {
        '1': 'Electrónica',
        '2': 'Hogar',
        '3': 'Alimentación',
        '4': 'Deportes',
        '5': 'Ropa',
    }

    nombre_categoria = categorias_dict[categoria_elegida]

    if eleccion_consulta == '2':
        calcular_unidades_categoria(nombre_categoria)
    elif eleccion_consulta == '3':
        calcular_ventas_categoria(nombre_categoria)
