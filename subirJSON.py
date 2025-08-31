import json
import pyodbc
import re
from datetime import datetime

# Configuración de conexión a SQL Server
server = 'localhost'
database = 'BASE'
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

# Leer el archivo JSON
with open('personal.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Función para limpiar y convertir valores
def clean_value(value, field_type):
    if value is None or value == '':
        return None
    
    if field_type == 'int':
        try:
            return int(value)
        except:
            return None
    elif field_type == 'float' or field_type == 'decimal':
        # Extraer números de cadenas como " S/ 3,000.00 "
        if isinstance(value, str):
            numbers = re.findall(r'[\d,]+\.?\d*', value)
            if numbers:
                clean_num = numbers[0].replace(',', '')
                try:
                    return float(clean_num)
                except:
                    return None
        try:
            return float(value)
        except:
            return None
    elif field_type == 'date':
        try:
            return datetime.strptime(value, '%Y-%m-%d').date()
        except:
            return None
    elif field_type == 'bit':
        return bool(int(value)) if value != '' else False
    else:
        return str(value).strip()

# Preparar la consulta de inserción
insert_query = """
INSERT INTO [dbo].[administracion_personal] (
    dni, nombre, apellido, n_contrato, dependencia_id, activo, es_conductor, acceso,
    fecha_habilitacion_acceso, habilitado_por_id, email, user_id, celular, email_per,
    ruc, cel_emergencia, cont_emergencia, direccion, distrito, fecha_fin, fecha_inicio,
    fecha_nac, n_hijos, padre_madre, salario, sexo, telefono, anexo_id, area_id,
    cargo_id, condicion_id, estado_id, generica_id, grupo_ocupacional_id, profesion_id,
    nivel_id, regimen_id
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

# Insertar cada registro
for record in data:
    # Limpiar y convertir los valores
    values = (
        clean_value(record.get('dni'), 'str'),
        clean_value(record.get('nombre'), 'str'),
        clean_value(record.get('apellido'), 'str'),
        clean_value(record.get('n_contrato'), 'str'),
        clean_value(record.get('dependencia_id'), 'int'),
        clean_value(record.get('activo'), 'bit'),
        clean_value(record.get('es_conductor'), 'bit'),
        clean_value(record.get('acceso'), 'bit'),
        clean_value(record.get('fecha_habilitacion_acceso'), 'date'),
        clean_value(record.get('habilitado_por_id'), 'int'),
        clean_value(record.get('email'), 'str'),
        clean_value(record.get('user_id'), 'str'),
        clean_value(record.get('celular'), 'str'),
        clean_value(record.get('email_per'), 'str'),
        clean_value(record.get('ruc'), 'str'),
        clean_value(record.get('cel_emergencia'), 'str'),
        clean_value(record.get('cont_emergencia'), 'str'),
        clean_value(record.get('direccion'), 'str'),
        clean_value(record.get('distrito'), 'str'),
        clean_value(record.get('fecha_fin'), 'date'),
        clean_value(record.get('fecha_inicio'), 'date'),
        clean_value(record.get('fecha_nac'), 'date'),
        clean_value(record.get('n_hijos'), 'int'),
        clean_value(record.get('padre_madre'), 'str'),
        clean_value(record.get('salario'), 'decimal'),
        clean_value(record.get('sexo'), 'str'),
        clean_value(record.get('telefono'), 'str'),
        clean_value(record.get('anexo_id'), 'int'),
        clean_value(record.get('area_id'), 'int'),
        clean_value(record.get('cargo_id'), 'int'),
        clean_value(record.get('condicion_id'), 'int'),
        clean_value(record.get('estado_id'), 'int'),
        clean_value(record.get('generica_id'), 'int'),
        clean_value(record.get('grupo_ocupacional_id'), 'int'),
        clean_value(record.get('profesion_id'), 'int'),
        clean_value(record.get('nivel_id'), 'int'),
        clean_value(record.get('regimen_id'), 'int')
    )
    
    # Ejecutar la inserción
    cursor.execute(insert_query, values)

# Confirmar y cerrar la conexión
conn.commit()
conn.close()

print("Datos importados exitosamente!")