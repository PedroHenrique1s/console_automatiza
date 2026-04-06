#  Automação de Análise de Logs - Protheus com IA (Gemini)

Este projeto é uma automação em Python desenvolvida para ler arquivos de log gigantes (`console.log`) do servidor Protheus, extrair blocos específicos de erro (`THREAD ERROR`), processar esses dados utilizando a Inteligência Artificial do Google Gemini e disparar um relatório formatado em HTML por e-mail.

## 🚀 Funcionalidades

- **Extração Inteligente:** Lê arquivos de log pesados sem sobrecarregar a memória RAM, fatiando apenas os blocos que contêm erros.
- **Integração com IA:** Envia os blocos extraídos para a API do Google Gemini (Flash) para gerar uma análise limpa e estruturada.
- **Notificação por E-mail:** Dispara automaticamente o relatório em HTML para os responsáveis através de SMTP.
- **Organização Local:** Salva um backup em HTML de todas as análises geradas na pasta `/atas_salvas`.

---

## 📁 Estrutura do Projeto

```text
/
├── main.py                 # Arquivo principal que orquestra a automação
├── envio_email.py          # Módulo responsável pelo disparo de e-mails via SMTP
├── requirements.txt        # Lista de dependências do Python
├── .env                    # Arquivo de configuração (Senhas e API Keys) - NÃO COMMITAR
├── shared/
│   ├── prompt_ia.py        # Módulo de comunicação com a API do Google Gemini
│   └── filtra_log.py       # Algoritmo de varredura e extração nativa dos logs
└── atas_salvas/            # Pasta gerada automaticamente com os relatórios em HTML
```

---

## ⚙️ Pré-requisitos

Certifique-se de ter o **Python 3.10 ou superior** instalado em sua máquina.

## 🛠️ Passo a Passo de Configuração

### 1. Preparar o Repositório
Baixe os arquivos deste projeto e abra a pasta raiz no seu terminal (ou VS Code).

### 2. Criar e Ativar o Ambiente Virtual (venv)
O ambiente virtual é essencial para isolar as bibliotecas deste projeto do resto do seu computador. No terminal, dentro da pasta do projeto, execute:

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux / macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar as Bibliotecas Necessárias
Com o ambiente ativado, instale as dependências oficiais do Google Gemini e o gerenciador de variáveis de ambiente. Se você já tem o arquivo `requirements.txt` criado, execute:

```bash
pip install -r requirements.txt
```

Caso queira instalar manualmente as bibliotecas, o comando é:
```bash
pip install python-dotenv google-genai
```

### 4. Configurar as Variáveis de Ambiente (.env)
Crie um arquivo novo chamado exatamente **`.env`** na raiz do seu projeto (na mesma pasta onde está o `main.py`). Abra este arquivo e preencha com as suas credenciais:

```env
# Configurações da API do Google Gemini
GEMINI_API_KEY=cole_sua_chave_gerada_no_google_ai_studio_aqui

# Configurações de Disparo de E-mail (SMTP)
EMAIL_REMETENTE=seu_email@empresa.com.br
EMAIL_SENHA=sua_senha_de_aplicativo_aqui
EMAIL_DESTINATARIOS=joao@empresa.com.br, maria@empresa.com.br
EMAIL_COPIA=gestor@empresa.com.br
```
⚠️ **AVISO CRÍTICO DE SEGURANÇA:** O arquivo `.env` contém senhas reais. **Nunca** faça o commit (envio) deste arquivo para o GitHub ou qualquer outro repositório público.

### 5. Executar a Automação
Com tudo instalado e as credenciais configuradas, basta rodar o arquivo principal. Ele fará a varredura nas pastas mapeadas, processará os erros com a IA e disparará os relatórios.

```bash
python main.py
```