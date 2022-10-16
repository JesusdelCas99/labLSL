#!/usr/bin/env python3

import tkinter as tk
from pylsl import StreamInfo, StreamOutlet
import random
from datetime import datetime
import configparser
from enum import Enum, auto
import serial
from PIL import ImageTk, Image
import pandas as pd


# fichero de configuracion
CONFIG_FILE = 'picture_naming.conf'


class Markers(Enum):
    EXPERIMENT_START = auto()
    EXPERIMENT_END = auto()
    EXPERIMENT_RESTART = auto()
    EXPERIMENT_REST = auto()
    START_SHOW_IMG = auto()
    END_SHOW_IMG = auto()
    START_NAME_IMG = auto()
    END_NAME_IMG = auto()
    START_BLOCK_SAYING = auto()
    START_BLOCK_THINKING = auto()


class singleImagesGui:

    def __init__(self, master, list_images, dict_images, font_type, font_size, tiempo_leer, tiempo_pensar, min_duration, max_duration, block_size, trigger_port, test):
        # Inicializamos los atributos del objeto
        self.root = master
        self.list_images = list_images
        self.data_images = dict_images
        self.font_size = font_size
        self.font_type = font_type
        self.tiempo_leer = tiempo_leer
        self.tiempo_pensar = tiempo_pensar
        self.min_duration = min_duration
        self.max_duration = max_duration
        self.block_size = block_size
        self.experiment_start = datetime.now()
        self.test = test

        self.num_trials = 1

        # Para que en caso de que se hagan varias grabaciones que en el txt aparezca reflejado el número de bloque.
        self.record_number = 0

        # Esta variable nos indicará si se ha guardado (volcado en el txt) ya el bloque
        # Inicialmente todo esta guardado osea que True
        self.record_saved = True
        # Creamos una lista vacia donde iremos almacenando las imagenes que se han leido
        self.lista_read = []
        # Cuando haya habido una parada a mitad lo indicaremos. Para que el trial se quede esperando
        self.suddenlyStop = False
        self.normalStop = False

        self.trialIniciado = False  # Variable para que trial solo se inicie una vez
        self.bloque_leido = False  # Variable de control de que se ha terminado un bloque
        self.fin_programa = False  # Variable de control de que se ha llamado a la función en (Basicamente es para el volcado de palabras que no se hayan leido)
        self.bloque_hablado = True

        # Layout de la UI
        self.root.attributes('-fullscreen', True)
        self.root.config(cursor="none")
        self.root.title("Picture Naming")

        # Initialize LSL
        info = StreamInfo('PictureNamingMarkerStream', 'Markers', 1, 0, 'string', 'emuidw22')
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
                              font=(str(self.font_type), self.font_size), compound='top')  # , background='gray'
        self.label.pack(expand=1)

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
            if len(self.list_images) == 0:
                self.root.after(0, self.end)
            elif self.num_trials % (block_size + 1) == 0:
                self.bloque_leido = True
                self.root.after(0, self.rest)
            else:
                fix_duration = random.randint(self.min_duration, self.max_duration)
                # img_name = self.images['name'][self.i]
                img_name = self.list_images.pop()
                # self.tk_image=ImageTk.PhotoImage(Image.open(self.images['url'][self.i]))
                # image = Image.open(self.data_images[img_name])
                # image = image.resize((450, 450), Image.ANTIALIAS)
                # self.tk_image = ImageTk.PhotoImage(image)
                # Espera inicial
                self.lblVar.set('+')
                self.root.update_idletasks()
                self.root.after(fix_duration)
                # Ver imagen
                self.send_markers(Markers.START_SHOW_IMG, img_name)
                # self.label.configure(image=self.tk_image)
                self.label.configure(image=self.data_images[img_name])
                if self.test:
                    self.lblVar.set(img_name)
                else:
                    self.lblVar.set('')
                self.root.update_idletasks()
                self.root.after(self.tiempo_leer)
                self.send_markers(Markers.END_SHOW_IMG, img_name)
                # Nombra la imagen (en voz alta o silencio)
                self.send_markers(Markers.START_NAME_IMG, img_name)
                self.lblVar.set('***')
                self.label.configure(image='')
                self.root.update_idletasks()
                self.root.after(self.tiempo_pensar)
                self.send_markers(Markers.END_NAME_IMG, img_name)
                # Una vez que se ha mostrado la palabra la añadimos a la lista de leidas
                # self.lista_read.append(self.images['name'][self.i])
                self.lista_read.append(img_name)

            self.num_trials = self.num_trials + 1
            # self.i = self.i + 1
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
            self.list_images.append(self.lista_read[-1])
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

    def send_markers(self, marker, img=None):
        if marker is Markers.START_SHOW_IMG:
            if self.serial_port:
                self.serial_port.write(b"WRITE 255 50000 0\n")
            self.outlet.push_sample(['StartReading:' + img])
            # print('StartReading:' + img)
        elif marker is Markers.END_SHOW_IMG:
            if self.serial_port:
                self.serial_port.write(b"WRITE 224 50000 0\n")
            self.outlet.push_sample(['EndReading:' + img])
            # print('EndReading:' + img)
        elif marker is Markers.START_NAME_IMG:
            if self.serial_port:
                self.serial_port.write(b"WRITE 192 50000 0\n")
            self.outlet.push_sample(['StartSaying:' + img])
            # print('StartSaying:' + img)
        elif marker is Markers.END_NAME_IMG:
            if self.serial_port:
                self.serial_port.write(b"WRITE 160 50000 0\n")
            self.outlet.push_sample(['EndSaying:' + img])
            # print('EndSaying:' + img)
        elif marker is Markers.START_BLOCK_SAYING:
            if self.serial_port:
                self.serial_port.write(b"WRITE 128 50000 0\n")
            self.outlet.push_sample(['StartBlockSaying'])
            # print('StartBlockSaying')
        elif marker is Markers.START_BLOCK_THINKING:
            if self.serial_port:
                self.serial_port.write(b"WRITE 96 50000 0\n")
            self.outlet.push_sample(['StartBlockThinking'])
            # print('StartBlockThinking')
        elif marker is Markers.EXPERIMENT_RESTART:
            if self.serial_port:
                self.serial_port.write(b"WRITE 64 50000 0\n")
            self.outlet.push_sample(['ExperimentRestarted'])
            # print('ExperimentRestarted')
        elif marker is Markers.EXPERIMENT_REST:
            if self.serial_port:
                self.serial_port.write(b"WRITE 32 50000 0\n")
            self.outlet.push_sample(['ExperimentResting'])
            # print('ExperimentResting')
        elif marker is Markers.EXPERIMENT_START:
            if self.serial_port:
                self.serial_port.write(b"WRITE 16 50000 0\n")
            self.outlet.push_sample(['ExperimentStarted'])
            # print('ExperimentStarted')
        elif marker is Markers.EXPERIMENT_END:
            if self.serial_port:
                self.serial_port.write(b"WRITE 8 50000 0\n")
            self.outlet.push_sample(['ExperimentEnded'])
            # print('ExperimentEnded')
        else:
            raise Exception("Undefined marker: {}".format(marker))

    def saveData(self):
        fecha = self.experiment_start.strftime("%d-%m-%Y_%H-%M-%S")
        with open("picture_naming_{}.log".format(fecha), 'a') as f:
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
                f.write('--- Imagenes que se han leido:  ---\n')
                f.write('-----------------------------------\n')
                for x in range(len(self.lista_read)):
                    f.write(self.lista_read[x] + '\n')
                self.record_saved = True
            if self.fin_programa and len(self.list_images) != 0:  # Si NO esta vacio quiere decir que NO se han leido todas
                f.write('------------------------------------\n')
                f.write('--- Imagenes NO que se han leido:---\n')
                f.write('------------------------------------\n')
                for x in range(len(self.list_images)):
                    f.write(self.list_images[x] + '\n')


def mezclar_lista(lista_original):
    l_copia = lista_original.copy()
    random.shuffle(l_copia)
    return l_copia


def generate_stimuli(imgs, n_reps=1, block_size=10):
    spoken_imgs = []
    silent_imgs = []
    for i in range(n_reps):
        spoken_imgs += mezclar_lista(imgs)
        silent_imgs += mezclar_lista(imgs)

    img_list = []
    for i in range(0, len(spoken_imgs), block_size):
        img_list += (spoken_imgs[i:i + block_size] + silent_imgs[i:i + block_size])
    return img_list


def generate_stimuli_test(imgs, n_reps=1, block_size=10):
    img_list = []
    for i in range(n_reps):
        img_list += mezclar_lista(imgs)
    return img_list


def load_img(img_paths):
    tk_imgs = []
    for path in img_paths:
        image = Image.open(path).resize((450, 450), Image.ANTIALIAS)
        tk_imgs.append(ImageTk.PhotoImage(image))
    return tk_imgs


if __name__ == '__main__':
    random.seed()
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)

    # Leemos el archivo de palabras
    num_repetitions = int(config['DEFAULT']['img_repetitions'])
    block_size = int(config['DEFAULT']['img_in_block'])

    root = tk.Tk()
    if 'port' in config['TRIGGER']:
        trigger_port = config['TRIGGER']['port']
    else:
        trigger_port = None

    data_images = pd.read_csv(config['DEFAULT']['images'])
    img_names = [name.upper() for name in data_images['Nombre'].tolist()]
    img_paths = data_images['Archivo'].tolist()
    # dict_images = dict(zip(img_names, img_paths))
    # Precargamos las imágenes por eficiencia
    dict_images = dict(zip(img_names, load_img(img_paths)))
    initial_test = config.getboolean('DEFAULT', 'test')
    if initial_test:
        list_images = generate_stimuli_test(img_names, num_repetitions, block_size)
    else:
        list_images = generate_stimuli(img_names, num_repetitions, block_size)
    my_gui = singleImagesGui(master=root,
                             list_images=list_images,
                             dict_images=dict_images,
                             font_type=config['GUI']['font_type'],
                             font_size=int(config['GUI']['font_size']),
                             tiempo_leer=int(config['DEFAULT']['tiempo_leer']),
                             tiempo_pensar=int(config['DEFAULT']['tiempo_pensar']),
                             min_duration=int(config['DEFAULT']['min_duration']),
                             max_duration=int(config['DEFAULT']['max_duration']),
                             block_size=block_size,
                             trigger_port=trigger_port,
                             test=initial_test)

    root.mainloop()
