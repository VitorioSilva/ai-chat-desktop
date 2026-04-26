import customtkinter as ctk
import threading
from services.ai_service import responder
import sys


class ChatApp:
    def __init__(self):
        self.app = ctk.CTk()
        ctk.set_appearance_mode("dark")
        self.app.title("AI Chat Desktop")
        self.app.geometry("700x800")

        # Para garantir que saia quando fechar pela janela
        self.app.protocol("WM_DELETE_WINDOW", self.sair_programa)

        self.criar_componentes()

    def criar_componentes(self):
        # Titulo
        self.titulo = ctk.CTkLabel(self.app, text="AI Chat Desktop", font=("Arial", 20))
        self.titulo.pack(pady=10)

        # chat
        self.chat_box = ctk.CTkTextbox(self.app)
        self.chat_box.pack(pady=10, fill="both", expand=True)

        # entrada
        self.entrada = ctk.CTkEntry(self.app, placeholder_text="Digite sua mensagem...")
        self.entrada.pack(pady=10, padx=10, fill="x")

        # Frame para botões
        self.frame_botoes = ctk.CTkFrame(self.app, fg_color="transparent")
        self.frame_botoes.pack(pady=10)

        # botão enviar
        self.botao_enviar = ctk.CTkButton(
            self.frame_botoes, text="Enviar", command=self.enviar, width=100
        )
        self.botao_enviar.pack(side="left", padx=5)

        # Botão sair
        self.botao_sair = ctk.CTkButton(
            self.frame_botoes,
            text="Sair",
            command=self.sair_programa,
            width=100,
        )
        self.botao_sair.pack(side="left", padx=5)

        # Bind Enter para enviar
        self.entrada.bind("<Return>", lambda e: self.enviar())

        # Bind ESC para sair
        self.app.bind("<Escape>", lambda e: self.sair_programa())

    def enviar(self):
        texto = self.entrada.get()

        if not texto.strip():
            return

        self.chat_box.insert("end", f"\nVocê: {texto}\n")
        self.chat_box.see("end")
        self.entrada.delete(0, "end")

        self.chat_box.insert("end", "\nAI: pensando...\n")
        self.chat_box.see("end")

        # Desabilita botão enquanto processa
        self.botao_enviar.configure(state="disabled")

        thread = threading.Thread(target=self.responder_ai, args=(texto,))
        thread.daemon = True  # Thread morre quando o programa fechar
        thread.start()

    def responder_ai(self, texto):
        try:
            resposta = responder(texto)

            # Atualiza interface na thread principal
            self.app.after(0, self.mostrar_resposta, resposta)
        except Exception as e:
            self.app.after(0, self.mostrar_resposta, f"Erro: {str(e)}")

    def mostrar_resposta(self, resposta):
        self.chat_box.delete("end-2l", "end-1l")  # Remove linha "pensando..."
        self.chat_box.insert("end", f"AI: {resposta.replace("**", "")}\n\n")
        self.chat_box.see("end")

        # Reabilita botão
        self.botao_enviar.configure(state="normal")

    def sair_programa(self):
        print("Encerrando programa...")
        self.app.quit()
        self.app.destroy()
        sys.exit(0)

    def iniciar(self):
        self.app.mainloop()
