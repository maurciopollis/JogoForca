from tkinter import *
from tkinter import ttk
import random


def normalizador_de_resposta(palavra):

    equivalentes_a = ['à', 'á', 'â', 'ã', 'ä']
    equivalentes_c = ['ç']
    equivalentes_e = ['è', 'é', 'ê', 'ë']
    equivalentes_i = ['ì', 'í', 'î', 'ï']
    equivalentes_o = ['ò', 'ó', 'ô', 'õ', 'ö']
    equivalentes_u = ['ù', 'ú', 'û', 'ü']

    normalizacao = palavra.lower()

    for i in range(len(normalizacao)):
        if normalizacao[i] in equivalentes_a:
            normalizacao = normalizacao[:i] + 'a' + normalizacao[i + 1:]
        elif normalizacao[i] in equivalentes_c:
            normalizacao = normalizacao[:i] + 'c' + normalizacao[i + 1:]
        elif normalizacao[i] in equivalentes_e:
            normalizacao = normalizacao[:i] + 'e' + normalizacao[i + 1:]
        elif normalizacao[i] in equivalentes_i:
            normalizacao = normalizacao[:i] + 'i' + normalizacao[i + 1:]
        elif normalizacao[i] in equivalentes_o:
            normalizacao = normalizacao[:i] + 'o' + normalizacao[i + 1:]
        elif normalizacao[i] in equivalentes_u:
            normalizacao = normalizacao[:i] + 'u' + normalizacao[i + 1:]

    return normalizacao


def mascara_inicial(resposta):
    palavra = "*"*len(resposta)
    for i in range(len(resposta)):
        if resposta[i] == '-' or resposta[i] == '.':
            palavra = palavra[:i] + resposta[i] + palavra[i + 1:]
    return palavra


def chutou_letra(*args):
    mensagem.set('')
    if len(chuteLetra.get()) != 1:
        mensagem.set('O chute deve ser apenas um caracter!')
    else:
        if chuteLetra.get() in letras_tentadas:
            mensagem.set('Essa letra já foi!')
        else:
            letras_tentadas.append(chuteLetra.get())
            if chuteLetra.get() not in resposta_normalizada:
                letras_erradas_tentadas.append(chuteLetra.get())
                letrasTentadas.set(letras_erradas_tentadas)
                chancesRestantes.set(int(chancesRestantes.get()) - 1)
                if int(chancesRestantes.get()) == 0:
                    mensagem.set(f'Acabaram suas chances! A resposta é {resposta}')
                    mensagem_label['foreground'] = 'red'
                    chances_restantes_label['foreground'] = 'red'
                    situacaoAtual.set(resposta)
                    situacao_atual_label['foreground'] = 'red'
            else:
                aux = situacaoAtual.get()
                for i in range(len(resposta_normalizada)):
                    if resposta_normalizada[i] == chuteLetra.get():
                        aux = aux[:i] + resposta[i] + aux[i + 1:]
                situacaoAtual.set(aux)
                if '*' not in situacaoAtual.get():
                    mensagem.set('Acertou!')
                    mensagem_label['foreground'] = 'green'
                    situacaoAtual.set(resposta)
                    situacao_atual_label['foreground'] = 'green'
                    chances_restantes_label['foreground'] = 'green'
    chuteLetra.set('')
        

def chutou_palavra():
    if len(chutePalavra.get()) == 0:
        mensagem.set('O chute não pode ter tamanho nulo!')
    else:
        if chutePalavra.get() != resposta_normalizada:
            mensagem.set(f'Errou! A resposta é {resposta}')
            mensagem_label['foreground'] = 'red'
            chancesRestantes.set(0)
            chances_restantes_label['foreground'] = 'red'
            situacaoAtual.set(resposta)
            situacao_atual_label['foreground'] = 'red'

        else:
            mensagem.set('Acertou!')
            mensagem_label['foreground'] = 'green'
            situacaoAtual.set(resposta)
            situacao_atual_label['foreground'] = 'green'


dados = open('palavras1(imeusp).txt', 'r', encoding='utf-8-sig')
universo_de_palavras = []
for linha in dados:
    universo_de_palavras.append(linha[:-1])
dados.close()

resposta = universo_de_palavras[random.randrange(len(universo_de_palavras))]
resposta_normalizada = normalizador_de_resposta(resposta)

letras_erradas_tentadas = []
letras_tentadas = []

root = Tk()
root.title('Jogo da Forca')

mainframe = ttk.Frame(root, padding=(3, 3, 12, 12))
mainframe.grid(row=0, column=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

situacaoAtual = StringVar()
situacaoAtual.set(mascara_inicial(resposta_normalizada))
situacao_atual_label = ttk.Label(mainframe, textvariable=situacaoAtual)
situacao_atual_label.grid(row=0, column=0, columnspan=3)

ttk.Label(mainframe, text='Letras tentadas:').grid(row=1, column=0, sticky=W)
letrasTentadas = StringVar()
letras_tentadas_label = ttk.Label(mainframe, textvariable=letrasTentadas)
letras_tentadas_label.grid(row=1, column=1, sticky=W)

ttk.Label(mainframe, text='Chances restantes:').grid(row=2, column=0)
chancesRestantes = StringVar()
chancesRestantes.set(5)
chances_restantes_label = ttk.Label(mainframe, textvariable=chancesRestantes)
chances_restantes_label.grid(row=2, column=1, sticky=W)

mensagem = StringVar()
mensagem_label = ttk.Label(mainframe, textvariable=mensagem)
mensagem_label.grid(row=5, column=0, columnspan=3)

ttk.Label(mainframe, text='Insira a letra:').grid(row=3, column=0, sticky=W)
chuteLetra = StringVar()
chute_letra_entry = ttk.Entry(mainframe, textvariable=chuteLetra)
chute_letra_entry.grid(row=3, column = 1)
chutar_letra_btn = ttk.Button(mainframe, text='Chutar letra', command=chutou_letra)
chutar_letra_btn.grid(row=3, column=2, sticky=W)

ttk.Label(mainframe, text='Chutar palavra:').grid(row=4, column=0, sticky=W)
chutePalavra = StringVar()
chute_palavra_entry = ttk.Entry(mainframe, textvariable=chutePalavra)
chute_palavra_entry.grid(row=4, column=1)
chutar_palavra_btn = ttk.Button(mainframe, text='Chutar palavra', command=chutou_palavra)
chutar_palavra_btn.grid(row=4, column=2, sticky=W)

chute_letra_entry.focus()
root.bind("<Return>", chutou_letra)

root.mainloop()
