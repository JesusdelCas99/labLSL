#!/usr/bin/env python3

import tkinter as tk
from pylsl import StreamInfo, StreamOutlet
import random
from datetime import datetime
import configparser
from enum import Enum, auto
import serial

# fichero de configuracion
CONFIG_FILE = 'single_words.conf'

# # Parámetros para generar los beeps
# BEEP_DUR = 0.05  # in secons
# BEEP_FREQ = 2000  # Hz
# BEEP_FS = 44100  # Hz


class Markers(Enum):
    EXPERIMENT_START = auto()
    EXPERIMENT_END = auto()
    EXPERIMENT_RESTART = auto()
    EXPERIMENT_REST = auto()
    START_READ_WORD = auto()
    END_READ_WORD = auto()
    START_SAY_WORD = auto()
    END_SAY_WORD = auto()
    START_BLOCK_SAYING = auto()
    START_BLOCK_THINKING = auto()


class singleWordsGui:

    def __init__(self, master, words, font_type, font_size, tiempo_leer, tiempo_pensar, min_duration, max_duration, block_size, trigger_port):
        # Inicializamos los atributos del objeto
        self.root = master
        self.words_list = words  # Este se mantendrá para no tener que leer el archivo cada vez que se hace el run
        self.font_size = font_size
        self.font_type = font_type
        self.tiempo_leer = tiempo_leer
        self.tiempo_pensar = tiempo_pensar
        self.min_duration = min_duration
        self.max_duration = max_duration
        self.block_size = block_size
        self.experiment_start = datetime.now()

        self.num_trials = 1

        # Para que en caso de que se hagan varias grabaciones que en el txt aparezca reflejado el número de bloque.
        self.record_number = 0

        # Esta variable nos indicará si se ha guardado (volcado en el txt) ya el bloque
        # Inicialmente todo esta guardado osea que True
        self.record_saved = True
        # Creamos una lista vacia donde iremos almacenando las palabras que se han leido
        self.lista_read = []
        # Cuando haya habido una parada a mitad lo indicaremos. Para que el trial se quede esperando
        self.suddenlyStop = False
        self.normalStop = False

        self.trialIniciado = False  # Variable para que trial solo se inicie una vez
        self.bloque_leido = False  # Variable de control de que se ha terminado un bloque
        self.fin_programa = False  # Variable de control de que se ha llamado a la función en (Basicamente es para el volcado de palabras que no se hayan leido)
        self.bloque_hablado = True

        # Layout de la UI
        # self.width = self.root.winfo_screenwidth() * 2 / 3
        # self.height =self.root.winfo_screenheight() * 2 / 3
        # self.root.geometry('%dx%d+0+0' % (self.width, self.height))
        self.root.attributes('-fullscreen', True)
        self.root.config(cursor="none")
        self.root.title("Single Words")

        # Initialize LSL
        info = StreamInfo('SingleWordsMarkerStream', 'Markers', 1, 0, 'string', 'emuidw22')
        # next make an outlet
        self.outlet = StreamOutlet(info)

        # Abrimos el puerto USB para mandar triggers al amplificador Natus
        if trigger_port:
            self.serial_port = serial.Serial(trigger_port, baudrate=128000, timeout=0.01)  # Port_name es el id del puerto. Aquí te dice cómo obtenerlo: https://pyserial.readthedocs.io/en/latest/pyserial_api.html
        else:
            self.serial_port = None

        self.lblVar = tk.StringVar()
        self.lblVar.set("BLOQUE EN VOZ ALTA \n Presione <Espacio> para comenzar")

        self.label = tk.Label(self.root, textvariable=self.lblVar, anchor=tk.CENTER, justify=tk.CENTER,
                              font=(self.font_type, self.font_size))  # , background='gray'
        self.label.pack(expand=1)

        # Calculamos la longitud de la palabra más larga para imprimirlas formateadas
        self.max_word_len = max([len(x) for x in words])

        # Hacemos los bindings de las teclas a los distintos métodos
        self.root.bind('<space>', self.run)
        self.root.bind('<Escape>', self.rest)
        self.root.bind('<q>', self.end)

    def run(self, event):
        self.root.unbind('<space>')
        if not self.suddenlyStop:
            self.send_markers(Markers.EXPERIMENT_START)
            self.normalStop = False
            self.record_saved = False
            if self.bloque_hablado:
                self.send_markers(Markers.START_BLOCK_SAYING)
            else:
                self.send_markers(Markers.START_BLOCK_THINKING)

            self.bloque_hablado = not self.bloque_hablado

            # A su vez cada vez que iniciemos se vaciará la lista que almacena las palabras que se van leyendo.
            self.lista_read = []
            if not self.trialIniciado:
                self.root.after(0, self.trial)
                self.trialIniciado = True

        # En caso de que venga de parada inesperada, no llamamos a una lista nueva, sino que "desbloqueamos" el trial diciendo que ya no esta descansando.
        # Indicamos con el push_sample, que se esta reanudando.
        else:
            self.send_markers(Markers.EXPERIMENT_RESTART)
            self.suddenlyStop = False

    def trial(self):
        if not self.suddenlyStop and not self.normalStop:  # Si no esta en ningun tipo de parada que siga mostrando palabras
            self.label.pack(expand=1)
            self.root.update_idletasks()
            if len(self.words_list) == 0:
                self.root.after(0, self.end)
            elif self.num_trials % (block_size + 1) == 0:
                self.bloque_leido = True
                self.root.after(0, self.rest)
            else:
                fix_duration = random.randint(self.min_duration, self.max_duration)
                pause_duration = random.randint(self.min_duration, self.max_duration)
                # Espera inicial
                self.lblVar.set('[' + (' ' * (self.max_word_len + 4)) + ']')
                self.root.update_idletasks()
                self.root.after(fix_duration)
                word = self.words_list.pop()
                word = word.upper()
                # Leer la palabra
                self.send_markers(Markers.START_READ_WORD, word)
                word_len = len(word)
                leading_spaces = (self.max_word_len + 4 - word_len) // 2
                trailing_spaces = (self.max_word_len + 4 - word_len) - leading_spaces
                self.lblVar.set('[' + (' ' * leading_spaces) + word + (' ' * trailing_spaces) + ']')
                self.root.update_idletasks()
                self.root.after(self.tiempo_leer)
                self.send_markers(Markers.END_READ_WORD, word)
                # Espera intermedia
                self.lblVar.set('[' + (' ' * (self.max_word_len + 4)) + ']')
                self.root.update_idletasks()
                self.root.after(pause_duration)
                # Parte pensada o dicha
                self.send_markers(Markers.START_SAY_WORD, word)
                self.lblVar.set('[' + (' ' * leading_spaces) + ('*' * word_len) + (' ' * trailing_spaces) + ']')
                self.root.update_idletasks()
                self.root.after(self.tiempo_pensar)
                self.send_markers(Markers.END_SAY_WORD, word)
                # Una vez que se ha mostrado la palabra la añadimos a la lista de leidas
                self.lista_read.append(word)
            self.num_trials = self.num_trials + 1
        self.root.after(10, self.trial)

    def rest(self, event=None):
        self.send_markers(Markers.EXPERIMENT_REST)
        mensaje_parada = "PAUSA DEL EXPERIMENTO"
        # Cuando descansa el programa si ha terminado una bloque, las guardamos.
        # En caso contrario esperaremos a que termine el bloque
        if self.bloque_leido:
            self.record_number += 1
            self.saveData()
            self.normalStop = True
            print("NORMAL STOP")
            self.bloque_leido = False
            if self.bloque_hablado:
                mensaje_parada = "BLOQUE EN VOZ ALTA"
            else:
                mensaje_parada = "BLOQUE EN SILENCIO"
        else:  # Si quedan palabras y hemos llegado al rest quiere decir que esta en una parada intermedia
            self.suddenlyStop = True
            self.words_list.append(self.lista_read[-1])
            self.num_trials = self.num_trials - 1
            print("SUDDENLY STOP")

        self.lblVar.set(mensaje_parada)
        self.root.update_idletasks()
        self.root.bind('<q>', self.end)
        self.root.bind('<space>', self.run)

    def end(self, event=None):
        self.root.unbind('<q>')
        self.send_markers(Markers.EXPERIMENT_END)
        self.lblVar.set("FIN DEL EXPERIMENTO")

        self.fin_programa = True
        # Cuando termina el programa guardamos los "metadatos"
        self.saveData()

        self.root.update_idletasks()
        self.root.destroy()

        # Cerramos el puerto serie usado para mandars triggers
        if self.serial_port:
            self.serial_port.close()

    def send_markers(self, marker, word=None):
        if marker is Markers.START_READ_WORD:
            if self.serial_port:
                self.serial_port.write(b"WRITE 255 50000 0\n")
            self.outlet.push_sample(['StartReading:' + word])
        elif marker is Markers.END_READ_WORD:
            if self.serial_port:
                self.serial_port.write(b"WRITE 224 50000 0\n")
            self.outlet.push_sample(['EndReading:' + word])
        elif marker is Markers.START_SAY_WORD:
            if self.serial_port:
                self.serial_port.write(b"WRITE 192 50000 0\n")
            self.outlet.push_sample(['StartSaying:' + word])
        elif marker is Markers.END_SAY_WORD:
            if self.serial_port:
                self.serial_port.write(b"WRITE 160 50000 0\n")
            self.outlet.push_sample(['EndSaying:' + word])
        elif marker is Markers.START_BLOCK_SAYING:
            if self.serial_port:
                self.serial_port.write(b"WRITE 128 50000 0\n")
            self.outlet.push_sample(['StartBlockSaying'])
        elif marker is Markers.START_BLOCK_THINKING:
            if self.serial_port:
                self.serial_port.write(b"WRITE 96 50000 0\n")
            self.outlet.push_sample(['StartBlockThinking'])
        elif marker is Markers.EXPERIMENT_RESTART:
            if self.serial_port:
                self.serial_port.write(b"WRITE 64 50000 0\n")
            self.outlet.push_sample(['ExperimentRestarted'])
        elif marker is Markers.EXPERIMENT_REST:
            if self.serial_port:
                self.serial_port.write(b"WRITE 32 50000 0\n")
            self.outlet.push_sample(['ExperimentResting'])
        elif marker is Markers.EXPERIMENT_START:
            if self.serial_port:
                self.serial_port.write(b"WRITE 16 50000 0\n")
            self.outlet.push_sample(['ExperimentStarted'])
        elif marker is Markers.EXPERIMENT_END:
            if self.serial_port:
                self.serial_port.write(b"WRITE 8 50000 0\n")
            self.outlet.push_sample(['ExperimentEnded'])
        else:
            raise Exception("Undefined marker: {}".format(marker))

    def saveData(self):
        fecha = self.experiment_start.strftime("%d-%m-%Y_%H:%M:%S")
        with open("single_words_{}.log".format(fecha), 'a') as f:
            if not self.record_saved:
                if not self.bloque_hablado:
                    mensaje = "-HABLADA-"
                else:
                    mensaje = "-IMAGINADA-"
                if self.fin_programa:
                    self.record_number = self.record_number + 1
                f.write('***********************************\n')
                f.write('*** GRABACION BLOQUE:' + str(self.record_number) + mensaje + ' **\n')
                f.write('***********************************\n')
                f.write('-----------------------------------\n')
                f.write('--- Palabras que se han leido:  ---\n')
                f.write('-----------------------------------\n')
                for x in range(len(self.lista_read)):
                    f.write(self.lista_read[x] + '\n')
                self.record_saved = True
            if self.fin_programa and len(self.words_list) != 0:  # Si NO esta vacio quiere decir que NO se han leido todas
                f.write('------------------------------------\n')
                f.write('--- Palabras NO que se han leido:---\n')
                f.write('------------------------------------\n')
                for x in range(len(self.words_list)):
                    f.write(self.words_list[x] + '\n')


def getWords(filename):
    with open(filename, newline='') as file:
        words = [line.rstrip('\r\n') for line in file]
    return words


def mezclar_lista(lista_original):
    l_copia = lista_original.copy()
    random.shuffle(l_copia)
    return l_copia


def generate_stimuli(words, n_reps=1, block_size=10):
    spoken_words = []
    silent_words = []
    for i in range(n_reps):
        spoken_words += mezclar_lista(words)
        silent_words += mezclar_lista(words)

    word_list = []
    for i in range(0, len(spoken_words), block_size):
        word_list += (spoken_words[i:i + block_size] + silent_words[i:i + block_size])

    return word_list


if __name__ == '__main__':
    random.seed()
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)

    print(config)

    print(config['DEFAULT']['words_in_block'])

    # Leemos el archivo de palabras
    num_repetitions = int(config['DEFAULT']['word_repetitions'])
    block_size = int(config['DEFAULT']['words_in_block'])
    words = getWords(config['DEFAULT']['words'])
    words = generate_stimuli(words, num_repetitions, block_size)

    root = tk.Tk()
    if 'port' in config['TRIGGER']:
        trigger_port = config['TRIGGER']['port']
    else:
        trigger_port = None

    my_gui = singleWordsGui(master=root,
                            words=words,
                            font_type=config['GUI']['font_type'],
                            font_size=int(config['GUI']['font_size']),
                            tiempo_leer=int(config['DEFAULT']['tiempo_leer']),
                            tiempo_pensar=int(config['DEFAULT']['tiempo_pensar']),
                            min_duration=int(config['DEFAULT']['min_duration']),
                            max_duration=int(config['DEFAULT']['max_duration']),
                            block_size=block_size,
                            trigger_port=trigger_port)

    root.mainloop()
