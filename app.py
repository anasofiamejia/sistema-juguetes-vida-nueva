import flet as ft
from Modules.usuarios import SistemaUsuarios
from Modules.persistencia import AdministradorPersistencia

from Modules.catalogos import GestorCatalogos
from vista_catalogos import ComponenteCatalogos

def main(page: ft.Page):

    # Ventana Principal de Flet
    page.title = "JUGUETES VIDA NUEVA"
    page.window_width = 500
    page.window_height = 650
    page.theme_mode = ft.ThemeMode.LIGHT
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START

    page.bgcolor = "white"

    gestor_usuarios = SistemaUsuarios()
    gestor_datos = AdministradorPersistencia()

    container_logo = ft.Image(
    src="logo.png",         
    width=130,
    height=130,
    )

    txt_correo = ft.TextField(
        label="Correo Electrónico", 
        width=380, 
        border_color="#4DD0E1", 
        label_style=ft.TextStyle(color="bluegrey700"),
        prefix_icon="email"
    )
    
    txt_contrasena = ft.TextField(
        label="Contraseña", 
        password=True, 
        can_reveal_password=True, 
        width=380, 
        border_color = "#4DD0E1", 
        label_style=ft.TextStyle(color="bluegrey700"),
        prefix_icon="lock"
    )
    
    lbl_mensaje_error = ft.Text(
        "", 
        size=13, 
        color="redaccent700", 
        weight=ft.FontWeight.W_500
    )

    # Lógica y Autenticación:

    def desencadenar_login(e):
        usuario_activo = gestor_usuarios.autenticar(txt_correo.value, txt_contrasena.value)
        if usuario_activo:
            lbl_mensaje_error.value = ""
            renderizar_menu_por_rol(usuario_activo)
        else:
            lbl_mensaje_error.value = "Credenciales incorrectas. Verifique e intente de nuevo."
            page.update()

    btn_login = ft.ElevatedButton(
        content=ft.Text("Iniciar Sesión", color="white", weight=ft.FontWeight.BOLD),
        width=380,
        on_click=desencadenar_login,
        style=ft.ButtonStyle(
            bgcolor="#4DD0E1",
            shape=ft.RoundedRectangleBorder(radius=8),
        )
    )

    # Diseño parte inferior:

    linea_decorativa = ft.Divider(height=2, color="#4DD0E1")

    # Barra de enlaces:
    columna_izquierda = ft.Column([
    ft.Row([
        ft.Icon("info", color="#4DD0E1", size=16), 
        ft.Text("REPORTE DE IMPACTO", size=11, weight=ft.FontWeight.BOLD, color="white")
    ]),
    ft.Text("  SOPORTE TÉCNICO", size=11, weight=ft.FontWeight.BOLD, color="white"),
], spacing=6, horizontal_alignment=ft.CrossAxisAlignment.START)

    columna_derecha = ft.Column([
    ft.Text("REGISTRARSE (SOLO CLIENTES)", size=11, weight=ft.FontWeight.W_500, color="white", text_align=ft.TextAlign.RIGHT),
    ft.Text("RECOBRAR ACCESO (CONTRASEÑA)", size=11, weight=ft.FontWeight.W_500, color="white", text_align=ft.TextAlign.RIGHT),
], spacing=6, horizontal_alignment=ft.CrossAxisAlignment.END)

    # Contenedor de enlaces:
    contenedor_enlaces = ft.Container(
    content=ft.Row(
        controls=[columna_izquierda, columna_derecha],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    ),
    bgcolor="#0F4C5C", 
    padding=ft.padding.Padding(15, 12, 22, 12), # Un toque extra a la derecha
)

    # Barra de estado inferior:
    barra_estado = ft.Container(
        content=ft.Text(
            "SESIÓN ACTUAL: VISITANTE", 
            size=11, 
            weight=ft.FontWeight.BOLD,
            color="bluegrey700",
            text_align=ft.TextAlign.CENTER
        ),
        bgcolor="grey200",
        padding=8,
        width=500
    )

    # Menú por Perfiles de Usuario (Lógica Interna):
    def renderizar_menu_por_rol(usuario):
        page.controls.clear() 
        page.vertical_alignment = ft.MainAxisAlignment.START
        
        
        gestor_catalogos = GestorCatalogos(gestor_datos)


        def mostrar_pantalla_catalogo(titulo_vista, tipo_catalogo):
            page.controls.clear()
            
            # Encabezado del catálogo
            page.add(
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Text(titulo_vista.upper(), size=20, weight=ft.FontWeight.BOLD, color="#0F4C5C"),
                            ft.IconButton(
                                icon=ft.icons.ARROW_BACK, 
                                tooltip="Volver al Menú", 
                                on_click=lambda _: renderizar_menu_por_rol(usuario) # POO: Regresa pasando el estado del usuario activo
                            )
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ]),
                    padding=20
                ),
                ft.Divider(height=1, color="grey300")
            )

            # Contenedor donde se renderizará la información
            zona_render = ft.Column(spacing=15, scroll=ft.ScrollMode.AUTO, expand=True)

        
            if tipo_catalogo == "comercial":
                lista_juguetes = gestor_catalogos.obtener_catalogo_comercial()
                # Creamos una fila/malla para tarjetas
                malla = ft.Row(wrap=True, spacing=15, run_spacing=15)
                for j in lista_juguetes:
                    malla.controls.append(ComponenteCatalogos.crear_tarjeta_comercial_social(j))
                zona_render.controls.append(malla)

            elif tipo_catalogo == "social":
                lista_juguetes = gestor_catalogos.obtener_catalogo_social()
                malla = ft.Row(wrap=True, spacing=15, run_spacing=15)
                for j in lista_juguetes:
                    malla.controls.append(ComponenteCatalogos.crear_tarjeta_comercial_social(j))
                zona_render.controls.append(malla)

            elif tipo_catalogo == "residuos":
                lista_juguetes = gestor_catalogos.obtener_catalogo_residuos()
                # Para residuos usamos el método estático de la DataTable técnica
                tabla = ComponenteCatalogos.crear_tabla_residuos(lista_juguetes)
                zona_render.controls.append(ft.Row([tabla], scroll=ft.ScrollMode.AUTO)) # Scroll horizontal si es necesario

            # Mensaje por si la lista está vacía
            if not lista_juguetes:
                zona_render.controls.append(ft.Text("No hay registros en este catálogo actualmente.", italic=True, color="bluegrey400"))

            page.add(ft.Container(content=zona_render, padding=20, expand=True))
            page.update()


        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Text("Juguetes Vida Nueva", size=24, weight=ft.FontWeight.BOLD, color="#4DD0E1"),
                    ft.Text('"Porque todos merecemos una segunda oportunidad"', size=13, italic=True, color="bluegrey600"),
                    ft.Container(height=10),
                    ft.Text(f"Panel: {usuario.rol} | Activo: {usuario.nombre}", size=14, weight=ft.FontWeight.W_500, color="bluegrey700"),
                ]),
                padding=20
            ),
            ft.Divider(height=1, color="grey300")
        )

        bloque_acciones = ft.Column(spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER, width=400)

        if usuario.rol == "Familia":
            bloque_acciones.controls.extend([
                # Conectamos el botón al catálogo comercial
                ft.ElevatedButton(
                    content=ft.Text("Ver Catálogo Comercial (Comprar)", color="white"), 
                    width=350, 
                    style=ft.ButtonStyle(bgcolor="#4DD0E1"),
                    on_click=lambda _: mostrar_pantalla_catalogo("Catálogo Comercial", "comercial")
                ),
                ft.ElevatedButton(content=ft.Text("Registrar una nueva Donación (Donar)", color="white"), width=350, style=ft.ButtonStyle(bgcolor="#4DD0E1"))
            ])
        elif usuario.rol == "Fundación":
            bloque_acciones.controls.extend([
                # Conectamos el botón al catálogo social (Donaciones)
                ft.ElevatedButton(
                    content=ft.Text("Ver Artículos para Donación (Gratuitos)", color="white"), 
                    width=350, 
                    style=ft.ButtonStyle(bgcolor="#4DD0E1"),
                    on_click=lambda _: mostrar_pantalla_catalogo("Catálogo de Donaciones", "social")
                ),
                
                ft.ElevatedButton(
                    content=ft.Text("Ver Catálogo Comercial (Comprar)", color="white"), 
                    width=350, 
                    style=ft.ButtonStyle(bgcolor="#4DD0E1"),
                    on_click=lambda _: mostrar_pantalla_catalogo("Catálogo Comercial", "comercial")
                )
            ])
        elif usuario.rol == "Centro_Reciclaje":
            bloque_acciones.controls.extend([
                # Conectamos el botón a la tabla técnica de residuos
                ft.ElevatedButton(
                    content=ft.Text("Ver Inventario de Residuos", color="white"), 
                    width=350, 
                    style=ft.ButtonStyle(bgcolor="#4DD0E1"),
                    on_click=lambda _: mostrar_pantalla_catalogo("Inventario Técnico de Residuos", "residuos")
                )
            ])
        elif usuario.rol in ["Administrador", "Operario"]:
            bloque_acciones.controls.extend([
                ft.ElevatedButton(content=ft.Text("Vista Operativa Global de Inventario", color="white"), width=350, style=ft.ButtonStyle(bgcolor="#4DD0E1"))
            ])

        page.add(ft.Container(content=bloque_acciones, padding=30))
        page.update()


    # Formulario central:
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
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    # Diseño completo de pantalla:
    diseno_pantalla_completa = ft.Column(
        controls=[
            formulario_login,
            ft.Column(
                controls=[
                    linea_decorativa,
                    contenedor_enlaces,
                    barra_estado
                ],
                spacing=0
            )
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        expand=True
    )

    page.spacing = 0
    page.padding = 0

    page.add(diseno_pantalla_completa)

if __name__ == "__main__":
    ft.app(target=main, assets_dir="Assets")