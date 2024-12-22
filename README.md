# hackathon-tractian

This project is a Telegram bot that listens to voice messages sent by users, processes the audio content, and returns relevant information based on the audio. It leverages the OpenAI API for transcription and response generation, as well as external scripts for specific audio processing tasks.

## Features

- **Audio Processing**: The bot listens to voice messages, processes the audio using an external Python script, and returns results based on the content.
- **Manual Requests**: Users can request manual processing by providing the name of the manual they need help with.
- **Integration with OpenAI**: The bot uses OpenAI's Whisper API to transcribe the audio to text, and then uses GPT-4 to generate responses based on the transcription.
- **CSV Data Processing**: The bot can format and return CSV data as a readable JSON string, based on the request.

## Setup

To run this bot, you need to:

1. Install the dependencies:
   - `python-telegram-bot`
   - `openai`
   - `pandas`

2. Set up your Telegram Bot:
   - Create a bot on Telegram by chatting with the BotFather.
   - Obtain the bot token and replace the `TOKEN` variable in the script with your token.

3. Set up OpenAI API:
   - Sign up for OpenAI API access and obtain an API key.
   - Set up the OpenAI Python package and ensure your API key is accessible.

## Code Overview

### 1. Telegram Bot Setup

The bot listens for voice messages and handles the `/start` command and audio messages.

```python
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import subprocess
import os

# token bot telegram
TOKEN = "token aqui"

# mensagem inicial de boas vindas
async def start(update: Update, context):
    await update.message.reply_text("Olá! Envie um áudio para que eu processe.")

# função para processar o áudio recebido
async def audio_handler(update: Update, context):
    # baixa o áudio enviado
    audio_file = await update.message.voice.get_file()
    audio_path = os.path.join("audios", f"{audio_file.file_id}.ogg")
    await audio_file.download_to_drive(audio_path)

    try:
        # executa o script de processamento
        result = subprocess.check_output(["python3", "meu_script.py", audio_path], text=True)
        await update.message.reply_text(f"Resultado do processamento: {result.strip()}")
    except subprocess.CalledProcessError as e:
        await update.message.reply_text(f"Ocorreu um erro ao processar o áudio: {e}")

    # remove o arquivo de áudio baixado
    os.remove(audio_path)
    print(f"Áudio salvo em: {audio_path}")
```

### 2. Audio Processing Script

The bot uses the OpenAI API to transcribe the audio to text and process it.

```python 
import sys
from openai import OpenAI
import openai
import pandas as pd
import json

client = OpenAI()

def process_audio(file_path):
    audio_file = open(file_path, "rb")
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
        model="gpt-4",  # Escolha o modelo, como "gpt-3.5-turbo" ou "gpt-4"
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
                    Após, recomende as ferramentas necessárias para todas as tarefas com seu código SAP de acordo com a tabela, 
                    explicitando a disponibilidade da ferramente, citando ferramentas similares caso a ferramenta específica não 
                    esteja disponível: {formatar_dados_csv("Colinha de Códigos SAP.csv")}, me responda sem usar markdown, apenas 
                    como se estivesse escrevendo um txt comum.Sugira em forma de lista os equipamentos relativos a Ferramentas Manuais
                    e Equipamentos de Segurança ao solicitante, ele pode precisar, me responda sem usar markdown, apenas como se estivesse 
                    escrevendo um txt comum."""
                 
    resposta = gerar_resposta(prompt)
    print(f'Resposta: {resposta}')
```
### Flowchart

![Flowchart](https://i.imgur.com/ghhzCW6.png)


### Conclusion

This Telegram bot is designed to process voice messages, transcribe them using the OpenAI Whisper model, and return relevant information in the form of text responses. The bot integrates with an external processing script that interprets the content of the audio and generates useful recommendations based on the transcription and data from a CSV file. With the help of OpenAI's language models, this bot can assist in various tasks by analyzing audio content and providing actionable insights.