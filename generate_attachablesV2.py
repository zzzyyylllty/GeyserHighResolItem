@echo off
chcp 65001 >nul
title Bedrock Large Item Generator v2.0
color 0B

:: Define color codes
set INFO= 
set SUCCESS= 
set WARNING= 
set ERROR= 
set RESET= 
set BOLD= 
set TITLE= 

cls
echo.
echo ================================================================
echo                                                                 
echo          Bedrock Edition Large Item Generator v2.0            
echo                                                                 
echo ================================================================
echo.
echo Step 1: Preparation
echo ----------------------------------------------------------------
echo.
echo   Please place your Bedrock Edition resource pack in the
echo   'input' folder.
echo   The structure should be: input/textures/...
echo.
echo   Press ENTER to continue...
pause >nul

echo.
echo Step 2: Validation
echo ----------------------------------------------------------------
echo.

echo   [CHECK] Checking for input folder...
if not exist "input" (
    color 0C
    echo   [ERROR] 'input' folder not found!
    echo.
    echo   Please create an 'input' folder and place your resource pack inside.
    echo.
    pause
    exit /b 1
)
echo   [OK] Input folder found.

echo   [CHECK] Checking for Python environment...
python --version >nul 2>&1
if errorlevel 1 (
    color 0C
    echo   [ERROR] Python is not installed or not in PATH!
    echo.
    echo   Please install Python 3.x and try again.
    echo.
    pause
    exit /b 1
)
echo   [OK] Python environment ready.

echo.
echo Step 3: Processing
echo ----------------------------------------------------------------
echo.

echo   [INFO] Creating output folder...
if exist "output" (
    echo   [INFO] Cleaning existing output folder...
    rmdir /s /q "output"
)

echo   [INFO] Copying input to output...
xcopy "input" "output\" /e /i /h /y >nul
if errorlevel 1 (
    color 0C
    echo   [ERROR] Failed to copy files!
    pause
    exit /b 1
)
echo   [OK] Files copied successfully.

echo.
python generate_attachables.py

if errorlevel 1 (
    color 0C
    echo.
    echo   [ERROR] Failed to process files!
    echo.
    pause
    exit /b 1
)

color 0A
echo.
echo ================================================================
echo                                                                 
echo             Conversion Completed Successfully!                   
echo                                                                 
echo ================================================================
echo.
echo   Output files are located in the 'output' folder.
echo.
echo   Generated structure:
echo     output/
echo     +-- attachables/          (Item attachable files)
echo     +-- animations/           (Animation files)
echo     +-- models/entity/        (Geometry files)
echo     +-- render_controllers/   (Render controller files)
echo     +-- textures/             (Original textures)
echo.
pause
