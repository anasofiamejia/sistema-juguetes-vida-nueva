import datetime
import json

class GestorSalidas:
    
    @staticmethod
    # 💡 Le agregamos ', usuario_nombre="Admin"' al final de los parámetros de la función
    def registrar_salida(juguete_completo=None, tipo_salida="", detalle_destino="", precio_final=0.0, juguete_id=None, usuario_nombre="Admin"):
        
        import datetime
        try:
            # 1. Leer el inventario activo para buscar el juguete si nos pasaron un id/uuid
            with open("Data/inventario.json", "r", encoding="utf-8") as f:
                inventario = json.load(f)

            # Si la interfaz nos mandó 'juguete_id', buscamos el objeto completo aquí
            if juguete_completo is None and juguete_id is not None:
                juguete_completo = next((j for j in inventario if j.get("uuid") == juguete_id or j.get("id") == juguete_id), None)

            if not juguete_completo:
                return False, "No se encontró el juguete especificado en el inventario activo."

            # 2. Registrar en el Histórico de Salidas con los datos completos del objeto
            try:
                with open("Data/historico_salidas.json", "r", encoding="utf-8") as f:
                    historico = json.load(f)
            except Exception:
                historico = []

            # Clonamos el juguete y agregamos los metadatos de la salida
            nueva_salida = juguete_completo.copy()
            nueva_salida["fecha_salida"] = str(datetime.date.today())
            nueva_salida["usuario_id"] = usuario_nombre  # 💡 ¡ESTA ES LA LÍNEA NUEVA QUE GUARDA AL USUARIO RESPONSABLE!
            nueva_salida["tipo_salida"] = tipo_salida
            nueva_salida["detalle_destino"] = detalle_destino
            nueva_salida["precio_final"] = precio_final
            nueva_salida["uuid_juguete"] = juguete_completo.get("uuid")

            historico.append(nueva_salida)

            with open("Data/historico_salidas.json", "w", encoding="utf-8") as f:
                json.dump(historico, f, indent=4, ensure_ascii=False)

            # 3. Eliminarlo del inventario activo
            inventario = [j for j in inventario if j.get("uuid") != juguete_completo.get("uuid")]

            with open("Data/inventario.json", "w", encoding="utf-8") as f:
                json.dump(inventario, f, indent=4, ensure_ascii=False)

            return True, f"Salida de '{juguete_completo.get('nombre')}' procesada con éxito."
        except Exception as e:
            return False, f"Error al procesar la salida: {str(e)}"

    @staticmethod
    def revertir_salida(uuid_juguete):
        
        try:
            with open("Data/historico_salidas.json", "r", encoding="utf-8") as f:
                historico = json.load(f)
            
            salida_a_revertir = next((s for s in historico if s.get("uuid_juguete") == uuid_juguete), None)
            
            if not salida_a_revertir:
                return False, "No se encontró el registro en el historial."

            # Limpiamos las propiedades añadidas en la salida para restaurar el juguete original
            nuevo_juguete = salida_a_revertir.copy()
            nuevo_juguete.pop("fecha_salida", None)
            nuevo_juguete.pop("usuario_id", None) # 💡 También limpiamos el usuario al devolver el juguete al almacén
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