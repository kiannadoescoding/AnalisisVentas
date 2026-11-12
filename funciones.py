from lectura import calcular_total_ventas, calcular_unidades_categoria, calcular_ventas_categoria, \
    mostrar_registro_consultas

nombre_usuario = []
numero_consultas = 0

def iniciar_consulta():
    global numero_consultas

    while True:
        if numero_consultas == 0:
            while not nombre_usuario:
                nombre_usuario_actual = input('Introduce tu nombre: ').title()

                if not nombre_usuario_actual.isalpha():
                    print('Nombre inválido. Introduce solo caracteres alfabéticos.')
                else:
                    nombre_usuario.append(nombre_usuario_actual)
                    print('Hola,', nombre_usuario[0])
                    numero_consultas += 1

        eleccion_consulta = str(input(
            f'¿Qué tipo de consulta deseas realizar?\n\n'
            f'Elige uno:\n'
            f'1. Importe total vendido\n'
            f'2. Número de unidades por categoría\n'
            f'3. Ventas por categoría\n'
            f'4. Registro de consultas\n\n'
            f'Introduce tu elección: '
            ))

        if eleccion_consulta == '1':
            calcular_total_ventas()
            break

        elif eleccion_consulta == '4':
            print('\n\nREGISTRO DE CONSULTAS')
            while True:
                tipo_consulta_registro = input('¿Qué tipo de consulta te gustaría hacer?\n\n'
                                               '1. Últimas cinco consultas realizadas\n'
                                               '2. Consultas por usuario\n'
                                               '3. Todas las consultas\n\n'
                                               'Escribe tu elección: ')

                if tipo_consulta_registro in ("1", "2", "3"):
                    mostrar_registro_consultas(tipo_consulta_registro)
                    break

                print('ERROR: Intenta de nuevo\n\n')

        elif eleccion_consulta in ("2","3"):
            asignar_categoria(eleccion_consulta)
            break

        else:
            print('ERROR: Elección inválida. Intenta de nuevo.\n\n')

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
    categorias_dict = {
        '1': 'Electrónica',
        '2': 'Hogar',
        '3': 'Alimentación',
        '4': 'Deportes',
        '5': 'Ropa',
    }
    categoria_elegida = input('\nElige una categoría:\n\n'
                              '1. Electrónica\n'
                              '2. Hogar\n'
                              '3. Alimentación\n'
                              '4. Deportes\n'
                              '5. Ropa\n\n'
                              'Introduce el número: ')

    if categoria_elegida in categorias_dict:
        nombre_categoria = categorias_dict[categoria_elegida]

        if eleccion_consulta == '2':
            calcular_unidades_categoria(nombre_categoria)
        elif eleccion_consulta == '3':
            calcular_ventas_categoria(nombre_categoria)
    else:
        print('ERROR: Categoria no existe. Intenta de nuevo.')
        asignar_categoria(eleccion_consulta)