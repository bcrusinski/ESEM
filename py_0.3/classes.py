import numpy as np 
import pandas as pd

from typing import Union 
from copy import deepcopy

class FilaPrioridade:    
    def __init__(self) -> None:

        self.fila = []

        self.pai            = lambda x: (x-1)//2
        self.filho_direito  = lambda x: x*2 + 2
        self.filho_esquerdo = lambda x: x*2 + 1
        
        return None

    def inserir(self, item: np.ndarray) -> "FilaPrioridade":
        self.fila.append(item)
        
        i: int = np.shape(self.fila)[0] - 1

        while i > 0:
            pai = self.pai(i)
            if self.fila[pai][0] > self.fila[i][0]:
                self.fila[pai], self.fila[i] = self.fila[i], self.fila[pai]
                i = pai
            else:
                break

        return self

    def retirar(self) -> np.ndarray:
        if np.shape(self.fila)[0] == 0:
            raise ValueError("Lista vazia")

        item: np.ndarray = deepcopy(self.fila[0])
        self.fila[0] = self.fila[-1]
        self.fila.pop()
        
        i: int = 0
        len: int = np.shape(self.fila)[0]

        while True:
            filho_d:int = self.filho_direito(i)
            filho_e:int = self.filho_esquerdo(i)

            if filho_e >= len:
                break

            maior_filho = filho_e
            if filho_d < len and self.fila[filho_d][0] < self.fila[filho_e][0]:
                maior_filho = filho_d

            if self.fila[i][0] > self.fila[maior_filho][0]:
                self.fila[i], self.fila[maior_filho] = self.fila[maior_filho], self.fila[i]
                i = maior_filho
            else:
                break

        return item
class Date_ESEM:

    def __init__(self, file_path: Union[str, pd.DataFrame]) -> None:
        
        self.dado: pd.DataFrame = self.__ler_dado(file_path=file_path)
        #self.dado.rename(columns={'Qual a sua sexualidade? ': 'Qual a sua sexualidade?'}, inplace=True)


        return None

    def __ler_dado(self, file_path: Union[str, pd.DataFrame]) -> pd.DataFrame:

        if file_path is pd.DataFrame:

            return file_path

        elif file_path.endswith('.csv'):

            return pd.read_csv(file_path)
        
        elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):

            return pd.read_excel(file_path)
        
        else:

            raise "A extenção do arquivo  deve ser .csv, .xlsx ou .xls; \n também é possivel passar a proprioa clss pandas.DataFrame."
        
    def __pontuacao(self, pessoa_0: pd.DataFrame, pessoa_1: pd.DataFrame) -> float:

        nome:        tuple[str] = pessoa_0['Nome'],        pessoa_1['Nome']
        genero:      tuple[str] = pessoa_0['Qual o seu gênero?'],      pessoa_1['Qual o seu gênero?']
        sexualidade: tuple[str] = pessoa_0['Qual a sua sexualidade?'], pessoa_1['Qual a sua sexualidade?']
        respostas:   np.ndarray = pessoa_0.drop(['Nome','Qual o seu gênero?', 'Qual a sua sexualidade?'], axis=0).to_numpy() - pessoa_1.drop(['Nome','Qual o seu gênero?', 'Qual a sua sexualidade?'], axis=0).to_numpy()

        combinacoes_incompativeis: dict[set] = {
            "Heterossexual": {
                ("F", "F"),
                ("M", "M")
            },
            "Homossexual": {
                ("M", "F"),
                ("F", "M"),
                ("F", "NB")
            },
            "Lesbica": {
                ("F", "M"),
                ("M", "F"),
                ("M", "NB")
            },
            "Bissexual": set(),
            "NB": set()
        }

        if (genero[0], genero[1]) in combinacoes_incompativeis.get(sexualidade[0]) | combinacoes_incompativeis.get(sexualidade[1]):

            return 100
        
        else:

            return np.linalg.norm(respostas)
        
    def agrupar_casais(self, colunas_interesse: list[str], colunas_sou: list[str]) -> set:
        #Ao não adicionar parâmetro entende-se que tdas as colunas imputadas a classe são os dados de interresse

        if len(colunas_interesse) != len(colunas_sou):

            raise ('colunas imcompativos, reveja as entradas')
        
        colunas_default: list =  ['Nome', 'Qual o seu gênero?', 'Qual a sua sexualidade?']

        colunas_interesse, colunas_sou = colunas_interesse + colunas_default, colunas_sou + colunas_default

        dado_i: pd.DataFrame = self.dado[colunas_interesse]
        dado_s: pd.DataFrame = self.dado[colunas_sou]

        lenth: int =  dado_i.shape[0]
        
        fila_prioridade: FilaPrioridade = FilaPrioridade()

        for i in range(0, lenth):

            for j in range(0, lenth):

                if i != j:

                    pontuacao = self.__pontuacao(dado_i.iloc[i], dado_s.iloc[j]) + self.__pontuacao(dado_s.iloc[i], dado_i.iloc[j]) 
                    if pontuacao != 200: 
                        fila_prioridade.inserir(np.array([pontuacao, dado_i.iloc[i]['Nome'], dado_s.iloc[j]['Nome']]))

        pessoas: set[str]        = set()
        casais: set[tuple[str, str, float]] = set()

        while np.shape(fila_prioridade.fila)[0] > 0:

            par: tuple[float, str, str] = fila_prioridade.retirar()

            if par[1] not in pessoas and par[2] not in pessoas and par[0] != 200:

                casais.add((par[0], par[1], par[2]))
                pessoas.add(par[1])
                pessoas.add(par[2])

            else:
                pass
        

        #print(pessoas)
        return casais

teste = Date_ESEM('C:\\Users\\Bruno\\Downloads\\DATE ESEM(72)_limpo.xlsx')

sou =["Palavras de afirmação ", "Tempo de qualidade", "Presentes", "Atos de serviço ", "Toque físico ", "Rock", "Trap", "Funk", "MPB", "Rap Nacional", "Sertanejo ", "Samba", "Kpop", "Ação ", "Romance", "Aventura", "Drama", "Comédia", "Ficção científica ", "Comédia Brasileira", "Column", "Esportes", "Pintura", "Teatro", "Cinema", "Dança", "Desenhar", "Introvertida", "Extrovertida"]
interesse =["Palavras de afirmação 2", "Tempo de qualidade2", "Presentes2", "Atos de serviço  2", "Toque físico 2", "Rock2", "Trap2", "Funk2", "MPB2", "Rap Nacional2", "Sertanejo 2", "Samba2", "Kpop2", "Ação 2", "Romance2", "Aventura2", "Drama2", "Comédia2", "Ficção científica 2", "Comédia Brasileira2", "2", "Esportes2", "Pintura2", "Teatro2", "Cinema2", "Dança2", "Desenhar2", "Introvertida2", "Extrovertida2"]
resposta = teste.agrupar_casais(interesse, sou) 
print(resposta)