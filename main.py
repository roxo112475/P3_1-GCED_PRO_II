from linked_ordered_positional_list import LinkedOrderedPositionalList as LOP
from array_ordered_positional_list import ArrayOrderedPositionalList as AOP

def read_orders(path="pedidos.txt"):
    lista_pedidos = []
    with open(path) as f:
        for l in f.readlines():
            ls = l.strip().split(",")
            customer, model_name = ls[0], ls[1]
            lista_pedidos.append([model_name, customer])
    return lista_pedidos

      
        
def procesar_pedidos(lista_pedidos:list):
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

    with open(path) as f:
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
    with open(path) as f:
        for l in f.readlines():
            ls = l.strip().split(",")
            model_name, part_name, qty = ls[0], ls[1], int(ls[2])
            piezas = (part_name, qty)
            
            if model_name not in catalogo.keys(): #Si el modelo aun no se ha registrado crea una LOP sobre la que añadir tuplas en vez de reescribirlas
                catalogo[model_name] = LOP()
                
            catalogo[model_name].add(piezas)
    return catalogo


def ensamblar(construccion: str): #Resta del inventario las partes necesarias para construir el coche (construccion)
    if isinstance( construccion, str):
        a  = catalogo[construccion]

    for _ in range(len(catalogo[construccion])):
        pieza, cantidad = (catalogo[construccion].get_element(a))
        
        a = catalogo[construccion].after(a) #Reiniciar el bucle para iterar sobre la LOP



if __name__ == "__main__":
    lista_pedidos = read_orders()
    while len(lista_pedidos) > 0: 
        inventario = read_parts() #array de partes disponibles
        catalogo = read_models() # diccionario de automóviles disponibles
        construccion = procesar_pedidos(lista_pedidos)

        print("---STOCK--- \n ")  #Imprimir el stock
        for elementos in inventario:
            print(*elementos)
        print()
        
        print("-----CATÁLOGO---- \n")    #Imprimir el catálogo
        for modelo, lista in catalogo.items():
            print("Modelo : ", modelo)
            frase = "| ".join(f"{pieza[0]}: {pieza[1]}" for pieza in lista)
            print(f"{frase} \n" )
