import random
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
from datetime import datetime

# ================== SISTEMA DE RECOMENDAÇÃO SIMULADO ==================
class SistemaIA:
    def __init__(self):
        # Dicionário de sugestões pré-definidas para simular a IA
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
        """Simula a análise de contexto com sugestões pré-definidas"""
        sugestao = self.sugestoes.get(ocasiao, {
            "cozinha": None,
            "dieta_entrada": None,
            "dieta_principal": None,
            "bebida": "vinhos",
            "sugestao_especial": "Sugestão personalizada do chef"
        })
        
        # Ajusta com base no comando específico
        if "vegetariano" in comando.lower():
            sugestao["dieta_entrada"] = "vegetariana"
            sugestao["dieta_principal"] = "vegetariana"
        elif "vegano" in comando.lower():
            sugestao["dieta_entrada"] = "vegana"
            sugestao["dieta_principal"] = "vegana"
        
        return sugestao

    def recomendar_sobremesa(self, contexto):
        """Gera recomendações de sobremesa baseadas no contexto"""
        sobremesas = [
            {
                "nome": "Tiramisu",
                "tipo": "italiana",
                "dieta": "vegetariana",
                "harmonizacao": "Vinho doce ou café expresso",
                "intensidade": "média",
                "dica_servico": "Servir gelado"
            },
            {
                "nome": "Petit Gateau",
                "tipo": "francesa",
                "dieta": "vegetariana",
                "harmonizacao": "Sorvete de baunilha",
                "intensidade": "alta",
                "dica_servico": "Servir quente com sorvete"
            },
            {
                "nome": "Mousse de Chocolate Vegano",
                "tipo": "internacional",
                "dieta": "vegana",
                "harmonizacao": "Frutas vermelhas",
                "intensidade": "leve",
                "dica_servico": "Decorar com folhas de hortelã"
            },
            {
                "nome": "Cheesecake de Frutas",
                "tipo": "americana",
                "dieta": "vegetariana",
                "harmonizacao": "Calda de frutas",
                "intensidade": "média",
                "dica_servico": "Servir em fatias generosas"
            }
        ]
        
        # Filtra por dieta se especificado
        dieta = contexto.get("dieta_principal") or contexto.get("dieta_entrada")
        if dieta:
            opcoes = [s for s in sobremesas if s["dieta"] == dieta]
            return random.choice(opcoes) if opcoes else sobremesas[0]
        
        return random.choice(sobremesas)

    def explicar_harmonizacao(self, menu_completo):
        """Gera explicação detalhada simulada"""
        explicacoes = [
            f"Este menu foi cuidadosamente elaborado para a ocasião {menu_completo['ocasiao']}. "
            f"A entrada {menu_completo['entrada']['nome']} prepara o paladar para o prato principal "
            f"{menu_completo['principal']['nome']}, criando uma progressão harmoniosa de sabores. "
            "Recomendamos servir as bebidas na temperatura adequada para melhor apreciação.",
            
            f"Para {menu_completo['expectativas']}, este menu combina perfeitamente. "
            f"A sobremesa {menu_completo['sobremesa']['nome']} finaliza a experiência com um toque especial. "
            "Sugerimos degustar cada prato com calma para apreciar todos os sabores.",
            
            f"Harmonização perfeita para {menu_completo['ocasiao']}. "
            f"O {menu_completo['bebidas']['entrada']['nome']} acompanha maravilhosamente a entrada, "
            f"enquanto o {menu_completo['bebidas']['principal']['nome']} complementa o prato principal. "
            "Uma experiência gastronômica equilibrada e memorável."
        ]
        
        return random.choice(explicacoes)

# ================== BANCO DE DADOS GASTRONÔMICO ==================
cardapio = {
    "entradas": [
        {"nome": "Bruschetta", "tipo": "italiana", "dieta": "vegetariana", "intensidade": "leve"},
        {"nome": "Carpaccio", "tipo": "europeia", "dieta": "carnes", "intensidade": "média"},
        {"nome": "Salada Caesar", "tipo": "americana", "dieta": "vegetariana", "intensidade": "leve"},
        {"nome": "Tábua de Queijos", "tipo": "francesa", "dieta": "vegetariana", "intensidade": "média"},
        {"nome": "Bolinhos de Bacalhau", "tipo": "portuguesa", "dieta": "peixes", "intensidade": "média"},
        {"nome": "Canapés Variados", "tipo": "internacional", "dieta": "vegetariana", "intensidade": "leve"},
        {"nome": "Terrine de Legumes", "tipo": "francesa", "dieta": "vegana", "intensidade": "leve"}
    ],
    "principais": [
        {"nome": "Risoto de Funghi", "tipo": "italiana", "dieta": "vegetariana", "intensidade": "média"},
        {"nome": "Filé Mignon", "tipo": "francesa", "dieta": "carnes", "intensidade": "alta"},
        {"nome": "Salmão Grelhado", "tipo": "mediterrânea", "dieta": "peixes", "intensidade": "média"},
        {"nome": "Lasagna", "tipo": "italiana", "dieta": "carnes", "intensidade": "alta"},
        {"nome": "Ratatouille", "tipo": "francesa", "dieta": "vegana", "intensidade": "leve"},
        {"nome": "Feijoada Light", "tipo": "brasileira", "dieta": "carnes", "intensidade": "alta"},
        {"nome": "Curry Vegetariano", "tipo": "indiana", "dieta": "vegana", "intensidade": "média"}
    ]
}

bebidas_base = {
    "vinhos": [
        {"nome": "Prosecco", "tipo": "espumante", "intensidade": "leve", "harmonizacao": "Aperitivos", "preco": 120},
        {"nome": "Chianti", "tipo": "tinto", "intensidade": "média", "harmonizacao": "Massas", "preco": 180},
        {"nome": "Malbec", "tipo": "tinto", "intensidade": "alta", "harmonizacao": "Carnes", "preco": 250},
        {"nome": "Sauvignon Blanc", "tipo": "branco", "intensidade": "leve", "harmonizacao": "Peixes", "preco": 150}
    ],
    "cervejas": [
        {"nome": "Weissbier", "tipo": "trigo", "intensidade": "leve", "harmonizacao": "Entradas", "preco": 25},
        {"nome": "IPA", "tipo": "artesanal", "intensidade": "alta", "harmonizacao": "Pratos fortes", "preco": 30},
        {"nome": "Stout", "tipo": "escura", "intensidade": "alta", "harmonizacao": "Carnes", "preco": 28}
    ],
    "sem_alcool": [
        {"nome": "Suco de Uva", "tipo": "suco", "intensidade": "leve", "harmonizacao": "Geral", "preco": 15},
        {"nome": "Água Aromatizada", "tipo": "água", "intensidade": "leve", "harmonizacao": "Geral", "preco": 10},
        {"nome": "Mocktail de Frutas", "tipo": "coquetel", "intensidade": "média", "harmonizacao": "Sobremesas", "preco": 18}
    ],
    "digestivos": [
        {"nome": "Porto", "tipo": "vinho doce", "intensidade": "alta", "harmonizacao": "Sobremesas", "preco": 80},
        {"nome": "Licor de Chocolate", "tipo": "licor", "intensidade": "alta", "harmonizacao": "Sobremesas", "preco": 65},
        {"nome": "Amaretto", "tipo": "licor", "intensidade": "média", "harmonizacao": "Doces", "preco": 70}
    ]
}

# ================== LÓGICA DE HARMONIZAÇÃO ==================
def filtrar_itens(lista, filtros):
    """Filtra itens com fallback inteligente"""
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
    """Recomenda bebida com fallback seguro"""
    try:
        intensidade = prato["intensidade"]
        opcoes = bebidas_base.get(tipo_bebida, [])
        
        intensidade_map = {
            "leve": ["leve"],
            "média": ["leve", "média"],
            "alta": ["média", "alta"]
        }
        
        opcoes = [b for b in opcoes if b["intensidade"] in intensidade_map[intensidade]]
        
        if cozinha and tipo_bebida in ["vinhos", "cervejas"]:
            opcoes_cozinha = [b for b in opcoes if b.get("tipo", "") == cozinha]
            if opcoes_cozinha:
                opcoes = opcoes_cozinha
        
        return random.choice(opcoes) if opcoes else None
        
    except Exception as e:
        print(f"Erro na harmonização: {e}")
        return {
            "nome": "Seleção do Chef",
            "tipo": tipo_bebida,
            "preco": 0,
            "harmonizacao": "Harmonização equilibrada"
        }

# ================== INTERFACE GRÁFICA ==================
class HarmonizadorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Métre Digital - Versão Simplificada")
        self.ia = SistemaIA()
        self.criar_interface()

    def criar_interface(self):
        """Cria toda a interface gráfica"""
        self.root.geometry("1100x850")
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Seção de contexto
        context_frame = ttk.LabelFrame(main_frame, text="Contexto da Refeição", padding=10)
        context_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(context_frame, text="Ocasião:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.ocasiao = ttk.Combobox(context_frame, values=["Jantar Romântico", "Aniversário", "Jantar de Negócios", "Família", "Amigos", "Outro"])
        self.ocasiao.grid(row=0, column=1, sticky=tk.EW, padx=5)
        
        ttk.Label(context_frame, text="Expectativas:").grid(row=1, column=0, sticky=tk.W, padx=5)
        self.expectativas = ttk.Combobox(context_frame, values=["Refeição Leve", "Experiência Gourmet", "Confort Food", "Culinária Internacional", "Surpresa do Chef"])
        self.expectativas.grid(row=1, column=1, sticky=tk.EW, padx=5)
        
        # Seção de comando
        ttk.Label(main_frame, text="Comando Específico (opcional):").pack(pady=(10,0))
        self.entrada_comando = ttk.Entry(main_frame, width=80, font=('Arial', 11))
        self.entrada_comando.pack(pady=5)
        
        # Controles manuais
        control_frame = ttk.LabelFrame(main_frame, text="Preferências Manuais", padding=10)
        control_frame.pack(fill=tk.X, pady=10)
        
        # Linha 1 - Cozinha e Bebida
        linha1 = ttk.Frame(control_frame)
        linha1.pack(fill=tk.X, pady=5)
        
        ttk.Label(linha1, text="Cozinha:").pack(side=tk.LEFT, padx=5)
        self.cozinha = ttk.Combobox(linha1, values=["", "italiana", "francesa", "americana", "mediterrânea", "portuguesa", "brasileira", "japonesa"])
        self.cozinha.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        
        ttk.Label(linha1, text="Bebida:").pack(side=tk.LEFT, padx=5)
        self.tipo_bebida = ttk.Combobox(linha1, values=["vinhos", "cervejas", "sem_alcool"])
        self.tipo_bebida.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        self.tipo_bebida.set("vinhos")
        
        # Linha 2 - Dietas
        linha2 = ttk.Frame(control_frame)
        linha2.pack(fill=tk.X, pady=5)
        
        ttk.Label(linha2, text="Dieta Entrada:").pack(side=tk.LEFT, padx=5)
        self.dieta_entrada = ttk.Combobox(linha2, values=["", "vegetariana", "vegana", "carnes", "peixes"])
        self.dieta_entrada.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        
        ttk.Label(linha2, text="Dieta Principal:").pack(side=tk.LEFT, padx=5)
        self.dieta_principal = ttk.Combobox(linha2, values=["", "vegetariana", "vegana", "carnes", "peixes"])
        self.dieta_principal.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        
        # Botões de ação
        btn_action_frame = ttk.Frame(control_frame)
        btn_action_frame.pack(pady=10)
        
        ttk.Button(btn_action_frame, text="Consultar Métre", command=self.consultar_metre, 
                  style="Accent.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_action_frame, text="Gerar Menu Manual", command=self.gerar_menu_manual).pack(side=tk.LEFT, padx=5)
        
        # Área de resultado
        self.resultado = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, padx=15, pady=15, 
                                                 font=('Arial', 11), height=25)
        self.resultado.pack(fill=tk.BOTH, expand=True)
        
        # Botões de ação secundários
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Salvar Menu", command=self.salvar_menu).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Limpar", command=self.limpar_tela).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Explicação do Métre", command=self.mostrar_explicacao).pack(side=tk.LEFT, padx=5)
        
        # Variáveis para armazenamento
        self.menu_gerado = None
        self.explicacao_detalhada = None
        self.sugestao_especial = None
        
        # Mensagem inicial
        self.exibir_resultado(
            "Bem-vindo ao Métre Digital (Versão Simplificada)!\n\n"
            "Como usar:\n"
            "1. Informe a ocasião e expectativas\n"
            "2. Adicione comandos específicos se desejar\n"
            "3. Ajuste preferências manuais se necessário\n"
            "4. Escolha:\n"
            "   - 'Consultar Métre' para recomendações completas\n"
            "   - 'Gerar Menu Manual' para controle total\n\n"
            "O sistema irá:\n"
            "- Sugerir um menu completo e harmonizado\n"
            "- Recomendar sobremesa especial\n"
            "- Explicar a harmonização como um métre experiente"
        )
        
        # Configurar estilo
        style = ttk.Style()
        style.configure("Accent.TButton", foreground="white", background="#4a6da7", font=('Arial', 10, 'bold'))

    def consultar_metre(self):
        """Consulta o métre digital para recomendações completas"""
        try:
            # Obter contexto
            ocasiao = self.ocasiao.get()
            expectativas = self.expectativas.get()
            comando = self.entrada_comando.get().strip()
            
            if not ocasiao or not expectativas:
                raise ValueError("Informe pelo menos a ocasião e expectativas!")
            
            # Analisar contexto com IA simulada
            contexto_ia = self.ia.analisar_contexto(comando, ocasiao, expectativas)
            
            if contexto_ia.get("erro"):
                raise ValueError(contexto_ia["erro"])
            
            # Mesclar preferências manuais com sugestões simuladas
            cozinha = self.cozinha.get() or contexto_ia.get("cozinha")
            dieta_entrada = self.dieta_entrada.get() or contexto_ia.get("dieta_entrada")
            dieta_principal = self.dieta_principal.get() or contexto_ia.get("dieta_principal")
            tipo_bebida = self.tipo_bebida.get() or contexto_ia.get("bebida", "vinhos")
            self.sugestao_especial = contexto_ia.get("sugestao_especial")
            
            # Gerar menu com os parâmetros
            self.gerar_menu(cozinha, dieta_entrada, dieta_principal, tipo_bebida, ocasiao, expectativas)
            
        except Exception as e:
            self.exibir_resultado(f"⚠️ Métre informa: {str(e)}\n\nPor favor, ajuste seus critérios e consulte novamente.")

    def gerar_menu_manual(self):
        """Gera menu baseado apenas nas seleções manuais"""
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
            self.exibir_resultado(f"⚠️ Erro ao gerar menu: {str(e)}\n\nPreencha pelo menos o tipo de bebida.")

    def gerar_menu(self, cozinha, dieta_entrada, dieta_principal, tipo_bebida, ocasiao, expectativas):
        """Lógica central para gerar o menu"""
        # Filtrar entradas e principais com fallback seguro
        entrada = self.selecionar_com_fallback("entradas", cozinha, dieta_entrada)
        principal = self.selecionar_com_fallback("principais", cozinha, dieta_principal)
        
        # Contexto para sobremesa
        contexto_sobremesa = {
            "ocasiao": ocasiao,
            "expectativas": expectativas,
            "cozinha": cozinha,
            "dieta_entrada": dieta_entrada,
            "dieta_principal": dieta_principal
        }
        
        # Recomendar sobremesa com IA simulada
        sobremesa = self.ia.recomendar_sobremesa(contexto_sobremesa)
        
        # Harmonizar bebidas
        bebidas = {
            "entrada": recomendar_bebida(entrada, tipo_bebida, cozinha),
            "principal": recomendar_bebida(principal, tipo_bebida, cozinha),
            "sobremesa_alcool": random.choice(bebidas_base["digestivos"]),
            "sobremesa_sem_alcool": random.choice(bebidas_base["sem_alcool"])
        }
        
        # Calcular valor total
        valor_total = sum(b.get("preco", 0) for b in bebidas.values())
        
        # Preparar menu completo
        menu_completo = {
            "ocasiao": ocasiao,
            "expectativas": expectativas,
            "entrada": entrada,
            "principal": principal,
            "sobremesa": sobremesa,
            "bebidas": bebidas,
            "valor_total": valor_total
        }
        
        # Gerar explicação detalhada simulada
        self.explicacao_detalhada = self.ia.explicar_harmonizacao(menu_completo)
        
        # Formatar menu
        self.menu_gerado = self.formatar_menu(menu_completo)
        self.exibir_resultado(self.menu_gerado)

    def selecionar_com_fallback(self, categoria, cozinha, dieta):
        """Seleciona prato com sistema de fallback inteligente"""
        # Tentativa 1: Com todos os filtros
        filtros = {}
        if cozinha:
            filtros["cozinha"] = cozinha
        if dieta:
            filtros["dieta"] = dieta
        
        itens = filtrar_itens(cardapio[categoria], filtros)
        
        # Tentativa 2: Apenas cozinha
        if not itens and cozinha:
            itens = filtrar_itens(cardapio[categoria], {"cozinha": cozinha})
        
        # Tentativa 3: Apenas dieta
        if not itens and dieta:
            itens = filtrar_itens(cardapio[categoria], {"dieta": dieta})
        
        # Tentativa 4: Sem filtros
        if not itens:
            itens = cardapio[categoria]
        
        return random.choice(itens)

    def formatar_menu(self, menu):
        """Formata o menu de forma profissional"""
        data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")
        
        texto = f"""🍽️ *MENU RECOMENDADO* • {data_atual}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎉 *Ocasião*: {menu['ocasiao']}
✨ *Expectativas*: {menu['expectativas']}

{self.sugestao_especial or "Sugestão especial: Aproveite cada momento desta experiência gastronômica"}

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
🍰 *SOBREMESA ESPECIAL*: {menu['sobremesa']['nome']}
   ├─ *Estilo*: {menu['sobremesa']['tipo'].title()}
   ├─ *Dieta*: {menu['sobremesa']['dieta'].title()}
   ├─ *Bebida Alcoólica*: {menu['bebidas']['sobremesa_alcool']['nome']}
   │  ├─ *Tipo*: {menu['bebidas']['sobremesa_alcool']['tipo'].title()}
   │  ├─ *Preço*: R${menu['bebidas']['sobremesa_alcool'].get('preco', '--')}
   │  └─ *Dica*: {menu['sobremesa'].get('dica_servico', 'Servir em temperatura ambiente')}
   └─ *Bebida Sem Álcool*: {menu['bebidas']['sobremesa_sem_alcool']['nome']}
      ├─ *Tipo*: {menu['bebidas']['sobremesa_sem_alcool']['tipo'].title()}
      └─ *Preço*: R${menu['bebidas']['sobremesa_sem_alcool'].get('preco', '--')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💰 *VALOR TOTAL DAS BEBIDAS*: R${menu['valor_total']:.2f}

🔍 *Detalhes*:
   ├─ *Cozinha*: {menu['entrada']['tipo'].title()} / {menu['principal']['tipo'].title()}
   ├─ *Dieta Entrada*: {menu['entrada']['dieta'].title()}
   └─ *Dieta Principal*: {menu['principal']['dieta'].title()}"""
        
        return texto

    def mostrar_explicacao(self):
        """Exibe a explicação detalhada do métre"""
        if not self.explicacao_detalhada:
            messagebox.showwarning("Aviso", "Gere um menu primeiro para ver a explicação!")
            return
        
        explicacao_window = tk.Toplevel(self.root)
        explicacao_window.title("Explicação do Métre")
        explicacao_window.geometry("900x700")
        
        text_area = scrolledtext.ScrolledText(explicacao_window, wrap=tk.WORD, 
                                            padx=15, pady=15, font=('Arial', 11))
        text_area.pack(fill=tk.BOTH, expand=True)
        
        text_area.insert(tk.END, "🧑‍🍳 *ANÁLISE DO MÉTRE* 🍷\n\n")
        text_area.insert(tk.END, self.explicacao_detalhada)
        
        ttk.Button(explicacao_window, text="Fechar", 
                  command=explicacao_window.destroy).pack(pady=10)

    def salvar_menu(self):
        """Salva o menu em arquivo"""
        if not self.menu_gerado:
            messagebox.showerror("Erro", "Nenhum menu para salvar!")
            return
        
        try:
            filename = f"menu_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(self.menu_gerado)
                
                if self.explicacao_detalhada:
                    f.write("\n\n=== ANÁLISE DO MÉTRE ===\n\n")
                    f.write(self.explicacao_detalhada)
                
                if self.sugestao_especial:
                    f.write("\n\n=== SUGESTÃO ESPECIAL ===\n\n")
                    f.write(self.sugestao_especial)
            
            messagebox.showinfo("Sucesso", f"Menu salvo como '{filename}'")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar: {str(e)}")

    def exibir_resultado(self, texto):
        """Exibe texto na área de resultados"""
        self.resultado.config(state=tk.NORMAL)
        self.resultado.delete(1.0, tk.END)
        self.resultado.insert(tk.END, texto)
        self.resultado.config(state=tk.DISABLED)

    def limpar_tela(self):
        """Limpa a tela e reseta o menu"""
        self.menu_gerado = None
        self.explicacao_detalhada = None
        self.sugestao_especial = None
        self.exibir_resultado(
            "Informe a ocasião e expectativas para consultar o métre digital."
        )
        self.entrada_comando.delete(0, tk.END)
        self.ocasiao.set("")
        self.expectativas.set("")
        self.cozinha.set("")
        self.dieta_entrada.set("")
        self.dieta_principal.set("")
        self.tipo_bebida.set("vinhos")

# ================== EXECUÇÃO ==================
if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = HarmonizadorApp(root)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Erro Inesperado", f"O programa encontrou um erro: {str(e)}")