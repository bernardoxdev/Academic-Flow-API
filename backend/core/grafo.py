from collections import defaultdict, deque

from backend.core.lazy_loader import LazyLoader

class GrafoMaterias:
    def ordenar(self) -> list[str]:
        df = LazyLoader.prerequisitos().collect()

        grafo = defaultdict(list)
        grau = defaultdict(int)

        for row in df.iter_rows(named=True):
            grafo[row["pre_requisito"]].append(row["materia"])
            grau[row["materia"]] += 1

        fila = deque([m for m in grafo if grau[m] == 0])
        ordem = []

        while fila:
            atual = fila.popleft()
            ordem.append(atual)

            for viz in grafo[atual]:
                grau[viz] -= 1
                if grau[viz] == 0:
                    fila.append(viz)

        return ordem
    
if __name__ == '__main__':
    pass