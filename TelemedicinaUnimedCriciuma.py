########################## Unimed Criciúma ##########################
#-------------------------------------------------------------------#
##### Aplicação para autoatendimento dos totens de Telemedicina #####
#-------------------------------------------------------------------#
# Autor.: Marcos Rocha                                              #
# Data..: 19/12/2022                                                #    
# Versão: 1.1                                                       #
#-------------------------------------------------------------------#
import PySimpleGUI as sg
import textwrap
import threading
from os import system
import time
import psutil as ps
import webbrowser as wb
#-------------------------------------------------------------------
#URL_CHAT = 'https://unimedcriciuma.syngoo-talk.app/webchat/v2/?cid=63247b5ebae605001985770a&host=https://unimedcriciuma.syngoo-talk.app'
URL_CHAT = 'https://unimedcriciuma.syngoo-talk.app/webchat/v2/?cid=63247b5ebae605001985770a'
START_CHROME = "powershell -WindowStyle Hidden Start-Process chrome.exe -ArgumentList @( '-incognito', '" + URL_CHAT + "' )"
WIN_MARGIN = 60
#-------------------------------------------------------------------
FUNDO_VERDE = "#033c1e"
FUNDO_CINZA = "#363636"
TEXT_COLOR = "#ffffff"
TEMPO_CONFIRMAR_FINALIZAR = 60000 # 1 minuto
TEMPO_TOTAL_ATENDIMENTO = 1800 * 1000 #30 minutos
ICONE_INICIANDO = b'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAAAA3NCSVQICAjb4U/gAAAACXBIWXMAAAEKAAABCgEWpLzLAAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAAAHJQTFRF////ZsxmbbZJYL9gZrtVar9VZsJcbMRYaMZVasFYaL9XbMFbasRZaMFZacRXa8NYasFaasJaasFZasJaasNZasNYasJYasJZasJZasJZasJZasJZasJYasJZasJZasJZasJZasJaasJZasJZasJZasJZ2IAizQAAACV0Uk5TAAUHCA8YGRobHSwtPEJJUVtghJeYrbDByNjZ2tvj6vLz9fb3/CyrN0oAAADnSURBVDjLjZPbWoUgFIQnbNPBIgNKiwwo5v1fsQvMvUXI5oqPf4DFOgCrhLKjC8GNVgnsJY3nKm9kgTsduVHU3SU/TdxpOp15P7OiuV/PVzk5L3d0ExuachyaTWkAkLFtiBKAqZHPh/yuAYSv8R7XE0l6AVXnwBNJUsE2+GMOzWL8k3OEW7a/q5wOIS9e7t5qnGExvF5Bvlc4w/LEM4Abt+d0S5BpAHD7seMcf7+ZHfclp10TlYZc2y2nOqc6OwruxUWx0rDjNJtyp6HkUW4bJn0VWdf/a7nDpj1u++PBOR694+Ftj/8PKNdnDLn/V8YAAAAASUVORK5CYII='
#-------------------------------------------------------------------
def display_notification(message):
    title = 'Telemedicina Unimed Criciúma'
    alpha = 0.9
    message = textwrap.fill(message, 50)
    win_msg_lines = message.count("\n") + 1
    screen_res_x, screen_res_y = sg.Window.get_screen_size()
    win_margin = WIN_MARGIN  # distance from screen edges
    win_width, win_height = 370, 66 + (14.8 * win_msg_lines)
    win_location = (199, screen_res_y/2 - win_height - win_margin)

    layout = [[sg.Graph(canvas_size=(win_width, win_height), graph_bottom_left=(0, win_height), graph_top_right=(win_width, 0), key="-GRAPH-", background_color=FUNDO_CINZA, enable_events=True)]]

    window = sg.Window(title, layout, background_color=FUNDO_CINZA, no_titlebar=True, location=win_location, keep_on_top=True, alpha_channel=0, margins=(0, 0), element_padding=(0, 0), finalize=True)
    window["-GRAPH-"].draw_rectangle((win_width, win_height), (-win_width, -win_height), fill_color=FUNDO_CINZA, line_color=FUNDO_CINZA)
    window["-GRAPH-"].draw_text(title, location=(64, 20), color=TEXT_COLOR, font=("Arial", 12, "bold"), text_location=sg.TEXT_LOCATION_TOP_LEFT)
    window["-GRAPH-"].draw_text(message, location=(64, 44), color=TEXT_COLOR, font=("Arial", 9), text_location=sg.TEXT_LOCATION_TOP_LEFT)
    window["-GRAPH-"].draw_image(data=ICONE_INICIANDO, location=(20, 20))
    
    for i in range(1,int(alpha*100)):               # fade in
        window.set_alpha(i/100)
        event, values = window.read(timeout=10)
        if event != sg.TIMEOUT_KEY:
            window.set_alpha(1)
            break
    event, values = window(timeout=3000)
    if event == sg.TIMEOUT_KEY:
        for i in range(int(alpha*100),1,-1):       # fade out
            window.set_alpha(i/100)
            event, values = window.read(timeout=10)
            if event != sg.TIMEOUT_KEY:
                break
    window.close()
#-------------------------------------------------------------------
class abreNavegador(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        
    def close(self):
        self.close

    def run(self):
        #navegador = wb.open(URL_CHAT,1,True)
        navegador = system(START_CHROME)
#-------------------------------------------------------------------
def fecha_navegador():
    lista = []
    for proc in ps.process_iter():
        info = proc.as_dict(attrs=['pid', 'name','status'])
        lista.append(info)

    #Lista reversa
    for reverso in reversed(lista):
        if reverso['name'] == 'chrome.exe':
            for processo in ps.process_iter():
                info2 = processo.as_dict(attrs=['pid', 'name','status'])
                
                if reverso['pid'] == info2['pid']:   
                    processo.kill()
                    break
#-------------------------------------------------------------------
def encerrar_atendimento():
    message = textwrap.fill('', 50)
    win_msg_lines = message.count("\n") + 1
    win_margin = WIN_MARGIN
    win_width, win_height = 364, 66 + (14.8 * win_msg_lines)
    win_location = (win_width - win_margin, win_height - win_margin)
    largura, altura = sg.Window.get_screen_size()

    layout =[  
                [sg.Graph(canvas_size=(largura, 12), graph_bottom_left=(0, win_height), graph_top_right=(win_width, 0), key="-GRAPH-", background_color=FUNDO_VERDE, enable_events=True)],
                [sg.Button('ENCERRAR', image_data=imagemBotaoVermelho, font='Helvetica 30 bold italic', button_color=('white', FUNDO_VERDE),border_width=0, )]
            ]

    notificacao = sg.Window('', layout, background_color=FUNDO_VERDE, no_titlebar=True, location=(0,0), keep_on_top=True, alpha_channel=0, margins=(0, 0), element_padding=(0, 0), finalize=True)
    notificacao["-GRAPH-"].draw_rectangle((0, 0), (-win_width, -win_height), fill_color=FUNDO_VERDE, line_color=FUNDO_VERDE)
    notificacao.set_alpha(100)
    encerrarAtendimento = False

    #Loop do tempo de atendimento
    while True:
        event = notificacao.read(timeout=TEMPO_TOTAL_ATENDIMENTO) 
        if event[0] == 'ENCERRAR':
            encerrarAtendimento = True                                        
            notificacao.close()            
            break

        if event[0] == sg.TIMEOUT_KEY:  
            encerrarAtendimento = False                
            notificacao.close()
            break

    return encerrarAtendimento
# -------------------------------------------------------------------
def main():
    sg.theme('Dark Green 5')
    layoutPrincipal = [     
                            [sg.Image(filename="C:/Totem/telemedicinaTopoPequeno.png")],
                            [sg.Text(' ')], 
                            [sg.Text('FAÇA SUA CONSULTA AQUI!', font='Tahoma 25')],
                            [sg.Text(' ')], 
                            [sg.Text(' ')],                                      
                            [sg.Text(' ')], 
                            [sg.Text(' ')],                                      
                            [sg.Button('Iniciar Atendimento', image_data=imagemBotaoVerde, font='Helvetica 22 bold italic', button_color=('white', sg.theme_background_color()),border_width=0, )],
                            [sg.Text(' ')],   
                            [sg.Text(' ')],   
                            [sg.Text(' ')], 
                            [sg.Text(' ')], 
                            [sg.Text(' ')],                                                        
                            [sg.Text(' ')],   
                            [sg.Text(' ')],   
                            [sg.Text(' ')],                            
                            [sg.Image(filename="C:/Totem/logo_transparente.png")],
                        ]

    layoutPrincipal = layoutPrincipal = [[sg.Sizer(0,1366), sg.Column([[sg.Sizer(768,0)]] + layoutPrincipal, element_justification='c', pad=(0,0))]]
    janelaPrincipal = sg.Window('Telemedicina Unimed Criciúma', layoutPrincipal, disable_close=True, disable_minimize=True, no_titlebar=True ,finalize=True)
    janelaPrincipal.maximize()

    #Loop principal
    while True:
        event, values = janelaPrincipal.read()
        
        if event == sg.WIN_CLOSED or event == 'Exit':
            break

        if event == 'Iniciar Atendimento':            
            background = abreNavegador()
            background.start()
            display_notification('Iniciando Atendimento...')
            continuar = True

            #Loop do atendimento iniciado
            while continuar:
                
                if not encerrar_atendimento():
                    
                    title = "Telemedicina Unimed Criciúma"
                    message = textwrap.fill("Telemedicina Unimed Criciúma", 100)
                    win_msg_lines = message.count("\n") 
                    screen_res_x, screen_res_y = sg.Window.get_screen_size()
                    win_width, win_height = 520, 66 + (20 * win_msg_lines)
                    win_location = (62, screen_res_y /2.5)

                    layout = [  
                                [sg.Graph(canvas_size=(win_width, win_height), graph_bottom_left=(0, win_height), graph_top_right=(win_width, 0), key="-GRAPH-", background_color=FUNDO_VERDE, enable_events=True)],
                                [sg.Graph(canvas_size=(win_width, win_height + 50), graph_bottom_left=(0, win_height), graph_top_right=(win_width, 0), key="-GRAPH2-", background_color=FUNDO_VERDE, enable_events=True)],
                                [sg.Button('Continuar', image_data=imagemBotaoVerde, font='Helvetica 30 bold italic', button_color=('white', FUNDO_VERDE),border_width=0)] + 
                                [sg.Button('Finalizar', image_data=imagemBotaoVermelho, font='Helvetica 30 bold italic', button_color=('white', FUNDO_VERDE),border_width=0, )]
                            ]

                    notificacao = sg.Window(title, layout, background_color=FUNDO_VERDE, no_titlebar=True, location=win_location, keep_on_top=True, alpha_channel=0, margins=(0, 0), element_padding=(0, 0), finalize=True)
                    notificacao["-GRAPH-"].draw_rectangle((win_width, win_height), (-win_width, -win_height), fill_color=FUNDO_VERDE, line_color=FUNDO_VERDE)
                    notificacao["-GRAPH-"].draw_text(title, location=(320, 20), color=TEXT_COLOR, font=("Helvetica 12"), text_location=sg.TEXT_LOCATION_CENTER)
                    notificacao["-GRAPH2-"].draw_text('O atendimento atingiu o tempo máximo de 30 minutos.\n\nPor gentileza, escolha uma das opções abaixo', location=(264, 20), color=TEXT_COLOR, font=("Arial", 15, "bold"), text_location=sg.TEXT_LOCATION_CENTER)
                    notificacao.set_alpha(100)

                    event = notificacao.read(timeout=TEMPO_CONFIRMAR_FINALIZAR)
                    
                    if continuar == False:
                        break
                        
                    if event[0] == 'Finalizar':                                        
                        continuar = False                    
                        display_notification('Finalizando Atendimento...')
                        notificacao.close()
                        fecha_navegador()

                    if event[0] == 'Continuar':
                        notificacao.set_alpha(0)
                        continue

                    if event[0] == sg.TIMEOUT_KEY:                    
                        continuar = False
                        display_notification('Encerrando Atendimento...')
                        notificacao.close()
                        fecha_navegador()
                        
                else:
                    display_notification('Encerrando Atendimento...')
                    continuar = False
                    fecha_navegador()
                    
# -------------------------------------------------------------------
if __name__ == '__main__':    
    #Botões Grandes
    imagemBotaoVerde = b'iVBORw0KGgoAAAANSUhEUgAAAUYAAAA8CAYAAAAaGRPjAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAARXSURBVHhe7d3PcpNVGMfx5+RtFZq2SZsWqoMMCkibC3AcWbtgRsfJ6FKvobfgVldwDWxFFjqyYO/0BsSKoijDINL0b1oMJe/x/EvInzNeQJ/vh/llJu8btr95zjlvGiNJo7V6w5TyuVQqi+kSAKhgRXZEypvt25vr/n0oxuXPmnbu/bqcXpkXYwp3cdCXAHCi2fCvlOdP9uRgY1eefXPPmEareb12tb5eXXSDYqcQ6fmPUowAtHDzoqs+me1J59m27G9sf1VU15bv1N9bEWm7OyWFCEAHYyr+Nca6HBspzkzJ0U+7TX8nFCZTIgBNrC1H07OxLCuVxVCMYU/RlyMhhGjJhNSDTjGztvxldW1BpMPECECP3CGzqVrp/LwrcSk9UaWEEHKyY20m7o6XihEAtJksyxg3OS61mvZM64KYp1PhAgCoYGIJjjjbk6ffPkx7jKs1MR2GRwCa+D3G0dhqKYebgz1GAFDGuokxFydNjHVOpQFg1rqJcW9oYvRFSQghWvI/QjH6Y+rsfySEEE1J2GMEoFOmGMOQ6MQ9xis1MQfsMQJQbtbK0S97sRhnrsxTjAB0MZnOm4vFyFIagE7Dj+ik9L8UmIqRaREA+sJXApc+Pi/mMeUIQJHMUtq+WcrWd3/19xhrIvsUIwA9so03L3J0f7DHGNfVAKBFZotxgMMXABiI7Rj3GD96S+QRS2kAiuQq75yVre8fxT3G0+/WRPbSDQDQwA+H43FV+Pz+fjp8uTxPMQLQJfeAdypG9hgB6JQ7ffFx4lL68hwTIwD4ifHXgzgxhpIkhBDlSQNjPJVeuHZOKn+mKwCggM1sMdrzIjt3Hqel9CW3lN6lGAHo4X9w33fjcGzdyL+/cfgCQKmRH9pPcS/hXpoY593EGN4DgF5hYjyIxXjKLaXNDktpAIrknmMcKcaLFCMAbXznjcYuxGJkjxGATpO9GOOk5xjdu/GbhBCiLv4lHb74pbTshPcAoJZfSncfdFIxvuOLMTYlAGhgcocvqRjDN19qH74h8uBlugMAGmSK8WIhe3ef9A9f/LTYf/abEEI0ZLCxOJbhnzbI3SeEkBMbV47jSdLhy6xIu0yXAECB3B7jopHu7x2eYwSgVP+70cNJ0nOM/oUQQnSn341DE+PYJwghRF2isMf42tt+j7GXLgHAyZd9jrFRGdtjzJUnIYSc0NjSTsbfc1hKE0LIIFFaSld5XAeAetYtpV/8ccjjOgAwjmIEgDFxKX2hKoZTaQDa+aX0w8NXe4ymXUr4g7UAoFB4fKdRhGKMS+lK5nkeANAmdaFZ+mS1Xb22smg2X4o5DtcAQB077bI2JYc//L1tGq3m9VNXa+vTL9zVf3oix245zZM7ALTw6+ZpNymeLaRb6crxxsHXYW5c+rRpX/+gLsXMtFR67lM99hoBKFEYKYtSekfH0v1xV7Zu3Xv1ZcFGa/WGq84v3IWFdAkAVHCj4I5bKt9s395cFxH5DymOXcehSf6GAAAAAElFTkSuQmCC'    
    imagemBotaoVermelho = b'iVBORw0KGgoAAAANSUhEUgAAAUYAAAA8CAYAAAAaGRPjAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAQ8SURBVHhe7d3Lax1lGMfx35xzGi+RoAUvFAqmiTlJpYgiNYtYmp1Lt4J27WURLwW1td4qYlHU4HVtF+JfIK4qWtGKilAwXppUEaubWhtKK21Pxud9Z96cnJkB9+f5fg5P2sxk/eN53vedOZlKBzS22FPv/kz55vISADiRnWmpffigVhfib+HH8xrL79MWjWukuAAAzqzooj7UKcvD1Szbr9E392jrwg3q6S/7XLZ/FQsAPGirY3WTff5QSx/pz0PtXdr08b263tLyN61ZLEp58bcAMMSy2ACGvOvF7DuvC5q0LDyi09tb4Q+KKKRLBOBHbl3ixrpkP8NSYthnsVH66vwZTehnLRV/DQAOZBaGVV37vKgTWg/Gn/RjeQsAhp91huX/+qY0o5e0XATjszZZL1nPCAB+1JcPu5qOwRjXGAHAnzBKD1YrrjJaNxk6xv02Si/ZMA0AXoQYrJqxYTqsMa7vSlMURXmqcEinXuGOGKUB+FQNylRBHKX32Sj9A5svAJzbbqP0y2lXOgTjcYIRgCP1U4yVYHw6BiMHvAH40XTAe0cZjKwxAnApj1st1SrEjvGp2DHy5AsA33ZoWq+kUToE4/f6pbwFAMOvbR1iVQpGRmkALvViNA5WQjACQMX6KP0djwQCcKTpa1xuV3dwjfFbjusAcCRrGJjvKIMx3snXN6kBwIdca7VKWGMEgFJqEuMovVfbbJTmHCMAPzoNq4y32Sj9mlaKYHzSgvEYmy8AnLvLgvFQCsYnLBi/4SUSABxp+s6XFIysMQJwKXxZarXCN+sHsWN8XOPWMZ4oLwGAT3dqUq/rZBGMj1kwfk0wAnBupwXjG4PByOYLAE/q72OsBeMxNl8AONK0+bJT3RiMbL4AcKlp8yVZ7xi/4oA3AOdmNd0fpR+1YPyCF9UCcKSj+otqUzAySgNw6bJGapVWHQlGAE6FjrFahThKL8RRmuM6AHyb1ZTe1q/9YDzKi2oBODenGS2mzZdHdLO+pGME4EjTOcZaMB61XwDAj/6aYjKnSb2TRukiGHlWGoAn9UcC5zQ+GIyfM0oDcO5udQeD8TOelQbgSNMaYwpGzjECcOl/n5V+2DrGT+kYATi3W1N6N43SRTAul7cAwKfdmugH40MxGFfKWwAw/JrWGGvBeIS36wBwbl636L3BYKRjBODbvLb1g/HBGIwc8Abg27wm9b4FI8d1AKCCYASAig3BGA43UhRFea7ChjXG5YGT3wDgSTi+M6+J/hpjJ14GAN9SFmb7NHp6r8Y3f2IpeUH/lpcBwJerdKXusen5VZ38u71LI1tmNDY7qlGd1UVrJnOtxRPh1dmboihq+KpjnyssFG/VjdYc5jqus2+FO3pO1+R7tFXX2mQdovFSDEYAGH6bLBxHrP6xlvAD/a4XdC6LwRgc0NjimnoPSPl15SUAcCI701L78EGtLkjSf9vJqwmcV0HYAAAAAElFTkSuQmCC'
    main()