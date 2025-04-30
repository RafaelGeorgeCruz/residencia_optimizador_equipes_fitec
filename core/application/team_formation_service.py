from core.infrastructure.gateway.gemini_model import GeminiModel
import pandas as pd
from core.infrastructure.markdown import save_on_markdown
from core.infrastructure.collaborators_processing import process_collaborators
from core.infrastructure.team_formation import TeamFormation
import markdown


def create_new_team(
    arquiteto: int,
    front_end: int,
    back_end: int,
    quality_assurance: int,
    iniciante: int,
    team_description: str,
    gemini_model: GeminiModel,
    team_formator: TeamFormation,
) -> tuple[list[str], str]:
    """
    Create a new team based on the input parameters and return the suggested workers and project CV.
    """
    new_team = [arquiteto, front_end, back_end, quality_assurance, iniciante]
    team_formator.run_optmization_model(initial=False, wanted_team=new_team)
    suggested_workers = team_formator.get_suggested_workers()

    summarys = ""
    for worker in suggested_workers:
        f = open(f"./core/data/cvs/{worker}.md", "r", encoding="utf-8")
        cv_worker = markdown.markdown(f.read())
        worker_cv_summary = gemini_model.generate_cv_for_candidate(
            cv_worker, temperature=0.5
        )
        summarys += worker_cv_summary + "\n\n"
    project_cv = gemini_model.generate_cv_for_project(
        summarys, team_description, temperature=0.5, max_output_tokens=1000
    )

    return suggested_workers, project_cv


if __name__ == "__main__":

    team, project_cv = create_new_team(
        arquiteto=1,
        front_end=1,
        back_end=1,
        quality_assurance=1,
        iniciante=1,
        team_description="Forme uma equipe",
        gemini_model=GeminiModel(gemini_model="gemini-2.0-flash"),
        team_formator=TeamFormation(
            "./core/data/data_frame_summary/colaborators_data.xlsx"
        ),
    )

    print("Team:", team)
    print("Project CV:", project_cv)
