import json
import flet as ft
from Modules.usuarios import SistemaUsuarios
from Modules.persistencia import AdministradorPersistencia

from Modules.catalogos import GestorCatalogos
from vista_catalogos import ComponenteCatalogos
from vista_salidas import crear_vista_salidas
from vista_historial import crear_vista_historial
from vista_catalogos import abrir_pantalla_catalogo
from vista_reportes import crear_vista_reportes

def main(page: ft.Page):

    
    # Ventana principal:

    page.title = "JUGUETES VIDA NUEVA"
    page.window_width = 500
    page.window_height = 760
    page.theme_mode = ft.ThemeMode.LIGHT
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.SPACE_BETWEEN
    page.padding = 0
    page.bgcolor = "white"

   
    gestor_usuarios = SistemaUsuarios()
    gestor_datos = AdministradorPersistencia()

    
    # Componenetes visuales del login:
    
    container_logo = ft.Image(
        src="logo.png",         
        width=200,
        height=200,
        fit="contain"
    )

    container_logo_con_margen = ft.Container(
        content=container_logo,
        margin=ft.Padding(0, 20, 0, 0) 
    )

    txt_correo = ft.TextField(
        label="Correo Electrónico", 
        width=380, 
        border_color="grey400", 
        label_style=ft.TextStyle(color="bluegrey700"),
        prefix_icon="email" 
    )
    
    txt_contrasena = ft.TextField(
        label="Contraseña", 
        password=True, 
        can_reveal_password=True, 
        width=380, 
        border_color="grey400", 
        label_style=ft.TextStyle(color="bluegrey700"),
        prefix_icon="lock" 
    )
    
    lbl_mensaje_error = ft.Text(
        "", 
        size=13, 
        color="redaccent700", 
        weight=ft.FontWeight.W_500
    )

    # Lógica al activar el Login:
    def desencadenar_login(e):
        usuario_activo = gestor_usuarios.autenticar(txt_correo.value, txt_contrasena.value)
        if usuario_activo:
            lbl_mensaje_error.value = ""
            renderizar_menu_por_rol(usuario_activo)
        else:
            lbl_mensaje_error.value = "Credenciales incorrectas. Verifique e intente de nuevo."
            page.update()

    btn_login = ft.ElevatedButton(
        content=ft.Text("Iniciar Sesión", color="white", weight=ft.FontWeight.BOLD, size=16),
        width=380,
        height=48,
        on_click=desencadenar_login,
        style=ft.ButtonStyle(
            bgcolor="#4DD0E1",
            shape=ft.RoundedRectangleBorder(radius=6),
        )
    )

    # Componentes parte inferior del Login:
    linea_decorativa = ft.Container(height=3, bgcolor="#4DD0E1")

    columna_izquierda = ft.Column([
        ft.Row([
            ft.Icon("info", color="#0F4C5C", size=16), 
            ft.Text("REPORTE DE IMPACTO", size=11, weight=ft.FontWeight.BOLD, color="white")
        ], spacing=5),
        ft.Container(
            padding=ft.Padding(21, 2, 0, 2),
            content=ft.Text("   SOPORTE TÉCNICO", size=11, weight=ft.FontWeight.BOLD, color="bluegrey200")
        ),
    ], spacing=4, horizontal_alignment=ft.CrossAxisAlignment.START)

    columna_derecha = ft.Column([
        ft.Text("REGISTRARSE (SOLO CLIENTES)", size=11, weight=ft.FontWeight.W_500, color="white", text_align=ft.TextAlign.RIGHT),
        ft.Text("RECOBRAR ACCESO (CONTRASEÑA)", size=11, weight=ft.FontWeight.W_500, color="white", text_align=ft.TextAlign.RIGHT),
    ], spacing=6, horizontal_alignment=ft.Alignment(0, 0)
    ) 

    contenedor_enlaces = ft.Container(
        content=ft.Row(
            controls=[columna_izquierda, columna_derecha],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ),
        bgcolor="#4DD0E1", 
        padding=15, 
        height=68
    )

    barra_estado = ft.Container(
        content=ft.Text(
            "SESIÓN ACTUAL: VISITANTE", 
            
        ),
        bgcolor="white",
        padding=8,
        alignment=ft.Alignment(0, 0)  
    )

    
    # Lógica de Menús y Cátalogos:

    def renderizar_menu_por_rol(usuario):
        page.controls.clear() 
        page.vertical_alignment = ft.MainAxisAlignment.START
        
        gestor_catalogos = GestorCatalogos(gestor_datos)

        def mostrar_pantalla_catalogo(titulo_vista, tipo_catalogo):
            page.controls.clear()
        
            # 1. ENCABEZADO DE LA VISTA DEL CATÁLOGO
            page.add(
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Text(titulo_vista.upper(), size=20, weight=ft.FontWeight.BOLD, color="#0F4C5C"),
                            
                            # Botón Atrás universal compatible
                            ft.ElevatedButton(
                                content=ft.Text("Atrás", color="white"),
                                bgcolor="#0F4C5C",
                                on_click=lambda _: renderizar_menu_por_rol(usuario)
                            )
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ]),
                    padding=20
                ),
                ft.Divider(height=1, color="grey300")
            )

            zona_render = ft.Column(spacing=15, scroll=ft.ScrollMode.AUTO, expand=True)
            lista_juguetes = []

            # 2. CATÁLOGO COMERCIAL (CLIENTES)
            if tipo_catalogo == "comercial":
                lista_juguetes = gestor_catalogos.obtener_catalogo_comercial()
                malla = ft.Row(wrap=True, spacing=15, run_spacing=15)
                for j in lista_juguetes:
                    malla.controls.append(ComponenteCatalogos.crear_tarjeta_comercial_social(j))
                zona_render.controls.append(malla)

            # 3. CATÁLOGO SOCIAL (FUNDACIONES)
            elif tipo_catalogo == "social":
                lista_juguetes = gestor_catalogos.obtener_catalogo_social()
                malla = ft.Row(wrap=True, spacing=15, run_spacing=15)
                for j in lista_juguetes:
                    malla.controls.append(ComponenteCatalogos.crear_tarjeta_comercial_social(j))
                zona_render.controls.append(malla)

            # 4. CATÁLOGO DE RESIDUOS (RECICLADORAS)
            elif tipo_catalogo == "residuos":
                lista_juguetes = gestor_catalogos.obtener_catalogo_residuos()
                tabla = ComponenteCatalogos.crear_tabla_residuos(lista_juguetes)
                zona_render.controls.append(ft.Row([tabla], scroll=ft.ScrollMode.AUTO))

            if not lista_juguetes:
                zona_render.controls.append(
                    ft.Text("No hay registros en este catálogo actualmente.", italic=True, color="bluegrey400")
                )

            page.add(ft.Container(content=zona_render, padding=20, expand=True))
            page.update()

        # Diseño del menú principal centrado
        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Text("Juguetes Vida Nueva", size=24, weight=ft.FontWeight.BOLD, color="#4DD0E1", text_align=ft.TextAlign.CENTER),
                    ft.Text('"Porque todos merecemos una segunda oportunidad"', size=14, italic=True, color="bluegrey600", text_align=ft.TextAlign.CENTER),
                    ft.Container(height=10),
                    
                    ft.Container(
                        content=ft.Text(f"Panel: {usuario.rol} | Activo: {usuario.nombre}", size=14, weight=ft.FontWeight.W_500, color="bluegrey700"),
                        alignment=ft.alignment.Alignment(-1, 0) # Izquierda absoluta infalible
                    ),
                ], 
                alignment=ft.MainAxisAlignment.CENTER, 
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                padding=20,
                alignment=ft.alignment.Alignment(0, 0) # Centro absoluto infalible
            ),
            ft.Divider(height=1, color="grey300")
        )

        bloque_acciones = ft.Column(spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER, width=400)

        # CONTROL DE ACCIONES POR ROL (Utilizando 'content' y 'style' tradicionales)
        if usuario.rol == "Familia":
            bloque_acciones.controls.extend([
                ft.ElevatedButton(
                    content=ft.Text("Ver Catálogo Comercial (Comprar)", color="white"), 
                    width=350, style=ft.ButtonStyle(bgcolor="orange"),
                    on_click=lambda _: mostrar_pantalla_catalogo("Catálogo Comercial", "comercial")
                ),
                ft.ElevatedButton(
                    content=ft.Text("Registrar una nueva Donación (Donar)", color="white"), 
                    width=350, style=ft.ButtonStyle(bgcolor="purple"),
                    on_click=lambda _: abrir_info_donacion(page)
                )
            ])
        elif usuario.rol == "Fundación":
            bloque_acciones.controls.extend([
                ft.ElevatedButton(
                    content=ft.Text("Ver Artículos para Donación (Gratuitos)", color="white"), 
                    width=350, style=ft.ButtonStyle(bgcolor="purple"),
                    on_click=lambda _: mostrar_pantalla_catalogo("Artículos para Donación", "social")
                ),
                ft.ElevatedButton(
                    content=ft.Text("Ver Catálogo Comercial (Comprar)", color="white"), 
                    width=350, style=ft.ButtonStyle(bgcolor="orange"),
                    on_click=lambda _: mostrar_pantalla_catalogo("Catálogo Comercial", "comercial")
                )
            ])
        elif usuario.rol == "Centro_Reciclaje":
            bloque_acciones.controls.extend([
                ft.ElevatedButton(
                    content=ft.Text("Ver Inventario de Residuos", color="white"), 
                    width=350, style=ft.ButtonStyle(bgcolor="green"),
                    on_click=lambda _: mostrar_pantalla_catalogo("Inventario de Residuos", "residuos")
                )
            ])
        elif usuario.rol in ["Administrador", "Operario"]:
            bloque_acciones.controls.extend([
                ft.ElevatedButton(
                    content=ft.Text("Vista Operativa Global de Inventario", color="white"), 
                    width=350, style=ft.ButtonStyle(bgcolor="#4DD0E1"),
                    on_click=lambda _: cargar_pantalla_tecnica(page, usuario, renderizar_menu_por_rol)
                ), 
                ft.ElevatedButton(
                    content=ft.Text("Registrar e Ingresar Juguete", color="white"), 
                    width=350, style=ft.ButtonStyle(bgcolor="#26A69A"),
                    on_click=lambda _: abrir_formulario_ingreso(page, usuario, renderizar_menu_por_rol)
                ), 
                ft.ElevatedButton(
                    content=ft.Text("Registrar Salida de Juguetes", color="white"),
                    width=350, style=ft.ButtonStyle(bgcolor="#0F4C5C"),
                    on_click=lambda _: crear_vista_salidas(page, usuario, renderizar_menu_por_rol)
                ),
                ft.ElevatedButton(
                    content=ft.Text("Historial / Devoluciones", color="white"),
                    width=350, style=ft.ButtonStyle(bgcolor="#E2711D"),
                    on_click=lambda _: crear_vista_historial(page, usuario, renderizar_menu_por_rol)
                ),
            ])
            
            if usuario.rol == "Administrador":
                bloque_acciones.controls.append(
                    ft.ElevatedButton(
                        content=ft.Text("Visualizar Reporte de Impacto Ambiental", color="white"), 
                        width=350, style=ft.ButtonStyle(bgcolor="#0F4C5C"),
                        icon="poll",
                        on_click=lambda _: crear_vista_reportes(page, usuario, renderizar_menu_por_rol)
                    )
                )

        page.add(ft.Container(content=bloque_acciones, padding=30, alignment=ft.alignment.Alignment(0, 0)))
        page.update()

        
    
    formulario_login = ft.Column(
        controls=[
            container_logo,
            ft.Container(height=5),
            txt_correo,
            txt_contrasena,
            lbl_mensaje_error,
            ft.Container(height=5),
            btn_login,
        ],
        spacing=8,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER 
    )

    bloque_pie_pagina = ft.Column(
        controls=[
            linea_decorativa,
            contenedor_enlaces,
            barra_estado
        ],
        spacing=0
    )

    diseno_pantalla_completa = ft.Column(
        controls=[
            # Quitamos el alignment="center" problemático de aquí
            ft.Container(
                content=formulario_login, 
                expand=True
            ),
            # El pie de página se acopla abajo con su espacio real
            bloque_pie_pagina
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        expand=True 
    )

    page.spacing = 0
    page.padding = 0

    page.window_width = 500
    page.window_height = 760
    
    page.add(diseno_pantalla_completa)

def cargar_pantalla_tecnica(page, usuario, volver_menu_fn):
    import json
    page.controls.clear()
    
    # 1. Título y botón de atrás seguro
    page.add(
        ft.Container(
            content=ft.Row([
                ft.Text("INVENTARIO TÉCNICO GLOBAL", size=20, weight=ft.FontWeight.BOLD, color="#0F4C5C"),
                ft.ElevatedButton("Atrás", bgcolor="#0F4C5C", color="white", on_click=lambda _: volver_menu_fn(usuario))
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=20
        )
    )
    
    # 2. Intentar cargar los juguetes para pasárselos a tu tabla
    try:
        with open("Data/inventario.json", "r", encoding="utf-8") as f:
            datos = json.load(f)
            
        class JugueteObjeto:
            def __init__(self, d):
                self.uuid = d.get("uuid", "n/a")
                self.nombre = d.get("nombre", "n/a")
                self.material = d.get("material", "n/a")
                self.alto_cm = d.get("alto_cm", 0)
                self.ancho_cm = d.get("ancho_cm", 0)
                self.largo_cm = d.get("largo_cm", 0)
        
        lista_objetos = [JugueteObjeto(j) for j in datos]
        
        # 3. Llamar a tu componente de tabla real
        tabla = ComponenteCatalogos.crear_tabla_residuos(lista_objetos)
        page.add(ft.Container(content=tabla, padding=20))
    except Exception as e:
        page.add(ft.Text(f"Error al cargar el inventario técnico: {str(e)}", color="red"))
        
    page.update()

def abrir_info_donacion(page):
    
    dialogo = ft.AlertDialog(
        title=ft.Text("¿Cómo donar un juguete?"),
        content=ft.Text( 
            "¡Gracias por contribuir con la economía circular! "
            "Para garantizar la calidad de nuestro servicio, recibimos los juguetes físicamente "
            "en nuestra tienda de lunes a viernes (9:00 AM a 5:00 PM).\n\n"
            "Nuestro equipo se encargará de realizar la evaluación de cada juguete. ¡Te esperamos!",
            size=14
        ),
        actions=[ft.TextButton("Entendido", on_click=lambda _: setattr(dialogo, "open", False) or page.update())]
    )
    page.overlay.append(dialogo)
    dialogo.open = True
    page.update()


def abrir_formulario_ingreso(page, actualizar_tabla_fn, e=None):
    # Campos de texto y selectores según tu estructura exacta de datos
    txt_nombre = ft.TextField(label="Nombre del Juguete", width=300)
    txt_marca = ft.TextField(label="Marca (ej. Mattel, Hasbro o n/a)", width=300, value="n/a")
    txt_categoria = ft.Dropdown(
        label="Categoría", width=300,
        options=[ft.dropdown.Option("Peluches"), ft.dropdown.Option("Carros"), ft.dropdown.Option("Muñecas"), ft.dropdown.Option("Juegos de Mesa")]
    )
    txt_material = ft.TextField(label="Material (ej. Plástico, Tela/Algodón)", width=300)
    
    # Dimensiones
    txt_alto = ft.TextField(label="Alto (cm)", width=90, value="0.0")
    txt_ancho = ft.TextField(label="Ancho (cm)", width=90, value="0.0")
    txt_largo = ft.TextField(label="Largo (cm)", width=90, value="0.0")
    
    # Características
    sw_baterias = ft.Switch(label="¿Usa Baterías?", value=False)
    txt_incluye = ft.TextField(label="¿Qué incluye? (o n/a)", width=300, value="n/a")
    
    # Triaje y Calidad
    drop_estado = ft.Dropdown(
        label="Estado Físico", width=300,
        options=[ft.dropdown.Option("excelente"), ft.dropdown.Option("bueno"), ft.dropdown.Option("regular"), ft.dropdown.Option("malo")]
    )
    sw_piezas_faltantes = ft.Switch(label="¿Tiene piezas faltantes?", value=False)
    
    # Datos Comerciales / Visuales
    txt_precio = ft.TextField(label="Precio (USD)", width=300, value="0.0")
    txt_imagen = ft.TextField(label="Ruta de la Imagen", width=300, value="Assets/default.jpg")

    def guardar_juguete_click(e):
        # 1. Validación básica
        if not txt_nombre.value or not txt_categoria.value or not drop_estado.value:
            page.snack_bar = ft.SnackBar(ft.Text("Por favor, llena los campos obligatorios (Nombre, Categoría y Estado)"))
            page.snack_bar.open = True
            page.update()
            return

        ruta_json = "Data/inventario.json"
        
        # 2. Cargar inventario existente para generar el UUID secuencial
        try:
            with open(ruta_json, "r", encoding="utf-8") as f:
                inventario = json.load(f)
        except Exception:
            inventario = []

        nuevo_id = f"t{len(inventario) + 1:03d}" # Genera t001, t002, etc.

        # Clasificación por reglas de calidad
        estado = drop_estado.value
        faltantes = sw_piezas_faltantes.value

        if estado in ["excelente", "bueno"] and not faltantes:
            resultado_triaje = "venta"
        elif estado in ["bueno", "regular"]:
            resultado_triaje = "donacion"
            txt_precio.value = "0.0" # Las donaciones no tienen costo comercial
        else:
            resultado_triaje = "reciclaje"
            txt_precio.value = "0.0"

        
        nuevo_juguete = {
            "uuid": nuevo_id,
            "nombre": txt_nombre.value,
            "marca": txt_marca.value,
            "categoria": txt_categoria.value,
            "material": txt_material.value,
            "alto_cm": float(txt_alto.value or 0.0),
            "ancho_cm": float(txt_ancho.value or 0.0),
            "largo_cm": float(txt_largo.value or 0.0),
            "usa_baterias": sw_baterias.value,
            "incluye": txt_incluye.value,
            "estado_fisico": estado,
            "piezas_faltantes": faltantes,
            "triaje_resultado": resultado_triaje, # Generado automáticamente
            "precio_usd": float(txt_precio.value or 0.0),
            "imagen_ruta": txt_imagen.value
        }

        
        inventario.append(nuevo_juguete)
        with open(ruta_json, "w", encoding="utf-8") as f:
            json.dump(inventario, f, indent=4, ensure_ascii=False)

        # Cerrar modal y refrescar la tabla de la interfaz
        dlg_formulario.open = False
        page.update()
        actualizar_tabla_fn()

    # Estructura visual del Modal (Pop-up) organizada en scroll
    dlg_formulario = ft.AlertDialog(
        title=ft.Text("Registrar Ficha Técnica de Juguete"),
        content=ft.Container(
            content=ft.Column([
                txt_nombre, txt_categoria, txt_marca, txt_material,
                ft.Text("Dimensiones:", weight="bold", size=12),
                ft.Row([txt_alto, txt_ancho, txt_largo], spacing=10),
                sw_baterias, txt_incluye,
                ft.Divider(),
                ft.Text("Calidad y Triaje:", weight="bold", size=12),
                drop_estado, sw_piezas_faltantes,
                ft.Divider(),
                txt_precio, txt_imagen
            ], spacing=12, scroll="auto"),
            width=340, height=500
        ),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda _: setattr(dlg_formulario, "open", False) or page.update()),
            ft.ElevatedButton("Guardar e Ingresar", bgcolor="#0F4C5C", color="white", on_click=guardar_juguete_click)
        ]
    )

    page.overlay.append(dlg_formulario) 
    dlg_formulario.open = True
    page.update()

if __name__ == "__main__":
    ft.app(target=main, assets_dir="Assets")