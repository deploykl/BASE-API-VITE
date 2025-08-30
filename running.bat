@echo off
chcp 65001 > nul
echo ====================================
echo    INICIANDO BACKEND Y FRONTEND
echo ====================================

REM Verificar si Python está instalado
python --version > nul 2>&1
if errorlevel 1 (
    echo Error: Python no está instalado o no está en el PATH
    pause
    exit /b 1
)

REM Ejecutar el script de Python
python run_dev.py
pause