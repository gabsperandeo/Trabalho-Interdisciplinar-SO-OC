import platform

arq = open('Python/teste.csv', 'r')
arq2 = open('Python/hardware.txt', 'w')

dados = arq.read()

print(dados)


arq2.write("INFORMAÇÕES DO HARDWARE: \n")
#arq2.write('\nArquitetura: ' + platform.architecture())
arq2.write('\nProcessador: ' + platform.processor())
arq2.write('\nPlataforma: ' + platform.platform())
arq2.write('\nInformações Plataforma: ' + platform.machine())
arq2.write('\nInformações do Sistema: ' + platform.system() + ' ' + platform.release())


arq2.write("\n\n============================ \n\nINFORMAÇÕES DO ARQUIVO 'teste.csv': \n")
arq2.write("\n" + dados)

arq.close()
arq2.close()