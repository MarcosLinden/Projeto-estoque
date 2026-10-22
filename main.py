produtos = []


def cadastrar_produto(nome, preco, quantidade):
    produto = {'nome': nome, 'preço': preco, 'quantidade': quantidade}
    for p in produtos:
        if not p['nome'].lower() == produto['nome'].lower():
            produtos.append(produto)
            return produtos
    return 'Produto já existe'

