import os
import sys
import subprocess

def main():
    # Configura las rutas según tu estructura de proyecto
    base_path = os.path.dirname(os.path.abspath(__file__))
    
    # Intenta detectar automáticamente las rutas
    backend_path = os.path.join(base_path, "backend")
    frontend_path = os.path.join(base_path, "frontend")
    
    # Si no existen en la ubicación por defecto, pregunta al usuario
    if not os.path.exists(backend_path):
        backend_path = input("Ingresa la ruta completa del backend: ")
    
    if not os.path.exists(frontend_path):
        frontend_path = input("Ingresa la ruta completa del frontend: ")
    
    # Verificar que las rutas existen
    if not os.path.exists(backend_path):
        print(f"Error: La ruta del backend no existe: {backend_path}")
        return
    
    if not os.path.exists(frontend_path):
        print(f"Error: La ruta del frontend no existe: {frontend_path}")
        return
    
    print(f"Backend path: {backend_path}")
    print(f"Frontend path: {frontend_path}")
    
    # Definir los comandos a ejecutar
    backend_cmd = f'uvicorn config.asgi:application --reload --interface asgi3'
    frontend_cmd = f'pnpm run dev'
    
    # Ejecutar en terminales separados (solución para Windows)
    try:
        # Abrir backend en nueva ventana de terminal
        subprocess.Popen(f'start cmd /k "cd {backend_path} && {backend_cmd}"', shell=True)
        
        # Esperar un momento para que el primer terminal se abra
        import time
        time.sleep(2)
        
        # Abrir frontend en nueva ventana de terminal
        subprocess.Popen(f'start cmd /k "cd {frontend_path} && {frontend_cmd}"', shell=True)
        
        print("Ambos servidores están iniciando en terminales separados...")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()