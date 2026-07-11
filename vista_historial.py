import flet as ft
import json
from Modules.salidas import GestorSalidas

def crear_vista_historial(page, usuario, renderizar_menu_por_rol):
    txt_titulo = ft.Text("HISTORIAL DE SALIDAS Y DEVOLUCIONES", size=20, weight=ft.FontWeight.BOLD, color="#0F4C5C")
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
            contenedor_tabla.controls.append(ft.Text("No hay registros de salidas en el sistema.", italic=True, color="bluegrey400"))
            page.update()
            return

        filas = []
        for s in historico:
            uuid_j = s.get("uuid_juguete", s.get("uuid"))
            nombre_j = s.get("nombre", "Sin Nombre")
            
            # Botón dinámico configurado con 'content' para evitar errores visuales
            btn_revertir = ft.ElevatedButton(
                content=ft.Text("Devolver", color="white"),
                bgcolor="#E2711D",
                on_click=lambda e, uid=uuid_j: ejecutar_reversion(uid)
            )

            filas.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(s.get("fecha_salida", ""))),
                        ft.DataCell(ft.Text(nombre_j.upper())),
                        ft.DataCell(ft.Text(s.get("tipo_salida", "").upper())),
                        ft.DataCell(ft.Text(s.get("detalle_destino", ""))),
                        ft.DataCell(ft.Text(f"${s.get('precio_final', 0.0)}")),
                        ft.DataCell(btn_revertir),
                    ]
                )
            )

        tabla = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Fecha")),
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

    def ejecutar_reversion(uuid_juguete):
        exito, msg = GestorSalidas.revertir_salida(uuid_juguete)
        if exito:
            lbl_mensaje.value = msg
            lbl_mensaje.color = "green"
            cargar_tabla_historial()
        else:
            lbl_mensaje.value = msg
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