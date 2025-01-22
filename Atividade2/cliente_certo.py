import Pyro4

def main():
    uri = "PYRONAME:itamar_junior"  # Nome do servidor registrado no Name Server
    servidor = Pyro4.Proxy(uri)

    while True:
        print("Menu:")
        print("1. Cadastrar animal")
        print("2. Ler animal")
        print("3. Atualizar animal")
        print("4. Excluir animal")
        print("5. Sair")

        choice = input("Escolha uma opção: ")

        if choice == "1":
            nome = input("Nome do animal: ")
            idade = input("Idade do animal: ")
            sexo = input("Sexo do animal (f / m): ")
            peso = input("Peso do animal: ")
            tamanho = float(input("Tamanho do animal (cm): "))
            telefone = input("Telefone do tutor (apenas números): ")

            response = servidor.cadastrar_animal(nome, idade, sexo, peso, tamanho, telefone)
            print(response)

        elif choice == "2":
            animal_id = int(input("ID do animal: "))
            animal = servidor.ler_animal(animal_id)
            if isinstance(animal, str):
                print(animal)  # Caso o retorno seja uma string (animal não encontrado)
            else:
                print(f"Animal encontrado: {animal}")  # Caso o retorno seja um objeto Animal

        elif choice == "3":
            animal_id = int(input("ID do animal: "))
            nome = input("Nome do animal: ")
            idade = input("Idade do animal: ")
            sexo = input("Sexo do animal (f / m): ")
            peso = input("Peso do animal: ")
            tamanho = float(input("Tamanho do animal (cm): "))
            telefone = input("Telefone do tutor (apenas números): ")

            if servidor.atualizar_animal(animal_id, nome, idade, sexo, peso, tamanho, telefone):
                print("Animal atualizado com sucesso.")
            else:
                print("Animal não encontrado.")

        elif choice == "4":
            animal_id = int(input("ID do animal: "))
            if servidor.excluir_animal(animal_id):
                print("Animal excluído com sucesso.")
            else:
                print("Animal não encontrado.")

        elif choice == "5":
            break

        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()

