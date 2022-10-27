LANZAMIENTO DE EXPERIMENTOS
------------------------------------------------
1. Comprobar que ambos PCs no disponen de adaptador Wi-Fi habilitado y en su caso deshabilitarlo.

2. Permitir una aplicación a través del firewall de Windows 
	2.1 Habilitar todas las aplicaciones LSL para su uso en redes públicas y privadas.
	    Esto incluye al intérprete de Python.

3. (PC Nox) Lanzar actiCHamp.exe (seleccionar fs y #channels)
	1.1 Scan
	1.2 Link

4. (PC Nox) Lanzar sigvisualizer.exe
	2.1 Update Streams

5. (PC Nox) Lanzar labrecorder.exe
	3.1 Update
 
6. (PC studio xps) Lanzar AudioCaptureWin.exe
	4.1 Link

7. (PC studio xps) Lanzar VideoCapture.exe
	5.1 Start recording

8. (PC Nox) Update Streams (Labrecorder.exe)

9. (PC studio xps) Lanzar single_words.py

10. (PC Nox) Update Streams (Labrecorder.exe)
	8.1 Start (inicio de grabación)

------------------------------------------------
REQUISITOS HARDWARE

- Verificar conexión entre PC studio xps y PC Nox (adaptador Ethernet)
- Conectar cámara: Logitech C170 (con conector USB)
- Conectar micrófono (con conector minijack)
- [MIC Feedback] Sonido > Panel de control de sonido > Varios micrófonos > Escuchar > Escuchar este dispositivo

------------------------------------------------
COMPATIBILIDAD CON BRAINVISION

- BrainVision no detecta el dispositivo amplificador actiCHamp si está siendo usado por otra aplicación.

- La configuración del casco EEG debe realizarse previo a su uso desde la herramienta BrainVision Recorder.

- La lectura (visualización en tiempo real) de las mediciones EEG deberá realizarse desde aplicaciones específicas (SigVisualizer.py) circunscritas al entorno de LSL.

	$ BrainVision Recorder
	$ File > New Workspace > Scan for Amplifier

	$ ./Apps/BrainProducts/ActiChamp/build64/Release/ActiCHamp.exe
	$ Scan
