from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()

class Funcionarios(BaseModel):
    nome: str
    cargo: str
    salario: int

class Percentual(BaseModel):
    percentual: int

funcionarios = [
    {"id": 1, "nome": "Carlos", "cargo": "Vendedor", "salario": 2200},
    {"id": 2, "nome": "Ana", "cargo": "Gerente", "salario": 4500},
    {"id": 3, "nome": "João", "cargo": "Caixa", "salario": 2100}
]

@app.get('/')
def inicio():
    return {'mensagem':'Essa é uma API de funcionários'}

@app.get('/funcionarios')
def apresentar_funcionarios():
    return funcionarios

@app.get('/funcionarios/lista')
def lista(pagina: int, quantidade: int):
    if pagina >0 and quantidade >0:
        inicio = (pagina - 1) * quantidade
        fim = inicio + quantidade
        return {"pagina": pagina, "quantidade": quantidade, "total de funcionários": len(funcionarios), "funcionários": funcionarios[inicio:fim]}
    raise HTTPException(status_code=400, detail='Pagina e quantidade devem ser maiores que ZERO')

@app.get('/funcionarios/ordenar')
def salarios_ordenados():
    salarios = sorted(funcionarios, key=lambda funcionario: funcionario['salario'], reverse=True)
    return salarios


@app.get('/funcionarios/salario/{salario}')
def salarios_maiores_que(salario: int):
    salarios = [f for f in funcionarios if f['salario'] >= salario]

    if not salarios:
        raise HTTPException(status_code=404, detail='Nenhum funcionário com sálario maior ou igual ao digitado')

    return salarios


@app.get('/funcionarios/maior_salario')
def funcionario_maior_salario():
    maior_salario = funcionarios[0]
    for funcionario in funcionarios:
        if funcionario['salario'] > maior_salario['salario']:
            maior_salario = funcionario
    return maior_salario

@app.get('/funcionarios/cargo/{cargo}')
def buscar_por_cargo(cargo: str):
    encontrados = [f for f in funcionarios if f['cargo'].lower() == cargo.lower()]

    if not encontrados:
        raise HTTPException(status_code=404, detail='Funcionário não encontrado')

    return encontrados

@app.get('/funcionarios/{cargo}/{salario_minimo}')
def cargo_salario(cargo: str, salario_minimo: int):
    lista = []
    for funcionario in funcionarios:
        if funcionario['cargo'].lower() == cargo.lower() and funcionario['salario'] >= salario_minimo:
                lista.append(funcionario)
    if lista:
        return lista

    raise HTTPException(status_code=404, detail='Nenhum funcionário encontrado')

@app.get('/funcionarios/buscar')
def buscar_nome(nome: str, cargo: str):
     for funcionario in funcionarios:
         if funcionario['nome'].lower() == nome.lower() and funcionario['cargo'].lower() == cargo.lower():
             return funcionario

     raise HTTPException(status_code=404, detail='Funcionário não encontrado')

@app.get('/funcionarios/{id}')
def buscar_funcionario(id: int):
    for funcionario in funcionarios:
        if funcionario['id'] == id:
            return funcionario
    raise HTTPException(status_code=404, detail='Funcionário não encontrado')

@app.post('/funcionarios')
def criar_funcionario(funcionario: Funcionarios):
    dados = funcionario.model_dump()
    dados['id'] = len(funcionarios) + 1
    funcionarios.append(dados)
    return 'Funcionario criado com sucesso'

@app.post('/funcionarios/aumentar/{id}')
def aumentar_salario(id: int, percentual: Percentual):
    for funcionario in funcionarios:
        if funcionario['id'] == id:
            if percentual.percentual >0:
                aumento = funcionario['salario'] * percentual.percentual / 100
                funcionario['salario'] += aumento
                return funcionario
            raise HTTPException(status_code=400, detail='O percentual deve ser maior que 0')
    raise HTTPException(status_code=404, detail='Funcionário não encontrado')



@app.put('/funcionarios/{id}')
def atualizar_funcionario(id: int, funcionario: Funcionarios):
    for item in funcionarios:
        if item['id'] == id:
            dados = funcionario.model_dump()
            dados['id'] = item['id']
            indice = funcionarios.index(item)
            funcionarios[indice] = dados
            return 'Funcionário atualizado'
    raise HTTPException(status_code=404, detail='Funcionário não encontrado')

@app.delete('/funcionarios/{id}')
def remover_funcionario(id: int):
    for funcionario in funcionarios:
        if funcionario['id'] == id:
            if funcionario['cargo'].lower() == 'gerente':
                raise HTTPException(status_code=400, detail='Gerente não pode ser removido')

            funcionarios.remove(funcionario)
            return 'Funcionário removido'
    raise HTTPException(status_code=404, detail='Funcionário não encontrado')
