from collections import defaultdict
from typing import Any
from core.infrastructure.information_extraction_solver import (
    VarArrayAndObjectiveSolutionPrinter,
)


# Validado: 15/04/2025
def combinacao_performances(
    performance_individual: list,
) -> defaultdict[int, list[Any]]:
    Performance = defaultdict(list)
    for i in range(len(performance_individual)):
        aux = []
        for k in range(len(performance_individual)):
            if i == k:
                aux.append(performance_individual[i])
            else:
                aux.append((performance_individual[i] + performance_individual[k]) // 2)
        Performance[i] = aux
    return Performance


# Validado: 15/04/2025
def get_max_performance(
    Performance: defaultdict[int, list[Any]], Profissionais: list[str]
) -> int:
    Max_Performance = sum(
        [
            Performance[i][k]
            for i in range(len(Profissionais))
            for k in range(len(Profissionais))
        ]
    )
    return Max_Performance


if __name__ == "__main__":
    import pandas as pd

    df = pd.read_excel("./core/data/data_frame_summary/colaborators_data.xlsx")
    Performace = combinacao_performances(
        performance_individual=df["Performance"].tolist()
    )
    print(f"Performance: {Performace[0]}")
    Max_performance = get_max_performance(
        Performance=Performace, Profissionais=df["Profissionais"].tolist()
    )
    print(f"Max_performance: {Max_performance}")
