from Modules.juguete import Juguete

class GestorCatalogos:
    def __init__(self, administrador_persistencia):
        
        self.persistencia = administrador_persistencia

    def _convertir_inventario_a_objetos(self):
        
        datos_crudos = self.persistencia.cargar_datos_primarios()
        return [Juguete.desde_diccionario(item) for item in datos_crudos]
    
    def obtener_catalogo_comercial(self):
        
        todos = self._convertir_inventario_a_objetos()
        return [j for j in todos if j.triaje_resultado == "venta"]

    def obtener_catalogo_social(self):
        
        todos = self._convertir_inventario_a_objetos()
        return [j for j in todos if j.triaje_resultado == "donacion"]

    def obtener_catalogo_residuos(self):
       
        todos = self._convertir_inventario_a_objetos()
        return [j for j in todos if j.triaje_resultado == "reciclaje"]