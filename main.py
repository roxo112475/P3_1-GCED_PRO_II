from linked_ordered_positional_list import LinkedOrderedPositionalList as LOP
from array_ordered_positional_list import ArrayOrderedPositionalList as AOP

def read_orders(path="pedidos.txt"):
    with open(path, encoding = 'utf8') as f:
        for l in f.readlines():
            ls = l.strip().split(",")
            customer, model_name = ls[0], ls[1]
            print("Nuevo pedido; Modelo: ", model_name , " | Cliente: ",customer)
            if model_name not in catalogo.keys():
                print("Pedido NO atendido. Modelo: ", model_name, "fuera del catalogo. \n")

            else:
                print(f"Modelo: {model_name}")
                for componentes in catalogo[model_name]:
                    print(*componentes)
                print()
                
           
            
            
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

    Precondition: Models must be ordered at .txt, don't repit a model after another appeared.

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



if __name__ == "__main__":

    inventario = read_parts() #array de partes disponibles
    catalogo = read_models() # diccionario de automóviles disponibles
    read_orders()

    print("\n -----STOCK----")  #Imprimir el stock
    for elementos in inventario:
        print(*elementos)
    print()
    
    print("\n -----CATÁLOGO----")    #Imprimir el catálogo
    for modelo, lista in catalogo.items():
        print("Modelo : ", modelo)
        frase = "| ".join(f"{pieza[0]}: {pieza[1]}" for pieza in lista)
        print(f"{frase} \n" )
