import flet as ft
import json
import datetime
import os

# Registro de sesión para ocultar del catálogo comercial los juguetes vendidos
class HistorialCompras:
    comprados = set()

# 1. Carrito en memoria unificada
class CarritoGlobal:
    items = []

    @staticmethod
    def agregar(producto):
        if not any(item["id"] == producto["id"] for item in CarritoGlobal.items):
            CarritoGlobal.items.append(producto)

    @staticmethod
    def remover(producto_id):
        CarritoGlobal.items = [item for item in CarritoGlobal.items if item["id"] != producto_id]

    @staticmethod
    def obtener_total():
        try:
            return sum(float(item["precio"]) for item in CarritoGlobal.items)
        except:
            return 0.0


# 2. Interfaz del Checkout Unificada con Eliminación de Inventario Único
def mostrar_checkout_personalizado(page, usuario, renderizar_menu_por_rol=None):
    lista_items = []
    
    if not CarritoGlobal.items:
        lista_items.append(ft.Text("El carrito está vacío.", italic=True, color="grey500"))
    else:
        for item in CarritoGlobal.items:
            emoji_item = "🛒" if item["tipo"] == "venta" else "❤️"
            try:
                precio_val = float(item['precio'])
                precio_str = f"${precio_val:.2f} USD" if item["tipo"] == "venta" else "Gratis"
            except:
                precio_str = f"${item['precio']} USD"

            lista_items.append(
                ft.Container(
                    content=ft.Row([
                        ft.Text(emoji_item, size=18),
                        ft.Column([
                            ft.Text(str(item["nombre"]).upper(), weight="bold", size=12, color="blueGrey900"),
                            ft.Text(f"Tipo: {str(item['tipo']).upper()}", size=10, color="bluegrey400")
                        ], expand=True),
                        ft.Text(precio_str, weight="bold", color="orange" if item["tipo"] == "venta" else "purple")
                    ], alignment="spaceBetween"),
                    padding=8, bgcolor="grey50", border_radius=6
                )
            )

    area_dinamica = ft.Column()

    def confirmar_pedido_directo(e):
        if not CarritoGlobal.items:
            if len(page.views) > 1:
                page.views.pop()
            page.update()
            return

        btn_confirmar.disabled = True
        btn_confirmar.visible = False
        page.update()

        try:
            fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            items_a_procesar = list(CarritoGlobal.items)
            
            # --- 1. ELIMINAR EL JUGUETE ÚNICO DEL INVENTARIO GLOBAL ---
            inventario_path = "Data/inventario.json"
            if os.path.exists(inventario_path):
                with open(inventario_path, "r", encoding="utf-8") as f:
                    juguetes_stock = json.load(f)
                
                # Nombres de los juguetes comprados en esta sesión
                nombres_comprados = [str(item["nombre"]).strip().upper() for item in items_a_procesar]
                
                # Buscamos el juguete en tu inventario original y cambiamos su estado
                for juguete in juguetes_stock:
                    nombre_juguete_json = str(juguete.get("nombre", "")).strip().upper()
                    if nombre_juguete_json in nombres_comprados:
                        # Lo marcamos como vendido. Así conservará su foto para siempre.
                        juguete["triaje_resultado"] = "vendido" 
                
                # Guardamos los cambios en tu mismo inventario.json
                with open(inventario_path, "w", encoding="utf-8") as f:
                    json.dump(juguetes_stock, f, indent=4, ensure_ascii=False)

            # --- 2. REGISTRAR EN EL HISTORIAL PARA EL ADMINISTRADOR ---
            historial_path = "Data/historico_salidas.json"
            historico = []
            if os.path.exists(historial_path):
                with open(historial_path, "r", encoding="utf-8") as f:
                    try: historico = json.load(f)
                    except: historico = []

            nombre_usr = "Usuario"
            if usuario:
                if isinstance(usuario, dict): nombre_usr = usuario.get("nombre", "Usuario")
                else: nombre_usr = getattr(usuario, "nombre", "Usuario")

            for item in items_a_procesar:
                uuid_juguete = item.get("id", f"GEN-{int(datetime.datetime.now().timestamp())}")
                
                # Buscamos capturar cualquier variante del campo de imagen que use tu catálogo
                img_path = item.get("imagen") or item.get("foto") or item.get("url_imagen") or item.get("path", "")

                historico.append({
                    "uuid_juguete": uuid_juguete,
                    "fecha_salida": fecha_actual,
                    "usuario_id": nombre_usr,
                    "nombre": item["nombre"],
                    "tipo_salida": "Venta" if item["tipo"] == "venta" else "Donación",
                    "detalle_destino": "Cliente Online",
                    "precio_final": float(item["precio"]),
                    "datos_completos": item  # Asegura guardar todo el objeto original
                })

            with open(historial_path, "w", encoding="utf-8") as f:
                json.dump(historico, f, indent=4, ensure_ascii=False)

            # --- 3. MOSTRAR COMPROBANTE EN PANTALLA ---
            resumen_texto =  "=========================================\n"
            resumen_texto += "         COMPROBANTE DE TRANSACCIÓN      \n"
            resumen_texto += f" Fecha/Hora: {fecha_actual}\n"
            resumen_texto += "=========================================\n\n"

            for item in items_a_procesar:
                resumen_texto += f" • {str(item['nombre']).upper()} - ${item['precio']} USD\n"

            resumen_texto += "-----------------------------------------\n"
            resumen_texto += f" TOTAL PROCESADO: ${CarritoGlobal.obtener_total():.2f} USD\n"
            resumen_texto += "=========================================\n"

            # Función de retorno inteligente al menú del rol del usuario
            def volver_al_inicio_real(e):
                CarritoGlobal.items.clear()  # 1. Limpiamos el carrito en memoria
                
                # 2. Retiramos el plato de arriba (Checkout / Comprobante)
                if len(page.views) > 1:
                    page.views.pop()
                
                # 3. Retiramos el plato del medio (Catálogo viejo en memoria)
                if len(page.views) > 1:
                    page.views.pop()
                
                # 4. Refrescamos. Ahora la pantalla activa será el Menú del Rol intacto.
                page.update()

            # Creamos el botón correctamente
            btn_volver_inicio = ft.ElevatedButton(
                "Volver al Inicio 🏠", 
                bgcolor="blueGrey700", 
                color="white", 
                expand=True,
                on_click=volver_al_inicio_real
            )

            # !!! AQUÍ ESTÁ EL CAMBIO IMPORTANTE: agregamos btn_volver_inicio a los controles !!!
            area_dinamica.controls = [
                ft.Divider(),
                ft.Text("🎉 ¡COMPRA LOGRADA CON ÉXITO!", weight="bold", color="green700", size=14),
                ft.Container(
                    content=ft.Text(resumen_texto, font_family="monospace", size=11, color="blueGrey900"),
                    padding=10, bgcolor="grey50", border_radius=5
                ),
                ft.Container(height=10),
                btn_volver_inicio  # <-- ¡Ahora sí está incluido aquí!
            ]
            
            btn_confirmar.visible = False
            page.update()

        except Exception as err:
            area_dinamica.controls = [ft.Text(f"Error interno: {err}", color="red")]
            page.update()

    btn_confirmar = ft.ElevatedButton(
        content=ft.Text("CONFIRMAR Y RECIBIR COMPROBANTE", color="white", weight="bold"),
        bgcolor="green700", width=380, height=45, 
        on_click=confirmar_pedido_directo
    )

    panel_checkout = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Text("MI CARRITO / CHECKOUT", size=16, weight="bold", color="#0F4C5C"),
                ft.ElevatedButton("Seguir Viendo", bgcolor="grey700", on_click=lambda _: [page.views.pop(), page.update()])
            ], alignment="spaceBetween"),
            ft.Divider(),
            ft.Column(controls=lista_items, scroll="auto", height=200),
            ft.Divider(),
            ft.Row([
                ft.Text("Total Estimado:", weight="bold"),
                ft.Text(f"${CarritoGlobal.obtener_total():.2f} USD", weight="bold", color="orange", size=15)
            ], alignment="spaceBetween"),
            ft.Container(height=10),
            btn_confirmar,   
            area_dinamica    
        ]),
        padding=20, bgcolor="white", border_radius=10, width=420
    )

    page.views.append(ft.View(route="/checkout_cliente", controls=[ft.Row([panel_checkout], alignment="center")], bgcolor="#F5F7FA"))
    page.update()


# 3. INTERCEPTOR RECURSIVO PROFUNDO CON RE-RENDER INMEDIATO
def inyectar_carrito_desde_afuera(page, usuario):
    if not page.views: return
    
    layout_principal = None
    for control in page.views[-1].controls:
        if isinstance(control, ft.Container) and isinstance(control.content, ft.Column):
            layout_principal = control.content
            break
        elif isinstance(control, ft.Column):
            layout_principal = control
            break

    if not layout_principal: return

    btn_carrito = ft.ElevatedButton(
        content=ft.Text("Ver Carrito 🛒", color="white", weight="bold"), 
        bgcolor="green700",
        on_click=lambda _: mostrar_checkout_personalizado(page, usuario)
    )

    ya_tiene_carrito = any(
        isinstance(c, ft.Row) and any(getattr(b, "text", "") == "Ver Carrito 🛒" or (isinstance(b, ft.ElevatedButton) and "Ver Carrito" in getattr(b.content, "value", "")) for b in c.controls)
        for c in layout_principal.controls
    )

    if not ya_tiene_carrito:
        barra_carrito = ft.Row([
            ft.Text("🛒 Gestión de Pedido Activa", size=12, color="grey600", italic=True),
            btn_carrito
        ], alignment="spaceBetween")
        layout_principal.controls.insert(1, barra_carrito)

    grid_articulos = None
    for control in layout_principal.controls:
        if isinstance(control, ft.Row) and getattr(control, "wrap", False):
            grid_articulos = control
            break

    if grid_articulos:
        for tarjeta in grid_articulos.controls:
            if isinstance(tarjeta, ft.Container) and isinstance(tarjeta.content, ft.Column):
                columna = tarjeta.content
                if not columna.controls: continue
                
                boton_original = columna.controls[-1]
                
                if isinstance(boton_original, ft.ElevatedButton):
                    
                    todos_los_textos = []
                    def buscar_textos_recursivo(ctrl_actual):
                        if isinstance(ctrl_actual, ft.Text) and ctrl_actual.value:
                            todos_los_textos.append(ctrl_actual.value)
                        elif hasattr(ctrl_actual, "controls") and ctrl_actual.controls:
                            for sub_ctrl in ctrl_actual.controls:
                                buscar_textos_recursivo(sub_ctrl)
                        elif hasattr(ctrl_actual, "content") and ctrl_actual.content:
                            buscar_textos_recursivo(ctrl_actual.content)

                    buscar_textos_recursivo(columna)

                    textos_validos = []
                    info_precio = "0.0"
                    
                    for txt in todos_los_textos:
                        txt_str = str(txt).strip()
                        txt_upper = txt_str.upper()
                        
                        if txt_upper in ["EXCELENTE", "PROCEDER AL PAGO", "SELECCIONADO ✓", "SELECCIONADO"]:
                            continue
                        if "PRECIO:" in txt_upper or "$" in txt_upper:
                            info_precio = txt_str
                            continue
                        if any(p in txt_upper for p in ["MARCA:", "CATEGORÍA:", "CATEGORIA:", "INCLUYE:"]):
                            continue
                        if txt_str:
                            textos_validos.append(txt_str)

                    nombre_juguete = textos_validos[0] if textos_validos else "Juguete"
                    
                    precio_limpio = info_precio.replace("Precio: $", "").replace("Costo: Gratis ($0.00)", "0.0").replace(" USD", "").replace("$", "").strip()
                    try: precio_num = float(precio_limpio)
                    except: precio_num = 0.0

                    tipo_catalogo = "donacion" if "Gratis" in info_precio or precio_num == 0.0 else "venta"
                    color_original = "orange" if tipo_catalogo == "venta" else "purple"

                    id_producto = str(hash(nombre_juguete))
                    datos_producto = {
                        "id": id_producto,
                        "nombre": nombre_juguete,
                        "precio": precio_num,
                        "tipo": tipo_catalogo
                    }

                    if id_producto in HistorialCompras.comprados:
                        tarjeta.visible = False
                        continue

                    if any(item["id"] == id_producto for item in CarritoGlobal.items):
                        boton_original.bgcolor = "grey500"
                        boton_original.content = ft.Text("Seleccionado ✓", color="white")
                    else:
                        boton_original.bgcolor = color_original
                        boton_original.content = ft.Text("Proceder al Pago", color="white")

                    def asociar_evento_click(prod_fijo, btn_fijo, color_fijo):
                        def al_hacer_click(e):
                            if any(item["id"] == prod_fijo["id"] for item in CarritoGlobal.items):
                                CarritoGlobal.remover(prod_fijo["id"])
                                btn_fijo.bgcolor = color_fijo
                                btn_fijo.content = ft.Text("Proceder al Pago", color="white")
                            else:
                                CarritoGlobal.agregar(prod_fijo)
                                btn_fijo.bgcolor = "grey500"
                                btn_fijo.content = ft.Text("Seleccionado ✓", color="white")
                            page.update()
                        return al_hacer_click

                    boton_original.on_click = asociar_evento_click(datos_producto, boton_original, color_original)

    page.update()