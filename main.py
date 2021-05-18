import winreg
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

#pegando o nome do processador
access_registry = winreg.ConnectRegistry(None,winreg.HKEY_LOCAL_MACHINE)
access_key = winreg.OpenKey(access_registry,r"HARDWARE\DESCRIPTION\System\CentralProcessor\0")

print('Arquitetura: ', platform.architecture())
print('Processador: ', platform.processor())
print('Nome do processador: ', winreg.QueryValueEx(access_key, 'ProcessorNameString'))
print('Plataforma: ', platform.platform())
print('Informações Plataforma: ', platform.machine())
print('Informações do Sistema: ', platform.system() + ' ' + platform.release())
print('Cores: ', multiprocessing.cpu_count())

freq = psutil.cpu_freq()

print('\nFrequência Processador\n\tAtual: ', freq[0], 'MHz',
      '\n\tMínima: ', freq[1], 'MHz',
      '\n\tMáxima: ', freq[2], 'MHz')

print()
print("=" * 40, "Informações do Disco", "=" * 40)
print()

# Disk Information
access_key_disks = winreg.OpenKey(access_registry, r"HARDWARE\DEVICEMAP\Scsi\Scsi Port 0")
subpastas = []

#pegando os nomes de todas as subpastas de Scsi Port 0
for n in range(20):
    try:
        x = winreg.EnumKey(access_key_disks, n)
        subpastas.append(x)
    except:
        break

#buscando as subpastas com o nome Target Id
targetId = []

#iterando dentro das subpastas de Scsi Port 0
for n in subpastas:
    try:
        for x in winreg.EnumKey(subpastas[n], n):
            if x.contains('Target Id'):
                targetId.append(x)
    except:
        break


print("Partições e Uso:")
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
print("=" * 40, "Informação da Memória", "=" * 40)
print()
# get the memory details
svmem = psutil.virtual_memory()
print(f"Total: {get_size(svmem.total)}")
print(f"Disponível: {get_size(svmem.available)}")
print(f"Usado: {get_size(svmem.used)}")
print(f"Porcentagem: {svmem.percent}%")

print()
print("=" * 20, "SWAP", "=" * 20)
print()
# get the swap memory details (if exists)
swap = psutil.swap_memory()
print(f"Total: {get_size(swap.total)}")
print(f"Free: {get_size(swap.free)}")
print(f"Used: {get_size(swap.used)}")
print(f"Percentage: {swap.percent}%")
print()

# Documentação da biblioteca: https://docs.python.org/3/library/platform.html#module-platform
# Documentação do psutil: https://psutil.readthedocs.io/en/latest/
# Documentação info. Disco Rígido: https://www.thepythoncode.com/article/get-hardware-system-information-python#Memory_Usage
