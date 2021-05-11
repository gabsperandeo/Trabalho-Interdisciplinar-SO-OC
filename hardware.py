import platform

print('Arquitetura: ', platform.architecture())
print('Processador: ', platform.processor())
print('Plataforma: ', platform.platform())
print('Informações Plataforma: ', platform.machine())
print('Informações do Sistema: ', platform.system() + ' ' + platform.release())

#Documentação da biblioteca: https://docs.python.org/3/library/platform.html#module-platform