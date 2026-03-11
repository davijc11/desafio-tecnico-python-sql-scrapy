import json
from datetime import datetime

def limpar_dados_evento(evento):
    """
    Função que recebe um dicionário de evento e aplica as regras de tratamento.
    """
    
    # 1. Remoção de Espaçamentos e Erros de NBSP
    chaves_texto = ['nome', 'sobrenome', 'titulo']
    for chave in chaves_texto:
        if chave in evento and isinstance(evento[chave], str):
            # O caractere NBSP no Python é representado por '\xa0'
            # Substituí por um espaço normal e usei .strip() para limpar as pontas
            evento[chave] = evento[chave].replace('\xa0', ' ').replace('NBSP', ' ').strip()
            
    # 2 e 3. Conversão de Data e Substituição de Marcadores no Título
    if 'dataRealizacao' in evento:
        data_string = evento['dataRealizacao'].strip()
        # Transformando a string em um objeto datetime do Python
        data_obj = datetime.strptime(data_string, "%d/%m/%Y %H:%M:%S")
        
        # Tratando o título antes de alterar a data principal para o formato SQL
        if 'titulo' in evento:
            data_formatada = data_obj.strftime("%d/%m/%Y")
            hora_formatada = data_obj.strftime("%H:%M:%S")
            
            # Substituindo o primeiro "..." pela data e o segundo "..." pela hora
            titulo = evento['titulo']
            titulo = titulo.replace('...', data_formatada, 1)
            titulo = titulo.replace('...', hora_formatada, 1)
            evento['titulo'] = titulo
            
        # Convertendo a chave dataRealizacao para o formato SQL datetime
        evento['dataRealizacao'] = data_obj.strftime("%Y-%m-%d %H:%M:%S")

    # 4. Transformação de Lista em String (Descrição)
    if 'descricao' in evento and isinstance(evento['descricao'], list):
        # Concatena a lista com um espaço entre os elementos
        evento['descricao'] = ' '.join([linha.strip() for linha in evento['descricao']])

    # 5. Tratamento de Arquivos (Datas e Título nulo)
    if 'arquivos' in evento and isinstance(evento['arquivos'], list):
        for arq in evento['arquivos']:
            # Conversão de data do arquivo para datetime SQL
            if 'data' in arq and arq['data']:
                data_arq_obj = datetime.strptime(arq['data'], "%d/%m/%Y")
                # Adicionando " 00:00:00" conforme o exemplo da saída esperada
                arq['data'] = data_arq_obj.strftime("%Y-%m-%d %H:%M:%S")
            
            # Observação: A instrução pede para excluir chaves nulas, mas o exemplo
            # de saída esperada mostra o 'titulo' do primeiro arquivo como uma string vazia "".
            # Mantive o padrão visual da saída esperada para essa chave específica.
            if 'titulo' in arq and arq['titulo'] is None:
                arq['titulo'] = ""

    # 6. Exclusão de chaves com valores nulos
    def remover_nulos(dicionario):
        if isinstance(dicionario, dict):
            # Recria o dicionário ignorando chaves cujo valor seja None (nulo)
            return {k: remover_nulos(v) for k, v in dicionario.items() if v is not None}
        elif isinstance(dicionario, list):
            return [remover_nulos(v) for v in dicionario]
        return dicionario

    evento_limpo = remover_nulos(evento)
    
    return evento_limpo

def main():
    # Caminho do arquivo de entrada
    arquivo_entrada = 'teste_instar.json'
    arquivo_saida = 'arquivo_tratado.json'
    
    # Lendo o arquivo JSON
    try:
        with open(arquivo_entrada, 'r', encoding='utf-8') as f:
            dados = json.load(f)
    except FileNotFoundError:
        print(f"Erro: O arquivo '{arquivo_entrada}' não foi encontrado.")
        return

    # O JSON raiz é uma lista de eventos, então iteramos sobre ela
    dados_processados = [limpar_dados_evento(evento) for evento in dados]

    # Exportando o resultado para um novo arquivo JSON
    with open(arquivo_saida, 'w', encoding='utf-8') as f:
        # ensure_ascii=False garante que acentos fiquem corretos e indent=4 formata visualmente
        json.dump(dados_processados, f, ensure_ascii=False, indent=4)
        
    print(f"Processamento concluído com sucesso! Verifique o arquivo '{arquivo_saida}'.")

if __name__ == "__main__":
    main()