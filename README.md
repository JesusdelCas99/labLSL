# labLSL
Directivas de operación y configuración del entorno de trabajo provisto por labstreaminglayer (LSL) en el marco del proyecto de investigación "Restauración de la Voz con Interfaces Cerebro Ordenador" del Plan Nacional 2019. Para mas información remítase al siguiente enlace: https://labstreaminglayer.org/#/

## Contenido
- :file_folder: EEG_Recorder: Contiene los experimentos desarrollados en Python específicos del proyecto. 

- :file_folder: labstreaminglayer: Incluye el entorno de trabajo LSL (remítase a los ficheros CMAKELIST.TXT para su construcción). No obstante muchas de las aplicaciones se encuentran ya compiladas y disponibles para su uso en Windows 10 (x86-64). En el marco de este proyecto de investigación solo se hará uso de las siguientes aplicaciones LSL, aunque como podrá ver el usuario dispone de un mayor número de aplicaciones a fin de proveer un entorno de trabajo íntegro: 

  - [Writer] LabRecorder: Habilita la captura y sincronización de datos provenientes de diferentes fuentes (e.g ActiCHamp, AudioCapture, VideoCapture...).
  - [Writer] AudioCapture: Captura de audio.
  - [Writer] SigVisualizer: Visualización de registros EEG en tiempo real. Permite configurar las etiquetas asignadas a los electrodos a elección propia.
  - [Writer] VideoCapture: Grabaciones de vídeo. El dispositivo de grabación seleccionado debe ser compatible con OpenCV.
  - [Writer] ActiCHamp: Configura la comunicación con el amplificador actiCHamp (www.brainproducts.com/solutions/actichamp/) por USB y habilita la captura de señales EEG.
  
- :file_folder: PlatformSpecs: Especifica los requisitos de plataforma. Adicionalmente se incluye cualquier software de terceros (e.g VSCode, Anaconda, etc). 

- :file_folder: VideoData: Contiene las grabaciones de vídeo realizadas desde la aplicación "SigVisualizer" implementada como parte del entorno LSL.
