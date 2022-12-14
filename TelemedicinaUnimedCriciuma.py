########################## Unimed Criciúma ##########################
#-------------------------------------------------------------------#
##### Aplicação para autoatendimento dos totens de Telemedicina #####
#-------------------------------------------------------------------#
# Autor.: Marcos Rocha                                              #
# Data..: 14/12/2022                                                #    
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
URL_CHAT = 'https://unimedcriciuma.syngoo-talk.app/webchat/v2/?cid=63247b5ebae605001985770a&host=https://unimedcriciuma.syngoo-talk.app'
WIN_MARGIN = 60
#-------------------------------------------------------------------
WIN_COLOR = "#033c1e"
TEXT_COLOR = "#ffffff"
TEMPO_CONFIRMAR_FINALIZAR = 60000 # 1 minuto
TEMPO_TOTAL_ATENDIMENTO = 1800 * 1000 #30 minutos
#-------------------------------------------------------------------
class abreNavegador(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        
    def close(self):
        self.close

    def run(self):
        navegador = wb.open_new(URL_CHAT)
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

    layout =[  
                [sg.Graph(canvas_size=(259, 1), graph_bottom_left=(0, win_height), graph_top_right=(win_width, 0), key="-GRAPH-", background_color=WIN_COLOR, enable_events=True)],
                [sg.Button('ENCERRAR', image_data=imagemBotaoVermelho, font='Helvetica 20 bold italic', button_color=('white', WIN_COLOR),border_width=0, )]
            ]

    notificacao = sg.Window('', layout, background_color=WIN_COLOR, no_titlebar=True, location=win_location, keep_on_top=True, alpha_channel=0, margins=(0, 0), element_padding=(0, 0), finalize=True)
    notificacao["-GRAPH-"].draw_rectangle((win_width, win_height), (-win_width, -win_height), fill_color=WIN_COLOR, line_color=WIN_COLOR)
    
    time.sleep(1)
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
                            [sg.Button('Iniciar Atendimento', image_data=imagemBotaoVerde, font='Helvetica 18 bold italic', button_color=('white', sg.theme_background_color()),border_width=0, )],
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
            
            continuar = True
            #Loop do atendimento iniciado
            while continuar:
                
                if not encerrar_atendimento():
                    
                    title = "Telemedicina Unimed Criciúma"
                    message = textwrap.fill("Telemedicina Unimed Criciúma", 100)
                    win_msg_lines = message.count("\n") 
                    screen_res_x, screen_res_y = sg.Window.get_screen_size()
                    win_width, win_height = 520, 66 + (20 * win_msg_lines)
                    win_location = (screen_res_x /2.5 - win_height, screen_res_y /2.5)

                    layout = [  
                                [sg.Graph(canvas_size=(win_width, win_height), graph_bottom_left=(0, win_height), graph_top_right=(win_width, 0), key="-GRAPH-", background_color=WIN_COLOR, enable_events=True)],
                                [sg.Graph(canvas_size=(win_width, win_height + 50), graph_bottom_left=(0, win_height), graph_top_right=(win_width, 0), key="-GRAPH2-", background_color=WIN_COLOR, enable_events=True)],
                                [sg.Button('Continuar', image_data=imagemBotaoVerde, font='Helvetica 20 bold italic', button_color=('white', WIN_COLOR),border_width=0)] + 
                                [sg.Button('Finalizar', image_data=imagemBotaoVermelho, font='Helvetica 20 bold italic', button_color=('white', WIN_COLOR),border_width=0, )]
                            ]

                    notificacao = sg.Window(title, layout, background_color=WIN_COLOR, no_titlebar=True, location=win_location, keep_on_top=True, alpha_channel=0, margins=(0, 0), element_padding=(0, 0), finalize=True)
                    notificacao["-GRAPH-"].draw_rectangle((win_width, win_height), (-win_width, -win_height), fill_color=WIN_COLOR, line_color=WIN_COLOR)
                    notificacao["-GRAPH-"].draw_text(title, location=(264, 20), color=TEXT_COLOR, font=("Helvetica 12"), text_location=sg.TEXT_LOCATION_CENTER)
                    notificacao["-GRAPH2-"].draw_text('O atendimento atingiu o tempo máximo de 30 minutos.\n\nPor gentileza, escolha uma das opções abaixo', location=(264, 20), color=TEXT_COLOR, font=("Arial", 15, "bold"), text_location=sg.TEXT_LOCATION_CENTER)
                    notificacao.set_alpha(100)

                    event = notificacao.read(timeout=TEMPO_CONFIRMAR_FINALIZAR)
                    
                    if continuar == False:
                        break
                        
                    if event[0] == 'Finalizar':                                        
                        notificacao.close()
                        continuar = False                    
                        fecha_navegador()
                
                    if event[0] == 'Continuar':
                        notificacao.set_alpha(0)
                        continue

                    if event[0] == sg.TIMEOUT_KEY:                    
                        continuar = False
                        notificacao.close()
                        fecha_navegador()
                else:
                    continuar = False
                    fecha_navegador()
# -------------------------------------------------------------------
if __name__ == '__main__':    
    imagemBotaoVerde = b'iVBORw0KGgoAAAANSUhEUgAAAQMAAAAwCAYAAAAVSB98AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAO+SURBVHhe7d3dclNVGAbgd+00Qmn+mrRN/AFbIhByBY4cqeOMzOhggEO9ht6Cp3oE18ApfzMy6AyDnjm9AqZWSxFU0rRJmyYthDR7+e21VqrDcAX53qfzDmXvfbpf1rdWGwyCUqN23cT4GlFUDJeIaIJZYAeIb7TvrC4nf3dlMH+1brMfFjBdycGYlFw86ggimkDWfcV48byL3soutm4+MqbUqF/LXygszxRlQdBPAaPkUZYB0WSTdYG87siM0N/qYG+l852Zu1RrL1xdLKY6x2TFEPnniEiHKMaoOEDr5pOOmWvUbfnKIkxrSu5wRUCki4wLC4fYvPUErgwql5dgttLhJhFpYueHaN7eGJfBaWAzGSCISJ3ySMrgsS+D8uVFlgGRVlIGm7fDmFBOxgSWAZFK1pVBGBMWvnpfyoB7BkQa2fIQrbt/wp8lmuQUwTIMozHu/QdSJ87PfztTywN9HisSqZSJsb/aDSuDxBsKg2EYBQlcGVgrV15/gGEYFXHvv/Bjwrk8TI9jApFKGYuD37q+DE6cy7EMiJSy2VjKYM+PCcb9kZQBwzDa4t9/+S75OYO5L0/B/J3cICJt7LsW2z88HY8JeWCPZUCkUg44WDs6WvS7iUSkkX///ZjwxUngGVcGRCqdlDHh3jM/JkyflTGhG24QkS7y+r9Y2wt7BmdkaGAZEOmUlMHvoQymz2RZBkRauTLo+T2D2YvvIXrKTUQijeJTBjs//jU+TRBJFzAMoy+BHxM+kDFh939XiUgPGRNe/tEbl0FOyiDcICJdCsaVgdszKHz+DsxGHO4QkSZ2KcLuT/+EX1R6fYZgGEZN3PsvXBnE/HAThlEb9/4Lv2dQzQE7/gIR6WJmI7xcD3sG+c/eBtYPwy0iUqU6he6D5+MyqMCsc2VApJGtGimDph8TjlczQIdlQKRS0WDwuD8ugyzQ5tEikUqllCsDd5rAj0pnGL0Zf1T6f7+b8KanGIZREM9tIGY/rcCsDcMlItLEnk2j97DJlQHDMJ7bQHxraYYbiERK2VKEVxv7YUz4hGMCkVZuTPi56csg8/ECy4BIqaQM+r+0wphQzcBsj46OGIhIB2MMMD8VxoRLtfbMxUrRrB7CcHFApIpNS85PYf9+s2NKjfq14xfyy+lXcrU1AoayOuBeItFkS84R07IqKKcwiAYYrvS+d/+N0tyVuj32UUFmhjSikTw14rhANNFSBnEqxuhgiMGvu9i+9SgZGLxSo3Zd6uIbuTAbLhHRBJN/8ndkDLjRvrO6DAD/AopWIVyrRKv6AAAAAElFTkSuQmCC'
    imagemBotaoVermelho = b'iVBORw0KGgoAAAANSUhEUgAAAQMAAAAwCAYAAAAVSB98AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsIAAA7CARUoSoAAAAN4SURBVHhe7dzdi1VVGMfx3z57N2vrjKVDXigYIZGiFIiCL+hczEA3/Qt24W0vDBUUJOgpVCywGsxuvdAL/wIvBL1IsYxCqhuDisCki3Lm+NLMbD17n9ZaZ28HNv4F5/l+4IHzdjs/nudZa0+S57mCbqK5fkcHk0ST8QMAo24hLXWuO9BseBPD4BNpcFBOG+L3AKz429d5FTrisyA5PpF/eajvZteHL1YX6mf+RRp+BmBklVLWlzYsOt3RQBeSR58mx8bzu4dLN3l7wgfBqvqHAEzIlqRND52Op8V86AwGH/Wd/lhT0BEA1vgOYfMDpxNZoZUweN6HAQBzNv/bCoNfJwkDwKIt860w+O05wgCw6KV77c6AMABM2tIOg1vsDACTtrZ3BrfWEQaARVsXhmGQzoxl3QNVpn/ysv4KgCXrlzNd7ZQrncEv7AwAk15p7wx+5mgRMOnV+mixU7+XBhRFmazak87gZriODMCcHe3ryDfXEgaARTt6rTD4kQUiYNLO9gLxB+4ZACbtqu8ZrCwQAZgWO4MPQmfAzgAwaVfP6TPfGcQbiFNVpr8cNxABi14oMl3rlMMxoe/racePFEWNfoW//yB2Bvt8Z3CHzgAwaaPvDK43zya833e68Sw7A8Ci3fedTjVHiyEMvmOBCJi0pzcMgydjwm3GBMCkTX5M+LZZIEbhFUVR9qoWx4T3/JhwbTVjAmDR/kWnz5udwawPg+s8tQiYtO+B01wTBu/6MLjKg0qASQfuOX3hwyBODHF12J4jKIoyUc3RQewM3vGdwTer6AwAi6aWnE43Y0IMA+4ZACZN9YZhEO8Z7K4y/ck9A8CkF4tM33dKwgCwrgmDOCa87ceEKzybAJg0fd/pq2ZnEMNgnDAALJr+bxgG4XBh+FxzQlGUyQoh4MXO4K3QGXC0CJg0veR0phkT3mRMAMwKY8LXTRiEzuDSBGEAWPTaw1ZncJmnFgGTZhaHnUG8Z7C3yvT7M6UGzSYBgAlJIr38ONONcM/g2Hh+98PSTV4cK7Ts6l8AMCH3A8Hrj5xOpsV8OuOyjduqbM9EmapXlap8UpT1cQNFUaNZaSk5HwTbH49pWYl+SsvTSZ7n+rijwaHKaa3/UdgcNP9HHcBoynyFQaDn62yn0NHKTwwhDIJuojnfHLzhX66LHwAYdQu+QzjXHWhWkv4HD+VJFubY6YoAAAAASUVORK5CYII='
    main()