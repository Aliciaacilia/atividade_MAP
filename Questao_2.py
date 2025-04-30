from abc import ABC, abstractmethod

class Pedido:
    def __init__(self, identificador, itens):
        self.identificador = identificador
        self.itens = itens  
        self.valor_total = 0

    def calcular_total(self):
        self.valor_total = sum(quantidade * preco for nome, quantidade, preco in self.itens)
        return self.valor_total


class EstoqueInterface(ABC):
    @abstractmethod
    def verificar_disponibilidade(self, produto, quantidade):
        pass

    @abstractmethod
    def atualizar_estoque(self, produto, quantidade):
        pass


class ServicoEstoque(EstoqueInterface):
    def __init__(self):
        self.produtos = {"Notebook": 10, "Mouse": 50, "Teclado": 30}

    def verificar_disponibilidade(self, produto, quantidade):
        return produto in self.produtos and self.produtos[produto] >= quantidade

    def atualizar_estoque(self, produto, quantidade):
        if self.verificar_disponibilidade(produto, quantidade):
            self.produtos[produto] -= quantidade
        else:
            raise Exception(f"Quantidade insuficiente em estoque para: {produto}")


class RepositorioPedidos(ABC):
    @abstractmethod
    def registrar_pedido(self, pedido):
        pass


class GravadorDePedidos(RepositorioPedidos):
    def registrar_pedido(self, pedido):
        with open(f"registro_pedido_{pedido.identificador}.txt", "w") as arquivo:
            arquivo.write(f"Pedido Nº {pedido.identificador} - Total: R$ {pedido.valor_total:.2f}")


class ComunicadorCliente(ABC):
    @abstractmethod
    def enviar_confirmacao(self, pedido):
        pass


class EmailServico(ComunicadorCliente):
    def enviar_confirmacao(self, pedido):
        print(f"E-mail enviado para o cliente do Pedido Nº {pedido.identificador} - Total: R$ {pedido.valor_total:.2f}")


class ProcessadorDePedidos:
    def __init__(self, estoque: EstoqueInterface, repositorio: RepositorioPedidos, comunicador: ComunicadorCliente):
        self.estoque = estoque
        self.repositorio = repositorio
        self.comunicador = comunicador

    def executar_pedido(self, pedido: Pedido):
        for produto, quantidade, preco in pedido.itens:
            if not self.estoque.verificar_disponibilidade(produto, quantidade):
                raise Exception(f"Produto fora de estoque: {produto}")
            self.estoque.atualizar_estoque(produto, quantidade)

        pedido.calcular_total()
        self.repositorio.registrar_pedido(pedido)
        self.comunicador.enviar_confirmacao(pedido)
        return pedido.valor_total
