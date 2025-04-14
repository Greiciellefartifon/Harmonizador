import random
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
from datetime import datetime
import requests  # For API simulation

# ================== MOCK API FOR ONLINE SEARCHES ==================
def fetch_online_data(prato=None, bebida=None, gastronomia=None):
    """Simulates fetching data from an online API for prices and pairings"""
    mock_api_data = {
        "pratos": {
            "Bruschetta": {"preco": 35, "gastronomia": "italiana"},
            "Carpaccio": {"preco": 45, "gastronomia": "europeia"},
            "Tábua de Queijos": {"preco": 60, "gastronomia": "francesa"},
            "Filé Mignon": {"preco": 90, "gastronomia": "francesa"},
            "Risoto de Funghi": {"preco": 65, "gastronomia": "italiana"},
            "Salmão Grelhado": {"preco": 80, "gastronomia": "mediterrânea"},
            "Petit Gateau": {"preco": 30, "gastronomia": "francesa"},
        },
        "bebidas": {
            "Prosecco": {"preco": 130, "harmonizacao": ["Aperitivos", "Queijos"], "categoria": "vinhos"},
            "Malbec": {"preco": 260, "harmonizacao": ["Carnes", "Pratos fortes"], "categoria": "vinhos"},
            "Sauvignon Blanc": {"preco": 160, "harmonizacao": ["Peixes", "Saladas"], "categoria": "vinhos"},
            "IPA": {"preco": 30, "harmonizacao": ["Pratos fortes", "Carnes"], "categoria": "cervejas"},
            "Weissbier": {"preco": 25, "harmonizacao": ["Entradas", "Pratos leves"], "categoria": "cervejas"},
            "Porto": {"preco": 85, "harmonizacao": ["Sobremesas", "Doces"], "categoria": "digestivos"},
            "Amaretto": {"preco": 70, "harmonizacao": ["Doces", "Sobremesas"], "categoria": "digestivos"},
            "Mocktail de Frutas": {"preco": 20, "harmonizacao": ["Sobremesas", "Pratos leves"], "categoria": "sem_alcool"},
            "Suco de Uva": {"preco": 15, "harmonizacao": ["Geral"], "categoria": "sem_alcool"},
        },
        "gastronomias": {
            "italiana": ["Bruschetta", "Risoto de Funghi"],
            "francesa": ["Tábua de Queijos", "Filé Mignon", "Petit Gateau"],
            "mediterrânea": ["Salmão Grelhado"],
        }
    }
    
    try:
        if prato:
            return mock_api_data["pratos"].get(prato, {"preco": 50, "gastronomia": "desconhecida"})
        if bebida:
            return mock_api_data["bebidas"].get(bebida, {"preco": 30, "harmonizacao": ["Geral"], "categoria": "desconhecida"})
        if gastronomia:
            return {
                "pratos": mock_api_data["gastronomias"].get(gastronomia, []),
                "bebidas_sugeridas": mock_api_data["bebidas"]
            }
        return mock_api_data
    except Exception as e:
        return {"erro": f"Falha na busca online: {str(e)}"}

# ================== SISTEMA DE RECOMENDAÇÃO SIMULADO ==================
class SistemaIA:
    def __init__(self):
        self.sugestoes = {
            "Jantar Romântico": {
                "cozinha": "francesa",
                "dieta_entrada": "vegetariana",
                "dieta_principal": "carnes",
                "bebida": "vinhos",
                "sugestao_especial": "Menu especial para uma noite romântica"
            },
            "Aniversário": {
                "cozinha": "italiana",
                "dieta_entrada": None,
                "dieta_principal": None,
                "bebida": "vinhos",
                "sugestao_especial": "Celebre com sabores especiais"
            },
            "Jantar de Negócios": {
                "cozinha": "internacional",
                "dieta_entrada": "leve",
                "dieta_principal": None,
                "bebida": "vinhos",
                "sugestao_especial": "Menu profissional para impressionar"
            },
            "Família": {
                "cozinha": "brasileira",
                "dieta_entrada": None,
                "dieta_principal": None,
                "bebida": "sem_alcool",
                "sugestao_especial": "Sabores que agradam a toda família"
            },
            "Amigos": {
                "cozinha": None,
                "dieta_entrada": None,
                "dieta_principal": None,
                "bebida": "cervejas",
                "sugestao_especial": "Para compartilhar momentos especiais"
            },
            "Outro": {
                "cozinha": None,
                "dieta_entrada": None,
                "dieta_principal": None,
                "bebida": "vinhos",
                "sugestao_especial": "Sugestão do chef para ocasião especial"
            }
        }

    def analisar_contexto(self, comando, ocasiao, expectativas):
        sugestao = self.sugestoes.get(ocasiao, {
            "cozinha": None,
            "dieta_entrada": None,
            "dieta_principal": None,
            "bebida": "vinhos",
            "sugestao_especial": "Sugestão personalizada do chef"
        })
        
        if "vegetariano" in comando.lower():
            sugestao["dieta_entrada"] = "vegetariana"
            sugestao["dieta_principal"] = "vegetariana"
        elif "vegano" in comando.lower():
            sugestao["dieta_entrada"] = "vegana"
            sugestao["dieta_principal"] = "vegana"
        
        return sugestao

    def recomendar_sobremesa(self, contexto):
        sobremesas = [
            {
                "nome": "Petit Gateau",
                "tipo": "francesa",
                "dieta": "vegetariana",
                "harmonizacao": "Sorvete de baunilha",
                "intensidade": "alta",
                "dica_servico": "Servir quente com sorvete"
            },
            {
                "nome": "Tiramisu",
                "tipo": "italiana",
                "dieta": "vegetariana",
                "harmonizacao": "Vinho doce",
                "intensidade": "média",
                "dica_servico": "Servir gelado"
            }
        ]
        dieta = contexto.get("dieta_principal") or contexto.get("dieta_entrada")
        if dieta:
            opcoes = [s for s in sobremesas if s["dieta"] == dieta]
            return random.choice(opcoes) if opcoes else sobremesas[0]
        return random.choice(sobremesas)

    def explicar_harmonizacao(self, menu_completo):
        return (f"Este menu foi elaborado para {menu_completo['ocasiao']}. "
                f"A entrada {menu_completo['entrada']['nome']} prepara o paladar, "
                f"enquanto o {menu_completo['bebidas']['principal']['nome']} complementa o prato principal.")

# ================== BANCO DE DADOS GASTRONÔMICO ==================
cardapio = {
    "entradas": [
        {"nome": "Bruschetta", "tipo": "italiana", "dieta": "vegetariana", "intensidade": "leve"},
        {"nome": "Tábua de Queijos", "tipo": "francesa", "dieta": "vegetariana", "intensidade": "média"},
        {"nome": "Carpaccio", "tipo": "europeia", "dieta": "carnes", "intensidade": "média"},
    ],
    "principais": [
        {"nome": "Risoto de Funghi", "tipo": "italiana", "dieta": "vegetariana", "intensidade": "média"},
        {"nome": "Filé Mignon", "tipo": "francesa", "dieta": "carnes", "intensidade": "alta"},
        {"nome": "Salmão Grelhado", "tipo": "mediterrânea", "dieta": "peixes", "intensidade": "média"},
    ]
}

bebidas_base = {
    "vinhos": [
        {"nome": "Prosecco", "tipo": "espumante", "intensidade": "leve", "harmonizacao": "Aperitivos"},
        {"nome": "Malbec", "tipo": "tinto", "intensidade": "alta", "harmonizacao": "Carnes"},
        {"nome": "Sauvignon Blanc", "tipo": "branco", "intensidade": "leve", "harmonizacao": "Peixes"},
    ],
    "cervejas": [
        {"nome": "IPA", "tipo": "artesanal", "intensidade": "alta", "harmonizacao": "Pratos fortes"},
        {"nome": "Weissbier", "tipo": "trigo", "intensidade": "leve", "harmonizacao": "Entradas"},
    ],
    "digestivos": [
        {"nome": "Porto", "tipo": "vinho doce", "intensidade": "alta", "harmonizacao": "Sobremesas"},
        {"nome": "Amaretto", "tipo": "licor", "intensidade": "média", "harmonizacao": "Doces"},
    ],
    "sem_alcool": [
        {"nome": "Mocktail de Frutas", "tipo": "coquetel", "intensidade": "média", "harmonizacao": "Sobremesas"},
        {"nome": "Suco de Uva", "tipo": "suco", "intensidade": "leve", "harmonizacao": "Geral"},
    ]
}

# ================== LÓGICA DE HARMONIZAÇÃO ==================
def filtrar_itens(lista, filtros):
    resultado = lista
    if filtros.get("cozinha"):
        filtrados = [item for item in resultado if item["tipo"] == filtros["cozinha"]]
        if filtrados:
            resultado = filtrados
    if filtros.get("dieta"):
        filtrados = [item for item in resultado if item["dieta"] == filtros["dieta"]]
        if filtrados:
            resultado = filtrados
    return resultado

def recomendar_bebida(prato, tipo_bebida, cozinha=None):
    intensidade = prato["intensidade"]
    opcoes = bebidas_base.get(tipo_bebida, [])
    intensidade_map = {
        "leve": ["leve"],
        "média": ["leve", "média"],
        "alta": ["média", "alta"]
    }
    opcoes = [b for b in opcoes if b["intensidade"] in intensidade_map[intensidade]]
    
    # Fetch online pairing data
    online_data = fetch_online_data(prato=prato["nome"])
    if "harmonizacao" in online_data and opcoes:
        online_harmonizacoes = online_data["harmonizacao"]
        opcoes = [b for b in opcoes if any(h in online_harmonizacoes for h in b.get("harmonizacao", ["Geral"]))]
    
    if not opcoes:
        opcoes = bebidas_base.get(tipo_bebida, [])
    
    bebida = random.choice(opcoes) if opcoes else {"nome": "Seleção do Chef", "tipo": tipo_bebida, "harmonizacao": "Geral"}
    
    # Ensure harmonizacao exists
    bebida["harmonizacao"] = bebida.get("harmonizacao", "Geral")
    
    # Fetch price from API
    bebida_data = fetch_online_data(bebida=bebida["nome"])
    bebida["preco"] = bebida_data.get("preco", 30)
    
    return bebida

# ================== INTERFACE GRÁFICA ==================
class HarmonizadorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Métre Digital - Versão Atualizada")
        self.ia = SistemaIA()
        self.menu_gerado = None
        self.explicacao_detalhada = None
        self.sugestao_especial = None
        self.criar_interface()

    def criar_interface(self):
        self.root.geometry("1200x900")
        
        # Create notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tab 1: Manual Selection
        tab_manual = ttk.Frame(notebook)
        notebook.add(tab_manual, text="Seleção Manual")
        
        # Tab 2: Automatic Recommendation
        tab_auto = ttk.Frame(notebook)
        notebook.add(tab_auto, text="Métre Online")
        
        # === Manual Tab ===
        manual_frame = ttk.Frame(tab_manual, padding=20)
        manual_frame.pack(fill=tk.BOTH, expand=True)
        
        # Context Section
        context_frame = ttk.LabelFrame(manual_frame, text="Contexto da Refeição", padding=10)
        context_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(context_frame, text="Ocasião:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.ocasiao = ttk.Combobox(context_frame, values=["Jantar Romântico", "Aniversário", "Jantar de Negócios", "Família", "Amigos", "Outro"])
        self.ocasiao.grid(row=0, column=1, sticky=tk.EW, padx=5)
        
        ttk.Label(context_frame, text="Expectativas:").grid(row=1, column=0, sticky=tk.W, padx=5)
        self.expectativas = ttk.Combobox(context_frame, values=["Refeição Leve", "Experiência Gourmet", "Confort Food", "Culinária Internacional"])
        self.expectativas.grid(row=1, column=1, sticky=tk.EW, padx=5)
        
        # Command Section
        ttk.Label(manual_frame, text="Comando Específico:").pack(pady=(10,0))
        self.entrada_comando = ttk.Entry(manual_frame, width=80)
        self.entrada_comando.pack(pady=5)
        
        # Preferences Section
        control_frame = ttk.LabelFrame(manual_frame, text="Preferências", padding=10)
        control_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(control_frame, text="Cozinha:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.cozinha = ttk.Combobox(control_frame, values=["", "italiana", "francesa", "mediterrânea", "brasileira"])
        self.cozinha.grid(row=0, column=1, sticky=tk.EW, padx=5)
        
        ttk.Label(control_frame, text="Bebida:").grid(row=1, column=0, sticky=tk.W, padx=5)
        self.tipo_bebida = ttk.Combobox(control_frame, values=["vinhos", "cervejas", "digestivos", "sem_alcool"])
        self.tipo_bebida.grid(row=1, column=1, sticky=tk.EW, padx=5)
        self.tipo_bebida.set("vinhos")
        
        ttk.Label(control_frame, text="Dieta Entrada:").grid(row=2, column=0, sticky=tk.W, padx=5)
        self.dieta_entrada = ttk.Combobox(control_frame, values=["", "vegetariana", "carnes", "peixes"])
        self.dieta_entrada.grid(row=2, column=1, sticky=tk.EW, padx=5)
        
        ttk.Label(control_frame, text="Dieta Principal:").grid(row=3, column=0, sticky=tk.W, padx=5)
        self.dieta_principal = ttk.Combobox(control_frame, values=["", "vegetariana", "carnes", "peixes"])
        self.dieta_principal.grid(row=3, column=1, sticky=tk.EW, padx=5)
        
        # Action Buttons
        btn_frame = ttk.Frame(manual_frame)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Gerar Menu", command=self.consultar_metre).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Limpar", command=self.limpar_tela).pack(side=tk.LEFT, padx=5)
        
        # Result Area
        self.resultado_manual = scrolledtext.ScrolledText(manual_frame, wrap=tk.WORD, height=20, font=('Arial', 11))
        self.resultado_manual.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # === Automatic Tab ===
        auto_frame = ttk.Frame(tab_auto, padding=20)
        auto_frame.pack(fill=tk.BOTH, expand=True)
        
        # Occasion Selection
        auto_context_frame = ttk.LabelFrame(auto_frame, text="Seleção de Ocasião", padding=10)
        auto_context_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(auto_context_frame, text="Ocasião:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.ocasiao_auto = ttk.Combobox(auto_context_frame, values=["Jantar Romântico", "Aniversário", "Jantar de Negócios", "Família", "Amigos", "Outro"])
        self.ocasiao_auto.grid(row=0, column=1, sticky=tk.EW, padx=5)
        self.ocasiao_auto.set("Jantar Romântico")
        
        ttk.Button(auto_frame, text="Consultar Métre Online", command=self.consultar_metre_online).pack(pady=10)
        
        self.resultado_auto = scrolledtext.ScrolledText(auto_frame, wrap=tk.WORD, height=25, font=('Arial', 11))
        self.resultado_auto.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Secondary Buttons
        btn_auto_frame = ttk.Frame(auto_frame)
        btn_auto_frame.pack(pady=10)
        
        ttk.Button(btn_auto_frame, text="Salvar Menu", command=self.salvar_menu).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_auto_frame, text="Explicação", command=self.mostrar_explicacao).pack(side=tk.LEFT, padx=5)
        
        # Initial Message
        self.exibir_resultado_manual("Selecione suas preferências e clique em 'Gerar Menu'.")
        self.exibir_resultado_auto("Escolha a ocasião e clique em 'Consultar Métre Online' para recomendações automáticas.")

    def consultar_metre(self):
        try:
            ocasiao = self.ocasiao.get()
            expectativas = self.expectativas.get()
            comando = self.entrada_comando.get().strip()
            
            if not ocasiao or not expectativas:
                raise ValueError("Informe ocasião e expectativas!")
            
            contexto_ia = self.ia.analisar_contexto(comando, ocasiao, expectativas)
            cozinha = self.cozinha.get() or contexto_ia.get("cozinha")
            dieta_entrada = self.dieta_entrada.get() or contexto_ia.get("dieta_entrada")
            dieta_principal = self.dieta_principal.get() or contexto_ia.get("dieta_principal")
            tipo_bebida = self.tipo_bebida.get() or contexto_ia.get("bebida", "vinhos")
            self.sugestao_especial = contexto_ia.get("sugestao_especial")
            
            self.gerar_menu(cozinha, dieta_entrada, dieta_principal, tipo_bebida, ocasiao, expectativas, manual=True)
            
        except Exception as e:
            self.exibir_resultado_manual(f"⚠️ Erro: {str(e)}")

    def consultar_metre_online(self):
        try:
            ocasiao = self.ocasiao_auto.get()
            if not ocasiao:
                raise ValueError("Selecione uma ocasião!")
            
            # Randomly select expectations for variety
            expectativas = random.choice(["Experiência Gourmet", "Refeição Leve", "Confort Food"])
            contexto_ia = self.ia.analisar_contexto("", ocasiao, expectativas)
            
            cozinha = contexto_ia.get("cozinha")
            dieta_entrada = contexto_ia.get("dieta_entrada")
            dieta_principal = contexto_ia.get("dieta_principal")
            tipo_bebida = contexto_ia.get("bebida", "vinhos")
            self.sugestao_especial = contexto_ia.get("sugestao_especial")
            
            self.gerar_menu(cozinha, dieta_entrada, dieta_principal, tipo_bebida, ocasiao, expectativas, manual=False)
            
        except Exception as e:
            self.exibir_resultado_auto(f"⚠️ Erro: {str(e)}")

    def gerar_menu(self, cozinha, dieta_entrada, dieta_principal, tipo_bebida, ocasiao, expectativas, manual=True):
        entrada = self.selecionar_com_fallback("entradas", cozinha, dieta_entrada)
        principal = self.selecionar_com_fallback("principais", cozinha, dieta_principal)
        
        contexto_sobremesa = {
            "ocasiao": ocasiao,
            "expectativas": expectativas,
            "cozinha": cozinha,
            "dieta_entrada": dieta_entrada,
            "dieta_principal": dieta_principal
        }
        sobremesa = self.ia.recomendar_sobremesa(contexto_sobremesa)
        
        # Fetch online prices
        entrada_preco = fetch_online_data(prato=entrada["nome"])["preco"]
        principal_preco = fetch_online_data(prato=principal["nome"])["preco"]
        sobremesa_preco = fetch_online_data(prato=sobremesa["nome"])["preco"]
        
        bebidas = {
            "entrada": recomendar_bebida(entrada, tipo_bebida, cozinha),
            "principal": recomendar_bebida(principal, tipo_bebida, cozinha),
            "sobremesa_alcool": recomendar_bebida(sobremesa, "digestivos", cozinha),
            "sobremesa_sem_alcool": recomendar_bebida(sobremesa, "sem_alcool", cozinha)
        }
        
        # Calculate total cost
        valor_total = (entrada_preco + principal_preco + sobremesa_preco +
                       sum(b.get("preco", 0) for b in bebidas.values()))
        
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
        self.menu_gerado = self.formatar_menu(menu_completo, entrada_preco, principal_preco, sobremesa_preco)
        
        if manual:
            self.exibir_resultado_manual(self.menu_gerado)
        else:
            self.exibir_resultado_auto(self.menu_gerado)

    def selecionar_com_fallback(self, categoria, cozinha, dieta):
        filtros = {}
        if cozinha:
            filtros["cozinha"] = cozinha
        if dieta:
            filtros["dieta"] = dieta
        
        itens = filtrar_itens(cardapio[categoria], filtros)
        if not itens:
            itens = cardapio[categoria]
        return random.choice(itens)

    def formatar_menu(self, menu, entrada_preco, principal_preco, sobremesa_preco):
        data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")
        texto = f"""🍽️ *MENU RECOMENDADO* • {data_atual}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎉 *Ocasião*: {menu['ocasiao']}
✨ *Expectativas*: {menu['expectativas']}

{self.sugestao_especial or "Sugestão especial: Uma experiência única!"}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🍴 *ENTRADA*: {menu['entrada']['nome']}
   ├─ *Estilo*: {menu['entrada']['tipo'].title()}
   ├─ *Dieta*: {menu['entrada']['dieta'].title()}
   ├─ *Preço*: R${entrada_preco}
   └─ *Bebida*: {menu['bebidas']['entrada']['nome']}
      ├─ *Preço*: R${menu['bebidas']['entrada']['preco']}
      └─ *Harmonização*: {menu['bebidas']['entrada']['harmonizacao']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🍲 *PRATO PRINCIPAL*: {menu['principal']['nome']}
   ├─ *Estilo*: {menu['principal']['tipo'].title()}
   ├─ *Dieta*: {menu['principal']['dieta'].title()}
   ├─ *Preço*: R${principal_preco}
   └─ *Bebida*: {menu['bebidas']['principal']['nome']}
      ├─ *Preço*: R${menu['bebidas']['principal']['preco']}
      └─ *Harmonização*: {menu['bebidas']['principal']['harmonizacao']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🍰 *SOBREMESA*: {menu['sobremesa']['nome']}
   ├─ *Estilo*: {menu['sobremesa']['tipo'].title()}
   ├─ *Dieta*: {menu['sobremesa']['dieta'].title()}
   ├─ *Preço*: R${sobremesa_preco}
   ├─ *Bebida Alcoólica*: {menu['bebidas']['sobremesa_alcool']['nome']}
   │  ├─ *Preço*: R${menu['bebidas']['sobremesa_alcool']['preco']}
   │  └─ *Harmonização*: {menu['bebidas']['sobremesa_alcool']['harmonizacao']}
   └─ *Bebida Sem Álcool*: {menu['bebidas']['sobremesa_sem_alcool']['nome']}
      ├─ *Preço*: R${menu['bebidas']['sobremesa_sem_alcool']['preco']}
      └─ *Harmonização*: {menu['bebidas']['sobremesa_sem_alcool']['harmonizacao']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💰 *VALOR TOTAL*: R${menu['valor_total']:.2f}"""
        return texto

    def mostrar_explicacao(self):
        if not self.explicacao_detalhada:
            messagebox.showwarning("Aviso", "Gere um menu primeiro!")
            return
        explicacao_window = tk.Toplevel(self.root)
        explicacao_window.title("Explicação do Métre")
        text_area = scrolledtext.ScrolledText(explicacao_window, wrap=tk.WORD, font=('Arial', 11))
        text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text_area.insert(tk.END, self.explicacao_detalhada)
        ttk.Button(explicacao_window, text="Fechar", command=explicacao_window.destroy).pack(pady=10)

    def salvar_menu(self):
        if not self.menu_gerado:
            messagebox.showerror("Erro", "Nenhum menu para salvar!")
            return
        filename = f"menu_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(self.menu_gerado)
            if self.explicacao_detalhada:
                f.write("\n\n=== ANÁLISE DO MÉTRE ===\n" + self.explicacao_detalhada)
        messagebox.showinfo("Sucesso", f"Menu salvo como '{filename}'")

    def exibir_resultado_manual(self, texto):
        self.resultado_manual.config(state=tk.NORMAL)
        self.resultado_manual.delete(1.0, tk.END)
        self.resultado_manual.insert(tk.END, texto)
        self.resultado_manual.config(state=tk.DISABLED)

    def exibir_resultado_auto(self, texto):
        self.resultado_auto.config(state=tk.NORMAL)
        self.resultado_auto.delete(1.0, tk.END)
        self.resultado_auto.insert(tk.END, texto)
        self.resultado_auto.config(state=tk.DISABLED)

    def limpar_tela(self):
        self.menu_gerado = None
        self.explicacao_detalhada = None
        self.sugestao_especial = None
        self.exibir_resultado_manual("Selecione suas preferências e clique em 'Gerar Menu'.")
        self.entrada_comando.delete(0, tk.END)
        self.ocasiao.set("")
        self.expectativas.set("")
        self.cozinha.set("")
        self.dieta_entrada.set("")
        self.dieta_principal.set("")
        self.tipo_bebida.set("vinhos")

# ================== EXECUÇÃO ==================
if __name__ == "__main__":
    root = tk.Tk()
    app = HarmonizadorApp(root)
    root.mainloop()