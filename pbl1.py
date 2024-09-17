# Autor: Adrielle Gimenes
# Componente Curricular: MI Algoritmos
# Concluído em: 14/09/2024
# Declaro que este código foi elaborado por mim de forma individual e não contém nenhum
# trecho de código de outro colega ou de outro autor, tais como provindos de livros e
# apostilas, e páginas ou documentos eletrônicos da Internet. Qualquer trecho de código
# de outra autoria que não a minha está destacado com uma citação para o autor e a fonte
# do código, e estou ciente que estes trechos não serão considerados para fins de avaliação.

# Solicita ao usuário a configuração da pontuação para cada tipo de problema
print (f"\033[1;37;46m{' Configuração da Maratona':^56}""\033[0m")
print ("\033[1;30;40m========================================================")
while True:
    quantidade_problemas = (input("\033[1;37;40mDigite a quantidade de problemas a serem resolvidos:\033[0m "))
    facil = (input("\033[1;37;40mInsira a pontuação para os problemas de tipo \033[0;37;42m Fácil \033[0m: "))
    medio = (input("\033[1;37;40mInsira a pontuação para os problemas de tipo \033[0;37;43m Médio \033[0m: "))
    dificil = (input("\033[1;37;40mInsira a pontuação para os problemas de tipo \033[0;37;41m Difícil \033[0m: "))
    if quantidade_problemas.isdigit() and facil.isdigit() and medio.isdigit() and dificil.isdigit():
        quantidade_problemas = int(quantidade_problemas)
        facil = int(facil)
        medio = int(medio)
        dificil = int(dificil)
        break
    else: print("\033[0;31;40mErro: Por favor, digite um número inteiro válido.")
        
# Solicita ao usuário para registrar o nome de cada equipe
print ("\n\033[1;30;40m========================================================")
print (f"\033[1;37;40m{' Insira os nomes das equipes ':^56}")
print ("\033[1;30;40m========================================================")
equipe1 = str(input("\033[1;37;40m[1º] | \033[0m")).upper()
equipe2 = str(input("\033[1;37;40m[2º] | \033[0m")).upper()
equipe3 = str(input("\033[1;37;40m[3º] | \033[0m")).upper()
equipe4 = str(input("\033[1;37;40m[4º] | \033[0m")).upper()
equipe5 = str(input("\033[1;37;40m[5º] | \033[0m")).upper()

# Dados das equipes: problemas resolvidos e o tempo levado total
facil1,medio1,dificil1,tempo1 = 0, 0, 0, 0
facil2,medio2,dificil2,tempo2 = 0, 0, 0, 0
facil3,medio3,dificil3,tempo3 = 0, 0, 0, 0
facil4,medio4,dificil4,tempo4 = 0, 0, 0, 0
facil5,medio5,dificil5,tempo5 = 0, 0, 0, 0

# Início da maratona, o usuário registra cada acerto das equipes
parar_maratona = "n"
while parar_maratona != "s":
    print ("\n\033[1;30;40m========================================================")
    print (f"\033[1;37;40m{' Registre uma questão ':^56}")
    print ("\033[1;30;40m=======================================================")
    quem_pontuou = str(input("\033[1;37;40mQual equipe resolveu um problema?\033[0m ")).upper()
    while True:
        tipo_problema = (input("\033[1;37;40mQual tipo de problema resolveu? (\033[1;37;42m 1 \033[0m para \033[1;37;42m Fácil \033[0m, \033[1;37;43m 2 \033[0m para \033[1;37;43m Médio \033[0m e \033[1;37;41m 3 \033[0m para \033[1;37;41m Difícil \033[0m) "))
        tempo_levado = (input("\033[1;37;40mQual o tempo gasto EM SEGUNDOS no problema?\033[0m "))
        if tipo_problema.isdigit() and tempo_levado.isdigit():
            tipo_problema = int(tipo_problema)
            tempo_levado = int(tempo_levado)
            break
        else:
            print("\033[0;31;40mErro: Por favor, digite um número inteiro válido.")
    print ("\033[1;30;40m=======================================================")
    parar_maratona = str(input("\033[1;37;40mDeseja encerrar a maratona? (s,n)? "))

    # Adicionar os acertos aos dados das respectivas equipes
    if quem_pontuou == equipe1:
        match tipo_problema:
            case 1: facil1 += 1
            case 2: medio1 += 1
            case 3: dificil1 += 1
        tempo1 += tempo_levado
    if quem_pontuou == equipe2:
        match tipo_problema:
            case 1: facil2 += 1
            case 2: medio2 += 1
            case 3: dificil2 += 1
        tempo2 += tempo_levado
    if quem_pontuou == equipe3:
        match tipo_problema:
            case 1: facil3 += 1
            case 2: medio3 += 1
            case 3: dificil3 += 1
        tempo3 += tempo_levado
    if quem_pontuou == equipe4:
        match tipo_problema:
            case 1: facil4 += 1
            case 2: medio4 += 1
            case 3: dificil4 += 1
        tempo4 += tempo_levado
    if quem_pontuou == equipe5:
        match tipo_problema:
            case 1: facil5 += 1
            case 2: medio5 += 1
            case 3: dificil5 += 1
        tempo5 += tempo_levado

# Cálculo da pontuação final de cada equipe
pontos1 = (facil1 * facil + medio1 * medio + dificil1 * dificil)
pontos2 = (facil2 * facil + medio2 * medio + dificil2 * dificil)
pontos3 = (facil3 * facil + medio3 * medio + dificil3 * dificil)
pontos4 = (facil4 * facil + medio4 * medio + dificil4 * dificil)
pontos5 = (facil5 * facil + medio5 * medio + dificil5 * dificil)

# Decisão de vitória e desempates
if pontos1 < pontos2 or (pontos1 == pontos2 and dificil1 < dificil2) or (pontos1 == pontos2 and dificil1 == dificil2 and tempo1 > tempo2):
    pontos2, equipe2, pontos1, equipe1 = pontos1, equipe1, pontos2, equipe2
    facil2, medio2, dificil2, facil1, medio1, dificil1 = facil1, medio1, dificil1, facil2, medio2, dificil2
    tempo2,tempo1 = tempo1,tempo2
if pontos1 < pontos3 or (pontos1 == pontos3 and dificil1 < dificil3) or (pontos1 == pontos3 and dificil1 == dificil3 and tempo1 > tempo3):
    pontos3, equipe3, pontos1, equipe1 = pontos1, equipe1, pontos3, equipe3
    facil3, medio3, dificil3, facil1, medio1, dificil1 = facil1, medio1, dificil1, facil3, medio3, dificil3
    tempo3,tempo1 = tempo1,tempo3
if pontos1 < pontos4 or (pontos1 == pontos4 and dificil1 < dificil4) or (pontos1 == pontos4 and dificil1 == dificil4 and tempo1 > tempo4):
    pontos4, equipe4, pontos1, equipe1 = pontos1, equipe1, pontos4, equipe4
    facil4, medio4, dificil4, facil1, medio1, dificil1 = facil1, medio1, dificil1, facil4, medio4, dificil4
    tempo4,tempo1 = tempo1,tempo4
if pontos1 < pontos5 or (pontos1 == pontos5 and dificil1 < dificil5) or (pontos1 == pontos5 and dificil1 == dificil5 and tempo1 > tempo5):
    pontos5, equipe5, pontos1, equipe1 = pontos1, equipe1, pontos5, equipe5
    facil5, medio5, dificil5, facil1, medio1, dificil1 = facil1, medio1, dificil1, facil5, medio5, dificil5
    tempo5,tempo1 = tempo1,tempo5

if pontos2 < pontos3 or (pontos2 == pontos3 and dificil2 < dificil3) or (pontos2 == pontos3 and dificil2 == dificil3 and tempo2 > tempo3):
    pontos3, equipe3, pontos2, equipe2 = pontos2, equipe2, pontos3, equipe3
    facil3, medio3, dificil3, facil2, medio2, dificil2 = facil2, medio2, dificil2, facil3, medio3, dificil3
    tempo3,tempo2 = tempo2,tempo3
if pontos2 < pontos4 or (pontos2 == pontos4 and dificil2 < dificil4) or (pontos2 == pontos4 and dificil2 == dificil4 and tempo2 > tempo4):
    pontos4, equipe4, pontos2, equipe2 = pontos2, equipe2, pontos4, equipe4
    facil4, medio4, dificil4, facil2, medio2, dificil2 = facil2, medio2, dificil2, facil4, medio4, dificil4
    tempo4,tempo2 = tempo2,tempo4
if pontos2 < pontos5 or (pontos2 == pontos5 and dificil2 < dificil5) or (pontos2 == pontos5 and dificil2 == dificil5 and tempo2 > tempo5):
    pontos5, equipe5, pontos2, equipe2 = pontos2, equipe2, pontos5, equipe5
    facil5, medio5, dificil5, facil2, medio2, dificil2 = facil2, medio2, dificil2, facil5, medio5, dificil5
    tempo5,tempo2 = tempo2,tempo5

if pontos3 < pontos4 or (pontos3 == pontos4 and dificil3 < dificil4) or (pontos3 == pontos4 and dificil3 == dificil4 and tempo3 > tempo4):
    pontos4, equipe4, pontos3, equipe3 = pontos3, equipe3, pontos4, equipe4
    facil4, medio4, dificil4, facil3, medio3, dificil3 = facil3, medio3, dificil3, facil4, medio4, dificil4
    tempo4,tempo3 = tempo3,tempo4
if pontos3 < pontos5 or (pontos3 == pontos5 and dificil3 < dificil5) or (pontos3 == pontos5 and dificil3 == dificil5 and tempo3 > tempo5):
    pontos5, equipe5, pontos3, equipe3 = pontos3, equipe3, pontos5, equipe5
    facil5, medio5, dificil5, facil3, medio3, dificil3 = facil3, medio3, dificil3, facil5, medio5, dificil5
    tempo5,tempo3 = tempo3,tempo5

if pontos4 < pontos5 or (pontos4 == pontos5 and dificil4 < dificil5) or (pontos4 == pontos5 and dificil4 == dificil5 and tempo4 > tempo5):
    pontos5, equipe5, pontos4, equipe4 = pontos4, equipe4, pontos5, equipe5
    facil5, medio5, dificil5, facil4, medio4, dificil4 = facil4, medio4, dificil4, facil5, medio5, dificil5
    tempo4,tempo5 = tempo5,tempo4

# Ranking das equipes
print (f"\033[1;37;46m{' Ranking das Equipes ':^56}""\033[0m")
print ("\033[1;30;40m========================================================")
print(f"{'\033[1;30;47m Equipes \033[0m':<29}{"\033[1;37;40m|"}{'\033[1;37;42m Fácil \033[0m':^23}{'\033[1;37;43m Médio \033[0m':^22}{'\033[1;37;41m Difícil \033[0m':^23}{'\033[1;37;45m Score \033[0m ':>25}") 
print ("\033[1;37;40m--------------------------------------------------------")
print (f"\033[1;37;40m[1°]{equipe1:<11}{"|"}\033[1;32;40m{facil1:^10}\033[1;33;40m{medio1:^6}\033[1;31;40m{dificil1:^11}\033[1;37;40m{pontos1:^8}")
print (f"\033[1;37;40m[2°]{equipe2:<11}{"|"}\033[1;32;40m{facil2:^10}\033[1;33;40m{medio2:^6}\033[1;31;40m{dificil2:^11}\033[1;37;40m{pontos2:^8}")
print (f"\033[1;37;40m[3°]{equipe3:<11}{"|"}\033[1;32;40m{facil3:^10}\033[1;33;40m{medio3:^6}\033[1;31;40m{dificil3:^11}\033[1;37;40m{pontos3:^8}")
print (f"\033[1;37;40m[4°]{equipe4:<11}{"|"}\033[1;32;40m{facil4:^10}\033[1;33;40m{medio4:^6}\033[1;31;40m{dificil4:^11}\033[1;37;40m{pontos4:^8}")
print (f"\033[1;37;40m[5°]{equipe5:<11}{"|"}\033[1;32;40m{facil5:^10}\033[1;33;40m{medio5:^6}\033[1;31;40m{dificil5:^11}\033[1;37;40m{pontos5:^8}")
input ()

# Exibir qual equipe foi a vencedora
print ("\033[1;30;40m=======================================================")
print (f"{'\033[1;37;40mA equipe \033[1;34;40mVENCEDORA\033[1;37;40m foi: ':>70}")
print (f"{'\033[1;37;40m ☆ ':>33}\033[1;30;44m {equipe1:^5} \033[0m{'\033[1;37;40m ☆ ':<33}\033[0m")
print ("\n\033[1;30;40m=======================================================")
input ()

# Dados da equipe vencedora
formatacao = f"{tempo1//60/60:.1f}"
print (f"\033[1;37;46m{' Dados da Equipe Vencedora ':^56}""\033[0m")
print ("\033[1;30;40m========================================================")
print ("\033[1;37;40m ☆  \033[1;30;44m", equipe1, "\033[1;37;40m ☆ \033[0m")
print (f"{'\033[1;37;40m[ TEMPO TOTAL EM HORAS]':<35}{"|"}\033[1;34;40m{formatacao:^10}")
print (f"{'\033[1;37;40m[ PROBLEMAS DIFÍCEIS ]':<35}{"|"}\033[1;34;40m{dificil1:^10}")
print (f"{'\033[1;37;40m[ PONTUAÇÃO TOTAL ]':<35}{"|"}\033[1;34;40m{pontos1:^10}")
input ()

# Exibir a média de cada equipe
print (f"\033[1;37;46m{' Média das Equipes ':^56}""\033[0m")
print ("\033[1;30;40m=======================================================")
print (f"\033[1;37;40m{equipe1:<20}{"|":>1} \033[1;34;40m{pontos1/quantidade_problemas:.1f}")
print (f"\033[1;37;40m{equipe2:<20}{"|":>1} \033[1;34;40m{pontos2/quantidade_problemas:.1f}")
print (f"\033[1;37;40m{equipe3:<20}{"|":>1} \033[1;34;40m{pontos3/quantidade_problemas:.1f}")
print (f"\033[1;37;40m{equipe4:<20}{"|":>1} \033[1;34;40m{pontos4/quantidade_problemas:.1f}")
print (f"\033[1;37;40m{equipe5:<20}{"|":>1} \033[1;34;40m{pontos5/quantidade_problemas:.1f}")

# Decisão de qual equipe resolveu mais problemas difíceis
if dificil1 < dificil2: dificil2,equipe2, dificil1,equipe1 = dificil1,equipe1, dificil2,equipe2
if dificil1 < dificil3: dificil3,equipe3, dificil1,equipe1 = dificil1,equipe1, dificil3,equipe3
if dificil1 < dificil4: dificil4,equipe4, dificil1,equipe1 = dificil1,equipe1, dificil4,equipe4
if dificil1 < dificil5: dificil5,equipe5, dificil1,equipe1 = dificil1,equipe1, dificil5,equipe5

if dificil2 < dificil3: dificil3,equipe3, dificil2,equipe2 = dificil2,equipe2, dificil3,equipe3
if dificil2 < dificil4: dificil4,equipe4, dificil2,equipe2 = dificil2,equipe2, dificil4,equipe4
if dificil2 < dificil5: dificil5,equipe5, dificil2,equipe2 = dificil2,equipe2, dificil5,equipe5

if dificil3 < dificil4: dificil4,equipe4, dificil3,equipe3 = dificil3,equipe3, dificil4,equipe4
if dificil3 < dificil5: dificil5,equipe5, dificil3,equipe3 = dificil3,equipe3, dificil5,equipe5

if dificil4 < dificil5: dificil5,equipe5, dificil4,equipe4 = dificil4,equipe4, dificil5,equipe5

# Exibir qual equipe resolveu mais problemas difíceis
print ("\033[1;30;40m=======================================================")
print (f"{'\033[1;37;40mA equipe que resolveu o maior número de problemas \033[1;31;40mDIFÍCEIS\033[1;37;40m foi: ':>60}")
print (f"{'\033[1;37;40m ঌ ':>33}\033[1;37;41m {equipe1:^5} \033[0m{'\033[1;37;40m ໒ ':<33}\033[0m")
print ("\n\033[1;30;40m=======================================================")