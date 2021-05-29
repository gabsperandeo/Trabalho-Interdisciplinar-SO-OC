import concurrent.futures
from os import close

def string_is_float(word):
    try:
        float(word)
        return True
    except ValueError:
        return False

def words_count(argumentos):
   if (not string_is_float(argumentos)):
     return len(argumentos.split())
   else:
     return 0

def all_words_count(valor):
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        future = executor.submit(words_count, valor)
        #arq.write(valor + '\n')
        return future.result()

array_de_array = [
                  [
                   ['Rotulo','Rotulo2','Rotulo3','Rotulo4'],
                   ['1.23','test2e sad', '312', 'quarta coluna'],
                   ['0.123','test2e ada', '4132', 'quarta coluna'],
                   ['1.123','test2e aas', '5415', 'quarta coluna'],
                   ['1.123','teste adsa', '5143', 'quarta coluna'],
                  ],
                  [
                   ['45.60','teste dasd dadda adas', '14514', 'quarta coluna'],
                   ['4.63','tes1te dasda', '5143', 'quarta coluna'],
                   ['456','tes1te', '1543', 'quarta coluna'],
                  ],
                  [
                   ['7.89','tes12 te', '14134', 'quarta coluna'],
                   ['783.94','t1este', '15345', 'quarta coluna'],
                   ['789','t1es te', '5143', 'quarta coluna'],
                  ]
              ]


array_de_array2 = [['Rotulo','Rotulo2','Rotulo3','Rotulo4'],
                   ['1.23','test2e sad', '312', 'quarta coluna'],
                   ['0.123','test2e ada', '4132', 'quarta coluna'],
                   ['1.123','test2e aas', '5415', 'quarta coluna'],
                   ['1.123','teste adsa', '5143', 'quarta coluna'],
                   ['45.60','teste dasd dadda adas', '14514', 'quarta coluna'],
                   ['4.63','tes1te dasda', '5143', 'quarta coluna'],
                   ['456','tes1te', '1543', 'quarta coluna'],
                   ['7.89','tes12 te', '14134', 'quarta coluna'],
                   ['783.94','t1este', '15345', 'quarta coluna'],
                   ['789','t1es te', '5143', 'quarta coluna'],
              ]

teste = array_de_array[0].pop(0)
tam = len(teste) #quantidade de colunas do dataset
count_array = [0,0,0,0]

i = 0
for particao in array_de_array:    # iterando por particionamento
    #arq = open('Python/' + teste[i] + '.txt', 'w')
    for linha in particao:
      index = 0             # iterando por linha do particionamento
      for valor in linha:         # iterando por coluna do particionamento
        count_array[index] += all_words_count(valor)
        #arq.write(valor + '\n')
        index += 1
    #arq.close()
    #i += 1


number_lines = 11
'''
FUNCIONANDO
for col in range(0, 4): #todas as colunas
    arq = open('Python/' + teste[col] + '.txt', 'w')
    for lin in range(1, number_lines): #a partir do '1' para desconsiderar o header
        arq.write(str(array_de_array2[lin][col]))
        arq.write('\n')
    arq.close()
'''
#Lendo o arquivo particionado e escrevendo as colunas em arquivos criados para cada coluna
for particao in range(0, len(array_de_array)):
    for col in range(0, 4): #todas as colunas
        arq = open('Python/' + teste[col] + '.txt', 'a')
        for lin in range(0, len(array_de_array[particao])): #a partir do '0' para desconsiderar o header
          arq.write(str(array_de_array[particao][lin][col]))
          arq.write('\n')
    arq.close()

'''
arq = open('Python/' + teste[0] + '.txt', 'w')
arq.write(str(array_de_array2[1][0]))
arq.write('\n')
arq.close()
'''

print(count_array)
print(tam)
print(teste)
