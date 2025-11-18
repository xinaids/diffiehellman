import tkinter as tk
from tkinter import ttk, messagebox

from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

chave_simetrica_global = None  # será usada nas abas 2


def gerar_chave():
    global chave_simetrica_global

    try:
        p = int(entry_p.get())
        g = int(entry_g.get())
        a = int(entry_a.get())
        b = int(entry_b.get())

        A = pow(g, a, p)
        B = pow(g, b, p)
        chave_A = pow(B, a, p)
        chave_B = pow(A, b, p)

        if chave_A != chave_B:
            messagebox.showerror("Erro", "As chaves não coincidem!")
            return

        hkdf = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b"dh-aes",
        )
        chave_simetrica_global = hkdf.derive(str(chave_A).encode())

        resultado = (
            f"p = {p}\ng = {g}\na = {a}\nb = {b}\n\n"
            f"A = {A}\nB = {B}\n\n"
            f"Chave Diffie-Hellman = {chave_A}\n\n"
            f"Chave simétrica derivada (AES-256):\n{chave_simetrica_global.hex()}"
        )

        messagebox.showinfo("Chave Gerada", resultado)

    except Exception as e:
        messagebox.showerror("Erro", str(e))


def criptografar():
    global chave_simetrica_global

    if chave_simetrica_global is None:
        messagebox.showwarning("Atenção", "Gere a chave primeiro na aba 1.")
        return

    try:
        texto = entry_msg_enc.get().encode()
        aes = AESGCM(chave_simetrica_global)
        nonce = os.urandom(12)

        cifrado = aes.encrypt(nonce, texto, None)

        entry_nonce.delete(0, tk.END)
        entry_nonce.insert(0, nonce.hex())

        entry_saida_enc.delete(0, tk.END)
        entry_saida_enc.insert(0, cifrado.hex())

        messagebox.showinfo("Criptografia", "Mensagem criptografada com sucesso.")

    except Exception as e:
        messagebox.showerror("Erro", str(e))


def descriptografar():
    global chave_simetrica_global

    if chave_simetrica_global is None:
        messagebox.showwarning("Atenção", "Gere a chave primeiro na aba 1.")
        return

    try:
        aes = AESGCM(chave_simetrica_global)
        nonce = bytes.fromhex(entry_nonce.get())
        cifrado = bytes.fromhex(entry_saida_enc.get())

        texto = aes.decrypt(nonce, cifrado, None).decode()

        entry_saida_dec.delete(0, tk.END)
        entry_saida_dec.insert(0, texto)

        messagebox.showinfo("Descriptografia", "Mensagem recuperada com sucesso.")

    except Exception as e:
        messagebox.showerror("Erro", str(e))


# ==========================================
# Interface
# ==========================================

root = tk.Tk()
root.title("Diffie–Hellman")
root.geometry("550x500")

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# ------------------------------------------
# ABA 1 — GERAÇÃO DA CHAVE
# ------------------------------------------
aba1 = ttk.Frame(notebook, padding=20)
notebook.add(aba1, text="Gerar Chave")

ttk.Label(aba1, text="p (primo):").pack(pady=5)
entry_p = ttk.Entry(aba1)
entry_p.pack()
entry_p.insert(0, "23")

ttk.Label(aba1, text="g (gerador):").pack(pady=5)
entry_g = ttk.Entry(aba1)
entry_g.pack()
entry_g.insert(0, "5")

ttk.Label(aba1, text="Segredo de Alice (a):").pack(pady=5)
entry_a = ttk.Entry(aba1)
entry_a.pack()
entry_a.insert(0, "6")

ttk.Label(aba1, text="Segredo de Bob (b):").pack(pady=5)
entry_b = ttk.Entry(aba1)
entry_b.pack()
entry_b.insert(0, "15")

ttk.Button(aba1, text="Gerar Chave Compartilhada", command=gerar_chave).pack(pady=20)

# ------------------------------------------
# ABA 2 — CRIPTOGRAFAR / DESCRIPTOGRAFAR
# ------------------------------------------
aba2 = ttk.Frame(notebook, padding=20)
notebook.add(aba2, text="Criptografar / Descriptografar")

ttk.Label(aba2, text="Mensagem para criptografar:").pack(pady=5)
entry_msg_enc = ttk.Entry(aba2, width=50)
entry_msg_enc.pack()

ttk.Button(aba2, text="Criptografar", command=criptografar).pack(pady=10)

ttk.Label(aba2, text="Nonce (hex):").pack(pady=5)
entry_nonce = ttk.Entry(aba2, width=50)
entry_nonce.pack()

ttk.Label(aba2, text="Ciphertext (hex):").pack(pady=5)
entry_saida_enc = ttk.Entry(aba2, width=50)
entry_saida_enc.pack()

ttk.Button(aba2, text="Descriptografar", command=descriptografar).pack(pady=10)

ttk.Label(aba2, text="Mensagem decifrada:").pack(pady=5)
entry_saida_dec = ttk.Entry(aba2, width=50)
entry_saida_dec.pack()

root.mainloop()
