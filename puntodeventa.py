import csv
import json

def cargar_inventario():
    with open('inventario.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        return [row for row in reader]

def guardar_inventario(inventario):
    with open('inventario.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Nombre", "Codigo", "Precio", "Stock"])
        writer.writerows(inventario)

def cargar_vendedores():
    with open('vendedores.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        return [row for row in reader]

def guardar_vendedores(vendedores):
    with open('vendedores.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["ID", "Nombre", "Contrasena"])
        writer.writerows(vendedores)

def cargar_ventas():
    try:
        with open('ventas.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            return [row for row in reader]
    except FileNotFoundError:
        return []

def guardar_ventas(ventas):
    with open('ventas.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["ID Vendedor", "Ticket", "Total"])
        writer.writerows(ventas)

def guardar_ventas_producto(ventas_producto):
    with open('VentasProd.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Codigo Producto", "Nombre Producto", "ID Vendedor", "Nombre Vendedor", "Precio"])
        writer.writerows(ventas_producto)

def acceso(vendedores):
    longitud_vendedores = len(vendedores)
    codigo_correcto = False
    contrasena_correcta = False

    while True:
        id_vendedor = int(input("Escribe un codigo de cajero para acceder: "))
        for i in range(longitud_vendedores):
            if id_vendedor == int(vendedores[i][0]):
                print("Codigo correcto")
                codigo_correcto = True
                indice_vendedor = i
                break
        else:
            codigo_correcto = False

        if not codigo_correcto:
            print("Error, introduce un codigo correcto")
            pass
        else:
            while True:
                contrasena = input(f"{vendedores[indice_vendedor][1]}, Escribe tu contrasena: ")
                if contrasena == vendedores[indice_vendedor][-1]:
                    print("Contrasena correcta")
                    contrasena_correcta = True
                    break
                else:
                    print("Contrasena incorrecta, intenta nuevamente: ")

        if contrasena_correcta:
            return indice_vendedor

def realizar_venta(inventario, id_vendedor):
    stock_inventario = inventario
    longitud_inventario = len(stock_inventario)
    ticket = []
    total_venta = 0

    while True:
        print("1) Añadir un producto\n"
              "2) Cancelar el último producto añadido\n"
              "-1) Terminar el ticket")
        opcion = int(input("Selecciona una opción: "))
        
        if opcion == -1:
            break
        elif opcion == 1:
            codigo_articulo = int(input("Introduce el código del artículo que deseas vender: "))
            encontrado = False 
            for i in range(1, longitud_inventario):
                if codigo_articulo == int(stock_inventario[i][1]):  
                    encontrado = True
                    if int(stock_inventario[i][3]) > 0:
                        ticket.append(stock_inventario[i])
                        stock_inventario[i][3] = str(int(stock_inventario[i][3]) - 1)
                        total_venta += float(stock_inventario[i][2])
                        print(f"Artículo {stock_inventario[i][0]} añadido al ticket.")
                    else:
                        print(f"El artículo {stock_inventario[i][0]} no está disponible en stock.")
                    break

            if not encontrado:
                print("Código de artículo no válido.")
                
        elif opcion == 2:
            if ticket:
                ultimo_producto = ticket.pop()
                for i in range(1, longitud_inventario):
                    if stock_inventario[i][1] == ultimo_producto[1]:
                        stock_inventario[i][3] = str(int(stock_inventario[i][3]) + 1)
                        total_venta -= float(stock_inventario[i][2])
                        print(f"Se ha cancelado el último producto añadido: {ultimo_producto[0]}")
                        break
            else:
                print("No hay productos para cancelar.")
        else:
            print("Opción no válida.")

    print("Ticket de venta:", ticket)
    print("TOTAL: ", total_venta)
    
    return ticket, total_venta

def registrar_articulo(inventario):
    codigo_articulo = int(input("Introduce el código del artículo: "))
    for articulo in inventario:
        if int(articulo[1]) == codigo_articulo:
            cantidad = int(input(f"El artículo '{articulo[0]}' ya existe. Introduce la cantidad a añadir al stock: "))
            articulo[3] = str(int(articulo[3]) + cantidad)
            print(f"Stock actualizado. El nuevo stock de '{articulo[0]}' es {articulo[3]}.")
            return
    nombre_nuevo_articulo = input("Introduce el nombre del nuevo artículo: ")
    precio_nuevo_articulo = float(input("Introduce el precio del artículo: "))
    stock_nuevo_articulo = int(input("Introduce la cantidad en stock: "))
    inventario.append([nombre_nuevo_articulo, codigo_articulo, precio_nuevo_articulo, stock_nuevo_articulo])
    print("Artículo registrado exitosamente.")

def mostrar_inventario(inventario):
    print("Inventario actual:")
    for articulo in inventario:
        print(articulo)

def mostrar_ventas_sesion(ventas_realizadas):
    print("Ventas en esta sesión:")
    for venta in ventas_realizadas:
        print(venta)

def registrar_vendedor(vendedores):
    nuevo_id = int(input("Introduce el ID del nuevo vendedor: "))
    for vendedor in vendedores:
        if int(vendedor[0]) == nuevo_id:
            print(f"El ID '{nuevo_id}' ya existe. Por favor, prueba con uno diferente.")
            return
    nombre_vendedor = input("Introduce el nombre del nuevo vendedor: ")
    contrasena_vendedor = input("Introduce la contraseña del nuevo vendedor: ")
    vendedores.append([nuevo_id, nombre_vendedor, contrasena_vendedor])
    print("Vendedor registrado exitosamente.")

def mostrar_ventas_por_vendedor(ventas_realizadas):
    id_vendedor = int(input("Introduce el ID del vendedor: "))
    total_vendido = 0
    encontrado = False
    print(f"Ventas realizadas por el vendedor con ID {id_vendedor}:")
    
    for venta in ventas_realizadas:
        if int(venta[0]) == id_vendedor:
            print(venta)
            total_vendido += float(venta[2])
            encontrado = True

    if not encontrado:
        print("No se encontraron ventas para este vendedor.")
    else:
        print(f"Total vendido por el vendedor con ID {id_vendedor}: {total_vendido}")

def mostrar_ventas_por_producto(ventas_realizadas):
    codigo_producto = int(input("Introduce el código del producto: "))
    cantidad_vendida = 0
    total_ventas = 0
    encontrado = False
    nombre_producto = ""
    precio_producto = 0.0

    for venta in ventas_realizadas:
        ticket = json.loads(venta[1])
        for item in ticket:
            if int(item[1]) == codigo_producto:
                nombre_producto = item[0]
                precio_producto = float(item[2])
                cantidad_vendida += 1
                total_ventas += precio_producto
                encontrado = True

    if encontrado:
        print(f"Ventas del producto {nombre_producto} (Código: {codigo_producto})")
        print(f"Cantidad vendida: {cantidad_vendida}")
        print(f"Total generado por ventas del producto: {total_ventas}")
    else:
        print(f"No se encontraron ventas para el producto con código {codigo_producto}.")

Inventario = cargar_inventario()
Vendedores = cargar_vendedores()
ventas_realizadas = cargar_ventas()
ventas_producto = []

indice_vendedor = acceso(Vendedores)

while True:
    print("\nMenu:")
    print("1. Realizar una venta")
    print("2. Consultar inventario")
    print("3. Consultar ventas de toda la historia")
    print("4. Consultar ventas por vendedor")
    print("5. Consultar ventas por producto")
    print("6. Registrar un artículo")
    print("7. Registrar un vendedor")
    print("8. Salir")

    opcion = int(input("Selecciona una opción: "))

    if opcion == 1:
        ticket, total = realizar_venta(Inventario, Vendedores[indice_vendedor][0])
        ventas_realizadas.append([Vendedores[indice_vendedor][0], json.dumps(ticket), total])
        print(f"Venta registrada. Total: {total:.2f}")
    elif opcion == 2:
        mostrar_inventario(Inventario)
    elif opcion == 3:
        mostrar_ventas_sesion(ventas_realizadas)
    elif opcion == 4:
        mostrar_ventas_por_vendedor(ventas_realizadas)
    elif opcion == 5:
        mostrar_ventas_por_producto(ventas_realizadas)
    elif opcion == 6:
        registrar_articulo(Inventario)
        guardar_inventario(Inventario)
    elif opcion == 7:
        registrar_vendedor(Vendedores)
        guardar_vendedores(Vendedores)
    elif opcion == 8:
        guardar_ventas(ventas_realizadas)
        guardar_ventas_producto(ventas_producto)
        print("Saliendo del programa...")
        break
    else:
        print("Opción no válida.")