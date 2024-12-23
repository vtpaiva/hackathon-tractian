from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import subprocess
import os

# token bot telegram
TOKEN = "token aqui"

# mensagem inicial de boas vindas
async def start(update: Update, context):
    await update.message.reply_text("Olá! Envie um áudio para que eu processe.")

# funcao para processar o pedido de um manual
async def manual_handler(update: Update, context):
    if len(context.args) != 1:
        await update.message.reply_text("Por favor, use o formato correto: /manual <nome_manual>")
        return
    
    manual_name = context.args[0]  # pega o nome do manual passado como argumento
    try:
        # executa o script de processamento de manual com o nome do manual como argumento
        result = subprocess.check_output(["python3", "manual_script.py", manual_name], text=True)
        await update.message.reply_text(f"Resultado do manual '{manual_name}': {result.strip()}")


    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o manual '{manual_name}': {e}")
        await update.message.reply_text(f"Ocorreu um erro ao executar o manual '{manual_name}': {e}")


# funcao para processar o audio recebido
async def audio_handler(update: Update, context):

    # baixa o audio enviado
    audio_file = await update.message.voice.get_file()
    audio_path = os.path.join("audios", f"{audio_file.file_id}.ogg")
    await audio_file.download_to_drive(audio_path)
    print(f"Áudio salvo em: {audio_path}")

    # enviar o audio para um script externo
    try:
        # executa o script de processamento
        result = subprocess.check_output(["python3", "meu_script.py", audio_path], text=True)
        await update.message.reply_text(f"Resultado do processamento: {result.strip()}")
        await update.message.reply_text("Se precisar de mais alguma coisa, é só enviar outro áudio!") 

    except subprocess.CalledProcessError as e:
        print(f"Erro ao processar o áudio: {e}")
        await update.message.reply_text(f"Ocorreu um erro ao processar o áudio: {e}")

    # removee o arquivo de audio baixado 
    os.remove(audio_path)
    print(f"Arquivo de áudio {audio_path} removido.")


if __name__ == "__main__":
    # cria a instancia do bot
    app = ApplicationBuilder().token(TOKEN).build()

    # comando inicial do bot
    app.add_handler(CommandHandler("start", start))      
    
    # Tratamento de mensagens de áudio
    app.add_handler(MessageHandler(filters.VOICE, audio_handler))

    print("Bot está rodando...")
    app.run_polling()
