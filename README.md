📜 README - Métre Digital (Harmonizador de Bebidas e Alimentos)
🍷 Visão Geral
O Métre Digital é um sistema inteligente que cria menus completos harmonizando bebidas com alimentos, simulando o conhecimento de um sommelier profissional. Esta versão simplificada oferece:

Recomendações personalizadas por ocasião (romântico, negócios, família etc.)

Harmonização automática de bebidas (vinhos, cervejas, sem álcool)

Explicações detalhadas sobre as combinações

Geração de menus com valores estimados

🛠️ Tecnologias Utilizadas
Python 3.8+

Tkinter (interface gráfica)

JSON (armazenamento de dados)

Random (seleção aleatória controlada)

📦 Instalação
Clone o repositório ou copie o arquivo metre_digital.py

Instale as dependências:

bash
Copy
pip install requests
🚀 Como Executar
bash
Copy
python metre_digital.py
🖥️ Funcionalidades Principais
1. Consulta ao Métre Digital
Analisa contexto (ocasião, expectativas)

Sugere menus completos com base em regras de harmonização

Explica as combinações como um sommelier profissional

2. Modo Manual
Permite selecionar:

Tipo de cozinha (italiana, francesa etc.)

Restrições dietéticas (vegetariano, vegano etc.)

Tipo de bebida preferida

3. Recursos Avançados
Sistema de fallback inteligente quando não encontra combinações perfeitas

Cálculo automático de valores

Exportação do menu para arquivo texto

🍽️ Exemplo de Saída
Copy
🍽️ MENU RECOMENDADO • 15/06/2023 19:30
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎉 Ocasião: Jantar Romântico
✨ Expectativas: Experiência Gourmet

Sugestão especial: Menu especial para uma noite romântica

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🍴 ENTRADA: Tábua de Queijos
   ├─ Estilo: Francesa
   ├─ Dieta: Vegetariana
   ├─ Intensidade: Média
   └─ Bebida: Prosecco (Espumante)
      ├─ Preço: R$120
      └─ Harmonização: Aperitivos

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🍲 PRATO PRINCIPAL: Filé Mignon
   ├─ Estilo: Francesa
   ├─ Dieta: Carnes
   ├─ Intensidade: Alta
   └─ Bebida: Malbec (Tinto)
      ├─ Preço: R$250
      └─ Harmonização: Carnes

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🍰 SOBREMESA ESPECIAL: Petit Gateau
   ├─ Estilo: Francesa
   ├─ Dieta: Vegetariana
   ├─ Bebida Alcoólica: Porto
   │  ├─ Tipo: Vinho Doce
   │  ├─ Preço: R$80
   │  └─ Dica: Servir quente com sorvete
   └─ Bebida Sem Álcool: Mocktail de Frutas
      ├─ Tipo: Coquetel
      └─ Preço: R$18

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💰 VALOR TOTAL DAS BEBIDAS: R$468.00
📝 Personalização
Edite os dicionários no início do arquivo para:

Adicionar novos pratos e bebidas

Modificar regras de harmonização

Ajustar preços e categorias

⚠️ Limitações
Banco de dados local (não conectado a APIs reais)

Versão simplificada para demonstração

📜 Licença
Projeto open-source para fins educacionais

🌟 Dica do Chef
Experimente combinar "Jantar de Negócios" com expectativa "Experiência Gourmet" para um menu impressionante!

