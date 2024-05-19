mutable struct FilaPrioridade

    fila::Array{Array{Any, 1}, 1}

    pai::Function
    filho_direito::Function
    filho_esquerdo::Function

end

function FilaPrioridade()

    fila = []

    pai(x)            = (x-1) ÷ 2
    filho_direito(x)  = x*2 + 2
    filho_esquerdo(x) = x*2 + 1

    return FilaPrioridade(fila, pai, filho_direito, filho_esquerdo)

end

function inserir(fp::FilaPrioridade, item::Array{Float64, 2})

    push!(fp.fila, item)

    i::Int = length(fp.fila)

    while i > 1

        pai::Int = fp.pai(i)

        if fp.fila[pai][1] < fp.fila[i][1]

            fp.fila[pai], fp.fila[i] = fp.fila[i], fp.fila[pai]

            i = pai

        else

            break

        end
    end

    return fp

end

function retirar(fp::FilaPrioridade)

    if isempty(fp.fila)

        error("Lista vazia")

    end

    item::Vector = deepcopy(fp.fila[1])

    fp.fila[1] = fp.fila[end]

    pop!(fp.fila)

    i::  Int = 1
    len::Int = length(fp.fila)

    while true

        filho_d::Int = fp.filho_direito(i)
        filho_e::Int = fp.filho_esquerdo(i)

        if filho_e ≤ len

            break

        end

        maior_filho::Int = filho_e

        if filho_d ≤ len && fp.fila[filho_d][1] > fp.fila[filho_e][1]

            maior_filho = filho_d

        end

        if fp.fila[i][1] < fp.fila[maior_filho][1]

            fp.fila[i], fp.fila[maior_filho] = fp.fila[maior_filho], fp.fila[i]

            i = maior_filho

        else

            break

        end
    end

    return item

end
