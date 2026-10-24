produtos = []


def cadastrar_produto(nome, preco, quantidade):
    if not produtos:
        produto = {'nome': nome, 'preço': preco, 'quantidade': quantidade}
        produtos.append(produto)
        return produtos

    for p in produtos:
            if p['nome'].lower() != nome.lower():
                produto = {'nome': nome, 'preço': preco, 'quantidade': quantidade}
                produtos.append(produto)
                return produtos
            return 'Produto já existe'

carro = cadastrar_produto('forza',50000, 1)
carro2 = cadastrar_produto('forza',50000, 1)

print(carro)
print(carro2)

