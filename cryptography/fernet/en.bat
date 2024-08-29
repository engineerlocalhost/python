@echo off
REM Ganti dengan path ke direktori Python Anda jika perlu
set PYTHON_PATH=C:\Users\captennem0\AppData\Local\Programs\Python\Python312

REM Ganti dengan path ke file skrip Python Anda
set SCRIPT_PATH=D:\en.py

REM Menjalankan skrip Python
"%PYTHON_PATH%\python.exe" "%SCRIPT_PATH%"

REM Menutup jendela Command Prompt secara otomatis setelah selesai
exit