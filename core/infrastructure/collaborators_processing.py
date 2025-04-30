from core.infrastructure.gateway.gemini_model import GeminiModel


def process_collaborators(colaborators: list, llm_model: GeminiModel):
    workers_cv = []
    worker_cv = {}
    cvs = ""
    cvs_summary = []
    for worker in colaborators:
        worker_cv["nome"] = worker
        with open(f"./core/data/cvs/{worker}.md", "r", encoding="utf-8") as file:
            content = file.read()
            worker_cv["curriculo"] = content
            cv = llm_model.generate_cv_for_candidate(
                content, temperature=0.5, top_p=0.9, top_k=40
            )
            cvs = f"curriculo de {worker}: \n {cv} \n {cvs}"
            cvs_summary.append(cv)
            worker_cv["resumo"] = cv
        workers_cv.append(worker_cv)

    project_cv = llm_model.generate_cv_for_project(
        cvs, temperature=0.7, top_p=0.9, top_k=40
    )

    return project_cv, cvs_summary


if __name__ == "__main__":
    # Example usage
    gemini_model = GeminiModel(gemini_model="gemini-2.0-flash")
    collaborators = [
        "Rafael George",
        "Leonides Neto",
        "João Ricardo",
        "Morgana Leite",
        "Tamires Rezende",
        "Washington Barbosa",
    ]
    project_cv, cvs_summary = process_collaborators(collaborators, gemini_model)
    print("Project CV:", project_cv)
    print("CVs Summary:", cvs_summary)
    for summary in cvs_summary:
        print(summary)
