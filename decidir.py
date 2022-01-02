from random import sample, randrange
import itertools
import time
from hand_strength import hand_strength
from collections import Counter
import numpy as np

"""
Corrigirt o comentario da class, pois a forma de calcualr a mao mais forte agora e atrtaves da emedia e nao fazendo aquelas merda toda comiida que eu tionha antes
"""


class Sim_Game:
    """
    Class responsavel por simular as maos, uma dada pontuacaop e atribuida a cada uma das jogadas
    tendo em conta a forca das jogadas bem como a sua probabilidade, a 'AI' dispoem as cartas que 
    tem na mao de todas as maneiras possiveis e recolhe do baralho o resto da cartas para completar 
    o seu jogo, calulando assim o pontuacao final do jogo, a forma que as cartas que a AI usa
    para completar o seu jogo sao dispostas na mesa de forma completamente aleatoria

    game -> Classe de jogo (onde esta defenido o baralho e os jogadore)
    player -> Classe do jogador que a 'AI' vai controlar 
    cards_to_place -> cartas que a 'AI' tem na mao
    order_to_place -> forma como as cartas que a 'AI' tem na mao sao dispostas na mesa
    card_off -> para as rondas onde a 'AI' recebe 3 cartas uma delas tem que ser discartada (card_off)
    """
    def __init__(self, game, player, cards_to_place, order_to_place, card_off):
        """
        Inicializacao da class 
            -Dispoe as cartas na mesa usando o tuplo order_to_place
            -Inicializacao de variavies
        """
        self.hand = {} 
        self.hand["top"] = list(player.top[:])
        self.hand["mid"] = list(player.mid[:])
        self.hand["bot"] = list(player.bot[:])
        self.order_to_place = order_to_place
        self.card_off = card_off
        for i in range(len(cards_to_place)):
            if order_to_place[i] == 0:
                self.hand["top"] += [cards_to_place[i]]
            elif order_to_place[i] == 1:
                self.hand["mid"] += [cards_to_place[i]]
            else: 
                self.hand["bot"] += [cards_to_place[i]]
        self.evs_ar = np.array([])
        self.times_run = 0
        self.deck = game.baralho[:]

    def run_hand(self):
        """
        Uma simulacao de Monte Carlo:
            -Distribui cartas de forma aleatoria
            -Calcula os pontos desse jogo, atribui 0 se a 'AI' cometer falta
        """
        run_hand = {}
        run_hand["top"] = self.hand["top"][:]
        run_hand["mid"] = self.hand["mid"][:]
        run_hand["bot"] = self.hand["bot"][:]
        
        top_len = len(run_hand["top"])
        mid_len = len(run_hand["mid"])
        bot_len = len(run_hand["bot"])
        
        card_samp = sample(list(self.deck), 13-top_len-mid_len-bot_len)

        if(top_len < 3):
            run_hand["top"] += card_samp[:3-top_len]
        if(mid_len < 5):
            run_hand["mid"] += card_samp[3-top_len:3-top_len+5-mid_len]
        if(bot_len < 5):    
            run_hand["bot"] += card_samp[3-top_len+5-mid_len:3-top_len+5-mid_len+5-bot_len]
        
        #self.times = 1

        top_str = hand_strength(run_hand["top"]) 
        mid_str = hand_strength(run_hand["mid"])
        bot_str = hand_strength(run_hand["bot"])

        if top_str > mid_str or top_str > bot_str or mid_str > bot_str:
            self.ev = -1 
        else:
            self.ev = hand_strength(run_hand["top"]) + hand_strength(run_hand["mid"]) + hand_strength(run_hand["bot"])
        
        self.evs_ar = np.append(self.evs_ar, self.ev)
        self.times_run += 1
        
        return "One game simulation"

    #def incre_times(self):
    #    """
    #    Incrementa a 'probabilidade'
    #    """
    #    self.times += 1
    #    return 

    def get_ev_ave(self):
        """
        Calcula a 'forca' media de cada mao
        """
        return sum(self.evs_ar)/self.times_run

def place_cards(game, player, cards_to_place, thread_scale = 20,  monte_carlo_stats=True):
    
    possible_hands = []
    possible_placements = []

    if len(player.top) < 3:
        possible_placements.append(0)
    if len(player.mid) < 5:
        possible_placements.append(1)
    if len(player.bot) < 5:
        possible_placements.append(2)
    
    for p in itertools.product(possible_placements, repeat=len(cards_to_place)):
        
        iter_off = dict(Counter(p))
        if len(cards_to_place) == 3:
            iter_off = dict(Counter(p[1:]))
        
        try:
            iter_off0 = iter_off[0]
        except:
            iter_off0 = 0
        try:
            iter_off1 = iter_off[1] 
        except:
            iter_off1 = 0
        try:
            iter_off2 = iter_off[2] 
        except:
            iter_off2 = 0

        if len(player.top) + iter_off0 > 3 or len(player.mid) + iter_off1 > 5 or len(player.bot) + iter_off2 > 5:
            continue
        else:
            card_off = None
            cards_to_place_on_sim = cards_to_place[:]
            p_on_sim = p[:]
            if len(cards_to_place) == 3:
                card_off = cards_to_place[p[0]]
                cards_to_place_on_sim = cards_to_place[1:]
                p_on_sim = p[1:]
            possible_hands.append(Sim_Game(game, player, cards_to_place_on_sim, p_on_sim, card_off))

    # Tempo para as simulacoes (defenido por um thread scale (dificuldade), mais tempo => jogadas mais "pensadas"
    start = time.time()
    fivecardtime = thread_scale + 5
    twocardtime = thread_scale//2 + 3
    max_time = fivecardtime if len(cards_to_place) == 5 else twocardtime
    
    num_sims = 0
    
    while(time.time() - start < max_time):
        for hand in possible_hands:
            hand.run_hand()
        num_sims += 1

    #########################################
    ## EM FASE DE TESTE, TEM QUE S#ER MELHORADO APENAS INCREMENTA UMA VEZ 
    ## Tentar fazer com que a AI tenha em consideracao as maos mais provaveis e nao so as mais fortes
    #hand_handstr_list = [] # faze de teste
    #for pos_hand in possible_hands:
    #    hand_handstr_list += [(pos_hand,pos_hand.hand_value)]
    #    
    #hand_str_list = [x[1] for x in hand_handstr_list]
    #count_game_poss = dict(Counter(hand_str_list))
    #for pos_hand in possible_hands:
    #    for _ in range(count_game_poss[pos_hand.hand_value]):
    #        pos_hand.incre_times()
    ######################################### 
    
    best_ev = -2
    for pos_hand in possible_hands:
        if pos_hand.get_ev_ave() > best_ev:
            best_ev = pos_hand.get_ev_ave()
            best_order_to_place = pos_hand.order_to_place
            card_off = pos_hand.card_off
    
    if monte_carlo_stats:
        explanation = f"After {num_sims} Monte Carlo simulations the best and more probable move was worth {best_ev}, on average, of {len(possible_hands)} possible hands"
        print(explanation)
    return best_order_to_place, card_off
