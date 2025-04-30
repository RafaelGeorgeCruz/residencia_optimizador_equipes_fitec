import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GOOGLE_GEMINI_API_KEY", None)
if API_KEY is None:
    raise ValueError(
        "API key not found. Please set the GOOGLE_GEMINI_API_KEY environment variable."
    )


class GeminiModel(object):

    def __init__(self, gemini_model: str = "gemini-2.0-flash"):
        API_KEY = os.getenv("GOOGLE_GEMINI_API_KEY", None)
        genai.configure(api_key=API_KEY)
        self.model = genai.GenerativeModel(gemini_model)
        self.temperature = 1.0

    def generate_cv_for_candidate(self, input: str, **kwargs: dict):
        """Gera texto usando o modelo Gemini com os parâmetros fornecidos.
        kwargs: Parâmetros de configuração para a geração de texto. {temperature, top_p, top_k, max_output_tokens, stop_sequences}
        """
        prompt = f"""Você é um assistente de texto e sua função principal é gerar resumos de currículos,\n
        Os resumos devem contér informações tecnicas e comportamentais presentes no currículo.\n
        Você deve gerar um resumo breve e objetivo, com no máximo 7 frases.\n
        \n siga o seguinte formato -> \n
        Nome do colaborador: [Nome]\n
        Cargo: [cargo]\n
        Resumo do colaborador: [resumo].\n\n
        Gere um resumo desse currículo: \n {input} \n"""
        generation_config = genai.GenerationConfig(**kwargs)
        response = self.model.generate_content(
            prompt, generation_config=generation_config
        )
        return response.text.strip()

    def generate_cv_for_project(self, cvs: str, project_description, **kwargs: dict):
        """Gera texto usando o modelo Gemini com os parâmetros fornecidos.
        kwargs: Parâmetros de configuração para a geração de texto. {temperature, top_p, top_k, max_output_tokens, stop_sequences}
        """
        prompt = f"""Você é um assistente de texto e sua função principal é gerar resumos dos curriculos dos colaboradores do projeto.\n
        Os resumos devem contér as principais informações tecnicas e comportamentais dos colaboradores presentes no projeto, seja breve.\n
        Você deve obrigatoriamente colocar o nome completo de todos os colaboradores alocados no projeto junto de seus respectivos cargos.\n
        Você deve gerar um resumo breve e objetivo, com no máximo 15 frases.\n
        crie um paragrafo explicando também como as escolhas dos colaboradores impactarão no resultado do projeto.\n
        Seja formal e objetivo, evite gírias, expressões coloquiais e expressões emocionais.\n
        A resposta deve ser em markdown.\n
        Um pouco da descrição do projeto: {project_description}
        Gere um resumo desse projeto: \n {cvs} \n"""
        generation_config = genai.GenerationConfig(**kwargs)
        response = self.model.generate_content(
            prompt, generation_config=generation_config
        )
        return response.text.strip()
