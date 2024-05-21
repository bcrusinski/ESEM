using LinearAlgebra
using DataFrames
using DeepCopy


module Fila_prioridade

    mutable struct FilaPrioridade

        fila::Array{Array{Any, 1}, 1}

        pai::           Function
        filho_direito:: Function
        filho_esquerdo::Function

    end

    function FilaPrioridade()::FilaPrioridade

        fila::Array{Array{Any, 1}, 1} = []
    
        pai(x)::           Function = (x-1) ÷ 2
        filho_direito(x):: Function = x*2 + 2
        filho_esquerdo(x)::Function = x*2 + 1
    
        return FilaPrioridade(fila, pai, filho_direito, filho_esquerdo)
    
    end
    
    function inserir(self::FilaPrioridade, item::Array{Float64, String, String})::FilaPrioridade
    
        push!(self.fila, item)
    
        i::Int = length(self.fila)
    
        while i > 1
    
            pai::Int = self.pai(i)
    
            if self.fila[pai][1] < self.fila[i][1]
    
                self.fila[pai], self.fila[i] = self.fila[i], self.fila[pai]
    
                i = pai
    
            else
    
                break
    
            end
        end
    
        return self
    
    end
    
    function retirar(self::FilaPrioridade)::Array{Float64, String, String}
    
        if isempty(self.fila)
    
            error("Lista vazia")
    
        end
    
        item::Vector = deepcopy(self.fila[1])
    
        self.fila[1] = self.fila[end]
    
        pop!(self.fila)
    
        i::  Int = 1
        len::Int = length(self.fila)
    
        while true
    
            filho_d::Int = self.filho_direito(i)
            filho_e::Int = self.filho_esquerdo(i)
    
            if filho_e ≤ len
    
                break
    
            end
    
            maior_filho::Int = filho_e
    
            if filho_d ≤ len && self.fila[filho_d][1] > self.fila[filho_e][1]
    
                maior_filho = filho_d
    
            end
    
            if self.fila[i][1] < self.fila[maior_filho][1]
    
                self.fila[i], self.fila[maior_filho] = self.fila[maior_filho], self.fila[i]
    
                i = maior_filho
    
            else
    
                break
    
            end
        end
    
        return item
    
    end
    
end


module Date_ESEM

    mutable struct DateESEM

        dado::DataFrame

    end 

    function DateESEM(dado::DataFrame)::Date_ESEM 

        return DateESEM(dado)

    end

    function _pontuacao(pessoa_0::Vector{Any}, pessoa_1::Vector{Any})::Int

        genero::     Tuple{String, String} = (pessoa_0[2], pessoa_1[2])
        sexualidade::Tuple{String, String} = (pessoa_0[3], pessoa_1[3])
        nomes::      Tuple{String, String} = (pessoa_0[1], pessoa_1[1])
        respostas::  Vector{Float64}       = [i - j for (i, j) in zip(pessoa_0[4:end], pessoa_1[4:end])]

        combinacoes_incompativeis::Dict{String, Set{Tuple{String, String}}} = Dict(

            "Hetero"    => Set([("F", "F"), ("M", "M")]),
            "Gay"       => Set([("M", "F"), ("F", "M"), ("F", "NB")]),
            "Lesbica"   => Set([("F", "M"), ("M", "F"), ("M", "NB")]),
            "Bissexual" => Set{Tuple{String, String}}(),
            "NB"        => Set{Tuple{String, String}}()

        )

        if genero in combinacoes_incompativeis[sexualidade[1]] || genero in combinacoes_incompativeis[sexualidade[2]]

            return 100.0

        else

            pontuacao::Float64 = dot(respostas, respostas)

            return pontuacao

        end
    end
    
    function agrupar_casais(self::Date_ESEM, colunas_interesse::Union{Vector{Symbol}, Nothing} = nothing)::Set{(String, String)}
        # Se colunas_interesse não for especificado, entende-se que todas as colunas imputadas à classe são os dados de interesse
        
        if colunas_interesse isa Vector{Symbol}

            dado::DataFrame = deepcopy(self.dado[:, colunas_interesse])

        elseif colunas_interesse === nothing

            dado::DataFrame = deepcopy(self.dado)

        else
            throw(ArgumentError("As colunas de interesse só são suportadas para o tipo Vector{Symbol} ou entregue o DataFrame pronto ao carregar o objeto."))
        end
        
        len::Int = size(dado, 1)
        
        fila_prioridade::FilaPrioridade = FilaPrioridade()
        
        for i in 1:len

            for j in 1:len

                if i != j

                    fila_prioridade.inserir(self._pontuacao(dado[i, :], dado[j, :]))

                end
            end
        end
        
        pessoas::Set{str}              = Set()
        casais:: Set{Array{str, str}}  = Set()
        
        while !isempty(fila_prioridade)

            par::Array{Float64, String, String} = fila_prioridade.retirar()
            
            if par[2] ∉ pessoas && par[3] ∉ pessoas

                push!(casais, par[2:3])  # [2:3] é para retirar apenas o nome do casal
                push!(pessoas, Set([par[2], par[3]]))

            end
        end
        
        return casais
    end
    
end

