from linked_ordered_positional_list import LinkedOrderedPositionalList as AOP
from array_ordered_positional_list import ArrayOrderedPositionalList as LOP

def read_orders(stock: AOP, catalogo: dict, path = "pedidos.txt") :
    """
    Read the car's orders.

    Attributes :
    ------------
        path
    the txt where the progrem reads the data

    Return :
    --------
        None
    """
    print()
    print()
    with open(path, encoding = 'utf8') as f:
        for l in f.readlines():
            ls = l.strip().split(",")
            customer, model_name = ls[0], ls[1]
            print("Nuevo pedido:", model_name , customer)
            if model_name not in catalogo.keys():
                print("Pedido NO atendido.", model_name, "fuera del catálogo. \n")

            else:
                print(f"Modelo: {model_name}")
                aval = avaliability(stock, catalogo, model_name) # comprueba que se puede atender al pedido
                if aval :
                    print(f'Pedido {model_name} atendido.')
                    update_stock(model_name, stock, catalogo) # actualiza el stock y el catalogo (catalogo en funcion auxiliar)
                    show_items(catalogo)
                    catalogo = dependent_car(stock, catalogo) # revisa si por falta de stock hay algun coche del catalogo que no pueda fabricarse y lo elimina
                    show_items(catalogo)
                else :
                    none_avaliable = avaliability(stock, catalogo, model_name)
                    print(f'Pedido {model_name} NO atendido. Faltan:', end = '\t')
                    for part, number in none_avaliable.items() :
                        print(f'{part}-{number}', end = '\t')
                    print()
    show_stock(inventario)
    return None


def update_stock(model_name: str, stock: AOP, catalogo: dict) : # algo no va bien
    """
    Update the stock, if there is no more parts, delete this part from the stock storage and all the cars dependent

    Precondition: the number of parts must be equal or more than the needed parts

    Attributes :
    ------------
        model_name
    string: car's name
        stock
    AOP: stock storage of parts

    Return :
    --------
        None
    """
    for componentes in catalogo[model_name]:
        i = 0
        while componentes[0] != stock.get_element(i)[0] :
            if i >= len(stock) - 1 :
                break
            i += 1
        if i < len(stock) - 1 :
            stock.get_element(i)[1] -= componentes[1]

        if stock.get_element(i)[1] == 0 :
            deleted = stock.delete(i)[0]
            print(f'Eliminada: Pieza {deleted}')
            
    return None


def dependent_car(stock: AOP, catalogo: dict) :
    """
    Delete all the cars dependent of a part.

    Attributes :
    ------------
        catalogo
    dict: cars avaliable to buy
        stock
    AOP: parts stock

    Return :
    --------
        None
    """
    catalogo_copy = catalogo.copy()
    for model in catalogo :
        for part in catalogo[model] :
            i = 0
            while part[0] != stock.get_element(i)[0] and len(stock) > i :
                i += 1
            if i >= len(stock) : # no existe esa pieza en el stock
                catalogo_copy.pop(model)
                break
            elif part[1] < stock.get_element(i)[1] : # no hay suficientes piezas
                catalogo_copy.pop(model)
                break
    return catalogo_copy


def avaliability(stock: AOP, catalogo: dict, model_name: str) :
    """
    Look for the part's avaliability, if there's some parts with not enough storage, return it.

    Attributes :
    ------------
        stock
    AOP: part's storage
        catalogo
    dict: cars and parts they use
        model_name
    string: car's name
    """
    comp = True
    none_avaliable = {}
    print()
    for componentes in catalogo[model_name]:
        i = 0
        print(*componentes)
        while componentes[0] != stock.get_element(i)[0] :
            if i == len(stock) - 1 : # evita el bucle infinito si no encuentra una pieza en el stock
                break
            i += 1
        if i > len(stock) - 1 : # en el caso de q no haya una pieza en stock devuelve que faltan el numero de piezas necesarias (ejemplo: Motor 5) porque hay 0 en stock
            comp = False
            none_avaliable[componentes[0]] = componentes[1]
        elif componentes[1] < stock.get_element(i)[1] :
            comp = False
            none_avaliable[componentes[0]] = componentes[1] - stock.get_element(i)[1]

    if comp :
        yield True
    else :
        yield False
        yield none_avaliable

            
            
def read_parts(path="piezas.txt"):  #Abrir y leer el documento piezas, crear inventario
    """
    Read the whole part's inventary, name and number of parts.

     Atributes :
     -----------
        path
    path of the txt where the program read the data.

    Return :
    --------
        inventario 
    Array Ordered Positional List ; with the inventary
    """
    inventario = AOP()

    with open(path, encoding = 'utf8') as f:
        for l in f.readlines():
            ls = l.strip().split(",")
            part_name, qty = ls[0], int(ls[1])
            print(f"Por hacer: añadir al inventario la pieza \"{part_name}\" con ({qty} unidades)")   

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
    models = {}
    with open(path) as f:
        for l in f.readlines():
            ls = l.strip().split(",")
            model_name, part_name, qty = ls[0], ls[1], int(ls[2])
            models[model_name] = (part_name, qty)
            print(f"Por hacer: añadir al catálogo pieza \"{part_name}\" ({qty} unidades) al modelo \"{model_name}\"")
    return models
			
if __name__ == "__main__":

    ### 1 LEER Y MOSTRAR EL STOCK ###
    inventario = read_parts() #array de partes disponibles
    show_stock(inventario)  #Imprimir el stock
    
    ### 2 LECTURA DEL CATALOGO ###
    catalogo = read_models() # diccionario de automóviles disponibles

    ### 3 MOSTRAR EL CATALOGO ###
    show_items(catalogo) # imprime el catalogo

    ### 4 PROCESAR EL FICHERO DE PEDIDOS ###
    read_orders(inventario, catalogo) 
    # queda eliminar los coches que no se puedan procesar (sin piezas),     las piezas q se hayan acabado (modtrar)   y   mostrar estado del stock

    ### 5 MOSTRAR CATÁLOGO ACTUALIZADO CON CAMBIOS ###
    # hasta que no se termine el paso 4 estará indicando lo mismo que en el 3
    show_items(catalogo) # imprime el catalogo final