import json
import os

class Usuario:

    def __init__(self, correo, contrasena, nombre, rol):

        self.correo = correo
        self.contrasena = contrasena
        self.nombre = nombre
        self.rol = rol


class SistemaUsuarios:
    
    def __init__(self):
      
        self.ruta_archivo = os.path.join("Data", "usuarios.json")
        self.usuarios = self.cargar_usuarios()

    def cargar_usuarios(self):
       
        if not os.path.exists(self.ruta_archivo):
            return []
            
        try:
            with open(self.ruta_archivo, "r", encoding="utf-8") as f:
                datos = json.load(f)  

                lista_usuarios_objetos = []
                
                for u in datos:
                    nuevo_usuario = Usuario(
                        correo=u["correo"],
                        contrasena=u["contrasena"],
                        nombre=u["nombre"],
                        rol=u["rol"]
                    )
                    
                    lista_usuarios_objetos.append(nuevo_usuario)
                
                return lista_usuarios_objetos
                
        except Exception:
            
            return []
        
    def autenticar(self, correo, contrasena):
        
        for usuario in self.usuarios:
            
            if usuario.correo == correo and usuario.contrasena == contrasena:
                return usuario
        
        return None