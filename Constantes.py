# Constantes de configuración de conexión con la base de datos.
BDD_user: str ='root'
BDD_password: str ='root'
BDD_host: str ='127.0.0.1'
BDD_port: str ='3306'
BDD_database_name: str ='temperaturas'

# URL de la API openweathermap
OPENWEATHERMAP_API_URL = "https://api.openweathermap.org/data/2.5/"
# Token de acceso a la API openweathermap
OPENWEATHERMAP_API_KEY = "a60fef3fc371c50c0c57c17361925fad"

# URL de la API restcountries
RESTCOUNTRIES_API_URL: str = "https://restcountries.com/v3.1/region/europe?fields=name,capital,currencies,region,subregion,cca2,cca3,region,borders"

# Estas constantes se utilizan en classes/Data_base.py
PALABRA_ESPECIAL_SELECT: str = "SELECT"
PALABRA_ESPECIAL_INSERT: str = "INSERT"
MENSAJE_ERROR_CONSULTA_PALABRA_ESPECIAL_SELECT: str = "ERROR Data_base.py: No has introducido una consulta SQL que empiece por 'SELECT '"
MENSAJE_ERROR_CONSULTA_PALABRA_ESPECIAL_INSERT: str = "ERROR Data_base.py: No has introducido una consulta SQL que empiece por 'INSERT '"
MENSAJE_ERROR_SINTAXIS_SELECT: str = "ERROR Data_base.py: No has escrito una consulta SELECT válida, hay errores de sintaxis o nombres inválidos."
MENSAJE_ERROR_SINTAXIS_INSERT: str = "ERROR Data_base.py: No has escrito una consulta INSERT válida, hay errores de sintaxis o nombres inválidos."
MENSAJE_ERROR_BUSCATE_LA_VIDA: str = "ERROR Data_base.py: No se ha podido conectar con la base de datos, búscate la vida xdd"
