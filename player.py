import numpy as np

class Player:
    def __init__(self, name):
        self.points = 0
        self.hand = np.array([]) # Todas as cartas que o jogador possui
        self.lixo = np.array([]) # Cartas descartadas pelo jogador
        self.top = np.array([]) # 3 cartas
        self.mid = np.array([]) # 5 cartas
        self.bot = np.array([]) # 5 cartas
        self.field = self.refresh_field() # Jogo do player

        self.name = name # nome do jodagor
        self.n_cards_table = 0 # nº de cartas na mesa
   
    def give_card(self, card):
        self.hand = np.append(self.hand, card)
        #self.n_cards_table += 1

    def refresh_field(self):
        top = self.top
        mid = self.mid
        bot = self.bot

        while len(top) < 5:
            top = np.append(top, None)
        while len(mid) < 5:
            mid = np.append(mid, None)
        while len(bot) < 5:
            bot = np.append(bot, None) 
        
        return np.vstack((top, mid, bot))

    def add_2_table(self, pos):
        r = f"Carta não colocada, verificar se {pos} é uma posição válida ou se nenhuma das posições já atingiu o seu limite de cartas"

        if pos == "top" and len(self.top) < 3:
            self.top = np.append(self.top, self.hand[self.n_cards_table])
            self.field = self.refresh_field()
            r = "Carta colocada no topo"
            self.n_cards_table += 1

        elif pos == "mid" and len(self.mid) < 5:
            self.mid = np.append(self.mid, self.hand[self.n_cards_table])
            self.field = self.refresh_field()
            r = "Carta colocada no meio"
            self.n_cards_table += 1

        elif pos == "bot" and len(self.bot) < 5:
            self.bot = np.append(self.bot, self.hand[self.n_cards_table])
            self.field = self.refresh_field()
            r = "Carta colocada no fundo"
            self.n_cards_table += 1

        else:
            print(r)
            pos = input(f"Introduza outra posição\n>>> ")
            self.add_2_table(pos)

        return r

    def add_lixo(self, card):
        
        self.hand = np.delete(self.hand, np.argwhere(self.hand == card))
        self.lixo = np.append(self.lixo, card) 
        
        return "Carta Descartado"

    def update_points(self, pontos):
        self.points += pontos

    def reset(self):
        self.hand = np.array([]) # Todas as cartas que o jogador possui
        self.lixo = np.array([]) # Cartas descartadas pelo jogador
        self.top = np.array([]) # 3 cartas
        self.mid = np.array([]) # 5 cartas
        self.bot = np.array([]) # 5 cartas
        self.field = self.refresh_field() # Jogo do player
        self.n_cards_table = 0 # nº de cartas na mesa
