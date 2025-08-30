import os
import sys
import subprocess
import time

def open_terminal(command, cwd, title):
    """Abre una nueva terminal y ejecuta el comando"""
    try:
        if sys.platform == "win32":
            # Windows
            subprocess.Popen(f'start cmd /k "title {title} && cd /d {cwd} && {command}"', shell=True)
        elif sys.platform == "darwin":
            # macOS
            subprocess.Popen([
                'osascript', '-e',
                f'tell app "Terminal" to do script "cd {cwd} && {command}"'
            ])
        else:
            # Linux
            subprocess.Popen([
                'gnome-terminal', '--', 'bash', '-c',
                f'cd {cwd} && {command}; exec bash'
            ])
        return True
    except Exception as e:
        print(f"Error abriendo terminal para {title}: {e}")
        return False

def start_redis_container():
    """Inicia el contenedor de Redis si existe, o crea uno nuevo si no existe"""
    try:
        # Verificar si el contenedor existe
        result = subprocess.run(
            ['docker', 'ps', '-a', '--filter', 'name=redis', '--format', '{{.Names}}'],
            capture_output=True, text=True, check=True
        )
        
        if 'redis' in result.stdout:
            print("🔄 Contenedor Redis encontrado, iniciando...")
            # Iniciar el contenedor existente
            subprocess.run(['docker', 'start', 'redis'], check=True)
            print("✅ Redis iniciado (contenedor existente)")
        else:
            print("🐳 Creando nuevo contenedor Redis...")
            # Crear nuevo contenedor
            subprocess.run([
                'docker', 'run', '--name', 'redis', '-d', 
                '-p', '6379:6379', 'redis'
            ], check=True)
            print("✅ Nuevo contenedor Redis creado y ejecutándose")
        
        # Verificar que Redis esté funcionando
        time.sleep(2)  # Esperar a que Redis se inicie
        health_check = subprocess.run(
            ['docker', 'exec', 'redis', 'redis-cli', 'ping'],
            capture_output=True, text=True
        )
        
        if 'PONG' in health_check.stdout:
            print("✅ Redis respondiendo correctamente")
        else:
            print("⚠️  Redis iniciado pero no responde PONG")
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al manejar Redis: {e}")
        print("Asegúrate de que Docker esté ejecutándose")
    except Exception as e:
        print(f"❌ Error inesperado con Redis: {e}")

def main():
    # Configura las rutas según tu estructura de proyecto
    base_path = os.path.dirname(os.path.abspath(__file__))

    # Intenta detectar automáticamente las rutas
    backend_path = os.path.join(base_path, "backend")
    frontend_path = os.path.join(base_path, "frontend")

    # Verificar si las rutas existen
    if not os.path.exists(backend_path):
        print(f"Error: No se encuentra el directorio backend en {backend_path}")
        sys.exit(1)

    if not os.path.exists(frontend_path):
        print(f"Error: No se encuentra el directorio frontend en {frontend_path}")
        sys.exit(1)

    print(f"Backend path: {backend_path}")
    print(f"Frontend path: {frontend_path}")

    # Iniciar Redis primero
    print("\n🐳 Iniciando Redis Docker container...")
    start_redis_container()

    # Pequeña pausa después de iniciar Redis
    time.sleep(1)

    # Definir los comandos a ejecutar
    backend_cmd = "uvicorn config.asgi:application --reload --interface asgi3"
    frontend_cmd = "pnpm run dev"

    # Abrir backend en terminal separada
    print("\n🌐 Abriendo backend en terminal separada...")
    if open_terminal(backend_cmd, backend_path, "Backend Server"):
        print("✅ Backend iniciado")
    else:
        print("❌ Error al iniciar backend")

    # Pequeña pausa para que las terminales no se abran encimadas
    time.sleep(1)

    # Abrir frontend en terminal separada
    print("\n⚛️  Abriendo frontend en terminal separada...")
    if open_terminal(frontend_cmd, frontend_path, "Frontend Server"):
        print("✅ Frontend iniciado")
    else:
        print("❌ Error al iniciar frontend")

    print("\n🎯 Todos los servicios están iniciando...")
    print("   - Redis Docker ✅")
    print("   - Backend Server ✅") 
    print("   - Frontend Server ✅")
    print("\n⚠️  Cierra las terminales manualmente cuando termines")

if __name__ == "__main__":
    main()