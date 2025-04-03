from infra.gateway.gemini_model import GeminiModel

def process_collaborators(colaborators: list, llm_model: GeminiModel):
    workers_cv = []
    worker_cv = {}
    cvs = ""
    cvs_summary = []
    for worker in colaborators:
        worker_cv["nome"] = worker
        with open(f"./data/cvs/{worker}.md", "r", encoding="utf-8") as file:
            content = file.read()
            worker_cv["curriculo"] = content
            cv = llm_model.generate_cv_for_candidate(content, temperature=0.5, top_p=0.9, top_k=40)
            cvs = f"curriculo de {worker}: \n {cv} \n {cvs}"
            cvs_summary.append(cv)
            worker_cv["resumo"] = cv
        workers_cv.append(worker_cv)

    project_cv = llm_model.generate_cv_for_project(cvs, temperature=0.7, top_p=0.9, top_k=40)
    
    return project_cv, cvs_summary