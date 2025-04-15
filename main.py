from linked_ordered_positional_list import LinkedOrderedPositionalList as LOP
from array_ordered_positional_list import ArrayOrderedPositionalList as AOP

def read_orders(stock: AOP, path = "pedidos.txt") :
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
                if aval == True :
                    print(f'Pedido {model_name} atendido.')
                    update_stock(model_name, stock, catalogo) # actualiza el stock y el catalogo (catalogo en funcion auxiliar)
                else :
                    print(f'Pedido {model_name} NO atendido. Faltan:', end = '\t')
                    for part, number in aval.items() :
                        print(f'{part}-{number}', end = '\t')
                    print()
                    print()
        print()
    print()
    show_stock(inventario)
    return None


def update_stock(model_name: str, stock: AOP, catalogo: dict) :
    """
    Update the stock, if there is no more parts, delete this part from the stock storage and all the cars dependent

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
        while componentes[0] != stock[i][0] :
            i += 1
        componentes[1] -= stock[i][1]
        if stock[i][1] == 0 :
            deleted = stock[i].delete()
            print(f'Eliminada: Pieza {deleted}')
            dependent_car(catalogo, model_name, deleted)
    return None


def dependent_car(catalogo: dict, model_name: str, deleted: list) :
    """
    Delete all the cars dependent of a part.

    Attributes :
    ------------
        catalogo
    dict: cars avaliable to buy
        model_name
    string: car's name
        deleted
    list: first attribute is the string part's name, the second is a 0 (number of parts avaliable)

    Return :
    --------
        None
    """
    for i in catalogo[model_name] :
        if deleted[0] == catalogo[model_name][i][0] :
            catalogo[model_name].pop()
    return None


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
    for componentes in catalogo[model_name]:
        i = 0
        print(*componentes)
        print()
        while componentes[0] != stock.get_element(i)[0] :
            i += 1
        if componentes[1] < stock.get_element(i)[1] :
            comp = False
            none_avaliable[componentes[0]] = stock.get_element(i)[1] - componentes[1]
    if comp :
        return True
    else :
        return none_avaliable

            
            
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
                catalogo[model_name] = LOP()
                
            catalogo[model_name].add(piezas)
    return catalogo


def show_stock(inventario: AOP) :
    """
    Show the stock

    Atributtes :
    ------------
        inventario
    AOP : Lista de piezas
    Return :
    --------
        None
    """
    print("\n -----STOCK----")  #Imprimir el stock
    for elementos in inventario:
        print(*elementos)
    print()
    return None


def show_items(catalogo: dict) :
    """
    Show the avaliable items (cars).

    Attributes :
    ------------
        catalogo
    dict: dictionario of tuples with all parts the cars need

    Return :
    --------
        None
    """
    print("\n -----CATÁLOGO----")
    for modelo, lista in catalogo.items():
        print("Modelo : ", modelo)
        frase = "| ".join(f"{pieza[0]}: {pieza[1]}" for pieza in lista)
        print(f"{frase} \n" )
    return None


if __name__ == "__main__":

    ### 1 LEER Y MOSTRAR EL STOCK ###
    inventario = read_parts() #array de partes disponibles
    show_stock(inventario)  #Imprimir el stock
    
    ### 2 LECTURA DEL CATALOGO ###
    catalogo = read_models() # diccionario de automóviles disponibles

    ### 3 MOSTRAR EL CATALOGO ###
    show_items(catalogo) # imprime el catalogo

    ### 4 PROCESAR EL FICHERO DE PEDIDOS ###
    read_orders(inventario) 
    # queda eliminar los coches que no se puedan procesar (sin piezas),     las piezas q se hayan acabado (modtrar)   y   mostrar estado del stock

    ### 5 MOSTRAR CATÁLOGO ACTUALIZADO CON CAMBIOS ###
    # hasta que no se termine el paso 4 estará indicando lo mismo que en el 3
    show_items(catalogo) # imprime el catalogo final