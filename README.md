# labLSL
Directivas de operación y configuración del entorno de trabajo provisto por labstreaminglayer (LSL) en el marco del proyecto de investigación "Restauración de la Voz con Interfaces Cerebro Ordenador" del Plan Nacional 2019. Para mas información remítase al siguiente enlace: https://labstreaminglayer.org/#/

## Contenido
- :file_folder: EEG_Recorder: Contiene los experimentos desarrollados en Python específicos del proyecto. 
- 
- :file_folder: labstreaminglayer: Incluye el entorno de trabajo LSL. Algunas de las aplicaciones se encuentran ya compiladas para una arquitectura x86-64. En caso de usar una arquitectura diferente remítase a los ficheros CMAKELIST.TXT para su construcción. En el marco de este proyecto de investigación solo se hará uso de las siguientes aplicaciones LSL, no obstante como podrá ver el usuario dispone de un mayor número de aplicaciones a fin de proveer un entorno de trabajo íntegro: 

  - ![#f03c15](LabRecorder: Habilita la captura y sincronización de datos provenientes de diferentes fuentes (e.g ActiCHamp, AudioCapture, VideoCapture...))
  
  - [Writer] AudioCapture: Captura de audio.
  
  - [Writer] SigVisualizer: Visualización de registros EEG en tiempo real.
  
  - [Writer] VideoCapture: Grabaciones de vídeo
  
  - [Writer] ActiCHamp: Configura la comunicación con el amplificador actiCHamp (www.brainproducts.com/solutions/actichamp/) y habilita la captura de datos
  
- :file_folder: PlatformSpecs: Requisitos de plataforma. 

- :file_folder: VideoData: Contiene las grabaciones de vídeo realizadas desde la aplicación "SigVisualizer" implementada como parte del entorno LSL.
