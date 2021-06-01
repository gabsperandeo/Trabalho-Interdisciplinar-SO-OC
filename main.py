'''
Trabalho Interdisciplinar Sistemas Operacionais e Organização de Computadores
Docentes: Márcio Luiz Piva e Thiago Ferauche
Autores: Felipe Rocha de Oliveira
         Gabriel Tellaroli Ramos
         Gabrielle Sperandeo Moraes Ferreira
         Verônica Marçal de Lemos Silva
'''

import platform
import multiprocessing
import psutil
import pandas as pd
import time
import datetime
from datetime import date
import concurrent.futures

# funções
# função que faz a conversão de bytes no formato apropriado, dependendo do tamanho
def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


# função que mostra sobre o Sistema Operacional e a Arquitetura do computador
def OS_architeture_information():
    print('\n\n\nArquitetura: ', platform.architecture())
    print('Plataforma: ', platform.platform())
    print('Informações Plataforma: ', platform.machine())
    print('Informações do Sistema: ', platform.system() + ' ' + platform.release())


# função que mostra o nome do processador, qual o processador, os cores e a sua frequência
def processor_information():
    if platform.system() == 'Windows': # biblioteca disponível somente para windows
        import winreg
        access_registry = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        # pegando o nome do processador
        access_key = winreg.OpenKey(access_registry, r"HARDWARE\DESCRIPTION\System\CentralProcessor\0")
        print('Nome do processador: ', winreg.QueryValueEx(access_key, 'ProcessorNameString'))
    else:
        print("\nAlerta! Informações de 'Nome do Processador' para o ambiente Linux ainda não são suportadas nesta versão. Aguarde novas atualizações!\n")

    print('Processador: ', platform.processor())
    print('Cores: ', multiprocessing.cpu_count())
    freq = psutil.cpu_freq()

    print('\nFrequência Processador\n\tAtual: ', freq[0], 'MHz',
          '\n\tMínima: ', freq[1], 'MHz',
          '\n\tMáxima: ', freq[2], 'MHz', "\n")


# função que mostra detalhes da memória, swap (se existir)
def memory_information():
    # informação da memória
    print("=" * 40, "Informação da Memória", "=" * 40, "\n")

    # pegando os detalhes da memória principal
    svmem = psutil.virtual_memory()
    print(f"Total: {get_size(svmem.total)}")
    print(f"Disponível: {get_size(svmem.available)}")
    print(f"Usado: {get_size(svmem.used)}")
    print(f"Porcentagem: {svmem.percent}%", "\n")
    print("=" * 20, "SWAP", "=" * 20, "\n")

    # caso haja, pegando detalhes da memória swap
    swap = psutil.swap_memory()
    print(f"Total: {get_size(swap.total)}")
    print(f"Free: {get_size(swap.free)}")
    print(f"Used: {get_size(swap.used)}")
    print(f"Percentage: {swap.percent}%", "\n")


# função que traz as informações dos discos
def disks_information():
    if platform.system() == 'Windows': # biblioteca disponível somente para windows
        import winreg
        access_registry = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        # mostrando HD ou SSD
        access_key_disk = winreg.OpenKey(access_registry, r"HARDWARE\DEVICEMAP\Scsi\Scsi Port 0\Scsi Bus 0\Target Id 0\Logical Unit Id 0")
        print('HD ou SSD: ', winreg.QueryValueEx(access_key_disk, 'Identifier'))
    else:
        print("\nAlerta! Informações de Nome do HD/SSD para o ambiente Linux ainda não são suportadas nesta versão. Aguarde novas atualizações!\n")

    print("=" * 40, "Informações do Disco", "=" * 40)
    print("Partições e Uso:")
    partitions = psutil.disk_partitions()
    for partition in partitions:
        print(f"=== Dispositivo: {partition.device} ===", "\n")
        print(f"  Mountpoint: {partition.mountpoint}")
        print(f"  Sistema de Arquivo: {partition.fstype}")
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            continue
        print(f"  Tamanho total: {get_size(partition_usage.total)}")
        print(f"  Usado: {get_size(partition_usage.used)}")
        print(f"  Disponível: {get_size(partition_usage.free)}")
        print(f"  Porcentagem: {partition_usage.percent}%", "\n")

    # get IO statistics since boot
    disk_io = psutil.disk_io_counters()
    print(f"Total lido: {get_size(disk_io.read_bytes)}")
    print(f"Total escrito: {get_size(disk_io.write_bytes)}", "\n")


# função que verifica se a string é um float
def string_is_float(word):
    try:
        float(word)
        return True
    except ValueError:
        return False


# função que devolve o total de palavras existentes nesta coluna
def words_count(argumentos):
    if (not string_is_float(argumentos)):
        return len(argumentos.split())
    else:
        return 0

# função que faz com que as threads executem a words_count
def all_words_count(valor):
    with concurrent.futures.ThreadPoolExecutor(max_workers=3096) as executor:
        future = executor.submit(words_count, valor)
        return future.result()




# ===== MAIN =====
OS_architeture_information()
processor_information()
memory_information()
disks_information()

# etapa 1
# abertura do arquivo
arq = 'dataset.csv'
number_lines = sum(1 for row in (open(arq, 'r', encoding="utf8")))  # quantidade de linhas do arquivo
rowsize = int((number_lines)/6)

matriz_dataset = []

# leitura e armazenamento dos dados em uma matriz
print("=========== ETAPA 1 ===========")
print("Inicio Etapa: ", date.today(), time.strftime("%H:%M:%S", time.localtime()))
inicio_etapa1 = time.time()

# particionando o arquivo em 6 para ler e armazenar na matriz
for i in range(0, number_lines, rowsize):
    df = pd.read_csv(arq,
        header = None,
        nrows = rowsize, # número de linhas que serão lidas a cada iteração
        skiprows = i, # pular as linhas que já foram lidas
        dtype = 'unicode')

    matriz_dataset.append(df.values.tolist())

duracao_etapa1 = time.time() - inicio_etapa1
print("Fim Etapa: ", date.today(), time.strftime("%H:%M:%S", time.localtime()))
print("Duração da Etapa: ", str(datetime.timedelta(seconds = round(duracao_etapa1))))

# guardando o nome das colunas
nome_colunas = matriz_dataset[0].pop(0)

'''
# etapa 2
# verificando se os valores das colunas da primeira linha são números ou não e setando no column_is_num
count_array = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

print("=========== ETAPA 1 ===========")
print("Inicio Etapa: ", date.today(), time.strftime("%H:%M:%S", time.localtime()))
inicio_etapa2 = time.time()

for particao in matriz_dataset:     # iterando por particionamento
    for linha in particao:          # iterando por linha do particionamento
      index = 0
      for valor in linha:           # iterando por coluna do particionamento
        count_array[index] += all_words_count(valor)
        index += 1

duracao_etapa2 = time.time() - inicio_etapa2
print("Fim Etapa: ", date.today(), time.strftime("%H:%M:%S", time.localtime()))
print("Duração da Etapa: ", str(datetime.timedelta(seconds = round(duracao_etapa2))))

print(count_array)
'''

# etapa 3
print("=========== ETAPA 3 ===========")
print("Inicio Etapa: ", date.today(), time.strftime("%H:%M:%S", time.localtime()))
inicio_etapa3 = time.time()

tam = len(nome_colunas) # quantidade de colunas do dataset

#Lendo o arquivo particionado e escrevendo as colunas em arquivos criados para cada coluna
for particao in range(0, len(matriz_dataset)):
    for col in range(0, tam): #todas as colunas
        arq = open('C:/Users/Gabrielle/PycharmProjects/SO-OC/' + nome_colunas[col] + '.txt', 'a')
        for lin in range(0, len(matriz_dataset[particao])): #a partir do '0' para desconsiderar o header
          arq.write(str(matriz_dataset[particao][lin][col]))
          arq.write('\n')
    arq.close()

duracao_etapa3 = time.time() - inicio_etapa3
print("Fim Etapa: ", date.today(), time.strftime("%H:%M:%S", time.localtime()))
print("Duração da Etapa: ", str(datetime.timedelta(seconds = round(duracao_etapa3))))
