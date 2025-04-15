class Piezas:
    def __init__(self, nombre, cantidad):
        self._nombre = nombre      
        self._cantidad = cantidad  


    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, nombre):
        if not isinstance(nombre, str):
            raise ValueError("El nombre debe ser una cadena de texto (str).")
        self._nombre = nombre

 
    @property
    def cantidad(self):
        return self._cantidad


    @cantidad.setter
    def cantidad(self, cantidad):
        if not isinstance(cantidad, int):
            raise ValueError("La cantidad debe ser un entero (int).")
        if cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa.")
        self._cantidad = cantidad

    def __str__(self):
        return f"Nombre de pieza: {self._nombre}, cantidad: {self._cantidad}"

    def __len__(self): #Es necesario que la clase tenga una long para que funcione en la AOP
        return 2

a = Piezas("Motor", 5)      
print(a)
print(len(a))