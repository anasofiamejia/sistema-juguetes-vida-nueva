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
            with open("Data/historico_salidas.json", "r", encoding="utf-8") as f:
                historico = json.load(f)

            registro_encontrado = None

            if isinstance(parametro_recibido, dict):
                registro_encontrado = parametro_recibido
            else:
                id_buscado = str(parametro_recibido).strip()
                for s in historico:
                    if str(s.get("uuid_juguete")) == id_buscado or str(s.get("fecha_salida")) == id_buscado:
                        registro_encontrado = s
                        break

            if not registro_encontrado:
                lbl_mensaje.value = "No se localizaron los datos asociados a este registro."
                lbl_mensaje.color = "red"
                page.update()
                return

            nombre_target = str(registro_encontrado.get("nombre") or "").strip().upper()
            tipo_salida_raw = str(registro_encontrado.get("tipo_salida") or "venta").lower()
            tipo_mapa = {"venta": "venta", "donación": "donacion", "donacion": "donacion", "reciclaje": "reciclaje"}
            tipo_salida = tipo_mapa.get(tipo_salida_raw, "venta")

            inventario_path = "Data/inventario.json"
            if os.path.exists(inventario_path):
                with open(inventario_path, "r", encoding="utf-8") as f:
                    inventario = json.load(f)

                for juguete in inventario:
                    nombre_json = str(juguete.get("nombre") or "").strip().upper()
                    if nombre_json == nombre_target and juguete.get("triaje_resultado") == "vendido":
                        juguete["triaje_resultado"] = tipo_salida
                        break

                with open(inventario_path, "w", encoding="utf-8") as f:
                    json.dump(inventario, f, indent=4, ensure_ascii=False)

            uuid_target = registro_encontrado.get("uuid_juguete")
            historico_limpio = []
            eliminado = False
            for s in historico:
                if s.get("uuid_juguete") == uuid_target and not eliminado:
                    eliminado = True
                else:
                    historico_limpio.append(s)

            with open("Data/historico_salidas.json", "w", encoding="utf-8") as f:
                json.dump(historico_limpio, f, indent=4, ensure_ascii=False)

            lbl_mensaje.value = f"¡Éxito! '{nombre_target.title()}' devuelto al catálogo y removido del historial."
            lbl_mensaje.color = "green"
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