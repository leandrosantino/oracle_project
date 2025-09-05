from pathlib import Path
from docling.document_converter import DocumentConverter

def processar_com_docling(input_dir: str, output_dir: str):
    """
    Converte todos os arquivos suportados de um diretório para Markdown usando a API do Docling.
    
    :param input_dir: Caminho do diretório de entrada com os arquivos originais
    :param output_dir: Caminho do diretório onde salvar os arquivos .md
    """
    suportados = {".pdf", ".docx", ".pptx", ".xlsx"}
    
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Inicializa o conversor
    converter = DocumentConverter()

    for file in input_path.iterdir():
        if file.suffix.lower() in suportados:
            saida = output_path / f"{file.stem}.md"
            print(f"Processando: {file.name} -> {saida.name}")

            try:
                result = converter.convert(file)
                md_text = result.document.export_to_markdown()
                
                with open(saida, "w", encoding="utf-8") as f:
                    f.write(md_text)

            except Exception as e:
                print(f"Erro ao processar {file.name}: {e}")

if __name__ == "__main__":
    entrada = "C:\\Users\\leand\\Documents\\Documentos\\Estatistica"   # diretório de entrada
    # entrada = "C:\\Users\\leand\\Documents\\Documentos\\Projeto Facility"   # diretório de entrada
    saida = "arquivos_md"       # diretório de saída
    processar_com_docling(entrada, saida)
