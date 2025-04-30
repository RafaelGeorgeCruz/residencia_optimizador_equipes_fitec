from collections import defaultdict
from typing import Any
from core.infrastructure.information_extraction_solver import (
    VarArrayAndObjectiveSolutionPrinter,
)
import pandas as pd
from pandas import DataFrame
from ortools.sat.python import cp_model
from time import time


class TeamFormation:
    Performance: defaultdict(list)
    Max_Performance: int
    df_workers: DataFrame
    Requisitos_Projetos = defaultdict(list)
    S: Any
    tic = time()
    model = cp_model.CpModel()
    COP_iterations = 100
    max_runtime = 60 * 10
    B = None
    aux: list[list] = [[1, 2, 1, 1, 2], [1, 1, 2, 1, 1], [1, 1, 1, 1, 0]]
    objective_terms: Any

    def __init__(self, data_base_workers_path: str):
        self.df_workers = pd.read_excel(data_base_workers_path)
        self.Performance = self.combinacao_performances(
            performance_individual=self.df_workers["Performance"].tolist()
        )
        self.Max_Performance = self.get_max_performance(
            Performance=self.Performance,
            Profissionais=self.df_workers["Profissionais"].tolist(),
        )

        self.run_optmization_model(initial=True)

    def combinacao_performances(
        self,
        performance_individual: list,
    ) -> defaultdict[int, list[Any]]:
        Performance = defaultdict(list)
        for i in range(len(performance_individual)):
            aux = []
            for k in range(len(performance_individual)):
                if i == k:
                    aux.append(performance_individual[i])
                else:
                    aux.append(
                        (performance_individual[i] + performance_individual[k]) // 2
                    )
            Performance[i] = aux
        return Performance

    # Validado: 15/04/2025
    def get_max_performance(
        self, Performance: defaultdict[int, list[Any]], Profissionais: list[str]
    ) -> int:
        Max_Performance = sum(
            [
                Performance[i][k]
                for i in range(len(Profissionais))
                for k in range(len(Profissionais))
            ]
        )
        return Max_Performance

    def get_requisitos_projetos(self):
        for t in range(len(self.aux)):
            self.Requisitos_Projetos[t] = defaultdict(list)

        for t in range(len(self.Requisitos_Projetos)):
            for j in range(len(set(self.df_workers["Funcoes_Num"]))):
                self.Requisitos_Projetos[t][j] = self.aux[t][j]

    def get_B(self):
        # B será uma matriz binária. Para cada projeto i, cada colaborador j Bij=1 se ele participa de i, Bij=0 caso contrário#
        self.B = []
        for i in range(len(self.Requisitos_Projetos)):
            self.aux1 = []
            for j in range(len(self.df_workers["Funcoes_Num"])):
                self.aux1.append(self.model.NewBoolVar(f"B_{i}_{j}"))
            self.B.append(self.aux1)

    def get_P(self):
        # P será uma matriz binária de profissões. Para cada projeto i, uma profissão k pode ou não ser adequada ao colaborador j,
        # tal que Pikj=1 quando houver aderência entre o profissional, sua profissão e a demanda do projeto, ou Pikj=0 caso contrário#
        self.P = []
        for i in range(len(self.Requisitos_Projetos)):
            self.aux1 = []
            for k in range(len(self.Requisitos_Projetos[i])):
                aux2 = []
                for j in range(len(self.df_workers["Funcoes_Num"])):
                    aux2.append(self.model.NewBoolVar(f"P_{i}_{k}_{j}"))
                self.aux1.append(aux2)
            self.P.append(self.aux1)

    def get_S(self):
        # S será uma matriz inteira. Cada projeto i receberá a Performance correspondente à atribuição do time#
        self.S = []
        for i in range(len(self.Requisitos_Projetos)):
            aux1 = []
            for j in range(len(self.df_workers["Funcoes_Num"])):
                aux2 = []
                for t in range(len(self.df_workers["Funcoes_Num"])):
                    aux2.append(
                        self.model.NewIntVar(0, self.Max_Performance, f"S_{i}_{j}_{t}")
                    )
                aux1.append(aux2)
            self.S.append(aux1)

    def restrictions_definition(self):
        # Restrição 1: #
        # Nenhum profissional pode ser alocado em mais de 2 projetos#
        for j in range(len(self.df_workers["Funcoes_Num"])):
            self.model.Add(
                cp_model.LinearExpr.Sum(
                    [self.B[i][j] for i in range(len(self.Requisitos_Projetos))]
                )
                <= 2
            )

        # Restrição 2: #
        # Cada projeto não pode receber a atribuição de um número diferente de profissionais que o pré-determinado para cada função#
        for i in range(len(self.Requisitos_Projetos)):
            for k in range(len(self.Requisitos_Projetos[i])):
                self.model.Add(
                    cp_model.LinearExpr.Sum(
                        [
                            self.P[i][k][j]
                            for j in range(len(self.df_workers["Funcoes_Num"]))
                        ]
                    )
                    == self.Requisitos_Projetos[i][k]
                )

        # Restrições 3, 4 e 5: #
        # Garanto que um profissional não tenha sobrecarga caso outro com mesma função esteja ocioso#
        for j in range(len(self.df_workers["Funcoes_Num"])):
            x_var = self.model.NewBoolVar(f"x_var_{j}")
            self.model.Add(
                cp_model.LinearExpr.Sum(
                    [self.B[i][j] for i in range(len(self.Requisitos_Projetos))]
                )
                >= 1
            ).OnlyEnforceIf(x_var)
            self.model.Add(
                cp_model.LinearExpr.Sum(
                    [self.B[i][j] for i in range(len(self.Requisitos_Projetos))]
                )
                == 0
            ).OnlyEnforceIf(x_var.Not())
            for t in range(len(self.df_workers["Funcoes_Num"])):
                if (
                    self.df_workers["Funcoes_Num"][j]
                    == self.df_workers["Funcoes_Num"][t]
                    and j != t
                ):
                    self.model.Add(
                        cp_model.LinearExpr.Sum(
                            [self.B[i][t] for i in range(len(self.Requisitos_Projetos))]
                        )
                        <= 1
                    ).OnlyEnforceIf(x_var.Not())

        # Restrições 6 e 7: #
        # Determino uma conexão entre as variáveis Bij com Pikj#
        for i in range(len(self.Requisitos_Projetos)):
            for j in range(len(self.df_workers["Funcoes_Num"])):
                self.model.Add(
                    cp_model.LinearExpr.Sum(
                        [
                            self.P[i][k][j]
                            for k in range(len(self.Requisitos_Projetos[i]))
                        ]
                    )
                    == 1
                ).OnlyEnforceIf(self.B[i][j])
                self.model.Add(
                    cp_model.LinearExpr.Sum(
                        [
                            self.P[i][k][j]
                            for k in range(len(self.Requisitos_Projetos[i]))
                        ]
                    )
                    == 0
                ).OnlyEnforceIf(self.B[i][j].Not())

        # Restrição 8: #
        # Os profissionais atribuídos a cada função devem corresponder exatamente à expectativa dos cargos#
        # Para definir esta restrição, primeiro devemos criar uma variável auxiliar booleana z_var#
        # z_var = 1 quando uma dada função é desejada em um projeto, ou z_var = 0 caso contrário#
        # Mais adiante, forçamos que B[i][j] > 0 somente quando z_var = 1#
        for i in range(len(self.Requisitos_Projetos)):
            for k in range(len(self.Requisitos_Projetos[i])):
                for j in range(len(self.df_workers["Funcoes_Num"])):
                    y_var = self.model.NewBoolVar(f"y_var_{i}_{k}_{j}")
                    self.model.Add(
                        k == self.df_workers["Funcoes_Num"][j]
                    ).OnlyEnforceIf(y_var)
                    self.model.Add(
                        k != self.df_workers["Funcoes_Num"][j]
                    ).OnlyEnforceIf(y_var.Not())
                    self.model.Add(self.P[i][k][j] >= 0).OnlyEnforceIf(y_var)
                    self.model.Add(self.P[i][k][j] == 0).OnlyEnforceIf(y_var.Not())

    def get_similarity(self):
        self.objective_terms = []
        for i in range(len(self.Requisitos_Projetos)):
            for j in range(len(self.df_workers["Funcoes_Num"])):
                aux_bool = self.model.NewBoolVar(f"constr_{i}_{j}")
                self.model.Add(self.B[i][j] == 1).OnlyEnforceIf(aux_bool)
                self.model.Add(self.B[i][j] == 0).OnlyEnforceIf(aux_bool.Not())
                for t in range(len(self.df_workers["Funcoes_Num"])):
                    aux_bool2 = self.model.NewBoolVar(f"constr_{i}_{t}")
                    self.model.Add(self.B[i][t] == 1).OnlyEnforceIf(aux_bool2)
                    self.model.Add(self.B[i][t] == 0).OnlyEnforceIf(aux_bool2.Not())
                    if j != t:
                        s = self.model.NewBoolVar(f"s_{i}_{j}_{t}")
                        self.model.AddBoolOr(aux_bool.Not(), aux_bool2.Not(), s)
                        self.model.AddImplication(s, aux_bool)
                        self.model.AddImplication(s, aux_bool2)
                        self.objective_terms.append(
                            int(self.Performance[j][t] * 10 / 2) * s
                        )
                        self.model.Add(
                            self.S[i][j][t] == int(self.Performance[j][t] * 10 / 2)
                        ).OnlyEnforceIf(s)
                        self.model.Add(self.S[i][j][t] == 0).OnlyEnforceIf(s.Not())

    def max_project_sinergy(self):
        self.model.Maximize(cp_model.LinearExpr.Sum(self.objective_terms))
        solver = cp_model.CpSolver()
        solution_collector = VarArrayAndObjectiveSolutionPrinter(
            [
                self.S[i][j][t]
                for i in range(len(self.Requisitos_Projetos))
                for j in range(len(self.df_workers["Funcoes_Num"]))
                for t in range(len(self.df_workers["Funcoes_Num"]))
            ],
            self.COP_iterations,
        )
        solver.parameters.max_time_in_seconds = self.max_runtime
        solver.parameters.log_search_progress = True
        # solver.parameters.num_search_workers = 1
        solver.log_callback = print
        status = solver.Solve(self.model, solution_collector)
        solution_collector.solution_list
        solution_collector.solution_time
        solution_collector.solution_objective
        # solver.parameters.exploit_best_solution = 130

        tac = time()  #
        sec1 = tac - self.tic  #
        print("Time =", sec1)
        print("Status =", solver.StatusName(status))
        print("FO =", solver.ObjectiveValue())

        self.B_Array = []
        for i in range(len(self.Requisitos_Projetos)):
            aux1 = []
            for j in range(len(self.df_workers["Funcoes_Num"])):
                aux1.append(solver.Value(self.B[i][j]))
            self.B_Array.append(aux1)

        S_Array = []
        for i in range(len(self.Requisitos_Projetos)):
            aux1 = []
            for j in range(len(self.df_workers["Funcoes_Num"])):
                aux2 = []
                for t in range(len(self.df_workers["Funcoes_Num"])):
                    aux2.append(int(solver.Value(self.S[i][j][t]) / 10))
                aux1.append(aux2)
            S_Array.append(aux1)

    def add_restriction(self):
        for i in range(len(self.Solucao_Parcial)):
            for j in range(len(self.df_workers["Funcoes_Num"])):
                self.model.Add(self.B[i][j] == self.Solucao_Parcial[i][j])

    def get_suggested_workers(self):
        team_numbers_array = self.B_Array[-1]
        names = self.df_workers["Profissionais"].tolist()

        return [name for numero, name in zip(team_numbers_array, names) if numero == 1]

    def run_optmization_model(self, initial: bool, wanted_team: list = []):
        if initial:
            self.get_requisitos_projetos()
            self.get_B()
            self.get_P()
            self.get_S()
            self.restrictions_definition()
            self.get_similarity()
            self.max_project_sinergy()
        else:
            self.aux.append(wanted_team)
            self.get_requisitos_projetos()
            self.get_B()
            self.get_P()
            self.get_S()
            self.restrictions_definition()
            self.add_restriction()
            self.get_similarity()
            self.max_project_sinergy()
            self.aux.pop()
            print(self.aux)


if __name__ == "__main__":
    data_base_workers_path = "./core/data/data_frame_summary/colaborators_data.xlsx"
    team_formation = TeamFormation(data_base_workers_path=data_base_workers_path)
    team_formation.get_requisitos_projetos()
    team_formation.get_B()
    team_formation.get_P()
    team_formation.get_S()
    team_formation.restrictions_definition()
    team_formation.get_similarity()
    team_formation.max_project_sinergy()

    df = pd.read_excel("./core/data/data_frame_summary/colaborators_data.xlsx")
    lista_de_projetos = []
    df["projeto_a"] = team_formation.B_Array[0]
    df["projeto_b"] = team_formation.B_Array[1]
    df["projeto_c"] = team_formation.B_Array[2]
    lista_de_projetos.append(df["projeto_a"].tolist())
    lista_de_projetos.append(df["projeto_b"].tolist())
    lista_de_projetos.append(df["projeto_c"].tolist())

    Solucao_Parcial = lista_de_projetos.copy()
    print(Solucao_Parcial)
