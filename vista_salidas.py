import flet as ft
from Modules.salidas import GestorSalidas
import json

def crear_vista_salidas(page, usuario, renderizar_menu_por_rol):
    # Cargar juguetes disponibles para el Dropdown (desplegable)
    def obtener_juguetes_disponibles():
        try:
            with open("Data/inventario.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    juguetes = obtener_juguetes_disponibles()
    
    # Elementos de la interfaz
    txt_titulo = ft.Text("REGISTRO DE SALIDA DE JUGUETES", size=20, weight=ft.FontWeight.BOLD, color="#0F4C5C")
    
    # Dropdown para elegir el juguete
    dropdown_juguete = ft.Dropdown(
        label="Selecciona el Juguete",
        width=400,
        options=[ft.dropdown.Option(key=str(j.get("id") or j.get("uuid")), text=f"{j['nombre'].upper()} ({j['triaje_resultado'].upper()})") for j in juguetes]
    )
    
    # Dropdown para el tipo de salida
    dropdown_tipo = ft.Dropdown(
        label="Tipo de Salida",
        width=400,
        options=[
            ft.dropdown.Option("venta", "Venta Comercial"),
            ft.dropdown.Option("donacion", "Donación Social"),
            ft.dropdown.Option("reciclaje", "Envío a Recicladora")
        ]
    )
    
    # Input para el destino especifico
    tf_destino = ft.TextField(label="Destinatario / Entidad Destino (Ej: Fundación Niños Sonrientes, Cliente Juan)", width=400)
    
    # Texto para mostrar mensajes de éxito o error
    lbl_mensaje = ft.Text("", size=14, weight=ft.FontWeight.BOLD)

    def procesar_formulario(e):
        if not dropdown_juguete.value or not dropdown_tipo.value or not tf_destino.value:
            lbl_mensaje.value = "Por favor, completa todos los campos del formulario."
            lbl_mensaje.color = "red"
            page.update()
            return
        
        # Ejecutar la lógica de negocio
        exito, msg = GestorSalidas.registrar_salida(
            juguete_id=dropdown_juguete.value,
            tipo_salida=dropdown_tipo.value,
            detalle_destino=tf_destino.value
        )
        
        if exito:
            lbl_mensaje.value = msg
            lbl_mensaje.color = "green"
            # Limpiar campos y recargar dropdown de juguetes
            tf_destino.value = ""
            dropdown_juguete.value = None
            dropdown_tipo.value = None
            # Recargar la lista de juguetes disponibles por si se quiere hacer otra salida
            nuevos_juguetes = obtener_juguetes_disponibles()
            dropdown_juguete.options = [ft.dropdown.Option(key=str(j.get("id") or j.get("uuid")), text=f"{j['nombre'].upper()} ({j['triaje_resultado'].upper()})") for j in nuevos_juguetes]
        else:
            lbl_mensaje.value = msg
            lbl_mensaje.color = "red"
            
        page.update()

    btn_guardar = ft.ElevatedButton("Confirmar Salida", on_click=procesar_formulario, bgcolor="#0F4C5C", color="white")
    
    btn_volver = ft.ElevatedButton(
        content=ft.Text("Atrás", color="white"),
        bgcolor="#0F4C5C",
        on_click=lambda _: renderizar_menu_por_rol(usuario)
    )

    page.controls.clear()

    # Añadir todo a la vista organizada de forma segura (Cero pantallas rosas)
    page.add(
        ft.Row([
            ft.Container(
                content=ft.Column([
                    ft.Row([txt_titulo, btn_volver], alignment="spaceBetween"), # 💡 Corregido a string
                    ft.Divider(height=10, color="transparent"),
                    dropdown_juguete,
                    dropdown_tipo,
                    tf_destino,
                    ft.Divider(height=10, color="transparent"),
                    btn_guardar,
                    lbl_mensaje
                ], horizontal_alignment="center"), # 💡 Corregido a string
                padding=30,
                width=450 
            )
        ], alignment="center") # 💡 Corregido a string
    )
    
    page.update()