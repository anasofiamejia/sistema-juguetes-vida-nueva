from Modules.persistencia import AdministradorPersistencia
from Modules.triaje import Juguete
from Modules.usuarios import SistemaUsuarios

def ejecutar_sistema():
    
    print("=========================================")
    print("SISTEMA - JUGUETES VIDA NUEVA")
    print("=========================================\n")

    gestor_datos = AdministradorPersistencia()
    gestor_usuarios = SistemaUsuarios()

    print("--- INICIAR SESIÓN EN LA PLATAFORMA ---")
    correo_ingresado = input("Introduce tu correo electrónico: ")
    contrasena_ingresada = input("Introduce tu contraseña: ")
    print("\nVerificando credenciales...\n")

    usuario_activo = gestor_usuarios.autenticar(correo_ingresado, contrasena_ingresada)

    if not usuario_activo:
        print("Error: Correo o contraseña incorrectos. Acceso denegado.")
        return
    
    print(f"¡Bienvenido/a, {usuario_activo.nombre}!")
    print(f"Perfil detectado: [{usuario_activo.rol}]\n")
    print("=========================================\n")

    datos_juguetes = gestor_datos.cargar_datos_primarios()

    if not datos_juguetes:
        print("No se encontraron juguetes en el inventario.")
        return

    # Control de accesos y catálogos según el rol

    # Familia:
    if usuario_activo.rol == "Familia":
        print("¿Qué acción deseas realizar hoy?")
        print("1 - Ver Catálogo Comercial (Comprar)")
        print("2 - Registrar una nueva Donación (Donar)")
        
        opcion = input("Selecciona una opción (1 o 2): ")
        print("")

        if opcion == "1":
            print("[VISTA COMERCIAL] - Juguetes disponibles para compra:")
            for datos in datos_juguetes:
                if datos["triaje_resultado"] == "comprar":
                    objeto_juguete = Juguete(**datos)
                    objeto_juguete.mostrar_ficha_tecnica()
        
        elif opcion == "2":
            print("[FORMULARIO PARA DONAR]")
            print(f"Registrando intención de donación a nombre de: {usuario_activo.nombre}")
            nombre_juguete = input("¿Qué juguete deseas donar hoy?: ")
            print(f"\n¡Muchas gracias! Tu '{nombre_juguete}' ha sido pre-registrado en el sistema.")
            print("Por favor, acércate a nuestra tienda para realizar el triaje técnico de control de calidad.")

    # Fundación:
    elif usuario_activo.rol == "Fundación":
        print("¿Qué acción deseas realizar hoy?")
        print("1 - Ver Juguetes para donar (Solicitar Donaciones Gratuitas)")
        print("2 - Ver Catálogo Comercial (Comprar Juguetes)")
        
        opcion = input("Selecciona una opción (1 o 2): ")
        print("")

        if opcion == "1":
            print("[VISTA JUGUETES PARA DONAR] - Artículos asignados para donación gratuita:")
            for datos in datos_juguetes:
                if datos["triaje_resultado"] == "donar":
                    datos["precio_usd"] = 0.0
                    objeto_juguete = Juguete(**datos)
                    objeto_juguete.mostrar_ficha_tecnica()
        
        elif opcion == "2":
            print("[VISTA COMERCIAL PARA FUNDACIONES] - Juguetes disponibles para compra:")
            for datos in datos_juguetes:
                if datos["triaje_resultado"] == "comprar":
                    objeto_juguete = Juguete(**datos)
                    objeto_juguete.mostrar_ficha_tecnica()

    # Centro de Reciclaje:
    elif usuario_activo.rol == "Centro_Reciclaje":
        print("[INVENTARIO TÉCNICO DE RESIDUOS] - Materiales para procesamiento:")
        for datos in datos_juguetes:
            if datos["triaje_resultado"] == "reciclar":
                print(f"- Residuo ID: {datos['uuid']} | Material: {datos['material']} | Estado: {datos['estado_fisico']}")

    # Administrador y Operario:
    elif usuario_activo.rol in ["Administrador", "Operario"]:
        print(f"[VISTA OPERATIVA TOTAL] - Acceso concedido para el rol: {usuario_activo.rol}")
        print(f"Cargando los {len(datos_juguetes)} juguetes del inventario global...\n")
        for datos in datos_juguetes:
            objeto_juguete = Juguete(**datos)
            objeto_juguete.mostrar_ficha_tecnica()

if __name__ == "__main__":
    ejecutar_sistema()