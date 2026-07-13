class Juguete:
    def __init__(self, uuid, nombre, marca, categoria, material, alto_cm, ancho_cm, largo_cm, usa_baterias, incluye, estado_fisico, piezas_faltantes, triaje_resultado, precio_usd):
        self.uuid = uuid
        self.nombre = nombre
        self.marca = marca
        self.categoria = categoria 
        self.material = material
        self.alto_cm = float(alto_cm)
        self.ancho_cm = float(ancho_cm)
        self.largo_cm = float(largo_cm)
        self.usa_baterias = bool(usa_baterias)
        self.incluye = incluye
        self.estado_fisico = estado_fisico
        self.piezas_faltantes = bool(piezas_faltantes)
        self.triaje_resultado = triaje_resultado  # "venta", "donacion", "reciclaje"
        self.precio_usd = float(precio_usd)

    @classmethod
    def desde_diccionario(cls, datos):
        return cls(
            uuid=datos.get("uuid"),
            nombre=datos.get("nombre"),
            marca=datos.get("marca"),
            categoria=datos.get("categoria", "Otros"),
            material=datos.get("material"),
            alto_cm=datos.get("alto_cm", 0.0),
            ancho_cm=datos.get("ancho_cm", 0.0),
            largo_cm=datos.get("largo_cm", 0.0),
            usa_baterias=datos.get("usa_baterias", False),
            incluye=datos.get("incluye", "n/a"),
            estado_fisico=datos.get("estado_fisico", "bueno"),
            piezas_faltantes=datos.get("piezas_faltantes", False),
            triaje_resultado=datos.get("triaje_resultado"),
            precio_usd=datos.get("precio_usd", 0.0)
        )
    
    def to_dict(self):
        return {
            "uuid": self.uuid,
            "nombre": self.nombre,
            "marca": self.marca,
            "categoria": self.categoria,
            "material": self.material,
            "alto_cm": self.alto_cm,
            "ancho_cm": self.ancho_cm,
            "largo_cm": self.largo_cm,
            "usa_baterias": self.usa_baterias,
            "incluye": self.incluye,
            "estado_fisico": self.estado_fisico,
            "piezas_faltantes": self.piezas_faltantes,
            "triaje_resultado": self.triaje_resultado,
            "precio_usd": self.precio_usd
        }