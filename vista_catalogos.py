import json
import flet as ft
from Modules.juguete import Juguete
from vista_salidas import crear_vista_salidas

class ComponenteCatalogos:
    @staticmethod
    def obtener_ruta_url_flet(ruta_json):
        """
        Limpia cualquier rastro de subcarpetas en el JSON para dejar 
        el nombre del archivo suelto, igual que tu logo.png.
        """
        if not ruta_json or str(ruta_json).strip() == "":
            return "placeholder.png" # Si no hay foto, busca placeholder.png en tu raíz
            
        # Removemos cualquier prefijo de carpeta que pudiera estar estorbando en el JSON
        nombre_limpio = str(ruta_json).replace("Assets/", "").replace("assets/", "")
        nombre_limpio = nombre_limpio.replace("Assets\\", "").replace("assets\\", "")
        nombre_limpio = nombre_limpio.lstrip("/") # Quitamos barras diagonales sobrantes
        
        return nombre_limpio.strip()

    @staticmethod
    def crear_tarjeta_comercial_social(juguete_obj):
        # --- BLINDAJE CONTRA ERRORES 'NONETYPE' ---
        # Si alguna propiedad viene vacía (None), la convertimos en un texto seguro
        nombre_safe = str(getattr(juguete_obj, "nombre", "") or "Juguete sin Nombre").upper()
        estado_safe = str(getattr(juguete_obj, "estado_fisico", "") or "Bueno").upper()
        marca_safe = str(getattr(juguete_obj, "marca", "") or "n/a")
        categoria_safe = str(getattr(juguete_obj, "categoria", "") or "General")
        incluye_safe = str(getattr(juguete_obj, "incluye", "") or "n/a")
        # ------------------------------------------

        es_venta = getattr(juguete_obj, "triaje_resultado", "venta") == "venta"
        color_borde = "orange" if es_venta else "purple"
        badge_color = "orange" if es_venta else "purple"
        texto_color_titulo = "#E65100" if es_venta else "#4A148C"
        
        precio_val = getattr(juguete_obj, "precio_usd", 0.0) or 0.0
        texto_inferior = f"Precio: ${precio_val:.2f} USD" if es_venta else "Costo: Gratis ($0.00)"

        # Obtención de la ruta ajustada al estilo de tu logo
        ruta_flet = ComponenteCatalogos.obtener_ruta_url_flet(getattr(juguete_obj, "imagen_ruta", ""))

        return ft.Container(
            content=ft.Column([
                ft.Image(src=ruta_flet, width=350, height=180, fit="cover", border_radius=4),
                ft.Row([
                    ft.Text(nombre_safe, size=14, weight="bold", color=texto_color_titulo), # Usamos variable segura
                    ft.Container(
                        content=ft.Text(estado_safe, size=10, color="white", weight="bold"), # Usamos variable segura
                        bgcolor=badge_color, padding=6, border_radius=4
                    ),
                ], alignment="spaceBetween"), 
                ft.Text(f"Marca: {marca_safe} | Categoría: {categoria_safe}", size=12, color="bluegrey500"), # Usamos variables seguras
                ft.Text(f"Incluye: {incluye_safe}", size=11, max_lines=2, overflow="ellipsis", color="bluegrey700"), # Usamos variable segura
                ft.Divider(height=1, color="grey200"),
                ft.Text(texto_inferior, size=13, weight="bold", color="bluegrey900")
            ], spacing=8),
            bgcolor="white", padding=15, border_radius=8, border=ft.Border.all(1.5, color_borde), width=380
        )
    
    @staticmethod
    def crear_tabla_residuos(lista_juguetes_reciclaje):
        columnas = [
            ft.DataColumn(ft.Text("ID/UUID", weight="bold")),
            ft.DataColumn(ft.Text("Vista Previa", weight="bold")),
            ft.DataColumn(ft.Text("Juguete", weight="bold")),
            ft.DataColumn(ft.Text("Material", weight="bold")),
            ft.DataColumn(ft.Text("Dimensiones (Al x An x La)", weight="bold")),
        ]
        filas = []
        for j in lista_juguetes_reciclaje:
            ruta_flet = ComponenteCatalogos.obtener_ruta_url_flet(getattr(j, "imagen_ruta", ""))
                
            filas.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(j.uuid)),
                    ft.DataCell(ft.Image(src=ruta_flet, width=50, height=50, fit="contain", border_radius=4)),
                    ft.DataCell(ft.Text(j.nombre)),
                    ft.DataCell(ft.Text(j.material, weight="bold", color="green")),
                    ft.DataCell(ft.Text(f"{j.alto_cm} x {j.ancho_cm} x {j.largo_cm} cm")),
                ])
            )
        return ft.DataTable(columns=columnas, rows=filas, heading_row_color="grey100", border=ft.Border.all(1, "green"), border_radius=5)


# ==========================================
# FUNCIÓN PRINCIPAL DIRECTA Y REACTIVA
# ==========================================
def abrir_pantalla_catalogo(page, usuario, volver_menu_fn, tipo_catalogo_solicitado=None):
    
    dd_categorias = ft.Dropdown(
        label="Filtrar por Categoría",
        width=300,
        value="Todos",
        options=[
            ft.dropdown.Option("Todos"),
            ft.dropdown.Option("Juguetes para niños"),
            ft.dropdown.Option("Juguetes para niñas"),
            ft.dropdown.Option("Juguetes para bebés"),
            ft.dropdown.Option("Peluches"),
            ft.dropdown.Option("Juegos de Mesa")
        ]
    )

    if tipo_catalogo_solicitado == "donacion":
        titulo_texto = "CATÁLOGO DE DONACIONES (GRATUITOS)"
    elif tipo_catalogo_solicitado == "venta":
        titulo_texto = "CATÁLOGO COMERCIAL (COMPRAR)"
    else:
        rol_titulo = getattr(usuario, "rol", "Invitado") if not isinstance(usuario, dict) else usuario.get("rol", "Invitado")
        titulo_texto = f"CATÁLOGO DE JUGUETES ({str(rol_titulo).upper()})"

    def procesar_salida_click(e):
        crear_vista_salidas(page, usuario, volver_menu_fn)

    def renderizar_interfaz_completa(e=None):
        grid_articulos = ft.Row(wrap=True, spacing=20, alignment="center")
        categoria_filtro = dd_categorias.value if dd_categorias.value else "Todos"
        
        try:
            with open("Data/inventario.json", "r", encoding="utf-8") as f:
                datos_raw = json.load(f)
        except Exception:
            datos_raw = []

        # 1. FILTRO ULTRA ESTRICTO: Solo pasan juguetes con nombre real y precio válido
        lista_juguetes = []
        for item in datos_raw:
            if not item:
                continue
                
            nombre = item.get("nombre")
            precio = item.get("precio") or item.get("precio_usd") or 0.0
            
            # Si el nombre está vacío, es nulo o contiene texto basura de errores previos, lo ignoramos
            if nombre is None or str(nombre).strip() == "" or "NONE" in str(nombre).upper() or "SIN NOMBRE" in str(nombre).upper():
                continue
                
            if float(precio) <= 0.0:
                continue
                
            # Si pasó los filtros, lo convertimos de forma segura en objeto
            lista_juguetes.append(Juguete.desde_diccionario(item))

        # Limpiamos los controles internos de la cuadrícula para evitar duplicados residuales
        grid_articulos.controls.clear() 

        # 3. CONTINUACIÓN DE TU LÓGICA DE ROLES Y RENDERIZADO DE TARJETAS
        rol_usuario_raw = getattr(usuario, "rol", "invitado") if not isinstance(usuario, dict) else usuario.get("rol", "invitado")
        rol_usuario = str(rol_usuario_raw).strip().lower()

        es_reciclaje = rol_usuario in ["escuela_reciclaje", "recicladora", "centro_reciclaje"]

        if es_reciclaje:
            juguetes_filtrados = [j for j in lista_juguetes if j.triaje_resultado == "reciclaje"]
            grid_articulos.controls.clear()
            grid_articulos.controls.append(ComponenteCatalogos.crear_tabla_residuos(juguetes_filtrados))
        
        else:
            for j in lista_juguetes:
                if j.triaje_resultado == "reciclaje":
                    continue
                
                if tipo_catalogo_solicitado is not None:
                    if j.triaje_resultado != tipo_catalogo_solicitado:
                        continue
                else:
                    if rol_usuario in ["cliente", "familia"] and j.triaje_resultado != "venta":
                        continue
                
                if categoria_filtro != "Todos":
                    if str(j.categoria).strip().lower() != str(categoria_filtro).strip().lower():
                        continue

                tarjeta_visual = ComponenteCatalogos.crear_tarjeta_comercial_social(j)
                texto_boton = "Confirmar Asignación" if j.triaje_resultado == "donacion" else "Proceder al Pago"
                color_boton = "purple" if j.triaje_resultado == "donacion" else "orange"
                
                boton_accion = ft.ElevatedButton(
                    content=ft.Text(texto_boton, color="white"), 
                    bgcolor=color_boton, 
                    on_click=procesar_salida_click
                )
                
                tarjeta_visual.content.controls.append(boton_accion)
                grid_articulos.controls.append(tarjeta_visual)

        fila_filtro = ft.Row([dd_categorias], alignment="center") if not es_reciclaje else ft.Container()

        # =========================================================================
        # ¡¡EL CAMBIO CLAVE AQUÍ!! Borrar las cuadrículas viejas acumuladas del layout
        # =========================================================================
        layout_principal.controls.clear() 

        layout_principal.controls = [
            ft.Row([
                ft.Text(titulo_texto, size=18, weight="bold", color="#0F4C5C"),
                ft.ElevatedButton(
                    content=ft.Text("Atrás", color="white"), bgcolor="#0F4C5C",
                    on_click=lambda _: [page.views.pop(), page.update(), volver_menu_fn(usuario)]
                )
            ], alignment="spaceBetween"),
            ft.Divider(),
            fila_filtro,
            ft.Container(height=10),
            grid_articulos
        ]
        
        page.update()

    dd_categorias.on_change = renderizar_interfaz_completa
    layout_principal = ft.Column(scroll="auto")
    renderizar_interfaz_completa(None)

    nueva_vista = ft.View(
        route="/catalogos",
        controls=[ft.Container(content=layout_principal, padding=20)]
    )
    
    page.views.append(nueva_vista)
    page.update()