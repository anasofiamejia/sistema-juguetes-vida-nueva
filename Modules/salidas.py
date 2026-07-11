import datetime
import json

class GestorSalidas:
    
    @staticmethod
    def registrar_salida(juguete_completo, tipo_salida, detalle_destino, precio_final=0.0):
        """
        Guarda automáticamente el objeto completo de CUALQUIER juguete en el histórico
        y lo elimina del inventario activo.
        """
        try:
            # 1. Registrar en el Histórico de Salidas con los datos completos
            try:
                with open("Data/historico_salidas.json", "r", encoding="utf-8") as f:
                    historico = json.load(f)
            except Exception:
                historico = []

            # Clonamos el juguete y añadimos metadatos de la salida
            nueva_salida = juguete_completo.copy()
            nueva_salida["fecha_salida"] = str(datetime.date.today())
            nueva_salida["tipo_salida"] = tipo_salida
            nueva_salida["detalle_destino"] = detalle_destino
            nueva_salida["precio_final"] = precio_final
            nueva_salida["uuid_juguete"] = juguete_completo.get("uuid")

            historico.append(nueva_salida)

            with open("Data/historico_salidas.json", "w", encoding="utf-8") as f:
                json.dump(historico, f, indent=4, ensure_ascii=False)

            # 2. Eliminarlo del inventario activo (inventario.json)
            with open("Data/inventario.json", "r", encoding="utf-8") as f:
                inventario = json.load(f)

            inventario = [j for j in inventario if j.get("uuid") != juguete_completo.get("uuid")]

            with open("Data/inventario.json", "w", encoding="utf-8") as f:
                json.dump(inventario, f, indent=4, ensure_ascii=False)

            return True, f"Salida de '{juguete_completo.get('nombre')}' procesada con éxito."
        except Exception as e:
            return False, f"Error al procesar la salida: {str(e)}"

    @staticmethod
    def revertir_salida(uuid_juguete):
        """
        Recupera automáticamente CUALQUIER juguete restaurando todos sus campos originales.
        """
        try:
            with open("Data/historico_salidas.json", "r", encoding="utf-8") as f:
                historico = json.load(f)
            
            salida_a_revertir = next((s for s in historico if s.get("uuid_juguete") == uuid_juguete), None)
            
            if not salida_a_revertir:
                return False, "No se encontró el registro en el historial."

            # Limpiamos las propiedades añadidas en la salida para restaurar el juguete original
            nuevo_juguete = salida_a_revertir.copy()
            nuevo_juguete.pop("fecha_salida", None)
            nuevo_juguete.pop("tipo_salida", None)
            nuevo_juguete.pop("detalle_destino", None)
            nuevo_juguete.pop("precio_final", None)
            nuevo_juguete.pop("uuid_juguete", None)

            # Reinyectar al inventario activo
            try:
                with open("Data/inventario.json", "r", encoding="utf-8") as f:
                    inventario = json.load(f)
            except Exception:
                inventario = []
                
            inventario.append(nuevo_juguete)
            
            with open("Data/inventario.json", "w", encoding="utf-8") as f:
                json.dump(inventario, f, indent=4, ensure_ascii=False)

            # Eliminar del historial de salidas
            historico.remove(salida_a_revertir)
            with open("Data/historico_salidas.json", "w", encoding="utf-8") as f:
                json.dump(historico, f, indent=4, ensure_ascii=False)

            return True, f"¡El juguete '{nuevo_juguete.get('nombre')}' ha vuelto al inventario de forma automática!"
        except Exception as e:
            return False, f"Error: {str(e)}"
    