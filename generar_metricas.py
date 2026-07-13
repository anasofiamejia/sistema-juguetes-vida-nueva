import json
import os

def generar_reporte_datos():
    ruta_json = "Data/inventario.json"
    
    if not os.path.exists(ruta_json):
        print(f"❌ Error: No se encontró el archivo en {ruta_json}")
        return

    try:
        with open(ruta_json, "r", encoding="utf-8") as f:
            inventario = json.load(f)
    except Exception as e:
        print(f"❌ Error al leer el JSON: {e}")
        return

    total_juguetes = len(inventario)
    
    # Contadores por destino (triaje_resultado)
    conteo_destinos = {
        "venta": 0,
        "donacion": 0,
        "reciclaje": 0
    }
    
    # Contadores por materiales (para la Escuela de Reciclaje)
    conteo_materiales = {}
    
    # Contadores por categorías
    conteo_categorias = {}

    for item in inventario:
        # 1. Clasificación por destino
        destino = item.get("triaje_resultado", "No clasificado").lower()
        if destino in conteo_destinos:
            conteo_destinos[destino] += 1
            
        # 2. Clasificación por material (solo si fue a reciclaje)
        if destino == "reciclaje" and "material" in item:
            mat = item["material"].capitalize()
            conteo_materiales[mat] = conteo_materiales.get(mat, 0) + 1
            
        # 3. Clasificación por categoría
        cat = item.get("categoria", "Sin Categoría")
        conteo_categorias[cat] = conteo_categorias.get(cat, 0) + 1

    # --- IMPRESIÓN DEL REPORTE EN TERMINAL ---
    print("=" * 50)
    print(" REPORTE DE DATOS PRELIMINAR - SEMANA 15")
    print("=" * 50)
    print(f"🔹 Total de juguetes registrados en el sistema: {total_juguetes}\n")
    
    print(" DISTRIBUCIÓN POR DESTINO (INDICADORES DE CIRCULARIDAD):")
    for destino, cantidad in conteo_destinos.items():
        porcentaje = (cantidad / total_juguetes * 100) if total_juguetes > 0 else 0
        print(f"  • {destino.upper()}: {cantidad} unidades ({porcentaje:.1f}%)")
    
    print("\n MATERIALES DESVIADOS A RECICLAJE (ESCUELA DE RECICLAJE):")
    if conteo_materiales:
        for material, cantidad in conteo_materiales.items():
            print(f"  • {material}: {cantidad} componentes listos para reinsertar")
    else:
        print("  • No hay juguetes registrados para reciclaje en este momento.")

    print("\n DISTRIBUCIÓN POR CATEGORÍAS (CONTROL DE INVENTARIO):")
    for cat, cantidad in conteo_categorias.items():
        print(f"  • {cat}: {cantidad} unidades")
    print("=" * 50)

if __name__ == "__main__":
    generar_reporte_datos()