import pandas as pd
import pyodbc
from datetime import datetime

# Configuración de conexión a SQL Server
server = 'localhost'
database = 'TEST'
username = 'angel'
password = 'Starwar1'

# Establecer conexión
conn = pyodbc.connect(
    f'DRIVER={{ODBC Driver 17 for SQL Server}};'
    f'SERVER={server};'
    f'DATABASE={database};'
    f'UID={username};'
    f'PWD={password}'
)
cursor = conn.cursor()

# Leer el archivo Excel
archivo_excel = 'D:/POWERBI\DATA\DENGUE.xlsx'
df = pd.read_excel(archivo_excel)

# Función para limpiar y convertir valores
def clean_value(value, field_type):
    if pd.isna(value) or value == '':
        return None
    
    if field_type == 'int':
        try:
            return int(value)
        except:
            return None
    elif field_type == 'float':
        try:
            return float(value)
        except:
            return None
    elif field_type == 'date':
        try:
            if isinstance(value, str):
                return datetime.strptime(value, '%d/%m/%Y %H:%M')
            return value
        except:
            return None
    elif field_type == 'bit':
        if isinstance(value, str):
            if value.lower() == 'si' or value.lower() == 'yes' or value.lower() == 'true':
                return 1
            elif value.lower() == 'no' or value.lower() == 'not' or value.lower() == 'false':
                return 0
        try:
            return int(bool(value))
        except:
            return 0
    else:
        return str(value).strip()

# Preparar la consulta de inserción
insert_query = """
INSERT INTO [dbo].[OPENLINE] (
    FECHA_HORA, APELLIDOS, NOMBRES, TELEFONO, CORREO, ESTABLECIMIENTO, CODIGO,
    INSTITUCION, DEPARTAMENTO, PROVINCIA, DISA, DISTRITO, CATEGORIA,
    TOTAL_HOSP_GENERAL, TOTAL_HOSP_GESTANTES_, SILLAS_PACIENTES, CAMILLAS_PACIENTES,
    TRANSITORIOS_PACIENTES, GESTANTES_DENGUE, UCI_OCUPADAS_DENGUE, UCI_OCUPADAS_GESTANTES,
    CAMAS_OFERTADAS_UVICLIN, CAMAS_OCUPADAS_UVICLIN, UNIDAD_FEBRIL, CAMILLAS_FEBRIL,
    CAMILLAS_FEBRIL_OCUP, UCIN_OCUPADAS_DENGUE
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

# Insertar cada registro
for index, row in df.iterrows():
    # Limpiar y convertir los valores
    values = (
        clean_value(row.get('FECHA_HORA'), 'date'),
        clean_value(row.get('APELLIDOS'), 'str'),
        clean_value(row.get('NOMBRES'), 'str'),
        clean_value(row.get('TELEFONO'), 'str'),
        clean_value(row.get('CORREO'), 'str'),
        clean_value(row.get('ESTABLECIMIENTO'), 'str'),
        clean_value(row.get('CODIGO'), 'str'),
        clean_value(row.get('INSTITUCION'), 'str'),
        clean_value(row.get('DEPARTAMENTO'), 'str'),
        clean_value(row.get('PROVINCIA'), 'str'),
        clean_value(row.get('DISA'), 'str'),
        clean_value(row.get('DISTRITO'), 'str'),
        clean_value(row.get('CATEGORIA'), 'str'),
        clean_value(row.get('TOTAL_HOSP_GENERAL'), 'int'),
        clean_value(row.get('TOTAL_HOSP_GESTANTES_'), 'int'),
        clean_value(row.get('SILLAS_PACIENTES'), 'int'),
        clean_value(row.get('CAMILLAS_PACIENTES'), 'int'),
        clean_value(row.get('TRANSITORIOS_PACIENTES'), 'int'),
        clean_value(row.get('GESTANTES_DENGUE'), 'int'),
        clean_value(row.get('UCI_OCUPADAS_DENGUE'), 'int'),
        clean_value(row.get('UCI_OCUPADAS_GESTANTES'), 'int'),
        clean_value(row.get('CAMAS_OFERTADAS_UVICLIN'), 'int'),
        clean_value(row.get('CAMAS_OCUPADAS_UVICLIN'), 'int'),
        clean_value(row.get('UNIDAD_FEBRIL'), 'str'),
        clean_value(row.get('CAMILLAS_FEBRIL'), 'int'),
        clean_value(row.get('CAMILLAS_FEBRIL_OCUP'), 'int'),
        clean_value(row.get('UCIN_OCUPADAS_DENGUE'), 'int')
    )
    
    # Ejecutar la inserción
    try:
        cursor.execute(insert_query, values)
    except Exception as e:
        print(f"Error insertando fila {index}: {e}")
        print(f"Datos: {values}")
        continue

# Confirmar y cerrar la conexión
conn.commit()
conn.close()

print("Datos importados exitosamente a la tabla OPENLINE!")