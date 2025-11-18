import tkinter as tk
from tkinter import messagebox, ttk

def calcular_chave():
    try:
        # Obtém valores da interface
        p = int(entry_p.get())
        g = int(entry_g.get())
        a = int(entry_a.get())
        b = int(entry_b.get())

        # Cálculos Diffie-Hellman
        A = pow(g, a, p)  # Alice envia para Bob
        B = pow(g, b, p)  # Bob envia para Alice

        chave_Alice = pow(B, a, p)
        chave_Bob = pow(A, b, p)

        # Exibe resultados
        resultado = (
            f"Parâmetros públicos:\n p = {p}, g = {g}\n\n"
            f"Segredo de Alice (a) = {a}\nSegredo de Bob (b) = {b}\n\n"
            f"A = g^a mod p = {A}\nB = g^b mod p = {B}\n\n"
            f"Chave de Alice = B^a mod p = {chave_Alice}\n"
            f"Chave de Bob   = A^b mod p = {chave_Bob}\n\n"
            f"Chave secreta compartilhada: {chave_Alice}"
        )
        messagebox.showinfo("Resultado da Troca de Chaves", resultado)

    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira apenas números inteiros.")

def mostrar_ajuda():
    ajuda_texto = (
        "📖 Ajuda - Protocolo Diffie–Hellman\n\n"
        "Este programa demonstra a troca de chaves Diffie–Hellman.\n"
        "Passos:\n"
        "1. Insira os parâmetros públicos p (primo) e g (gerador).\n"
        "2. Defina os segredos de Alice (a) e Bob (b).\n"
        "3. Clique em 'Calcular Chave Compartilhada'.\n\n"
        "O resultado mostrará os valores trocados e a chave secreta comum."
    )
    messagebox.showinfo("Ajuda", ajuda_texto)

# Criando janela principal
root = tk.Tk()
root.title("Demonstração Diffie–Hellman")
root.geometry("450x400")
root.configure(bg="#f0f0f0")

# Menu
menu_bar = tk.Menu(root)
ajuda_menu = tk.Menu(menu_bar, tearoff=0)
ajuda_menu.add_command(label="Sobre o protocolo", command=mostrar_ajuda)
menu_bar.add_cascade(label="Ajuda", menu=ajuda_menu)
root.config(menu=menu_bar)

# Frame principal
frame = ttk.Frame(root, padding="20")
frame.pack(fill="both", expand=True)

# Labels e entradas
ttk.Label(frame, text="Parâmetro público p (primo):").pack(pady=5)
entry_p = ttk.Entry(frame)
entry_p.pack()
entry_p.insert(0, "23")

ttk.Label(frame, text="Parâmetro público g (gerador):").pack(pady=5)
entry_g = ttk.Entry(frame)
entry_g.pack()
entry_g.insert(0, "5")

ttk.Label(frame, text="Segredo de Alice (a):").pack(pady=5)
entry_a = ttk.Entry(frame)
entry_a.pack()
entry_a.insert(0, "6")

ttk.Label(frame, text="Segredo de Bob (b):").pack(pady=5)
entry_b = ttk.Entry(frame)
entry_b.pack()
entry_b.insert(0, "15")

# Botão estilizado
btn_calcular = ttk.Button(frame, text="🔐 Calcular Chave Compartilhada", command=calcular_chave)
btn_calcular.pack(pady=20)

# Rodar aplicação
root.mainloop()
