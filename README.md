# labLSL
Directivas de operación y configuración del entorno de trabajo provisto por labstreaminglayer (LSL) en el marco del proyecto de investigación "Restauración de la Voz con Interfaces Cerebro Ordenador" del Plan Nacional 2019.

## Configuración de trabajo

### Requisitos hardware

- Dispositivo de grabación compatible con OpenCV

- Micrófono (adaptador minijack estéreo 3.5mm)

- Conexión Ethernet entre los equipos involucrados o PCs asociados a una determinada fuente de captura.

- Amplificador actiCHamp (www.brainproducts.com/solutions/actichamp/)

### Configuración del entorno de trabajo
La instalación del entorno de trabajo LSL será efectuada desde PowerShell. Para ello deberemos seguir los siguientes pasos:

#### PowerShell

1. Configuramos el inicio de sesión de PowerShell:
      ```
      Add-Content -Path $PROFILE -Value "$ProgressPreference = 'SilentlyContinue'"
      Add-Content -Path $PROFILE -Value "remove-item alias:curl"
      ```

2. Habilitamos la ejecución de scripts de terceros en PowerShell (requiere modo administrador):
      ```
      Set-ExecutionPolicy Unrestricted
      ```

3. Procedemos a instalar el gestor de paquetes *chocolatey*:

      ```
      Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
            
4. Abrimos una nueva sesión de PowerShell para actualizar los cambios efectuados y procedemos con la instalación del entorno de trabajo *labstreaminglayer*:
      ```
      ./installer.ps1
      ```

      Entre las herramientas software a instalar, además del propio entorno LSL incluimos: curl, Git, WireShark, ffmpeg, Anaconda, Psychopy, VLC (reproductor multimedia), Microsoft Redistributables y BrainVision LSL Viewer. 

      Remítase al instalador para ajustar los parámetros de la instalación y en su caso omitir las herramientas software que considere no necesarias. 

5. Junto a las dependencias software instaladas en el paso anterior, se nos deberá haber creado el directorio 'labLSL_v1' directamente en nuesto escritorio. En este directorio encontraremos el cuerpo principal del proyecto, estructurado de la siguiente manera:

      - :file_folder: **EEG_Recorder**: Contiene los experimentos desarrollados en Python y Psychopy. 

      - :file_folder: **labstreaminglayer**: Incluye el entorno de trabajo LSL. Remítase a los ficheros CMAKELIST.TXT para su construcción; no obstante muchas de las aplicaciones se encuentran ya compiladas y disponibles para su uso en Windows 10 (x86-64):

      - *[Reader]* **LabRecorder** (archivo principal ```LabRecorder.exe```): Habilita la captura y sincronización de datos provenientes de diferentes fuentes (e.g ActiCHamp, AudioCapture, VideoCapture, etc).

      - *[Writer]* **AudioCaptureWin** (archivo principal ```AudioCaptureWin.exe```): Captura de audio.

      - *[Writer]* **VideoCapture** (archivo principal ```VideoAcq.py```): Grabaciones de vídeo. El dispositivo de grabación seleccionado debe ser compatible con OpenCV.

      - *[Writer]* **ActiCHamp** (archivo principal ```actiCHamp.exe```): Configura la comunicación vía USB con el amplificador actiCHamp y habilita la captura de señales EEG.

      - :file_folder: **Timing Test**: Especifica los requisitos de plataforma. Se incluye cualquier software de terceros (e.g VSCode, Anaconda, etc). 

      - :file_folder: **VideoData**: Contiene las grabaciones de vídeo realizadas desde la aplicación "VideoCapture" implementada como parte del entorno LSL.
