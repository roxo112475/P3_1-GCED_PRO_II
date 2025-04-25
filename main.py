#Manuel Omil Barreiro, Nicolas García Iglesias
#manuel.omil.barreiro@udc.es , nicola.garcia.iglesias@udc.es


from linked_ordered_positional_list import LinkedOrderedPositionalList as LOP
from array_ordered_positional_list import ArrayOrderedPositionalList as AOP

def read_orders(path="pedidos.txt"):
    """
    Read all the orders with the client´s name and its car model.
    Atributes :
     -----------
    path
    path of the txt where the program read the data.

    Return :
    --------
    lista_pedidos = a list containing all of the orders so they can be processed individually
    """

    lista_pedidos = []
    with open(path, encoding = 'utf8') as f:
        for l in f.readlines():
            ls = l.strip().split(",")
            customer, model_name = ls[0], ls[1]
            lista_pedidos.append([model_name, customer])
    return lista_pedidos
 
            
def read_parts(path="piezas.txt"):  #Abrir y leer el documento piezas, crear inventario
    """
    Read the whole part's inventory, name and number of parts.

     Atributes :
     -----------
        path
    path of the txt where the program read the data.

    Return :
    --------
        inventario 
    Array Ordered Positional List ; with the inventary
    """
    #Para asegurar que el programa funciona solo con AOPs o solo con LOPs
    try:
        inventario = AOP()
    except NameError:
        inventario = LOP()


    with open(path, encoding = 'utf8') as f:
        for l in f.readlines():
            ls = l.strip().split(",")
            part_name, qty = ls[0], int(ls[1])
            print(f'Por hacer: Añadir al inventario la pieza {part_name} con {qty} unidades')
            piezas = [part_name, qty]
            inventario.add(piezas)

        return inventario
    
def read_models(path="modelos.txt") :
    """
    Read the car's parts and return the models with their own parts and number of parts.

    Precondition: Models must be ordered at .txt, don't repit a model after another appeared.

    Atributes :
    -----------
        path
    File .txt where the program read the data.
    Return :
    --------
        catalogo
    dict; {model : (part, int number of parts)}
    """
    catalogo = {}
    with open(path, encoding = 'utf8') as f:
        for l in f.readlines():
            ls = l.strip().split(",")
            model_name, part_name, qty = ls[0], ls[1], int(ls[2])
            piezas = (part_name, qty)
            print(f'Por hacer: Añadir al catálogo pieza {part_name} con {qty} unidades.')

            if model_name not in catalogo.keys(): #Si el modelo aun no se ha registrado crea una LOP sobre la que añadir tuplas en vez de reescribirlas
                try:
                    catalogo[model_name] = LOP()
                except NameError:
                    catalogo[model_name] = AOP()
                
                
            catalogo[model_name].add(piezas)
    return catalogo

       
def procesar_pedidos(lista_pedidos:list, catalogo):
    """
    Takes a list of the orders and processes them one by one  filtering the models which dont exist
    on the catalogue and telling the program which model assemble next

    Returns:
    None if the model does not exist
    model_name: The name of the next model the program will try to assemble
    """
    while len(lista_pedidos) != 0: 
        pedido = lista_pedidos.pop(0)
        model_name = pedido[0]; customer = pedido[1]
        print("-------------")
        print("Nuevo pedido; Modelo: ", model_name , " | Cliente: ",customer)
        if model_name not in catalogo.keys():
            print("Pedido NO atendido. Modelo: ", model_name, "fuera del catalogo.")
            print("------------- \n")
            return

        else:
            print("-------------")
            print(f"Modelo: {model_name}")
            for componentes in catalogo[model_name]:
                print(*componentes, sep= " - ")
            print("-------------\n")
            
        return model_name

    
def comprobacion(en_construccion: str, inventario, catalogo):
    """Dado el nombre de un modelo, comprueba si se puede ensamblar o indica cuantas piezas faltan para ello"""
    if  en_construccion in catalogo.keys():
        piezas_faltantes = []
        resta_piezas = []

        modelo = catalogo.get(en_construccion) #El coche en cuestion
    
        pos = modelo.first()  # Obtener la primera posición de la lista LOP (las piezas necesarias para el coche )

        while pos is not None:
            pieza, cantidad = modelo.get_element(pos)
            pos = modelo.after(pos)

            # Buscar la pieza en el inventario de forma comparativa
            inv_pos = inventario.first()
            found = False

            while inv_pos is not None: #Parará después del ultimo (el after del ultimo sera None)
                pieza_inv = inventario.get_element(inv_pos)
                if pieza_inv[0] == pieza:  #Pieza_inv[0]  = Nombre pieza inventario
                    found = True
                    if pieza_inv[1] >= cantidad:
                        resta_piezas.append([pieza_inv[0], cantidad])                     
                    else:
                        piezas_faltantes.append([pieza_inv[0], abs((cantidad - pieza_inv[1]))])
                    break

                inv_pos = inventario.after(inv_pos)
            
            if not found:
                piezas_faltantes.append([pieza, cantidad])

        if len(piezas_faltantes) > 0:
            frase = "\n".join(f"{pieza[0]}: {pieza[1]}" for pieza in piezas_faltantes)
            print(f"\nPedido NO atendido: Faltan:")
            print(frase,  "\n")
            

            catalogo.pop(en_construccion)
            print(f"El modelo {en_construccion} ha sido eliminado del catálogo")                        
            return None #Acaba la funcion tras eliminar el coche del catalogo
            
        else:
            return resta_piezas



def ensamblar(inventario, en_construccion, catalogo):
    resta_piezas = comprobacion(en_construccion, inventario, catalogo)
    if resta_piezas is None:
        return  # Exit the function if comprobacion returned None

    else:  # Caso de que el coche se pueda ensamblar
        for nombre, cantidad in resta_piezas:
            inv_pos = inventario.first()

            while inv_pos is not None:
                pieza_inv = inventario.get_element(inv_pos)
                
                if pieza_inv[0] == nombre:
                    if pieza_inv[1] >= cantidad:
                        pieza_inv[1] -= cantidad
                    
                    if pieza_inv[1] == 0:
                        print(f"* Eliminada: Pieza {nombre}")
                        inventario.delete(inv_pos)  # Eliminar del stock la pieza
                        modelos_dependientes(nombre ,catalogo)
                    break  

                inv_pos = inventario.after(inv_pos)
        print(f"Pedido {en_construccion} atendido.\n")


def modelos_dependientes(pieza, catalogo):
    "Checks for every car model that uses the piece that the stock ran out of"

    modelos_a_eliminar = []

    for modelo, lista_piezas in catalogo.items():
        pos = lista_piezas.first()
        while pos is not None:
            pieza_modelo, _ = lista_piezas.get_element(pos)
            if pieza_modelo == pieza: #Si la pieza en cuestion esta en el modelo, se guarda en la lista de modelos a eliminar
                modelos_a_eliminar.append(modelo)
                break
            pos = lista_piezas.after(pos) #Si no encuentra nada, saltar al siguiente 

    for modelo in modelos_a_eliminar:
        catalogo.pop(modelo)
        print(f"- Eliminado: Modelo {modelo} dependiente")
    print()




if __name__ == "__main__":
    ## PASO 1. Leer inventario y mostrarlo ##
    inventario = read_parts() #array de partes disponibles

    print("---STOCK---")  #Imprimir el stock
    for elementos in inventario:
        print(*elementos)
    print()

    ## PASO 2. Lectura del catálogo ##
    catalogo = read_models() # diccionario de automóviles disponibles
    
    ## PASO 3. Mostramos el catálogo ##
    print("---CATÁLOGO----- \n")    #Imprimir el catálogo
    for modelo, lista in catalogo.items():
        print("Modelo : ", modelo)
        frase = "| ".join(f"{pieza[0]}: {pieza[1]}" for pieza in lista)
        print(f"{frase} \n" )
    
    ## PASO 4. Procesamos el fichero con los pedidos de los clientes ##
    lista_pedidos = read_orders() #Lista de los pedidos, sirve de condicion de stop de la simulacion
    
    while len(lista_pedidos) > 0: 

        en_construccion = procesar_pedidos(lista_pedidos,catalogo) #retorna el modelo a ensamblar
        ensamblar(inventario, en_construccion, catalogo) # intenta ensamblar e indica si hay un error 



        print("---STOCK---")  #Imprimir el stock
        for elementos in inventario:
            print(*elementos)
        print()
        
        print("---CATÁLOGO----- \n")    #Imprimir el catálogo
        for modelo, lista in catalogo.items():
            print("Modelo : ", modelo)
            frase = "| ".join(f"{pieza[0]}: {pieza[1]}" for pieza in lista)
            print(f"{frase} \n" )

print("\n**FIN DE LOS PEDIDOS**\n")