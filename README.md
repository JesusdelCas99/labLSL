# labLSL
Directivas de operación y configuración del entorno de trabajo provisto por labstreaminglayer (LSL) en el marco del proyecto de investigación "Restauración de la Voz con Interfaces Cerebro Ordenador" del Plan Nacional 2019.

## Contenido
- :file_folder: **EEG_Recorder**: Contiene los experimentos desarrollados en Python específicos del proyecto. 

- :file_folder: **labstreaminglayer**: Incluye el entorno de trabajo LSL. Remítase a los ficheros CMAKELIST.TXT para su construcción; no obstante muchas de las aplicaciones se encuentran ya compiladas y disponibles para su uso en Windows 10 (x86-64). 
  
  En el marco de este proyecto de investigación solo se hará uso de las siguientes aplicaciones LSL, aunque como podrá ver, el usuario dispone de un mayor número de aplicaciones a fin de proveer un entorno de trabajo íntegro: 

  - *[Reader]* **LabRecorder**: Habilita la captura y sincronización de datos provenientes de diferentes fuentes (e.g ActiCHamp, AudioCapture, VideoCapture, etc).
  
  - *[Writer]* **AudioCapture**: Captura de audio.
  
  - *[Writer]* **BrainVision LSL Viewer**: Visualización de registros EEG en tiempo real.
  
  - *[Writer]* **VideoCapture**: Grabaciones de vídeo. El dispositivo de grabación seleccionado debe ser compatible con OpenCV.
  
  - *[Writer]* **ActiCHamp**: Configura la comunicación vía USB con el amplificador actiCHamp y habilita la captura de señales EEG.
  
- :file_folder: **Timing Test**: Especifica los requisitos de plataforma. Se incluye cualquier software de terceros (e.g VSCode, Anaconda, etc). 

- :file_folder: **VideoData**: Contiene las grabaciones de vídeo realizadas desde la aplicación "SigVisualizer" implementada como parte del entorno LSL.

## Configuración de trabajo

### Requisitos hardware

- Dispositivo de grabación compatible con OpenCV

- Micrófono (adaptador minijack estéreo 3.5mm)

- Conexión Ethernet entre los equipos involucrados o PCs asociados a una determinada fuente de captura.

- Amplificador actiCHamp (www.brainproducts.com/solutions/actichamp/)

### Configuración de trabajo
#### PowerShell

1. Configuración de inicio:
```
Add-Content -Path $PROFILE -Value "$ProgressPreference = 'SilentlyContinue'"
Add-Content -Path $PROFILE -Value "remove-item alias:curl"
```

2. Paso previo a proceder con la instalación de cualquier programa es necesario habilitar desde PowerShell la ejecución de scripts de terceros:
```
Set-ExecutionPolicy Unrestricted
```

3. Instalación del gestor de paquetes Chocolatey
```
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```
