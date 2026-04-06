import tempfile
import os

def extrair_blocos_de_erro(arquivo_origem, frase_chave, linhas_para_capturar=25):
    """
    Varre um log gigante, encontra a frase-chave e salva o bloco de erro 
    em um arquivo temporário menor, retornando o caminho desse arquivo.
    """
    print(f"Buscando por '{frase_chave}' em: {arquivo_origem}...")
    
    temp_fd, temp_path = tempfile.mkstemp(suffix=".txt", text=True)
    
    blocos_encontrados = 0
    capturando = False
    contador_linhas = 0

    try:
        with open(arquivo_origem, 'r', encoding='utf-8', errors='ignore') as f_origem, \
             os.fdopen(temp_fd, 'w', encoding='utf-8') as f_destino:
            
            for linha in f_origem:
                if frase_chave in linha:
                    capturando = True
                    contador_linhas = 0
                    blocos_encontrados += 1
                    
                    f_destino.write(f"\n{'='*50}\n")
                    f_destino.write(f"BLOCO DE ERRO #{blocos_encontrados}\n")
                    f_destino.write(f"{'='*50}\n")

                if capturando:
                    f_destino.write(linha)
                    contador_linhas += 1
                    
                    if contador_linhas >= linhas_para_capturar:
                        capturando = False

        print(f"Busca concluída! {blocos_encontrados} erro(s) encontrado(s).")
        
        if blocos_encontrados == 0:
            os.remove(temp_path)
            return None
            
        return temp_path
        
    except Exception as e:
        print(f"Falha ao extrair erros localmente: {e}")
        os.remove(temp_path)
        return None