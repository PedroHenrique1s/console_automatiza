
import os 
import time

from datetime import date
from google import genai
from google.genai import types
from google.genai import errors
from dotenv import load_dotenv
from .filtra_log import extrair_blocos_de_erro

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODELO_GEMINI = "gemini-flash-latest"

def processar_log_com_gemini(caminho_log, nome_casa):
    print(f"Iniciando processamento da {nome_casa}...")
    
    # PASSO 1: Filtrar o log gigante gerando um arquivo pequeno apenas com os erros
    caminho_log_filtrado = extrair_blocos_de_erro(
        arquivo_origem=caminho_log, 
        frase_chave="THREAD ERROR", 
        linhas_para_capturar=25
    )
    
    if not caminho_log_filtrado:
        print(f"Nenhum 'THREAD ERROR' encontrado na {nome_casa} ou erro na leitura.")
        return None

    data_hoje = date.today().strftime("%d/%m/%Y")
    
    try:
        print(f"Enviando log filtrado da {nome_casa} para o Gemini ({MODELO_GEMINI})...")
        
        # Faz o upload do arquivo filtrado (que é bem pequeno)
        arquivo_midia = client.files.upload(
            file=caminho_log_filtrado, 
            config={'mime_type': 'text/plain'}
        )
        
        while arquivo_midia.state.name == "PROCESSING":
            print("Processando log no servidor...")
            time.sleep(2)
            arquivo_midia = client.files.get(name=arquivo_midia.name)

        if arquivo_midia.state.name == "FAILED":
            raise ValueError(f"O processamento do arquivo filtrado da {nome_casa} falhou.")

        print(f"Log da {nome_casa} pronto. Gerando análise HTML...")

        prompt_erro_console = f"""
            Você é um analista técnico eficiente atuando em nome de Pedro Souza. 
            Analise o log de sistema ou registro de console fornecido e gere a Análise de Erro para a empresa {nome_casa}.

            REGRAS DE EXTRAÇÃO (CRÍTICO):
            1. **IDENTIFICAÇÃO DO ERRO:** Localize a tag **THREAD ERROR** ou padrões de erro no log.
            2. **DADOS OBRIGATÓRIOS:** Você deve extrair com precisão do texto:
            - Thread ID
            - Ambiente/Base (DBEnv)
            - Fonte/Função (Identificar o .PRW ou função do erro)
            - Número da Linha do Erro
            - Data e Hora do Log
            3. **QUERY/SQL:** Se o log contiver instruções SQL ou queries, isole-as e mantenha a formatação para facilitar a leitura.

            ESTRUTURA DE SAÍDA (HTML):
            1. Inicie com: <h2>Análise de Erro de Console - {nome_casa} - {data_hoje}</h2>
            2. Insira os dados extraídos exatamente nesta estrutura:
            <div style="border: 1px solid #cc0000; padding: 15px; background-color: #fff5f5;">
                <h3>Erro Identificado</h3>
                <ul>
                    <li><strong>Thread ID:</strong> [Extrair ID]</li>
                    <li><strong>Ambiente/Base:</strong> [Extrair DBEnv]</li>
                    <li><strong>Fonte/Função:</strong> [Identificar o .PRW ou função, ex: REST_WSDLMZ544]</li>
                    <li><strong>Linha do Erro:</strong> <b style="color:red;">[Número da Linha]</b></li>
                    <li><strong>Data/Hora do Log:</strong> [Data e Hora]</li>
                </ul>
                <h4>Query/SQL Relacionado:</h4>
                <pre style="background: #eee; padding: 10px; border-left: 5px solid #666;">[Colar a Query SQL formatada aqui]</pre>
            </div>
            
            3. FINALIZAÇÃO:
            Adicione exatamente esta assinatura ao final do HTML:
            <br><br>
            <hr>
            <p>Atenciosamente,</p>
            <p>
                <strong>Pedro Henrique Nascimento de Souza</strong><br>
                TI Sistemas/Projetos<br>
                Maza Tarraf<br>
                (17) 2138-9969<br>
                Av. Tarraf, 3210 | Jd. Alto Alegre<br>
                São José do Rio Preto / SP
            </p>
            <p style="font-size: 10px; color: #666; line-height: 1.2;">
                “As informações contidas nesta mensagem e em seus eventuais anexos são confidenciais e protegidas pelo sigilo legal. 
                A divulgação, distribuição ou reprodução deste documento depende da autorização do emissor. 
                Caso V. Sa. não seja o destinatário ou preposto, fica, desde já, notificado que qualquer divulgação, 
                distribuição ou reprodução é estritamente proibida, sujeitando-se o infrator às sanções legais. 
                Caso esta comunicação tenha sido recebida por engano, favor avisar o emissor imediatamente. Grato pela cooperação.”
            </p>

            Saída: Apenas o código HTML puro.
        """
        
        tentativas = 0
        max_tentativas = 3
        
        while tentativas < max_tentativas:
            try:
                response = client.models.generate_content(
                    model=MODELO_GEMINI,
                    contents=[
                        types.Content(
                            role="user",
                            parts=[
                                types.Part.from_uri(
                                    file_uri=arquivo_midia.uri,
                                    mime_type=arquivo_midia.mime_type
                                ),
                                types.Part.from_text(text=prompt_erro_console)
                            ]
                        )
                    ]
                )
                return response.text 
            
            except errors.ClientError as e:
                if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                    print(f"Cota excedida (429). Esperando 20 segundos... (Tentativa {tentativas+1}/{max_tentativas})")
                    time.sleep(20) 
                    tentativas += 1
                else:
                    raise e

        print(f"Falha na {nome_casa}: Limite de tentativas excedido no Gemini.")
        return None

    except Exception as e:
        print(f"Erro inesperado ao processar {nome_casa}: {e}")
        return None
        
    finally:
        if os.path.exists(caminho_log_filtrado):
            os.remove(caminho_log_filtrado)