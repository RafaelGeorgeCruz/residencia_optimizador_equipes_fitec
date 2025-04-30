from core.infrastructure.gateway.gemini_model import GeminiModel
from core.infrastructure.team_formation import TeamFormation
import pandas as pd

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import main_router
import os
from dotenv import load_dotenv


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("1/4: Loading env variables")
    load_dotenv()

    if "GOOGLE_API_KEY" not in os.environ:
        os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_GEMINI_API_KEY")

    print("2/4: Gemini model loaded")
    app.state.gemini_model = GeminiModel(gemini_model="gemini-2.0-flash")
    print("2/4: Done")

    app.state.optimization_model = TeamFormation(
        "./core/data/data_frame_summary/colaborators_data.xlsx"
    )

    df = pd.read_excel("./core/data/data_frame_summary/colaborators_data.xlsx")
    lista_de_projetos = []
    df["projeto_a"] = app.state.optimization_model.B_Array[0]
    df["projeto_b"] = app.state.optimization_model.B_Array[1]
    df["projeto_c"] = app.state.optimization_model.B_Array[2]
    df.to_excel("./core/data/data_frame_summary/colaborators_data.xlsx", index=False)
    lista_de_projetos.append(df["projeto_a"].tolist())
    lista_de_projetos.append(df["projeto_b"].tolist())
    lista_de_projetos.append(df["projeto_c"].tolist())
    app.state.optimization_model.Solucao_Parcial = lista_de_projetos.copy()

    yield


app = FastAPI(
    title="Formador de Equipes UPE",
    version="1.0.0",
    description="AI powered UPE detailing team formation",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(main_router)
