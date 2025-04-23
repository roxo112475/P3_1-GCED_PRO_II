from linked_ordered_positional_list import LinkedOrderedPositionalList as LOP
from array_ordered_positional_list import ArrayOrderedPositionalList as AOP

def read_orders(path="pedidos.txt"):
    lista_pedidos = []
    with open(path, encoding = 'utf8') as f:
        for l in f.readlines():
            ls = l.strip().split(",")
            customer, model_name = ls[0], ls[1]
            lista_pedidos.append([model_name, customer])
    return lista_pedidos

      
        
def procesar_pedidos(lista_pedidos:list):
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
            print("Pedido NO atendido. Modelo: ", model_name, "fuera del catalogo. \n")
            print("-------------")
            return

        else:
            print("-------------")
            print(f"Modelo: {model_name}")
            for componentes in catalogo[model_name]:
                print(*componentes)
            print("-------------")
            print()
        return model_name

    
            
def read_parts(path="piezas.txt"):  #Abrir y leer el documento piezas, crear inventario 
    inventario = AOP()

    with open(path, encoding = 'utf8') as f:
        for l in f.readlines():
            ls = l.strip().split(",")
            part_name, qty = ls[0], int(ls[1])
            piezas = [part_name, qty]
            inventario.add(piezas)

        return inventario
    
    


def read_models(path="modelos.txt") :
    """
    Read the car's parts and return the models with their own parts and number of parts.

    Atributes :
    -----------
        path
    File .txt where the program read the data.
    Return :
    --------
        dict : {model : (part, int number of parts)}
    """
    catalogo = {}
    with open(path, encoding = 'utf8') as f:
        for l in f.readlines():
            ls = l.strip().split(",")
            model_name, part_name, qty = ls[0], ls[1], int(ls[2])
            piezas = (part_name, qty)
            
            if model_name not in catalogo.keys(): #Si el modelo aun no se ha registrado crea una LOP sobre la que añadir tuplas en vez de reescribirlas
                catalogo[model_name] = LOP()
                
            catalogo[model_name].add(piezas)
    return catalogo


def ensamblar(construccion: str, inventario, catalogo):
    """Dado el nombre de un modelo, intenta ensamblarlo restando las piezas necesarias del inventario"""
    if  construccion in catalogo.keys():
    
        modelo = catalogo.get(construccion) #El coche en cuestion
    
        pos = modelo.first()  # Obtener la primera posición de la lista LOP

        while pos is not None:
            pieza, cantidad = modelo.get_element(pos)
            pos = modelo.after(pos)
    
            # Buscar la pieza en el inventario de forma comparativa
            inv_pos = inventario.first()

            found = False
            while inv_pos is not None: #Parará después del ultimo (el after del ultimo sera None)
                pieza_inv = inventario.get_element(inv_pos)
                if pieza_inv[0] == pieza: #Nombre pieza inventario
                    found = True
                    if pieza_inv[1] >= cantidad:
                        pieza_inv[1] -= cantidad
                        
                    else:
                        print(f"No hay suficientes unidades de '{pieza}' para ensamblar el modelo {construccion}.")
                        catalogo.pop(construccion)
                        print(f"El modelo {construccion} ha sido eliminado del catálogo")                        
                        return #Acaba la funcion tras detectar que falta al menos una pieza; elimina el coche del catalogo
                    
                inv_pos = inventario.after(inv_pos)
            
            if not found:
                catalogo.pop(construccion)
                print(f"Pieza '{pieza}' no encontrada en el inventario.")
    
            


if __name__ == "__main__":
    lista_pedidos = read_orders() #Lista de los pedidos, sirve de condicion de stop de la simulacion
    inventario = read_parts() #array de partes disponibles
    catalogo = read_models() # diccionario de automóviles disponibles
    
    while len(lista_pedidos) > 0: 

        construccion = procesar_pedidos(lista_pedidos) #retorna el modelo a ensamblar
        ensamblar(construccion, inventario, catalogo) # intenta ensamblar e indica si hay un error 

        print("---STOCK--- \n ")  #Imprimir el stock
        for elementos in inventario:
            print(*elementos)
        print()
        
        print("-----CATÁLOGO---- \n")    #Imprimir el catálogo
        for modelo, lista in catalogo.items():
            print("Modelo : ", modelo)
            frase = "| ".join(f"{pieza[0]}: {pieza[1]}" for pieza in lista)
            print(f"{frase} \n" )


 