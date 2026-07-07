import json
import os

class AdministradorPersistencia:

    def __init__(self):

        self.ruta_inventario = os.path.join("Data", "inventario.json")

    def cargar_datos_primarios(self):

        if not os.path.exists(self.ruta_inventario):
            return []
        
        with open(self.ruta_inventario, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
        
    def guardar_datos(self, datos):
        with open(self.ruta_inventario, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)