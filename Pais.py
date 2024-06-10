import requests


class Pais:
    id_pais: int = None
    nombre: str
    capital: str
    region: str
    subregion: str
    cca2: str
    cca3: str
    pertenece_a_UE: bool
    fronteras: list[str]

    def __init__(self, nombre="", capital="", region="", subregion="", cca2="", cca3="", pertenece_a_UE=False, fronteras=[]):
        self.nombre = nombre
        self.capital = capital
        self.region = region
        self.subregion = subregion
        self.cca2 = cca2
        self.cca3 = cca3
        self.pertenece_a_UE = pertenece_a_UE
        self.fronteras = fronteras

    def __str__(self) -> str:
        return f"{self.nombre}, {self.capital}, {self.region}, {self.subregion}, {self.cca2}, {self.cca3}, {self.pertenece_a_UE}, {self.fronteras}"
    
    @staticmethod
    def peticion_api(url):
        resultado = ""
        
        try:
            resultado = requests.get(url).json()
        except Exception as e:
            print("ERROR Pais.py: No se ha podido conectar con la API.")
        
        return resultado
    
    def obtener_datos_de_paises(self, url):
        """Obtener el resultado de la API formateado a objeto Pais"""
        paises_api = self.peticion_api(url)
        paises_formateados = self.formatear_json_a_obj_pais(paises_api)

        return paises_formateados
    
    def formatear_json_a_obj_pais(self, json):
        paises: list[object] = []

        for pais in json:
            pais_aux = self.obtener_datos_de_dict_pais(pais)
            paises.append(pais_aux)
        
        return paises
    
    def obtener_datos_de_dict_pais(self, dict_pais):
        pais = None
        try:
            nombre = dict_pais["name"]["common"]
            capital = dict_pais["capital"][0]
            region = dict_pais["region"]
            subregion = dict_pais["subregion"]
            cca2 = dict_pais["cca2"]
            cca3 = dict_pais["cca3"]
            pertenece_a_UE = True
            fronteras = dict_pais["borders"]

            pais = Pais(nombre, capital, region, subregion, cca2, cca3, pertenece_a_UE, fronteras)
        except Exception as e:
            print(f"Excepción encontrada: {e}\n{dict_pais}")
        
        return pais
