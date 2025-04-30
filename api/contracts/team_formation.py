from pydantic import BaseModel


class TeamFormationResponse(BaseModel):
    team: list[str]
    team_details: str


class TeamFormationRequest(BaseModel):
    arquiteto: int
    front_end: int
    back_end: int
    quality_assurance: int
    iniciante: int
    team_description: str
