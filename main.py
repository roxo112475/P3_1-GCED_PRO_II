from linked_ordered_positional_list import LinkedOrderedPositionalList as LOP
from array_ordered_positional_list import ArrayOrderedPositionalList as AOP

def read_orders(path="pedidos.txt"):
    with open(path) as f:
        for l in f.readlines():
            ls = l.strip().split(",")
            customer, model_name = ls[0], ls[1]
            print(f"Por hacer: procesar pedido {model_name} del cliente {customer}")
            
            
def read_parts(path="piezas.txt"):  #Abrir y leer el documento piezas, crear inventario 
    inventario = AOP()

    with open(path) as f:
        for l in f.readlines():
            ls = l.strip().split(",")
            part_name, qty = ls[0], int(ls[1])
            print(f"Por hacer: añadir al inventario la pieza \"{part_name}\" con ({qty} unidades)") 
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
            print(f"Por hacer: añadir al catálogo pieza \"{part_name}\" ({qty} unidades) al modelo \"{model_name}\"")
    return catalogo



if __name__ == "__main__":
    read_orders()
    
    inventario = read_parts() #array de partes disponibles
    catalogo = read_models() # diccionario de automóviles disponibles

    print("\n -----STOCK----")  #Imprimir el stock
    for elementos in inventario:
        print(*elementos)
    print()
    
    print("\n -----CATÁLOGO----")    #Imprimir el catálogo
    for modelo, lista in catalogo.items():
        print("Modelo : ", modelo)
        frase = "| ".join(f"{pieza[0]}: {pieza[1]}" for pieza in lista)
        print(f"{frase} \n" )