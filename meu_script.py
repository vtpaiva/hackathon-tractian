import sys

def process_audio(file_path):
    # Lógica de processamento do áudio
    # Exemplo: converter para texto, calcular duração, etc.
    # Retorne o resultado como string

    return "Áudio processado com sucesso!"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Caminho do arquivo não fornecido")
        sys.exit(1)

    file_path = sys.argv[1]
    resultado = process_audio(file_path)
    print(resultado)

