import sys
from openai import OpenAI
import openai
import pandas as pd
import json
client = OpenAI()

def process_audio(file_path):
    audio_file= open(file_path, "rb")
    transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file
    )

    texto = transcription.text
    return texto

def formatar_dados_csv(caminho_csv):
    # Ler o CSV usando pandas
    df = pd.read_csv(caminho_csv)
    
    # Converter para uma string legível
    dados_json = df.to_json(orient='records')
    dados_json_texto = json.dumps(json.loads(dados_json), indent=2)

    return dados_json_texto

def gerar_resposta(prompt):
    response = openai.chat.completions.create(
        model="gpt-4o",  # Escolha o modelo, como "gpt-3.5-turbo" ou "gpt-4"
        messages=[
            {"role": "system", "content": "Você é um assistente que ajuda com perguntas em Python."},
            {"role": "user", "content": prompt}
        ],
        n=1,  # Número de respostas
        stop=None,  # Pode definir uma palavra de parada, se necessário
        temperature=0.7  # Controla a criatividade da resposta (entre 0 e 1)
    )
    
    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Caminho do arquivo não fornecido")
        sys.exit(1)

    file_path = sys.argv[1]
    resultado = process_audio(file_path)

    # Exemplo de uso da função
    prompt = f"""A partir do texto a seguir, identifique e liste quais são os serviços mencionados, o texto é {resultado}. 
                 Após, recomende as ferramentas necessárias para todas as tarefas com seu código SAP de acordo com a tabela: 
                 {formatar_dados_csv("Colinha de Códigos SAP.csv")}, me responda sem usar markdown, apenas como se estivesse 
                 escrevendo um txt comum."""
                 
    resposta = gerar_resposta(prompt)
    print(f'Resposta: {resposta}')

