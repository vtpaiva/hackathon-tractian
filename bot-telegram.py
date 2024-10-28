import os
import subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

TOKEN = "7818166008:AAFbzLkyRsNXCSxyrNMWcFli6HBEtvhmfoQ"

# Função para iniciar o bot
async def start(update: Update, context):
    await update.message.reply_text("Olá! Envie um áudio para que eu processe.")

# Função para processar o áudio recebido
async def audio_handler(update: Update, context):
    # Baixar o áudio enviado
    audio_file = await update.message.voice.get_file()
    audio_path = os.path.join("audios", f"{audio_file.file_id}.ogg")
    await audio_file.download_to_drive(audio_path)
    print(f"Áudio salvo em: {audio_path}")

    # Enviar o áudio para um script externo
    try:
        # Execute o script de processamento
        result = subprocess.check_output(["python3", "meu_script.py", audio_path], text=True)
        await update.message.reply_text(f"Resultado do processamento: {result.strip()}")  # Remove quebras de linha extras

    except subprocess.CalledProcessError as e:
        print(f"Erro ao processar o áudio: {e}")
        await update.message.reply_text(f"Ocorreu um erro ao processar o áudio: {e}")

    # Remover o arquivo de áudio baixado (opcional)
    #os.remove(audio_path)
    #print(f"Arquivo de áudio {audio_path} removido.")

if __name__ == "__main__":
    # Criar uma instância do bot
    app = ApplicationBuilder().token(TOKEN).build()

    # Comandos do bot
    app.add_handler(CommandHandler("start", start))
    # Tratamento de mensagens de áudio
    app.add_handler(MessageHandler(filters.VOICE, audio_handler))

    print("Bot está rodando...")
    app.run_polling()
