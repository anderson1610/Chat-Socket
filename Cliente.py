import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, Entry, Button
from pathlib import Path
import getpass
from tkinter import messagebox
import tkinter.font as font

def get_username():
    return getpass.getuser()

def delete_history():
    if messagebox.askyesno("Deletar Histórico", "Tem certeza que deseja deletar o histórico?"):
        log_file = create_log_file()
        with open(log_file, 'w', encoding='utf8') as arquivo:
            arquivo.write("")
        chat_box.delete('1.0', tk.END)  # Limpa a caixa de mensagens



def create_log_file():
    name_user = get_username()
    log_file = f"C:\\Users\\{name_user}\\Desktop\\Chat\\historico_conversa.txt"
    path = Path(f"C:\\Users\\{name_user}\\Desktop\\Chat")
    path.mkdir(parents=True, exist_ok=True)
    with open(log_file, 'a') as arquivo:
        pass
    return log_file


def receive_messages():
    while True:
        mensagem = client_socket.recv(1024).decode()
        chat_box.insert(tk.END, f'{mensagem}\n')
        log_file = create_log_file()

        # Adicionar a mensagem ao arquivo de histórico
        with open(log_file, 'a') as arquivo:
            arquivo.write(f'{mensagem}\n')


def send_message():
    
    mensagem = input_box.get()
    mensagem_formatada = f'{Name}: {mensagem}'
    chat_box.insert(tk.END, f'{mensagem_formatada}\n')  # Adiciona à caixa de mensagens
    client_socket.send(mensagem_formatada.encode())
    log_file = create_log_file()

    # Adicionar a mensagem ao arquivo de histórico
    with open(log_file, 'a') as arquivo:
        arquivo.write(f'{mensagem_formatada}\n')
        
    input_box.delete(0, tk.END)

    if mensagem == "sair":
        client_socket.close()
        root.destroy()

   

# Configurações do cliente
HOST = '172.16.254.169'  # Endereço IP do servidor
PORT = 12345        # Porta do servidor
Name = input('Digite seu nome: ')
log_file = create_log_file()


# Inicializa o cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))


root = tk.Tk()
root.title(f'Chat Cliente: {Name} ')

chat_box = scrolledtext.ScrolledText(root, width=50, height=15)
chat_box.pack(padx=10, pady=10)

# Configurações de fonte para exibir emojis
emoji_font = font.nametofont("TkDefaultFont")  # Obtém a fonte padrão do tkinter
emoji_font.configure(size=12, family="Segoe UI Emoji")  # Altera o tamanho e a família da fonte
chat_box.configure(font=emoji_font)  # Aplica a nova fonte à caixa de mensagens

#Le o historico salvo e add ao box
with open(log_file, 'r') as arquivo:
    historico = arquivo.read()
    chat_box.insert(tk.END, historico)

input_box = Entry(root, width=40)
input_box.pack(padx=10, pady=(0, 10))

button_frame = tk.Frame(root)  # Cria um frame para os botões
button_frame.pack(padx=10, pady=5)  # Empacota o frame

send_button = Button(button_frame, text='Enviar', command=send_message)
send_button.pack(side=tk.LEFT, padx=5)

delete_button = Button(button_frame, text='Deletar Histórico', command=delete_history)
delete_button.pack(side=tk.LEFT, padx=5)

exit_button = Button(button_frame, text='Sair', command=root.destroy)  # Função para sair do chat
exit_button.pack(side=tk.RIGHT, padx=5)  # Posiciona o botão "Sair" à direita


receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

root.mainloop()
