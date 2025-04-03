
def save_on_markdown(file_name:str, markdown_content:str) -> None:
    try:
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(markdown_content)
        print(f"Arquivo '{file_name}' salvo com sucesso!")
    except Exception as e:
        print(f"Erro ao salvar o arquivo: {e}")