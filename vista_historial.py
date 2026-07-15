import flet as ft
import json
import os

def crear_vista_historial(page, usuario, renderizar_menu_por_rol):
    txt_titulo = ft.Text("HISTORIAL DE SALIDAS Y AUDITORÍA DE USUARIOS", size=20, weight=ft.FontWeight.BOLD, color="#0F4C5C")
    lbl_mensaje = ft.Text("", size=14, weight=ft.FontWeight.BOLD)
    contenedor_tabla = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)

    def cargar_tabla_historial():
        contenedor_tabla.controls.clear()
        try:
            with open("Data/historico_salidas.json", "r", encoding="utf-8") as f:
                historico = json.load(f)
        except Exception:
            historico = []

        if not historico:
            contenedor_tabla.controls.append(ft.Text("No hay registros de actividades en el sistema.", italic=True, color="bluegrey400"))
            page.update()
            return

        filas = []
        # Invertimos para ver lo más nuevo arriba
        for s in reversed(historico):
            uuid_j = s.get("uuid_juguete", s.get("uuid"))
            nombre_j = s.get("nombre", "Sin Nombre")
            usuario_responsable = s.get("usuario_id", s.get("usuario", "Admin_Sistema"))

            btn_revertir = ft.ElevatedButton(
                content=ft.Text("Devolver", color="white"),
                bgcolor="#E2711D",
                on_click=lambda e, uid=uuid_j: ejecutar_reversion(uid)
            )

            filas.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(s.get("fecha_salida", ""))),
                        ft.DataCell(ft.Text(usuario_responsable, weight="bold", color="bluegrey700")), 
                        ft.DataCell(ft.Text(nombre_j.upper())),
                        ft.DataCell(ft.Text(s.get("tipo_salida", "").upper())),
                        ft.DataCell(ft.Text(s.get("detalle_destino", ""))),
                        ft.DataCell(ft.Text(f"${s.get('precio_final', 0.0):.2f}")),
                        ft.DataCell(btn_revertir),
                    ]
                )
            )

        tabla = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Fecha")),
                ft.DataColumn(ft.Text("Operador / Usuario")), 
                ft.DataColumn(ft.Text("Juguete")),
                ft.DataColumn(ft.Text("Tipo")),
                ft.DataColumn(ft.Text("Destino")),
                ft.DataColumn(ft.Text("Precio Final")),
                ft.DataColumn(ft.Text("Acción")),
            ],
            rows=filas
        )
        contenedor_tabla.controls.append(tabla)
        page.update()

    def ejecutar_reversion(parametro_recibido):
        try:
            # 1. Leer la base de datos de transacciones del historial
            with open("Data/historico_salidas.json", "r", encoding="utf-8") as f:
                historico = json.load(f)

            registro_encontrado = None

            # DETECCIÓN INTELIGENTE DEL TIPO DE DATO
            if isinstance(parametro_recibido, dict):
                registro_encontrado = parametro_recibido
            else:
                id_o_fecha_buscada = str(parametro_recibido).strip()
                for s in historico:
                    if str(s.get("uuid_juguete")) == id_o_fecha_buscada or str(s.get("fecha")) == id_o_fecha_buscada:
                        registro_encontrado = s
                        break

            if not registro_encontrado:
                lbl_mensaje.value = "No se localizaron los datos asociados a este registro."
                lbl_mensaje.color = "red"
                page.update()
                return

            # Extraemos los datos asegurando que NUNCA sean None (si es None, usamos una cadena vacía)
            juguete_texto = registro_encontrado.get("juguete")
            nombre_target = str(juguete_texto if juguete_texto is not None else "").strip().upper()
            fecha_target = registro_encontrado.get("fecha")
            
            tipo_salida_raw = registro_encontrado.get("tipo")
            tipo_salida = str(tipo_salida_raw if tipo_salida_raw is not None else "venta").lower()

            # 2. RESTABLECER EL ESTADO DENTRO DE INVENTARIO.JSON
            inventario_path = "Data/inventario.json"
            if os.path.exists(inventario_path):
                with open(inventario_path, "r", encoding="utf-8") as f:
                    inventario = json.load(f)

                juguete_modificado = False
                for juguete in inventario:
                    nombre_json_raw = juguete.get("nombre")
                    nombre_json = str(nombre_json_raw if nombre_json_raw is not None else "").strip().upper()
                    
                    # Buscamos el artículo vendido cuyo nombre coincida exactamente
                    if nombre_json == nombre_target and juguete.get("triaje_resultado") == "vendido":
                        juguete["triaje_resultado"] = tipo_salida  # Regresa a 'venta' o 'donacion'
                        juguete_modificado = True
                        break

                # Si el juguete fue borrado físicamente en pruebas viejas, lo recreamos de forma 100% segura
                if not juguete_modificado and not any(str(j.get("nombre") if j.get("nombre") is not None else "").strip().upper() == nombre_target for j in inventario):
                    
                    # Deducción segura de la ruta de la imagen
                    nombre_archivo_foto = nombre_target.lower().replace(' ', '_')
                    if "osita" in nombre_archivo_foto:
                        ruta_foto = "assets/osita.png"
                    elif "cesta" in nombre_archivo_foto or "mercado" in nombre_archivo_foto:
                        ruta_foto = "assets/cesta.png"
                    elif "tren" in nombre_archivo_foto:
                        ruta_foto = "assets/tren.png"
                    else:
                        ruta_foto = f"assets/{nombre_archivo_foto}.png"

                    nuevo_juguete = {
                        "id": str(registro_encontrado.get("uuid_juguete") or "REF-NUEVO"),
                        "nombre": registro_encontrado.get("juguete") or "Juguete Restablecido",
                        "precio": float(registro_encontrado.get("precio_final") or registro_encontrado.get("monto") or 0.0),
                        "triaje_resultado": tipo_salida,
                        "marca": "n/a",       # Guardamos como texto "n/a" en vez de None para evitar el error
                        "categoria": "Juguetes",
                        "imagen": ruta_foto,
                        "foto": ruta_foto
                    }
                    inventario.append(nuevo_juguete)

                with open(inventario_path, "w", encoding="utf-8") as f:
                    json.dump(inventario, f, indent=4, ensure_ascii=False)

            # 3. ELIMINAR LA FILA SELECCIONADA DEL HISTORIAL JSON
            historico_limpio = []
            eliminado = False
            
            for s in historico:
                s_juguete_raw = s.get("juguete")
                s_juguete_str = str(s_juguete_raw if s_juguete_raw is not None else "").strip().upper()
                
                es_objeto_target = (s.get("fecha") == fecha_target and s_juguete_str == nombre_target)
                
                if es_objeto_target and not eliminado:
                    eliminado = True
                    continue 
                else:
                    historico_limpio.append(s)

            with open("Data/historico_salidas.json", "w", encoding="utf-8") as f:
                json.dump(historico_limpio, f, indent=4, ensure_ascii=False)

            # Mensaje exitoso
            lbl_mensaje.value = f"¡Éxito! '{registro_encontrado.get('juguete')}' devuelto al catálogo y removido del historial."
            lbl_mensaje.color = "green"
            
            # 4. RECARGAR LA TABLA VISUAL
            if "cargar_tabla_historial" in globals() or "cargar_tabla_historial" in locals():
                cargar_tabla_historial()

        except Exception as err:
            lbl_mensaje.value = f"Error crítico en devolución: {err}"
            lbl_mensaje.color = "red"
        
        page.update()

    btn_volver = ft.ElevatedButton(
        content=ft.Text("Atrás", color="white"),
        bgcolor="#0F4C5C",
        on_click=lambda _: renderizar_menu_por_rol(usuario)
    )

    cargar_tabla_historial()

    page.controls.clear()
    page.add(
        ft.Container(
            content=ft.Column([
                ft.Row([txt_titulo, btn_volver], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(height=10, color="transparent"),
                lbl_mensaje,
                ft.Divider(height=10, color="transparent"),
                contenedor_tabla
            ]),
            padding=20
        )
    )
    page.update()