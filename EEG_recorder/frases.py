import tkinter as  tk
from pylsl import StreamInfo, StreamOutlet
import csv, random
import numpy as np
import time
import configparser

fecha = time.strftime("%Y_%m_%d-%H_%M_%S")

#fichero de configuracion
CONFIG_FILE = 'config.conf'


class singleWordsGui:
    numTrials=100 
    durationWords=4
    durationCross=1
    #Para que en caso de que se hagan varias grabaciones que en el txt aparezca reflejado el número de bloque.
    record_number = 0

    #Esta variable nos indicará si se ha guardado (volcado en el txt) ya el bloque
    '''Inicialmente todo esta guardado osea que True'''
    record_saved = True
    # Creamos una lista vacia donde iremos almacenando las palabras que se han leido
    lista_read = []
    #En caso de que queramos mostrar una prueba inicial
    test_inicial = 1
    #Cuando haya habido una parada a mitad lo indicaremos. Para que el trial se quede esperando
    suddenlyStop = False
    normalStop = False
    trialIniciado = False


    def __init__(self, master, words ,separator, time_multiplicator, imaginada, frases):
        self.root = master
        self.words_list = words #Este se mantendrá para no tener que leer el archivo cada vez que se hace el run
        self.words = words
        self.time_multiplicator = time_multiplicator
        self.separator = separator
        self.imaginada = imaginada
        self.frases = frases


        #Layout
        #self.width = self.root.winfo_screenwidth() * 2 / 3
        #self.height =self.root.winfo_screenheight() * 2 / 3
        #self.root.geometry('%dx%d+0+0' % (self.width, self.height))
        self.root.attributes('-fullscreen', True)
        self.root.title("Sentences")
        #Initialize LSL
        info = StreamInfo('SentencesMarkerStream', 'Markers', 1, 0, 'string', 'emuidw22')
        # next make an outlet
        self.outlet = StreamOutlet(info)

        self.label = tk.Label(font=('Helvetica bold', 22)) #, background='gray'
        self.lblVar = tk.StringVar()
        self.label.configure(textvariable=self.lblVar)
        
        self.lblVar.set("Press <Space> to Start")
        self.label.pack(expand=1)        
  
        if self.test_inicial:
            self.root.bind('<space>', self.run_test)
        else:
            self.root.bind('<space>', self.run)
        self.root.bind('<Escape>',self.rest)
        self.root.bind('<q>', self.end)


    def run_test(self, event):

        self.root.unbind('<space>')
        self.words = self.words[:2]
        self.root.after(0, self.trial_test)

    def trial_test(self):
        self.label.pack(expand=1)
        self.root.update_idletasks()
        if len(self.words) == 0 or self.numTrials == 0:
            self.root.after(0, self.rest)
        else:
            self.numTrials = self.numTrials - 1
            word = self.words.pop()
            self.lblVar.set(word)
            self.root.update_idletasks()
            self.root.after(self.durationWords * 1000 * self.time_multiplicator)
            self.lblVar.set(self.separator)
            self.root.update_idletasks()
            self.root.after(self.durationCross * 1000 * self.time_multiplicator, self.trial_test)


    def run(self, event):
        self.root.unbind('<space>')
        if not self.suddenlyStop: #Sino viene de parada inesperada genera lista nueva.
            self.outlet.push_sample(['experimentStarted'])
            print("START")
            # Cada vez que se ejecuta leemos la lista de palabras que no se modificará
            # Esto lo hacemos porque nuestra lista words a lo largo de programa se va vaciando y volcando en el txt
            # De esta forma tenemos la lista guardada sin tener que leer el fichero de entrada otra vez
            self.words = self.words_list

            #Cada vez que se muestra un bloque hay que mezclar los datos
            self.words = self.mezclar_lista(self.words)

            self.normalStop = False

            self.record_number = self.record_number + 1
            self.record_saved = False
            # A su vez cada vez que iniciemos se vaciará la lista que almacena las palabras que se van leyendo.
            self.lista_read = [];
            if self.imaginada == 1:
                # En caso de que sea imaginada la separación entre palabra y palabra será un espacio en blanco
                self.separator = ' '
                # Además tambien añadiremos el doble de tiempo al experimento
                self.time_multiplicator = 2
                # La rellenamos con las palabras repetidas
                self.words = np.repeat(self.words, 2).tolist()
            if not self.trialIniciado:
                self.root.after(0, self.trial)
                self.trialIniciado = True

        # En caso de que venga de parada inesperada, no llamamos a una lista nueva, sino que "desbloqueamos" el trial diciendo que ya no esta descansando.
        # Indicamos con el push_sample, que se esta reanudando.
        else:
            self.outlet.push_sample(['experimentRestarted'])
            print("RESTARTED")
            self.suddenlyStop = False




        

    def trial(self):
        if not self.suddenlyStop and not self.normalStop: #Sino esta en ningun tipo de parada que siga mostrando palabras
            print("TRIAL")
            self.label.pack(expand=1)
            self.root.update_idletasks()
            if len(self.words)==0 or self.numTrials==0:
                self.root.after(0,self.rest)
            else:
                self.numTrials= self.numTrials-1
                #(ANTIGUO SUFFLE)Esta linea se encargaba de sacar un indice al azar pero ahora de hacer la mezcla nos encargamos en el main
                #idx = random.randint(1,len(self.words))-1
                #word=self.words.pop(idx)
                word = self.words.pop()
                self.outlet.push_sample(['start;' +  word])
                self.lblVar.set(word)
                self.root.update_idletasks()
                self. root.after(self.durationWords*1000*self.time_multiplicator)
                self.outlet.push_sample(['end;' +  word])
                self.lblVar.set(self.separator)

                self.root.update_idletasks()
                #Una vez que se ha mostrado la palabra la añadimos a la lista de leidas
                self.lista_read.append(word);
                #Long duration only needed in fNIRS

        self.root.after(self.durationCross*1000*self.time_multiplicator, self.trial)

    
    def rest(self, event=None):
        self.outlet.push_sample(['experimentResting'])
        self.lblVar.set("Resting of Experiment")
        self.root.update_idletasks()
        # Cuando descansa el programa si ha terminado una bloque, las guardamos.
        # En caso contrario esperaremos a que termine el bloque
        if len(self.words)==0:
            self.saveData()
            self.normalStop = True
            print("NORMAL STOP")
        else: #Si quedan palabras y hemos llegado al rest quiere decir que esta en una parada intermedia
            self.suddenlyStop = True
            self.words.append(self.lista_read[-1]);
            print("SUDDENLY STOP")
        self.root.bind('<q>', self.end)
        self.root.bind('<space>', self.run)



    def end(self, event=None):
        self.root.unbind('<q>')
        self.outlet.push_sample(['experimentEnded'])
        self.lblVar.set("End of Experiment")

        #Cuando termina el programa guardamos los "metadatos"
        self.saveData()

        self.root.update_idletasks()
        self.root.destroy()

    def saveData(self):
        if not self.record_saved:
            f = open('egg_recorder_' + fecha + '.txt', 'a')
            f.write('***********************************\n')
            f.write('*** GRABACION BLOQUE:'+str(self.record_number)+' ***********\n')
            f.write('***********************************\n')
            f.write('-----------------------------------\n')
            f.write('--- Frases que se han leido:  ---\n')
            f.write('-----------------------------------\n')
            for x in range(len(self.lista_read)):
                f.write(self.lista_read[x])
            if not len(self.words)==0: #Si NO esta vacio quiere decir que NO se han leido todas
                f.write('------------------------------------\n')
                f.write('--- Frases NO que se han leido:---\n')
                f.write('------------------------------------\n')
                for x in range(len(self.words)):
                    f.write(self.words[x])
            f.close()
            self.record_saved = True

    def mezclar_lista(self,lista_original):
        # Crear una copia, ya que no deberíamos modificar la original
        lista = lista_original[:self.frases]
        # Ciclo for desde 0 hasta la longitud que se haya especificado en config
        longitud_lista = self.frases
        for i in range(longitud_lista):
            # Obtener un índice aleatorio
            indice_aleatorio = random.randint(0, longitud_lista - 1)
            # Intercambiar
            temporal = lista[i]
            lista[i] = lista[indice_aleatorio]
            lista[indice_aleatorio] = temporal
        # Regresarla
        return lista




def getWords(filename):
    with open(filename, newline='') as file:
        words = [line.rstrip('\n') for line in file]
    return words






if __name__=='__main__':

    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)

    # El separador entre palabra y palabra será por defecto la cruz, en caso de que sea imaginada se cambia su valor en el main
    #Estaría bien meterlos en el fichero de configuración
    separator = ' '
    time_multiplicator = 1

    #Leemos el archivo
    #words=getWords('wordsIFADutch.txt')
    sentences = getWords('sentences_prueba.txt')

    #Tomamos la variable del fichero de configuración
    imaginada = int(config['DEFAULT']['imaginada'])
    
    frases = int(config['DEFAULT']['frases'])


    root = tk.Tk()
    my_gui = singleWordsGui(root,sentences,separator, time_multiplicator, imaginada, frases)



    root.mainloop()