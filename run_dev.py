import os
import sys
import subprocess
import threading

def run_command(command, cwd):
    """Ejecuta un comando en el directorio especificado"""
    try:
        print(f"Ejecutando: {command} en {cwd}")
        process = subprocess.Popen(
            command,
            cwd=cwd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
        
        # Imprimir la salida en tiempo real
        for line in process.stdout:
            print(f"[{os.path.basename(cwd)}] {line}", end='')
            
        process.wait()
        return process.returncode
    except Exception as e:
        print(f"Error ejecutando comando: {e}")
        return 1

def main():
    # Configura las rutas según tu estructura de proyecto
    # Puedes modificar estas rutas para cada computadora
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
    backend_cmd = "uvicorn config.asgi:application --reload --interface asgi3"
    frontend_cmd = "pnpm run dev"
    
    # Ejecutar ambos comandos en hilos separados
    threads = []
    
    # Hilo para el backend
    backend_thread = threading.Thread(
        target=run_command, 
        args=(backend_cmd, backend_path)
    )
    backend_thread.daemon = True
    threads.append(backend_thread)
    
    # Hilo para el frontend
    frontend_thread = threading.Thread(
        target=run_command, 
        args=(frontend_cmd, frontend_path)
    )
    frontend_thread.daemon = True
    threads.append(frontend_thread)
    
    # Iniciar los hilos
    for thread in threads:
        thread.start()
    
    print("Ambos servidores están iniciando...")
    print("Presiona Ctrl+C para detener ambos servidores")
    
    # Esperar a que todos los hilos terminen (o hasta Ctrl+C)
    try:
        for thread in threads:
            thread.join()
    except KeyboardInterrupt:
        print("\nDeteniendo servidores...")

if __name__ == "__main__":
    main()