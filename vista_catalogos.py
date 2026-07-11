import flet as ft

class ComponenteCatalogos:

    @staticmethod
    def crear_tarjeta_comercial_social(juguete_obj):
        es_venta = juguete_obj.triaje_resultado == "venta"

        color_borde = "orange" if es_venta else "purple"
        badge_color = "orange" if es_venta else "purple"
        texto_color_titulo = "#E65100" if es_venta else "#4A148C"

        texto_inferior = f"Precio: ${juguete_obj.precio_usd:.2f} USD" if es_venta else "Costo: Gratis ($0.00)"

        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text(juguete_obj.nombre.upper(), size=14, weight=ft.FontWeight.BOLD, color=texto_color_titulo),
                    ft.Container(
    content=ft.Text(juguete_obj.estado_fisico.upper(), size=10, color="white", weight=ft.FontWeight.BOLD),
    bgcolor=badge_color,
    padding=6,
    border_radius=4
),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Text(f"Marca: {juguete_obj.marca} | Categoría: {juguete_obj.categoria}", size=12, color="bluegrey500"),
                ft.Text(f"Incluye: {juguete_obj.incluye}", size=11, max_lines=2, overflow=ft.TextOverflow.ELLIPSIS, color="bluegrey700"),
                ft.Divider(height=1, color="grey200"),
                ft.Text(texto_inferior, size=13, weight=ft.FontWeight.BOLD, color="bluegrey900")
            ], spacing=8),
            bgcolor="white",
            padding=15,
            border_radius=8,
            border=ft.Border.all(1.5, color_borde),
            width=380
        )
    
    @staticmethod
    def crear_tabla_residuos(lista_juguetes_reciclaje):
        
        columnas = [
            ft.DataColumn(ft.Text("ID/UUID", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Juguete", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Material", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Dimensiones (Al x An x La)", weight=ft.FontWeight.BOLD)),
        ]

        filas = []
        for j in lista_juguetes_reciclaje:
            filas.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(j.uuid)),
                        ft.DataCell(ft.Text(j.nombre)),
                        
                        ft.DataCell(ft.Text(j.material, weight=ft.FontWeight.BOLD, color="green")),
                        ft.DataCell(ft.Text(f"{j.alto_cm} x {j.ancho_cm} x {j.largo_cm} cm")),
                    ]
                )
            )


        return ft.DataTable(
            columns=columnas,
            rows=filas,
            heading_row_color="grey100",
            border=ft.Border.all(1, "green"), 
            border_radius=5
        )