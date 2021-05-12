import platform
import multiprocessing
import psutil

def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

print()

print('Arquitetura: ', platform.architecture())
print('Processador: ', platform.processor())
print('Plataforma: ', platform.platform())
print('Informações Plataforma: ', platform.machine())
print('Informações do Sistema: ', platform.system() + ' ' + platform.release())
print('Cores: ', multiprocessing.cpu_count())

freq = psutil.cpu_freq()

print('Frequência Processador\n\tAtual: ', freq[0], 'MHz',
         '\n\tMínima: ', freq[1], 'MHz',
          '\n\tMáxima: ', freq[2], 'MHz')

'''
disco = psutil.disk_partitions()
disco_uso = psutil.disk_usage('/')

print('Disco Rígido\n\tDevice: ', disco[0][0],
         '\n\tSistema de Arquivo: ', disco[0][2],
         '\n\tUso do Disco: ', disco_uso)
'''

print()
print("="*40, "Informações do Disco", "="*40)
print()
# Disk Information

print("Partições e Uso:")
print()
# get all disk partitions
partitions = psutil.disk_partitions()
for partition in partitions:
    print(f"=== Dispositivo: {partition.device} ===")
    print()
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
    print(f"  Porcentagem: {partition_usage.percent}%")
    print()
    
# get IO statistics since boot
disk_io = psutil.disk_io_counters()
print(f"Total lido: {get_size(disk_io.read_bytes)}")
print(f"Total escrito: {get_size(disk_io.write_bytes)}")
print()

# Memory Information
print("="*40, "Informação da Memória", "="*40)
print()
# get the memory details
svmem = psutil.virtual_memory()
print(f"Total: {get_size(svmem.total)}")
print(f"Disponível: {get_size(svmem.available)}")
print(f"Usado: {get_size(svmem.used)}")
print(f"Porcentagem: {svmem.percent}%")

print()
print("="*20, "SWAP", "="*20)
print()
# get the swap memory details (if exists)
swap = psutil.swap_memory()
print(f"Total: {get_size(swap.total)}")
print(f"Free: {get_size(swap.free)}")
print(f"Used: {get_size(swap.used)}")
print(f"Percentage: {swap.percent}%")
print()

#Documentação da biblioteca: https://docs.python.org/3/library/platform.html#module-platform
#Documentação do psutil: https://psutil.readthedocs.io/en/latest/
#Documentação info. Disco Rígido: https://www.thepythoncode.com/article/get-hardware-system-information-python#Memory_Usage
