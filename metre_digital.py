import random
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
from datetime import datetime
from typing import Dict, List, Optional
import sqlite3
from pathlib import Path
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import pdfkit  # Para exportação em PDF (instalar via `pip install pdfkit`)

# ================== BANCO DE DADOS ==================
class Database:
    """Gerencia o banco de dados SQLite para pratos e bebidas."""
    def __init__(self, db_path: str = "metre_digital.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self) -> None:
        """Inicializa o banco de dados com tabelas padrão."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS pratos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    categoria TEXT NOT NULL,
                    tipo TEXT NOT NULL,
                    dieta TEXT NOT NULL,
                    intensidade TEXT NOT NULL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS bebidas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    tipo TEXT NOT NULL,
                    categoria TEXT NOT NULL,
                    intensidade TEXT NOT NULL,
                    harmonizacao TEXT NOT NULL,
                    preco REAL NOT NULL
                )
            """)
            conn.commit()
            self._populate_initial_data(cursor)

    def _populate_initial_data(self, cursor: sqlite3.Cursor) -> None:
        """Popula o banco com dados iniciais, se vazio."""
        cursor.execute("SELECT COUNT(*) FROM pratos")
        if cursor.fetchone()[0] == 0:
            pratos = [
                ("Bruschetta", "entrada", "italiana", "vegetariana", "leve"),
                ("Filé Mignon", "principal", "francesa", "carnes", "alta"),
                ("Petit Gateau", "sobremesa", "francesa", "vegetariana", "alta"),
            ]
            cursor.executemany("INSERT INTO pratos (nome, categoria, tipo, dieta, intensidade) VALUES (?, ?, ?, ?, ?)", pratos)

        cursor.execute("SELECT COUNT(*) FROM bebidas")
        if cursor.fetchone()[0] == 0:
            bebidas = [
                ("Prosecco", "espumante", "vinhos", "leve", "Aperitivos", 120.0),
                ("Malbec", "tinto", "vinhos", "alta", "Carnes", 250.0),
                ("Mocktail de Frutas", "coquetel", "sem_alcool", "média", "Sobremesas", 18.0),
            ]
            cursor.executemany("INSERT INTO bebidas (nome, tipo, categoria, intensidade, harmonizacao, preco) VALUES (?, ?, ?, ?, ?, ?)", bebidas)
        cursor.connection.commit()

    def get_pratos(self, categoria: str, tipo: Optional[str] = None, dieta: Optional[str] = None) -> List[Dict]:
        """Recupera pratos com filtros opcionais."""
        query = "SELECT nome, categoria, tipo, dieta, intensidade FROM pratos WHERE categoria = ?"
        params = [categoria]
        if tipo:
            query += " AND tipo = ?"
            params.append(tipo)
        if dieta:
            query += " AND dieta = ?"
            params.append(dieta)
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def get_bebidas(self, categoria: str, intensidade: Optional[str] = None) -> List[Dict]:
        """Recupera bebidas com filtros opcionais."""
        query = "SELECT nome, tipo, categoria, intensidade, harmonizacao, preco FROM bebidas WHERE categoria = ?"
        params = [categoria]
        if intensidade:
            query += " AND intensidade = ?"
            params.append(intensidade)
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

# ================== SISTEMA DE RECOMENDAÇÃO ==================
class SistemaIA:
    """Sistema de recomendação simulando um sommelier."""
    def __init__(self, db: Database):
        self.db = db
        self.sugestoes = {
            "Jantar Romântico": {
                "cozinha": "francesa",
                "dieta_entrada": "vegetariana",
                "dieta_principal": "carnes",
                "bebida": "vinhos",
                "sugestao_especial": "Menu especial para uma noite romântica"
            },
            # Outras ocasiões permanecem semelhantes ao original
        }

    def analisar_contexto(self, comando: str, ocasiao: str, expectativas: str) -> Dict:
        """Analisa o contexto para sugestões personalizadas."""
        sugestao = self.sugestoes.get(ocasiao, {
            "cozinha": None,
            "dieta_entrada": None,
            "dieta_principal": None,
            "bebida": "vinhos",
            "sugestao_especial": "Sugestão personalizada do chef"
        }).copy()
        comando = comando.lower()
        if "vegetariano" in comando:
            sugestao["dieta_entrada"] = "vegetariana"
            sugestao["dieta_principal"] = "vegetariana"
        elif "vegano" in comando:
            sugestao["dieta_entrada"] = "vegana"
            sugestao["dieta_principal"] = "vegana"
        return sugestao

    def recomendar_sobremesa(self, contexto: Dict) -> Dict:
        """Recomenda sobremesa com base no contexto."""
        sobremesas = self.db.get_pratos("sobremesa", contexto.get("cozinha"), contexto.get("dieta_principal"))
        return random.choice(sobremesas) if sobremesas else {"nome": "Surpresa do Chef", "tipo": "variada", "dieta": "vegetariana", "intensidade": "média"}

    def explicar_harmonizacao(self, menu_completo: Dict) -> str:
        """Gera explicação detalhada da harmonização."""
        return (
            f"Este menu foi elaborado para {menu_completo['ocasiao']}. "
            f"A entrada {menu_completo['entrada']['nome']} harmoniza com {menu_completo['bebidas']['entrada']['nome']}, "
            f"preparando o paladar para o prato principal {menu_completo['principal']['nome']} com {menu_completo['bebidas']['principal']['nome']}. "
            f"A sobremesa {menu_completo['sobremesa']['nome']} finaliza com elegância."
        )

# ================== LÓGICA DE HARMONIZAÇÃO ==================
def recomendar_bebida(db: Database, prato: Dict, tipo_bebida: str, cozinha: Optional[str] = None) -> Dict:
    """Recomenda bebida com base na intensidade do prato."""
    intensidade_map = {"leve": ["leve"], "média": ["leve", "média"], "alta": ["média", "alta"]}
    intensidades = intensidade_map.get(prato["intensidade"], ["média"])
    bebidas = db.get_bebidas(tipo_bebida)
    opcoes = [b for b in bebidas if b["intensidade"] in intensidades]
    return random.choice(opcoes) if opcoes else {"nome": "Seleção do Chef", "tipo": tipo_bebida, "preco": 0, "harmonizacao": "Geral"}

# ================== INTERFACE GRÁFICA ==================
class HarmonizadorApp:
    """Interface gráfica do Métre Digital."""
    def __init__(self, root: ttkb.Window):
        self.root = root
        self.root.title("Métre Digital - Versão 2.0")
        self.db = Database()
        self.ia = SistemaIA(self.db)
        self.menu_gerado = None
        self.explicacao_detalhada = None
        self.sugestao_especial = None
        self.criar_interface()

    def criar_interface(self) -> None:
        """Cria a interface gráfica com ttkbootstrap."""
        self.root.geometry("1200x900")
        main_frame = ttkb.Frame(self.root, padding=20, bootstyle=SECONDARY)
        main_frame.pack(fill=BOTH, expand=True)

        # Seção de contexto
        context_frame = ttkb.LabelFrame(main_frame, text="Contexto da Refeição", padding=10, bootstyle=INFO)
        context_frame.pack(fill=X, pady=10)

        ttkb.Label(context_frame, text="Ocasião:").grid(row=0, column=0, sticky=W, padx=5)
        self.ocasiao = ttkb.Combobox(context_frame, values=["Jantar Romântico", "Aniversário", "Jantar de Negócios", "Família", "Amigos", "Outro"], bootstyle=PRIMARY)
        self.ocasiao.grid(row=0, column=1, sticky=EW, padx=5)

        ttkb.Label(context_frame, text="Expectativas:").grid(row=1, column=0, sticky=W, padx=5)
        self.expectativas = ttkb.Combobox(context_frame, values=["Refeição Leve", "Experiência Gourmet", "Confort Food", "Culinária Internacional", "Surpresa do Chef"], bootstyle=PRIMARY)
        self.expectativas.grid(row=1, column=1, sticky=EW, padx=5)

        # Campo de comando
        ttkb.Label(main_frame, text="Comando Específico (opcional):").pack(pady=(10, 0))
        self.entrada_comando = ttkb.Entry(main_frame, width=80, font=('Arial', 12), bootstyle=PRIMARY)
        self.entrada_comando.pack(pady=5)

        # Controles manuais
        control_frame = ttkb.LabelFrame(main_frame, text="Preferências Manuais", padding=10, bootstyle=INFO)
        control_frame.pack(fill=X, pady=10)

        linha1 = ttkb.Frame(control_frame)
        linha1.pack(fill=X, pady=5)
        ttkb.Label(linha1, text="Cozinha:").pack(side=LEFT, padx=5)
        self.cozinha = ttkb.Combobox(linha1, values=["", "italiana", "francesa", "americana", "mediterrânea", "portuguesa", "brasileira"], bootstyle=PRIMARY)
        self.cozinha.pack(side=LEFT, padx=5, expand=True, fill=X)

        ttkb.Label(linha1, text="Bebida:").pack(side=LEFT, padx=5)
        self.tipo_bebida = ttkb.Combobox(linha1, values=["vinhos", "cervejas", "sem_alcool"], bootstyle=PRIMARY)
        self.tipo_bebida.pack(side=LEFT, padx=5, expand=True, fill=X)
        self.tipo_bebida.set("vinhos")

        linha2 = ttkb.Frame(control_frame)
        linha2.pack(fill=X, pady=5)
        ttkb.Label(linha2, text="Dieta Entrada:").pack(side=LEFT, padx=5)
        self.dieta_entrada = ttkb.Combobox(linha2, values=["", "vegetariana", "vegana", "carnes", "peixes"], bootstyle=PRIMARY)
        self.dieta_entrada.pack(side=LEFT, padx=5, expand=True, fill=X)

        ttkb.Label(linha2, text="Dieta Principal:").pack(side=LEFT, padx=5)
        self.dieta_principal = ttkb.Combobox(linha2, values=["", "vegetariana", "vegana", "carnes", "peixes"], bootstyle=PRIMARY)
        self.dieta_principal.pack(side=LEFT, padx=5, expand=True, fill=X)

        # Botões de ação
        btn_action_frame = ttkb.Frame(control_frame)
        btn_action_frame.pack(pady=10)
        ttkb.Button(btn_action_frame, text="Consultar Métre", command=self.consultar_metre, bootstyle=SUCCESS).pack(side=LEFT, padx=5)
        ttkb.Button(btn_action_frame, text="Gerar Menu Manual", command=self.gerar_menu_manual, bootstyle=PRIMARY).pack(side=LEFT, padx=5)

        # Área de resultado
        self.resultado = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, padx=15, pady=15, font=('Arial', 12), height=25, state='disabled')
        self.resultado.pack(fill=BOTH, expand=True)

        # Botões secundários
        btn_frame = ttkb.Frame(main_frame)
        btn_frame.pack(pady=10)
        ttkb.Button(btn_frame, text="Salvar Menu (TXT)", command=lambda: self.salvar_menu("txt"), bootstyle=INFO).pack(side=LEFT, padx=5)
        ttkb.Button(btn_frame, text="Salvar Menu (PDF)", command=lambda: self.salvar_menu("pdf"), bootstyle=INFO).pack(side=LEFT, padx=5)
        ttkb.Button(btn_frame, text="Limpar", command=self.limpar_tela, bootstyle=WARNING).pack(side=LEFT, padx=5)
        ttkb.Button(btn_frame, text="Explicação do Métre", command=self.mostrar_explicacao, bootstyle=PRIMARY).pack(side=LEFT, padx=5)

        self.exibir_resultado("Bem-vindo ao Métre Digital 2.0!\nSelecione ocasião e expectativas para começar.")

    def consultar_metre(self) -> None:
        """Consulta o métre para recomendações completas."""
        try:
            ocasiao = self.ocasiao.get()
            expectativas = self.expectativas.get()
            comando = self.entrada_comando.get().strip()
            if not ocasiao or not expectativas:
                raise ValueError("Informe ocasião e expectativas!")
            contexto = self.ia.analisar_contexto(comando, ocasiao, expectativas)
            cozinha = self.cozinha.get() or contexto.get("cozinha")
            dieta_entrada = self.dieta_entrada.get() or contexto.get("dieta_entrada")
            dieta_principal = self.dieta_principal.get() or contexto.get("dieta_principal")
            tipo_bebida = self.tipo_bebida.get() or contexto.get("bebida", "vinhos")
            self.sugestao_especial = contexto.get("sugestao_especial")
            self.gerar_menu(cozinha, dieta_entrada, dieta_principal, tipo_bebida, ocasiao, expectativas)
        except Exception as e:
            self.exibir_resultado(f"⚠️ Erro: {str(e)}")

    def gerar_menu_manual(self) -> None:
        """Gera menu com base nas seleções manuais."""
        try:
            cozinha = self.cozinha.get()
            dieta_entrada = self.dieta_entrada.get()
            dieta_principal = self.dieta_principal.get()
            tipo_bebida = self.tipo_bebida.get()
            ocasiao = self.ocasiao.get() or "Jantar"
            expectativas = self.expectativas.get() or "Experiência Personalizada"
            if not tipo_bebida:
                raise ValueError("Selecione um tipo de bebida!")
            self.gerar_menu(cozinha, dieta_entrada, dieta_principal, tipo_bebida, ocasiao, expectativas)
        except Exception as e:
            self.exibir_resultado(f"⚠️ Erro: {str(e)}")

    def gerar_menu(self, cozinha: str, dieta_entrada: str, dieta_principal: str, tipo_bebida: str, ocasiao: str, expectativas: str) -> None:
        """Gera o menu completo."""
        entrada = self.selecionar_com_fallback("entrada", cozinha, dieta_entrada)
        principal = self.selecionar_com_fallback("principal", cozinha, dieta_principal)
        sobremesa = self.ia.recomendar_sobremesa({"cozinha": cozinha, "dieta_principal": dieta_principal})
        bebidas = {
            "entrada": recomendar_bebida(self.db, entrada, tipo_bebida, cozinha),
            "principal": recomendar_bebida(self.db, principal, tipo_bebida, cozinha),
            "sobremesa_alcool": random.choice(self.db.get_bebidas("digestivos")),
            "sobremesa_sem_alcool": random.choice(self.db.get_bebidas("sem_alcool")),
        }
        valor_total = sum(b.get("preco", 0) for b in bebidas.values())
        menu_completo = {
            "ocasiao": ocasiao,
            "expectativas": expectativas,
            "entrada": entrada,
            "principal": principal,
            "sobremesa": sobremesa,
            "bebidas": bebidas,
            "valor_total": valor_total
        }
        self.explicacao_detalhada = self.ia.explicar_harmonizacao(menu_completo)
        self.menu_gerado = self.formatar_menu(menu_completo)
        self.exibir_resultado(self.menu_gerado)

    def selecionar_com_fallback(self, categoria: str, cozinha: Optional[str], dieta: Optional[str]) -> Dict:
        """Seleciona prato com fallback."""
        pratos = self.db.get_pratos(categoria, cozinha, dieta)
        if not pratos and cozinha:
            pratos = self.db.get_pratos(categoria, cozinha)
        if not pratos and dieta:
            pratos = self.db.get_pratos(categoria, dieta=dieta)
        if not pratos:
            pratos = self.db.get_pratos(categoria)
        return random.choice(pratos)

    def formatar_menu(self, menu: Dict) -> str:
        """Formata o menu para exibição."""
        data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")
        return f"""🍽️ *MENU RECOMENDADO* • {data_atual}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎉 *Ocasião*: {menu['ocasiao']}
✨ *Expectativas*: {menu['expectativas']}
{self.sugestao_especial or "Sugestão especial: Aproveite cada momento!"}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🍴 *ENTRADA*: {menu['entrada']['nome']}
   ├─ *Estilo*: {menu['entrada']['tipo'].title()}
   ├─ *Dieta*: {menu['entrada']['dieta'].title()}
   ├─ *Intensidade*: {menu['entrada']['intensidade'].title()}
   └─ *Bebida*: {menu['bebidas']['entrada']['nome']} ({menu['bebidas']['entrada']['tipo'].title()})
      ├─ *Preço*: R${menu['bebidas']['entrada'].get('preco', '--')}
      └─ *Harmonização*: {menu['bebidas']['entrada'].get('harmonizacao', 'Seleção do chef')}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🍲 *PRATO PRINCIPAL*: {menu['principal']['nome']}
   ├─ *Estilo*: {menu['principal']['tipo'].title()}
   ├─ *Dieta*: {menu['principal']['dieta'].title()}
   ├─ *Intensidade*: {menu['principal']['intensidade'].title()}
   └─ *Bebida*: {menu['bebidas']['principal']['nome']} ({menu['bebidas']['principal']['tipo'].title()})
      ├─ *Preço*: R${menu['bebidas']['principal'].get('preco', '--')}
      └─ *Harmonização*: {menu['bebidas']['principal'].get('harmonizacao', 'Combinação clássica')}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🍰 *SOBREMESA*: {menu['sobremesa']['nome']}
   ├─ *Estilo*: {menu['sobremesa']['tipo'].title()}
   ├─ *Dieta*: {menu['sobremesa']['dieta'].title()}
   ├─ *Bebida Alcoólica*: {menu['bebidas']['sobremesa_alcool']['nome']}
   │  ├─ *Tipo*: {menu['bebidas']['sobremesa_alcool']['tipo'].title()}
   │  └─ *Preço*: R${menu['bebidas']['sobremesa_alcool'].get('preco', '--')}
   └─ *Bebida Sem Álcool*: {menu['bebidas']['sobremesa_sem_alcool']['nome']}
      ├─ *Tipo*: {menu['bebidas']['sobremesa_sem_alcool']['tipo'].title()}
      └─ *Preço*: R${menu['bebidas']['sobremesa_sem_alcool'].get('preco', '--')}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💰 *VALOR TOTAL DAS BEBIDAS*: R${menu['valor_total']:.2f}"""

    def salvar_menu(self, formato: str) -> None:
        """Salva o menu em TXT ou PDF."""
        if not self.menu_gerado:
            messagebox.showerror("Erro", "Nenhum menu para salvar!")
            return
        filename = f"menu_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{formato}"
        try:
            if formato == "txt":
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(self.menu_gerado)
                    if self.explicacao_detalhada:
                        f.write("\n\n=== ANÁLISE DO MÉTRE ===\n" + self.explicacao_detalhada)
            elif formato == "pdf":
                html_content = f"<pre>{self.menu_gerado}</pre>"
                if self.explicacao_detalhada:
                    html_content += f"<h2>Análise do Métre</h2><pre>{self.explicacao_detalhada}</pre>"
                pdfkit.from_string(html_content, filename)
            messagebox.showinfo("Sucesso", f"Menu salvo como '{filename}'")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar: {str(e)}")

    def mostrar_explicacao(self) -> None:
        """Exibe explicação detalhada."""
        if not self.explicacao_detalhada:
            messagebox.showwarning("Aviso", "Gere um menu primeiro!")
            return
        explicacao_window = ttkb.Toplevel(self.root)
        explicacao_window.title("Explicação do Métre")
        explicacao_window.geometry("900x700")
        text_area = scrolledtext.ScrolledText(explicacao_window, wrap=tk.WORD, padx=15, pady=15, font=('Arial', 12))
        text_area.pack(fill=BOTH, expand=True)
        text_area.insert(tk.END, self.explicacao_detalhada)
        ttkb.Button(explicacao_window, text="Fechar", command=explicacao_window.destroy, bootstyle=SECONDARY).pack(pady=10)

    def exibir_resultado(self, texto: str) -> None:
        """Exibe texto na área de resultados."""
        self.resultado.config(state=tk.NORMAL)
        self.resultado.delete(1.0, tk.END)
        self.resultado.insert(tk.END, texto)
        self.resultado.config(state=tk.DISABLED)

    def limpar_tela(self) -> None:
        """Limpa a interface."""
        self.menu_gerado = None
        self.explicacao_detalhada = None
        self.sugestao_especial = None
        self.exibir_resultado("Informe a ocasião e expectativas para consultar o métre.")
        self.entrada_comando.delete(0, tk.END)
        self.ocasiao.set("")
        self.expectativas.set("")
        self.cozinha.set("")
        self.dieta_entrada.set("")
        self.dieta_principal.set("")
        self.tipo_bebida.set("vinhos")

# ================== EXECUÇÃO ==================
if __name__ == "__main__":
    root = ttkb.Window(themename="flatly")
    app = HarmonizadorApp(root)
    root.mainloop()