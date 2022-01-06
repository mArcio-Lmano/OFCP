from os import close
import PySimpleGUI as sg
import player
from PPL_proj import *
import decidir
import hand_strength

#Menu Multijogador
def multijogador():
    sg.theme('Topanga')
    titulo = sg.Text('Multijogador', font = 'Arial 22', text_color='Orange')
    numero_player = sg.Text('Quantos jogadores pretendem entrar?',font = 'Helvetica 16')

    layout_menu_multij = [[titulo],[numero_player],[sg.Radio("2 jogadores","Option",default = False, font = 'Helvetica 16')], [sg.Radio("3 jogadores","Option",default = False, font = 'Helvetica 16')],[sg.Button('Confirmar',font = 'Helvetica 12'), sg.Button('Sair',font = 'Helvetica 12')]]
    menu_multij = sg.Window("Multijogador", layout=layout_menu_multij, size = (500,300))

    while True:
        event, values = menu_multij.read()
        if event == sg.WIN_CLOSED or event == 'Sair':
            break
        elif values[0]:
            print('2 jogadores')
            jogo = Game(2,0)
            jogo.game_loop()
            menu_multij.close()
        elif values[1]:
            print('3 jogadores')
            jogo = Game(3,0)
            jogo.game_loop()
            menu_multij.close()
    


#Menu vs AI
def vsAI():
    sg.theme('Topanga')
    titulo = sg.Text('Desafiar AI', font = 'Arial 22', text_color='Orange')
    numero_ai = sg.Text('Quantos AI em jogo pretende?',font = 'Helvetica 16')
    numero_player = sg.Text('Quantos jogadores pretendem jogar?',font = 'Helvetica 16')

    layout_menu_vsai = [[titulo],[numero_ai],[sg.Radio("1 AI","Option",default = False, font = 'Helvetica 16')], [sg.Radio("2 AI","Option",default = False, font = 'Helvetica 16')], [sg.Radio("3 AI", "Option1",default = False, font = 'Helvetica 16')], [numero_player],[sg.Radio("1 Player","Option1",default = False, font = 'Helvetica 16')],[sg.Radio("2 Players","Option1",default = False, font = 'Helvetica 16')],[sg.Button('Confirmar',font = 'Helvetica 12'), sg.Button('Sair',font = 'Helvetica 12')]]
    menu_vsai = sg.Window("Desafiar AI", layout=layout_menu_vsai, size = (500,300))

    while True:
        event, values = menu_vsai.read()
        if event == sg.WIN_CLOSED or event == 'Sair':
            break
        elif values[1] and values[4]:
            print('escolha um máximo de 3 participantes (AI + Players)')
        elif values[2] and values[0]:
            print('escolha um máximo de 3 participantes (AI + Players)')
        elif values[2] and values[1]:
            print('escolha um máximo de 3 participantes (AI + Players)')
        elif values[0] and values[3]:
            print('1 AI e 1 jogador')
            jogo = Game(1,1)
            jogo.game_loop()
            menu_vsai.close()
        elif values[0] and values[4]:
            print('1 AI e 2 jogadores')
            jogo = Game(2,1)
            jogo.game_loop()
            menu_vsai.close()
        elif values[1] and values[3]:
            print('2 AI e 1 jogador')
            jogo = Game(1,2)
            jogo.game_loop()
            menu_vsai.close()
        elif values[2]:
            print('3 AI')
            jogo = Game(0,3)
            jogo.game_loop()
            menu_vsai.close()

#Criação de menu principal
def menu_principal():
    sg.theme('Topanga')
    titulo = sg.Text('Open Face Chinese Poker', font = 'Arial 22',text_color='Orange')
    opcoes_de_jogo = sg.Text('Deseja jogar Multijogador local ou Desafiar o AI?',font = 'Helvetica 16')

    layout_menu_principal = [[titulo],[opcoes_de_jogo], [sg.Radio("Multijogador Local:","Option",default = False,font = 'Helvetica 16')], [sg.Radio("Desafiar AI:", "Option",default = False,font = 'Helvetica 16')], [sg.Button('Confirmar',font = 'Helvetica 12'), sg.Button('Sair',font = 'Helvetica 12')]]
    menu_principal = sg.Window("Open Face Chinese Poker", layout_menu_principal, size = (500,300))


#Decisões de menu

    while True:
        event, values = menu_principal.read()
        if event == sg.WIN_CLOSED or event == 'Sair':
            break
        elif values[0]:
            multijogador()
            menu_principal.close()
        elif values[1]:
            vsAI()
            menu_principal.close()

menu_principal()