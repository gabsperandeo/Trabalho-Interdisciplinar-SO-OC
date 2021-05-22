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
    # Memory Information
    print("=" * 40, "Informação da Memória", "=" * 40, "\n")

    # get the memory details
    svmem = psutil.virtual_memory()
    print(f"Total: {get_size(svmem.total)}")
    print(f"Disponível: {get_size(svmem.available)}")
    print(f"Usado: {get_size(svmem.used)}")
    print(f"Porcentagem: {svmem.percent}%", "\n")
    print("=" * 20, "SWAP", "=" * 20, "\n")

    # get the swap memory details (if exists)
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
    # get all disk partitions
    partitions = psutil.disk_partitions()
    for partition in partitions:
        print(f"=== Dispositivo: {partition.device} ===", "\n")
        print(f"  Mountpoint: {partition.mountpoint}")
        print(f"  Sistema de Arquivo: {partition.fstype}")
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            # this can be catched due to the disk that
            # isn't ready
            continue
        print(f"  Tamanho total: {get_size(partition_usage.total)}")
        print(f"  Usado: {get_size(partition_usage.used)}")
        print(f"  Disponível: {get_size(partition_usage.free)}")
        print(f"  Porcentagem: {partition_usage.percent}%", "\n")

    # get IO statistics since boot
    disk_io = psutil.disk_io_counters()
    print(f"Total lido: {get_size(disk_io.read_bytes)}")
    print(f"Total escrito: {get_size(disk_io.write_bytes)}", "\n")


# MAIN
OS_architeture_information()
processor_information()
memory_information()
disks_information()

# abertura do arquivo
arq = 'dataset.csv'
number_lines = sum(1 for row in (open(arq, 'r', encoding="utf8")))  # quantidade de linhas do arquivo
rowsize = int((number_lines)/4)

'''
for i in range(1, number_lines, rowsize):
    df = pd.read_csv(arq,
        header = None,
        nrows = rowsize,#number of rows to read at each loop
        skiprows = i,#skip rows that have been read
        dtype = 'unicode')

    out_csv = 'input' + str(i) + '.csv'

    df.to_csv(out_csv,
    index = False,
    header = False,
    mode = 'a',  # append data to csv file
    chunksize = rowsize)  # size of data to append for each loop
'''

matriz_dataset = []

# etapa 1: leitura e carga em memória do arquivo
print("=========== ETAPA 1 ===========")
print("Inicio Etapa: ", date.today(), time.strftime("%H:%M:%S", time.localtime()))
inicio_etapa1 = time.time()

# particionando o arquivo em 4 para ler e armazenar na matriz
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
