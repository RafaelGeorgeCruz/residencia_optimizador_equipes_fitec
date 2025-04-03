from infra.gateway.gemini_model import GeminiModel
import pandas as pd
from infra.markdown import save_on_markdown
from infra.collaborators_processing import process_collaborators


suggested_workers = ["Rafael George", "Leonides Neto", "João Ricardo", "Morgana Leite", "Tamires Rezende", "Washington Barbosa"]
model = GeminiModel(gemini_model="gemini-2.0-flash")

project_cv, cvs_summary = process_collaborators(colaborators=suggested_workers, llm_model=model)

d = {"colaboradores" : suggested_workers, "curriculos" : cvs_summary}
pd.DataFrame(data=d).to_csv("./data/results/resumo_curriculos.csv", index=False)

save_on_markdown("./data/results/resumo_projeto.md", project_cv)
