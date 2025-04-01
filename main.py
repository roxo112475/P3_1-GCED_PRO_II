from linked_ordered_positional_list import LinkedOrderedPositionalList as ListaOrdenada
from array_ordered_positional_list import ArrayOrderedPositionalList as ListaOrdenada

def read_orders(path="pedidos.txt"):
    with open(path) as f:
        for l in f.readlines():
            ls = l.strip().split(",")
            customer, model_name = ls[0], ls[1]
            print(f"Por hacer: procesar pedido {model_name} del cliente {customer}")

def read_parts(path="piezas.txt"):
    with open(path) as f:
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
    read_parts()
    models = read_models() 
    read_orders()
    print(models) # printea el diccionario de automóviles