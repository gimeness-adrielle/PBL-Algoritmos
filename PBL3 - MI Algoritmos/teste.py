dic = {'Maria': '17 anos', 'João': '15 anos', 'Marcelo': '20 anos'}

nome_procurado = input("Qual o nome a procurar? ")

if not nome_procurado in dic:
    print ('Este nome NÃO está no dicionário')
else:
    print ('Este nome está no dicionário')