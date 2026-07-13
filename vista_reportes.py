import json
import os
import flet as ft

def crear_vista_reportes(page, usuario, volver_menu_fn):
    ruta_json = "Data/inventario.json"
    
    # 1. LEER DATOS REALES DEL INVENTARIO
    try:
        with open(ruta_json, "r", encoding="utf-8") as f:
            inventario = json.load(f)
    except Exception:
        inventario = []

    total = len(inventario)
    venta = sum(1 for j in inventario if j.get("triaje_resultado") == "venta")
    donacion = sum(1 for j in inventario if j.get("triaje_resultado") == "donacion")
    reciclaje = sum(1 for j in inventario if j.get("triaje_resultado") == "reciclaje")

    p_venta = (venta / total * 100) if total > 0 else 0
    p_donacion = (donacion / total * 100) if total > 0 else 0
    p_reciclaje = (reciclaje / total * 100) if total > 0 else 0

    # 2. COMPONENTE: TARJETAS KPI
    def crear_tarjeta_kpi(titulo, valor, color_borde):
        return ft.Container(
            content=ft.Column([
                ft.Text(titulo, size=11, weight="bold", color="bluegrey400"),
                ft.Text(str(valor), size=24, weight="bold", color="bluegrey900"),
            ], alignment="center", spacing=2),
            bgcolor="white", padding=10, border_radius=8,
            border=ft.Border.all(1.5, color_borde), width=150, height=80
        )

    tarjetas_kpi = ft.Row([
        crear_tarjeta_kpi("TOTAL PROCESADO", total, "#0F4C5C"),
        crear_tarjeta_kpi("EN VENTAS", venta, "orange"),
        crear_tarjeta_kpi("EN DONACIONES", donacion, "purple"),
        crear_tarjeta_kpi("A RECICLAJE", reciclaje, "green"),
    ], alignment="center", spacing=10)

    # 3. COMPONENTE: BARRAS DE PROGRESO (GRÁFICO)
    def crear_barra_impacto(label, porcentaje, color):
        return ft.Column([
            ft.Row([
                ft.Text(label, size=13, weight="bold"),
                ft.Text(f"{porcentaje:.1f}%", size=13, weight="bold", color=color)
            ], alignment="spaceBetween"),
            ft.ProgressBar(value=porcentaje/100, color=color, height=12, border_radius=5),
            ft.Container(height=5)
        ])

    seccion_grafico = ft.Container(
        content=ft.Column([
            crear_barra_impacto("Flujo Comercial (Ventas)", p_venta, "orange"),
            crear_barra_impacto("Flujo Social (Donaciones)", p_donacion, "purple"),
            crear_barra_impacto("Impacto Ambiental (Reciclaje)", p_reciclaje, "green"),
        ], spacing=10),
        padding=20, bgcolor="#F8F9FA", border_radius=10
    )

    # 4. DISEÑO DE LA PÁGINA (SOLO MÉTRICAS Y GRÁFICOS)
    layout_principal = ft.Column(
        controls=[
            ft.Row([
                ft.Text("📊 PANEL DE CONTROL ADMINISTRATIVO", size=18, weight="bold", color="#0F4C5C"),
                ft.ElevatedButton(
                    content=ft.Text("Atrás", color="white"), bgcolor="#0F4C5C",
                    on_click=lambda _: [page.views.pop(), page.update(), volver_menu_fn(usuario)]
                )
            ], alignment="spaceBetween"),
            ft.Divider(),
            
            ft.Text("Indicadores Clave de Desempeño (KPIs):", size=14, weight="bold", color="bluegrey700"),
            tarjetas_kpi,
            ft.Container(height=10),
            
            ft.Text("Distribución Ecológica del Inventario:", size=14, weight="bold", color="bluegrey700"),
            seccion_grafico,
        ],
        scroll="auto"
    )

    nueva_vista = ft.View(
        route="/reportes",
        controls=[ft.Container(content=layout_principal, padding=20)]
    )
    
    page.views.append(nueva_vista)
    page.update()