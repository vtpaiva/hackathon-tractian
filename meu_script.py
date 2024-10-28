import sys
from openai import OpenAI
import openai
client = OpenAI()

def process_audio(file_path):
    audio_file= open(file_path, "rb")
    transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file
    )

    texto = transcription.text
    return texto

def gerar_resposta(prompt):
    response = openai.chat.completions.create(
        model="gpt-4o",  # Escolha o modelo, como "gpt-3.5-turbo" ou "gpt-4"
        messages=[
            {"role": "system", "content": "Você é um assistente que ajuda com perguntas em Python."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=100,  # Limite de tokens na resposta
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
    print(resultado)

    print('------------------RESPOSTAGPT------------------------')

    # Exemplo de uso da função
    prompt = f'A partir do texto a seguir, poderia identificar e listar quais são os serviços mencionados, o texto é {resultado}'
    resposta = gerar_resposta(prompt)
    print(f'Resposta: {resposta}')

