import os
from openai import OpenAI
import openai
import sys
import fitz  # PyMuPDF

client = OpenAI()

def buscar_manual(manual_name):
    # Caminho para o repositório de manuais
    manual_dir = "manual"
    
    # Percorre o repositório procurando por um arquivo PDF que corresponda ao nome do manual
    for file_name in os.listdir(manual_dir):
        if file_name.lower().startswith(manual_name.lower()) and file_name.endswith(".pdf"):
            return os.path.join(manual_dir, file_name)
    
    return None

def traduzir_texto(texto):
    try:
        # Envia o texto para a API da OpenAI para traduzir
        response = openai.chat.completions.create(
            model="gpt-4o",  # ou o modelo que você preferir
            messages=[
                {"role": "user", "content": f"Resume and translate the following text to Portuguese:\n\n{texto}"}
            ],
            max_tokens=1000,
            temperature=0.5
        )
        # Extrai a tradução do resultado da API
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Erro ao traduzir: {str(e)}"
    
def extrair_texto_pdf(pdf_path):
    """Extrai o texto de um arquivo PDF."""
    texto = ""
    try:
        with fitz.open(pdf_path) as doc:
            for page in doc:
                texto += page.get_text()  # Extraí o texto de cada página
    except Exception as e:
        return f"Erro ao ler o PDF: {str(e)}"
    return texto

def dividir_texto(texto, limite):
    """Divide o texto em partes menores, respeitando o limite de tokens."""
    palavras = texto.split()
    partes = []
    parte_atual = ""

    for palavra in palavras:
        if len(parte_atual) + len(palavra) + 1 <= limite:  # +1 para o espaço
            parte_atual += " " + palavra if parte_atual else palavra
        else:
            partes.append(parte_atual)
            parte_atual = palavra
    
    if parte_atual:  # Adiciona a última parte
        partes.append(parte_atual)

    return partes

def processar_manual(manual_name):
    manual_path = buscar_manual(manual_name)
    
    if not manual_path:
        return f"Manual '{manual_name}' não encontrado."

    # Extrai o texto do PDF
    conteudo = extrair_texto_pdf(manual_path)
    
    if "Erro" in conteudo:  # Verifica se ocorreu um erro ao ler o PDF
        return conteudo
    
    # Divide o conteúdo em partes menores
    partes = dividir_texto(conteudo, 4000)  # Ajuste o limite conforme necessário
    traducao_total = ""

    # Traduz cada parte e acumula a tradução
    for parte in partes:
        traducao = traduzir_texto(parte)
        if "Erro" in traducao:
            return f"Erro ao traduzir parte do texto: {traducao}"
        traducao_total += traducao + "\n"  # Acumula as traduções
    
    return traducao_total

if __name__ == "__main__":
    # Verifica se um nome de manual foi passado como argumento
    if len(sys.argv) != 2:
        print("Uso: python3 script_manual.py <nome_manual>")
        sys.exit(1)

    nome_manual = sys.argv[1]
    resultado = processar_manual(nome_manual)
    print(resultado)