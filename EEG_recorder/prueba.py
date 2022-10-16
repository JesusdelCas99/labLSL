import configparser

# fichero de configuracion
CONFIG_FILE = 'single_words.conf'

config = configparser.ConfigParser()
config.read(CONFIG_FILE)



# Leemos el archivo de palabras
num_repetitions = int(config['DEFAULT']['word_repetitions'])
block_size = int(config['DEFAULT']['words_in_block'])

print(config.sections())
print(block_size)
print(num_repetitions)