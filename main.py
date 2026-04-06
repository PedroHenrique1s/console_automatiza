import os

from shared.envio_email import enviar_email
from shared.prompt_ia   import processar_log_com_gemini

if __name__ == "__main__":
    
    casas_logs = {
        "Escandinavia": r"P:\Protheus11\bin\appserver_ws_rest_EMAZA\console.log",
        "Cotave": r"S:\Protheus11\bin\appserver_ws_rest_EMAZA\console.log"
    }

    print("--- INICIANDO AUTOMAÇÃO DE LEITURA DE LOGS ---")

    for nome_casa, caminho_log in casas_logs.items():
        print(f"\n--- Processando: {nome_casa} ---")
        
        if os.path.exists(caminho_log):
            html_ata = processar_log_com_gemini(caminho_log, nome_casa)
            
            if html_ata:
                enviar_email(html_ata, nome_casa)
                
                pasta_destino = "atas_salvas"
                
                os.makedirs(pasta_destino, exist_ok=True)
                
                nome_arquivo_backup = f"ultima_ata_{nome_casa.lower()}.html"
                caminho_completo = os.path.join(pasta_destino, nome_arquivo_backup)
                
                # 4. Salva o arquivo no caminho completo
                with open(caminho_completo, "w", encoding="utf-8") as f:
                    f.write(html_ata)
                print(f"Cópia da análise salva na pasta: '{caminho_completo}'")
        else:
            print(f"AVISO: Arquivo de log não encontrado no caminho: {caminho_log}")
            
    print("\n--- PROCESSO FINALIZADO ---")