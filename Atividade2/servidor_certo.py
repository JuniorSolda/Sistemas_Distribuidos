import Pyro4
from Pyro4.util import SerpentSerializer

# Classe que representa o animal
@Pyro4.expose
class Animal:
    def __init__(self, id, nome, idade, sexo, peso, tamanho, telefone):
        self.id = id
        self.nome = nome
        self.idade = idade
        self.sexo = sexo
        self.peso = peso
        self.tamanho = tamanho
        self.telefone = telefone

    def __repr__(self):
        return (f"Animal(ID: {self.id}, Nome: {self.nome}, Idade: {self.idade}, "
                f"Sexo: {self.sexo}, Peso: {self.peso}, Tamanho: {self.tamanho} cm, "
                f"Telefone: {self.telefone})")

# Classe CRUD para gerenciar os animais
@Pyro4.expose
class CRUD:
    def __init__(self):
        self.animais = {}
        self.animal_id = 1

    def cadastrar_animal(self, nome, idade, sexo, peso, tamanho, telefone):
        animal = Animal(self.animal_id, nome, idade, sexo, peso, tamanho, telefone)
        self.animais[self.animal_id] = animal
        print(f"Animal cadastrado: {animal}")  # Log no servidor
        self.animal_id += 1
        return f"Animal cadastrado com sucesso! ID: {animal.id}"

    def ler_animal(self, animal_id):
        if animal_id in self.animais:
            animal = self.animais[animal_id]
            print(f"Animal encontrado: {animal}")  # Log no servidor
            return animal  # Retorna o objeto Animal
        print(f"Animal com ID {animal_id} não encontrado.")  # Log no servidor
        return f"Animal com ID {animal_id} não encontrado."

    def atualizar_animal(self, animal_id, nome, idade, sexo, peso, tamanho, telefone):
        if animal_id in self.animais:
            self.animais[animal_id] = Animal(animal_id, nome, idade, sexo, peso, tamanho, telefone)
            print(f"Animal atualizado: {self.animais[animal_id]}")  # Log no servidor
            return True
        print(f"Animal com ID {animal_id} não encontrado para atualização.")  # Log no servidor
        return False

    def excluir_animal(self, animal_id):
        if animal_id in self.animais:
            print(f"Animal excluído: {self.animais[animal_id]}")  # Log no servidor
            del self.animais[animal_id]
            return True
        print(f"Animal com ID {animal_id} não encontrado para exclusão.")  # Log no servidor
        return False

# Função principal do servidor
def main():
    # Configura a serialização para a classe Animal
    serializer = SerpentSerializer()
    serializer.register_class_to_dict(Animal, lambda obj: obj.__dict__)
    serializer.register_dict_to_class("Animal", lambda d: Animal(**d))

    # Configuração do servidor Pyro4
    host = '127.0.0.1'
    port = 12345

    # Inicializa o daemon Pyro4
    daemon = Pyro4.Daemon(host=host, port=port)

    # Registra a classe CRUD como objeto Pyro
    uri = daemon.register(CRUD)

    # Conecta ao Name Server e registra o servidor
    nameserver = Pyro4.locateNS(host='localhost', port=9090)
    nameserver.register("itamar_junior", uri)

    print("Servidor pronto para receber conexões...")
    daemon.requestLoop()

if __name__ == "__main__":
    main()

