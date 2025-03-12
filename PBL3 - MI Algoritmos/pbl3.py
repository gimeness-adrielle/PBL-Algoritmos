# Autor: Adrielle Gimenes
# Componente Curricular: MI Algoritmos
# Concluído em: 09/12/2024
# Declaro que este código foi elaborado por mim de forma individual e não contém nenhum
# trecho de código de outro colega ou de outro autor, tais como provindos de livros e
# apostilas, e páginas ou documentos eletrônicos da Internet. Qualquer trecho de código
# de outra autoria que não a minha está destacado com uma citação para o autor e a fonte
# do código, e estou ciente que estes trechos não serão considerados para fins de avaliação.

from customtkinter import *
import xmltodict
from PIL import Image
import random
import os

class App(CTk):
    def __init__(self):
        super().__init__()
        self.title ("AskMe")
        self.geometry ("800x700")

        code_folder = os.path.dirname(os.path.abspath(__file__))    # Diretório da pasta do código
        self.icons_folder = os.path.join(code_folder, "Icons")      # Abrindo a pasta de ícones (motivos estéticos)
        self.images_folder = os.path.join (code_folder, "Images")   # Abrindo a pasta de imagens das questões

        # Carregar o arquivo XML de questões
        with open("questions.xml", 'rb') as file:
            questions_data = xmltodict.parse(file)
        self.questions_data = questions_data['Quiz']['Questions']['question']
        self.settings = questions_data['Quiz']['Settings']   # Configurações do jogo

        # Carregar o arquivo XML do Hall da Fama
        with open ("ranking.xml", 'rb') as file:
            self.ranking = xmltodict.parse (file)

        self.question_index = 0     # Questão atual
        self.hint_idx = 0           # Dica atual
        self.help = int(self.settings['help_quantity']  )     # Quantidade inicial de ajudas do jogador, definida no arquivo XML pelo projetor

        self.questions_quantity = int(self.settings['questions_quantity'])      # Quantidade de perguntas, definida no arquivo XML pelo projetor
        if self.questions_quantity > len(self.questions_data):                  # Se a quantidade que o projetista colocar for maior do que a quantidade de questões do arquivo
            diferenca = self.questions_quantity - len(self.questions_data)      # Obtém a diferença
            self.questions_quantity -= diferenca                                # Regula a quantidade de questões

        self.time = int(self.settings['time_settings'])        # Tempo configurável
        self.score = 0                  # Score do jogador (pontos)
        self.consecutive_hits = 0       # Acertos consecutivos do jogador
        self.mode_stats = {"mode1": False, "mode2": False, "mode3": False}      # Modos de jogo

        # Frames (telas) do quiz
        self.main_page = MainPage (self)
        self.rank_page = RankPage(self)
        self.gamemode = Gamemode (self)
        self.question_screen = QuestionScreen (self)
        self.achievement = AchievementScreen (self)

        self.frame_list = [self.main_page, self.rank_page, self.gamemode, self.question_screen, self.achievement]

        # Começar o programa sempre na página inicial
        self.change_win(self.main_page)

    # Método para alternar entre as telas
    def change_win (self, win):
        for frame in self.frame_list:   # Percorre a lista de frames
            frame.pack_forget ()        # Oculta todos os frames da lista
        win.pack(pady=50)               # Mostra apenas o frame que quiser, dependendo do parâmetro inserido

    # Método para checar se a opção selecionada é a correta
    def check_answer (self, option, optionsButtons):
        correct_answer = self.questions_data[self.question_index]['answer']
        qst_value = int(self.questions_data[self.question_index]['value'])
        self.question_screen.next.configure(state="enabled")

        for button in optionsButtons:                                       # Percorre lista dos botões das opções
            if button == option:                                            # O botão na lista corresponde à opção escolhida?
                if option.cget("text") == correct_answer:                   # Então verifica se a opção escolhida corresponde à resposta correta
                    option.configure(fg_color="#4f8832", state="disabled")  # Reconfigura o botão da opção
                    self.score += qst_value                                 # Adiciona a pontuação
                    self.consecutive_hits += 1                              # Acertos consecutivos
                    self.info_refresh()                                     # Atualiza as informações de jogo na tela
                else:           # Se errar a questão
                    option.configure(fg_color="#c42c1f", state="disabled")
                    self.consecutive_hits = 0
                    self.info_refresh()

                    if self.mode_stats["mode3"]:     # Verifica se o modo de jogo escolhido é o "Tente não errar"
                        self.achievement.txt1.configure (text="G A M E  O V E R")
                        self.achievement.txt2.configure (text="Você errou a questão.")
                        self.change_win(self.achievement)       # Muda para a tela final de Game Over
                        self.can_enter_ranking(self.gamemode.mode)
            else:
                button.configure(fg_color="gray", state="disabled")
                self.question_screen.skip_qst.configure (state="disabled")
                self.question_screen.show_hint.configure (state="disabled")
                self.question_screen.delete_opt.configure (state="disabled")

    # Método para mostrar nova questão, ou pular a questão
    def next_question (self, txt, pressed_button):
        if pressed_button is None:          # Se for a primeira questão
            self.question_index = 0

        elif self.question_index + 1 >= self.questions_quantity:     # Se a próxima questão for ultrapassar a quantidade de questões disponíveis
            self.info_refresh
            self.change_win(self.achievement)      # Muda para a tela de vitória (o jogador conseguiu responder todas as questões)
            self.can_enter_ranking(self.gamemode.mode)      # Verifica se o jogador pode entrar no Hall da Fama
            return
        
        else:
            if pressed_button == self.question_screen.skip_qst:     # Verifica se o botão pressionado é o de ajuda (pular questão)
                if self.help > 0:       # Verifica se o jogador tem ajudas disponíveis para utilizar
                    self.help -= 1      # Gasta uma ajuda
                    self.info_refresh()       # Atualiza a informação de quantidade de ajudas para o jogador
                else: return
                
            self.question_screen.next.configure(state="disabled")
            self.question_index += 1

        next_qst = self.questions_data[self.question_index]['questionText']
        txt.configure(text=next_qst)

        for idx, option in enumerate(self.question_screen.optionsButtons):
            new_opt = self.questions_data[self.question_index][f'option{idx+1}']
            option.configure(text= new_opt, fg_color="#7F6CEB", state="normal")

        self.question_screen.skip_qst.configure (state="normal")
        self.question_screen.show_hint.configure (state="normal")
        self.question_screen.delete_opt.configure (state="normal")

        if self.consecutive_hits != 0 and self.consecutive_hits % 3 == 0:
            self.help += 1
            self.info_refresh()
        
        # Atualizar a barra de progresso visual
        progresso = (self.question_index) / self.questions_quantity
        self.question_screen.progress_bar.set(progresso)

        # Verificar se a questão possui uma imagem
        self.check_image()
    
    # Método de opção de ajuda: mostrar uma dica
    def show_hint (self):
        if self.help > 0:       # Verifica se o jogador tem ajudas disponíveis para utilizar
            hints=self.questions_data[self.question_index]['hint']

            if isinstance(hints, str):      # Verifica se hints é uma string, se for uma string significa que é apenas uma dica, se for uma lista, há mais de uma dica.
                hints = [hints]             # Se for string (uma dica), coloca a mesma em uma lista

            if self.hint_idx < len(hints):      # Índice dentro dos limites da lista de dicas
                hint = hints[self.hint_idx]     # Acessa a dica
                HelpWindow(self, hint)          # Mostra a dica
                self.help -= 1                  # Decrementa a quantidade de ajudas disponíveis em 1
                self.info_refresh()       # Atualiza a informação de quantidade de ajudas ao jogador

                if self.hint_idx + 1 >= len(hints):
                    self.hint_idx = 0
                else: 
                    self.hint_idx += 1

    # Método de opção de ajuda: deletar uma opção errada
    def delete_opts (self, optbuttons):
        if self.help > 0:
            correct_answer = self.questions_data[self.question_index]['answer']
            wrong_options = []

            for button in optbuttons:
                if button.cget("text") != correct_answer and button.cget("state") == "normal":      # Se for uma opção incorreta
                    wrong_options.append(button)

            if wrong_options:
                del_button = random.choice (wrong_options)      # Escolhe uma opção incorreta aleatória dentro das opções incorretas
                del_button.configure(fg_color="#c42c1f", state="disabled")      # Desativa este botão
                self.help -= 1
                self.info_refresh()       # Atualiza a informação de quantidade de ajudas ao jogador

    # Verificar se a questão possui uma imagem
    def check_image (self):
        question = self.questions_data[self.question_index]

        if question.get('questionPath'):
            image = CTkImage (light_image=Image.open(os.path.join(self.images_folder, question['questionPath'])), size=(854, 480))
            ImageWindow (self, image)

    # Reseta o jogo, suas configurações padrões e toda as informações de score, modo de jogo escolhido, botões, etc
    def reset_game (self):
        self.hint_idx = 0
        self.question_index = 0
        self.help = int(self.settings['help_quantity'])
        self.score = 0
        self.consecutive_hits = 0
        self.time = int(self.settings['time_settings'])
        self.mode_stats = {"mode1": False, "mode2": False, "mode3": False}

        for option in self.question_screen.optionsButtons:
            option.configure (fg_color="#7F6CEB", state="normal")

        self.question_screen.skip_qst.configure (state="normal")
        self.question_screen.show_hint.configure (state="normal")
        self.question_screen.delete_opt.configure (state="normal")
        self.question_screen.next.configure(state="disabled")

        self.info_refresh()
        self.next_question(self.question_screen.qst_txt, None)

    # Atualiza as informações de jogo na tela
    def info_refresh (self):
        self.question_screen.show_score.configure(text=f"SCORE: {self.score}")
        self.question_screen.amount_helps.configure(text=f"Ajudas disponíveis: {self.help}")
        self.achievement.final_score.configure(text=f"Score: {self.score}")
        self.question_screen.combo.configure(text=f"Combo: {self.consecutive_hits}")

    # Timer para o modo de jogo: Limite de Tempo
    def timer (self):
        if self.mode_stats ["mode2"]:   # Se o modo ativo for o de limite de tempo
            if self.time > 0:
                mins, secs = divmod(self.time, 60)
                self.question_screen.show_timer.configure (text=f"Tempo restante: {mins:02}:{secs:02}", text_color="#4f8832")
                self.time -= 1
                self.after(1000, self.timer)
                self.change_timer_color()
            else:
                self.achievement.txt1.configure (text="G A M E  O V E R")
                self.achievement.txt2.configure (text="Tempo esgotado.")
                self.change_win(self.achievement)

    # Método estético para trocar a cor do timer quando atingir certos valores
    def change_timer_color (self):
        if self.time < 30:
            self.question_screen.show_timer.configure (text_color="#b0833a")
        if self.time < 10:
            self.question_screen.show_timer.configure (text_color="#c42c1f")

    # Verificar se o jogador pode entrar no Hall da Fama
    def can_enter_ranking (self, mode):
        self.timemode_finalscore = self.score + self.time
        for idx, player in enumerate(self.ranking['Ranking'][mode]['Player']):
            player_score = player['Score']
            if not player_score:    
                player_score = 0
            else:
                player_score = int(player_score)

            if self.mode_stats['mode2']:
                current_score = self.timemode_finalscore
            else:
                current_score = self.score

            if current_score > player_score:
                self.player_idx = idx
                RankingPopup(self)  # Chama popup para pegar o nome do jogador
                break
            
    # Se o jogador pode entrar no Hall da Fama, verificar se ele colocou o nome dele e colocar no arquivo do Hall da Fama
    def check_name_for_rank (self, player_name, mode):
        if player_name.strip():
            if self.mode_stats['mode2']:
                final_score = self.timemode_finalscore
            else:
                final_score = self.score

            new_player = {'Name': player_name, 'Score': str(final_score)}

            players = self.ranking['Ranking'][mode]['Player']
            players.insert(self.player_idx, new_player)

            if len(players) > 5:
                players.pop()

            with open('ranking.xml', 'w') as file:
                file.write(xmltodict.unparse(self.ranking, pretty=True))

# Frame da tela inicial (principal)
class MainPage (CTkFrame):
    def __init__(self, master, width = 800, height = 600):
        super().__init__(master, width, height)
        global brain_img, play_icon, rank_icon
        self.grid_propagate(False)
        self.configure(fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Apenas alguns ícones para estética
        brain_img = CTkImage (light_image=Image.open(os.path.join(master.icons_folder, "brain.png")), size=(230, 190))
        play_icon = CTkImage (light_image=Image.open(os.path.join(master.icons_folder, "play_icon.png")), size=(35,35))
        rank_icon = CTkImage (light_image=Image.open(os.path.join(master.icons_folder, "mountain_top.png")), size=(35,35))

        # Widgets
        CTkLabel (self, text="", image=brain_img
                ).grid(sticky="n", columnspan=2)

        CTkLabel (self, text="A S K M E", font=("Trebuchet MS", 55, "bold"), 
                  text_color="#44D7FC"
                ).grid(row=1, sticky="n", columnspan=2)
        
        CTkLabel (self, 
                text="Teste seus conhecimentos", font=("Comic Sans MS", 20, "italic"),
                text_color="#7F6CEB"
                ).grid(row=2, column=0, sticky="n", columnspan=2)
        
        CTkButton (self, 
                text="Play", font=("Comic Sans MS", 30), 
                fg_color="#7F6CEB", hover_color="#9D44FC",
                width=230, image=play_icon, 
                command= lambda: (master.reset_game(), master.change_win(master.gamemode))
                ).grid(row=3,padx=20, pady=20)
        
        CTkButton (self,
                text="Hall da Fama", font=("Comic Sans MS", 30),
                fg_color="#7F6CEB", hover_color="#9D44FC",
                width=230, image=rank_icon,
                command=lambda: master.change_win(master.rank_page)
                ).grid(row=3, column=1, padx=20, pady=20)
    
        CTkLabel (self, 
                text="Produzido por Adrielle Gimenes.", font=("Comic Sans MS", 15)
                ).grid(row=4, sticky="n", columnspan=2)
        CTkLabel (self, 
                text="Utilizando CustomTKinter, 20 de nov. de 2024", font=("Comic Sans MS", 15)
                ).grid(row=5, sticky="n", columnspan=2)
        CTkLabel (self, 
                text="Windows 10 Pro - Python", font=("Comic Sans MS", 15)
                ).grid(row=6, sticky="n", columnspan=2)

# Frame da tela do Hall da Fama
class RankPage(CTkFrame):
    def __init__(self, master, width=550, height=600):
        super().__init__(master, width, height)
        self.grid_propagate(False)
        self.configure(fg_color="transparent")

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_columnconfigure(0, weight=1)

        medal1 = CTkImage (light_image=Image.open(os.path.join(master.icons_folder, "medal1.png")), size=(43, 40))
        medal2 = CTkImage (light_image=Image.open(os.path.join(master.icons_folder, "medal2.png")), size=(43, 40))
        medal3 = CTkImage (light_image=Image.open(os.path.join(master.icons_folder, "medal3.png")), size=(43, 40))
        pos4 = CTkImage (light_image=Image.open(os.path.join(master.icons_folder, "pos4.png")), size=(30, 27))
        pos5 = CTkImage (light_image=Image.open(os.path.join(master.icons_folder, "pos5.png")), size=(30, 27))
        self.icon_list = [medal1, medal2, medal3, pos4, pos5]

        # Widgets
        CTkLabel(self, text="Hall da Fama", 
                font=("Trebuchet MS", 55, "bold"), text_color="#44D7FC"
                ).grid(row=0, column=0, pady=(10, 20), sticky="n")

        self.tabview = CTkTabview(self, width=500, height=450)
        self.tabview.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        # Adicionando abas no TabView
        self.tabview.add("Questões fixas")
        self.tabview.add("Limite de tempo")
        self.tabview.add("Tente não errar")

        # Configurar abas
        abas = ["Questões fixas", "Limite de tempo", "Tente não errar"]
        for aba_nome in abas:
            aba = self.tabview.tab(aba_nome)
            aba.grid_columnconfigure(0, weight=0)
            aba.grid_columnconfigure(1, weight=1)
            aba.grid_columnconfigure(2, weight=0)
            aba.grid_columnconfigure(3, weight=1)

            CTkLabel(aba, text="PLAYER_NAME", font=("Arial", 18, "bold")).grid(row=0, column=1, padx=15, pady=10, sticky="w")
            CTkLabel(aba, text="SCORE", font=("Arial", 18, "bold")).grid(row=0, column=3, padx=15, pady=10, sticky="e")

        CTkButton(self,
                text="Voltar", font=("Comic Sans MS", 18),
                fg_color="#7F6CEB", hover_color="#9D44FC",
                command=lambda: master.change_win(master.main_page)
                ).grid(row=2, column=0, pady=(10, 20))

        # Adicionando os espaços de jogadores no ranking
        self.player_names_frame("Questões fixas", ["#474747", "#474747", "#474747", "#474747", "#474747"], "mode1")
        self.player_names_frame("Limite de tempo", ["#474747", "#474747", "#474747", "#474747", "#474747"], "mode2")
        self.player_names_frame("Tente não errar", ["#474747", "#474747", "#474747", "#474747", "#474747"], "mode3")

    # Montar o Ranking
    def player_names_frame(self, tab_name, colors, mode):
        aba = self.tabview.tab(tab_name)

        for idx, cor in enumerate(colors):
            player_name = self.master.ranking['Ranking'][mode]['Player'][idx]['Name']
            player_score = self.master.ranking['Ranking'][mode]['Player'][idx]['Score']
            frame = CTkFrame(aba, fg_color=cor, height=50)
            frame.grid(row=idx + 1, column=0, columnspan=4, pady=5, padx=10, sticky="ew")
            frame.grid_propagate(False)

            frame.grid_columnconfigure(0, weight=0)
            frame.grid_columnconfigure(1, weight=1)
            frame.grid_columnconfigure(2, weight=0)
            frame.grid_columnconfigure(3, weight=1)

            CTkLabel (frame, text=player_name).grid(row=0, column=1, padx=15, pady=10, sticky="w")
            CTkLabel (frame, text=player_score).grid(row=0, column=3, padx=15, pady=10, sticky="e")

            # Colocação dos jogadores
            placement_frame = CTkFrame(frame, width=50, height=50, corner_radius=0)
            placement_frame.grid(row=0, column=0, padx=(0, 5), sticky="w")
            placement_frame.grid_propagate(False)

            medal_icon = self.icon_list[idx]
            CTkLabel(placement_frame, 
                    text="", image=medal_icon
                    ).grid(pady=5, padx=3, sticky="nsew")

            # Nome do jogador
            CTkLabel(frame, 
                    text=player_name, font=("Comic Sans MS", 18)
                    ).grid(row=0, column=1, padx=(5, 5), sticky="w")
            # Score
            CTkLabel(frame, 
                    text=player_score, font=("Comic Sans MS", 18)
                    ).grid(row=0, column=3, padx=(5, 10), sticky="e")

# Frame da tela de selecionar modo de jogo
class Gamemode (CTkFrame):
    def __init__(self, master, width = 800, height = 400):
        super().__init__(master, width, height)
        self.configure(fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Abrindo ícones
        pin = CTkImage (light_image=Image.open(os.path.join(master.icons_folder, "pin.png")), size=(70,70))
        clock = CTkImage (light_image=Image.open(os.path.join(master.icons_folder, "time.png")), size=(70,70))
        mistakes = CTkImage (light_image=Image.open(os.path.join(master.icons_folder, "x.png")), size=(60,60))

        # Widgets
        CTkLabel (self, 
                text= "MODO DE JOGO", font=("Trebuchet MS", 50, "bold"), 
                text_color="#44D7FC"
                ).grid(sticky="n", columnspan=2)
        
        CTkLabel (self, 
                text= "Escolha um modo de jogo", font=("Comic Sans MS", 15, "italic"),
                text_color="#7F6CEB"
                ).grid(sticky="n", columnspan=2)

        # Colocando alguns ícones para estética
        CTkLabel (self, text="", image=pin).grid(row=3, pady=10)
        CTkLabel (self, text="", image=clock).grid(row=4, pady=10)
        CTkLabel (self, text="", image=mistakes).grid(row=5, pady=10)

        CTkButton (self,
                text= "Questões fixas", font=("Comic Sans MS", 20), 
                fg_color="#7F6CEB", hover_color="#9D44FC",
                width=200, height=40,
                command= lambda: (self.selected_mode("mode1"))
                ).grid(row=3, column=1, pady=10)
        
        CTkButton (self, 
                text= "Limite de tempo", font=("Comic Sans MS", 20), 
                fg_color="#7F6CEB", hover_color="#9D44FC", 
                width=200, height=40,
                command= lambda: (self.selected_mode("mode2"), master.timer())
                ).grid(row=4, column=1, pady=10)

        CTkButton (self, 
                text= "Tente não errar", font=("Comic Sans MS", 20), 
                fg_color="#7F6CEB", hover_color="#9D44FC",
                width=200, height=40, 
                command= lambda: (self.selected_mode("mode3"))
                ).grid(row=5, column=1, pady=10)
        
        CTkButton (self, 
                text= "Voltar", font=("Comic Sans MS", 20), 
                fg_color="#7F6CEB", hover_color="#9D44FC",
                width=170, height=40, 
                command= lambda: (master.change_win(master.main_page))).grid(row=7, pady=50, sticky="ew")

    # Ativar o modo de jogo
    def selected_mode (self, mode):
        self.master.mode_stats[mode] = True     # Seleciona o modo
        self.master.change_win(self.master.question_screen)     # Muda para a tela de perguntas
        self.master.check_image()       # Checa se a primeira pergunta tem alguma imagem
        if mode == "mode1" or mode == "mode3":      # Se o modo de jogo escolhido não for de limite de tempo
            self.master.question_screen.show_timer.configure (text="")      # Tira a informação que mostra o timer
        self.mode = mode

# Frame da tela de perguntas do quiz
class QuestionScreen (CTkFrame):
    def __init__(self, master, width = 700, height = 700):
        super().__init__(master, width, height)
        self.grid_propagate(False)
        self.configure(fg_color="transparent")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=0)

        hint_icon = CTkImage (light_image=Image.open(os.path.join(master.icons_folder, "hint.png")), size=(22, 22))
        delete_icon = CTkImage (light_image=Image.open(os.path.join(master.icons_folder, "delete.png")), size=(22, 22))

        self.progress_bar = CTkProgressBar(self, width=300, height=25, progress_color="blue")
        self.progress_bar.grid(row=0, column=0, columnspan=2, sticky="ew")
        self.progress_bar.set(0)

        self.qst_txt = CTkLabel (self, 
                            text=master.questions_data[0]['questionText'], 
                            font=("Comic Sans MS", 22), 
                            wraplength=510)
        self.qst_txt.grid(columnspan=2, padx=20, pady=55)

        self.optionspack_pos = [(2, 0, 1, "we"), (3, 0, 1, "we"), (2, 1, 1, "ew"), (3, 1, 1, "ew"), (4, 0, 2, "nsew")]      # Posições onde ficará cada botão de opção
        self.optionsButtons = []        # Lista de botões de opções

        for i in range (5):     # Cria 5 botões para as opções
            opt_txt = master.questions_data[0][f'option{i+1}']
            option = self.create_optButtons (opt_txt, i)
            self.optionsButtons.append(option)

        # Botão de ajuda: mostrar dica
        self.show_hint = CTkButton (self, 
                                    text="", image=hint_icon,
                                    width=35, height=35, 
                                    fg_color="#4463FC", hover_color="#6277de",
                                    command= lambda: master.show_hint())
        self.show_hint.grid(row=5, column=1, padx=20, pady=30, columnspan=2)

        # Botão de ajuda: deletar uma opção
        self.delete_opt = CTkButton (self, 
                                    text="", image=delete_icon,
                                    width=35, height=35, 
                                    fg_color="#4463FC", hover_color="#6277de",
                                    command= lambda: master.delete_opts(self.optionsButtons))
        self.delete_opt.grid(row=5, column=1, padx=115, pady=30, sticky="e")

        # Botão de ajuda: pular uma questão
        self.skip_qst = CTkButton (self, 
                                text=">>", font=("Comic Sans MS", 20),
                                width=35, height=20, 
                                fg_color="#4463FC", hover_color="#6277de",
                                command= lambda: master.next_question (self.qst_txt, self.skip_qst))
        self.skip_qst.grid(row=5, column=1, padx=75, pady=30, sticky="se")

        # Botão de próxima questão após responder
        self.next = CTkButton (self, 
                               text="Próxima Questão", font=("Comic Sans MS", 20), 
                               width=235, 
                               fg_color="#4f8832", hover_color="#376121", 
                               state="disabled",
                               command=lambda: master.next_question(self.qst_txt, self.next))
        self.next.grid(row=5, column=0, padx=75, pady=30, columnspan=2, sticky="nsw")

        # Labels para mostrar as informações de jogo respectivamente: score, quantidade de dicas, combo e o tempo
        self.show_score = CTkLabel (self, text=f"SCORE: {master.score}", font=("Comic Sans MS", 18))
        self.show_score.grid(row=7, column=1, padx=20, columnspan=2)
        
        self.amount_helps = CTkLabel (self, text=f"Ajudas disponíveis: {master.help}", font=("Comic Sans MS", 18))
        self.amount_helps.grid(row=6, column=1, padx=20, columnspan=2)

        self.combo = CTkLabel (self, text=f"Combo: {master.consecutive_hits}", font=("Comic Sans MS", 18))
        self.combo.grid(row=8, column=1, padx=20, columnspan=2)

        self.show_timer = CTkLabel (self, text=f"Tempo restante: 01:30", font=("Comic Sans MS", 18))
        self.show_timer.grid(row=9, column=1, padx=20, columnspan=2)
                                      
    # Apenas para a criação de botões das opções do quiz
    def create_optButtons (self, opt_txt, i):
        row, col, colspan, sticky = self.optionspack_pos[i]
        option = CTkButton (self, 
                            text=opt_txt, font=("Comic Sans MS", 18),
                            fg_color="#7F6CEB", hover_color="#9D44FC",
                            command= lambda: self.master.check_answer(option, self.optionsButtons))
        option.grid(row=row, column=col, columnspan=colspan, padx=75, pady=15, sticky=sticky)

        return option

# Criando um pop-up para mostrar a dica para a questão
class HelpWindow(CTkToplevel):
    def __init__(self, master, hint):
        super().__init__(master)
        self.geometry("300x200")
        self.title("Dica")
        self.transient(master)
        self.grab_set()
        self.grid_propagate(False)
        self.configure(fg_color="#474747")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)

        # Label de dica
        CTkLabel(self, 
                text=hint, font=("Comic Sans MS", 18),
                wraplength=250).grid(row=0, column=0, padx=20, pady=30, sticky="nsew")

        # Botão de Fechar
        CTkButton(self, 
                text="Fechar", font=("Comic Sans MS", 14),
                fg_color="#4463FC", hover_color="#6277de",
                command=self.destroy).grid(row=1, column=0, padx=20, sticky="nsew")
        CTkLabel (self,
                  text="Feche a dica para continuar o Quiz!", font=("Comic Sans MS", 13)).grid()

# Abrir outra janela para mostrar a imagem
class ImageWindow (CTkToplevel):
     def __init__(self, master, image):
        super().__init__(master)
        self.geometry("854x550")
        self.title ("Imagem")
        self.transient(master)
        self.grab_set()

        self.image_label = CTkLabel (self, image=image, text='')
        self.image_label.grid()

        self.close = CTkButton(self, 
                            text="Fechar", font=("Comic Sans MS", 14),
                            fg_color="#4463FC", hover_color="#6277de",
                            command=self.destroy)
        self.close.grid(pady=5)

        CTkLabel (self, 
                  text='Feche a imagem para continuar o Quiz!', font=("Comic Sans MS", 13)).grid()

# Frame da tela de vitória
class AchievementScreen (CTkFrame):
    def __init__(self, master, width = 800, height = 600):
        super().__init__(master, width, height)
        self.grid_propagate(False)
        self.configure(fg_color="transparent")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Widgets
        CTkLabel (self, text="", image=brain_img
                ).grid(columnspan=2)

        # Labels configuráveis para cada ocasião: game over e vitória
        self.txt1 = CTkLabel (self, text=" Y O U  W I N", font=("Trebuchet MS", 55, "bold"), 
                  text_color="#44D7FC")
        self.txt1.grid(row=1, columnspan=2)
        
        self.txt2 = CTkLabel (self, 
                text="Parabéns!! Você concluiu o Quiz!", font=("Comic Sans MS", 20, "italic"),
                text_color="#7F6CEB")
        self.txt2.grid(row=2, columnspan=2)
        
        CTkButton (self, 
                text="Play Again", font=("Comic Sans MS", 30), 
                fg_color="#7F6CEB", hover_color="#9D44FC",
                width=230, 
                image=play_icon, 
                command= lambda: (master.reset_game(), master.change_win(master.gamemode))
                ).grid(row=3,padx=20, pady=20)
        
        CTkButton (self,
                text="Hall da Fama", font=("Comic Sans MS", 30),
                fg_color="#7F6CEB", hover_color="#9D44FC",
                width=230,
                image=rank_icon,
                command=lambda: master.change_win(master.rank_page)
                ).grid(row=3, column=1, padx=20, pady=20)

        self.final_score = CTkLabel (self, 
                                text = f"Score: {master.score}", font= ("Trebuchet MS", 28, "bold"),
                                text_color="#4f8832")
        self.final_score.grid(row=5, columnspan=2)

class RankingPopup(CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.transient(master)
        self.grab_set()
        self.geometry("500x400")
        self.title("Hall da Fama")
        self.columnconfigure(0, weight=1)

        brain_img_resized = CTkImage (light_image=Image.open(os.path.join(master.icons_folder, "brain.png")), size=(150, 120))

        # Widgets
        CTkLabel(self, text="", image=brain_img_resized
                ).grid(row=0, column=0, pady=(10,0))

        CTkLabel(self, text="Parabéns!!", 
            font=("Trebuchet MS", 55, "bold"), text_color="#44D7FC"
        ).grid(row=1, column=0, pady=(0, 1))

        CTkLabel(self, text="Você está qualificado para entrar no Hall da Fama.", 
                font=("Comic Sans MS", 20, "italic"), text_color="#7F6CEB"
        ).grid(row=2, column=0, pady=(1, 3))

        CTkLabel(self,
                text="Coloque seu nome para entrar no Hall da Fama", 
                font=("Comic Sans MS", 13)
        ).grid(row=3, column=0, pady=(3, 1))

        CTkLabel(self,
                text="*Até 10 caracteres", font=("Comic Sans MS", 11)
        ).grid(row=4, column=0)

        self.entry = CTkEntry(self, placeholder_text="Nickname")
        self.entry.grid(row=5, column=0, pady=(3, 3))
        self.entry.bind("<KeyRelease>", self.limit_name)

        CTkButton(self,
                text="Fechar", font=("Comic Sans MS", 14),
                fg_color="#4463FC", hover_color="#6277de",
                command=self.close
        ).grid(row=6, column=0, pady=(3, 3))

        CTkLabel(self, text="FECHE NO BOTÃO ACIMA", 
                font=("Comic Sans MS", 12), text_color="#c42c1f"
        ).grid(row=7, column=0, pady=(0, 10))
        
    # Para o botão de fechar:
    def close (self):
        player_name = self.entry.get()
        self.master.check_name_for_rank (player_name, self.master.gamemode.mode)
        self.destroy ()

    # Limitar o nome do jogador para sempre caber no Hall da Fama sem problemas
    def limit_name(self, event):
        max_chars = 10
        if len(self.entry.get()) > max_chars:
            self.entry.delete(max_chars, END)
        
if __name__ == "__main__":
    app = App()
    app.mainloop()