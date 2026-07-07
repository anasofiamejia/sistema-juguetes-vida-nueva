class Juguete:

    def __init__(self, uuid, nombre, marca, material, alto_cm, ancho_cm, largo_cm, usa_baterias, incluye, estado_fisico, piezas_faltantes, triaje_resultado, categoria, precio_usd):

        self.uuid = uuid
        self.nombre = nombre
        self.marca = marca
        self.material = material
        self.alto_cm = alto_cm
        self.ancho_cm = ancho_cm
        self.largo_cm = largo_cm
        self.usa_baterias = usa_baterias
        self.incluye = incluye
        self.estado_fisico = estado_fisico
        self.piezas_faltantes = piezas_faltantes
        self.triaje_resultado = triaje_resultado
        self.categoria = categoria
        self.precio_usd = precio_usd


    def mostrar_ficha_tecnica(self):
       
        print(f"--- JUGUETE: {self.nombre} ({self.uuid}) ---")
        print(f"Marca: {self.marca} | Material: {self.material}")
        print(f"Dimensiones: {self.alto_cm}x{self.ancho_cm}x{self.largo_cm} cm")
        print(f"Estado: {self.estado_fisico} | ¿Faltan piezas?: {self.piezas_faltantes}")
        print(f"Destino: {self.triaje_resultado.upper()} | Precio: ${self.precio_usd}")
        print("-" * 40)
