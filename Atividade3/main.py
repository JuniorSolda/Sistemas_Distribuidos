import cherrypy
import json

# Serviço de Tutores
class TutorService:
    exposed = True

    def __init__(self):
        self.tutores = {}
        self.tutor_id = 1

    def formatar_erro(self, status, mensagem):
        cherrypy.response.status = status
        cherrypy.response.headers['Content-Type'] = 'application/json'
        return json.dumps({"error": mensagem}).encode('utf-8')

    def buscar(self, id=None):
        cherrypy.response.headers['Content-Type'] = 'application/json'
        if id is None:
            return json.dumps(
                [{"id": k, **v} for k, v in self.tutores.items()]
            ).encode('utf-8')
        else:
            id = int(id)
            if id in self.tutores:
                return json.dumps(self.tutores[id]).encode('utf-8')
            else:
                return self.formatar_erro(404, "Tutor não encontrado.")

    def inserir(self):
        try:
            data = json.loads(cherrypy.request.body.read().decode('utf-8'))
        except Exception as e:
            return self.formatar_erro(400, f"Erro ao processar dados JSON: {str(e)}")

        campos_obrigatorios = ["nome", "telefone", "endereco"]
        for campo in campos_obrigatorios:
            if campo not in data:
                return self.formatar_erro(400, f"Campo '{campo}' faltando.")

        tutor = {
            "nome": data["nome"],
            "telefone": data["telefone"],
            "endereco": data["endereco"]
        }
        self.tutores[self.tutor_id] = tutor
        self.tutor_id += 1

        cherrypy.response.status = 201
        return json.dumps({"message": "Tutor cadastrado com sucesso.", "id": self.tutor_id - 1}).encode('utf-8')

    def atualizar(self, id):
        try:
            data = json.loads(cherrypy.request.body.read().decode('utf-8'))
        except Exception as e:
            return self.formatar_erro(400, f"Erro ao processar dados JSON: {str(e)}")

        id = int(id)
        if id not in self.tutores:
            return self.formatar_erro(404, "Tutor não encontrado.")

        tutor = self.tutores[id]
        for key, value in data.items():
            if key in tutor:
                tutor[key] = value

        cherrypy.response.status = 200
        return json.dumps({"message": "Tutor atualizado com sucesso."}).encode('utf-8')

    def deletar(self, id):
        id = int(id)
        if id not in self.tutores:
            return self.formatar_erro(404, "Tutor não encontrado.")

        del self.tutores[id]
        cherrypy.response.status = 200
        return json.dumps({"message": "Tutor excluído com sucesso."}).encode('utf-8')

# Serviço de Animais
class AnimalService:
    exposed = True

    def __init__(self, tutor_service):
        self.animais = {}
        self.animal_id = 1
        self.tutor_service = tutor_service

    def formatar_erro(self, status, mensagem):
        cherrypy.response.status = status
        cherrypy.response.headers['Content-Type'] = 'application/json'
        return json.dumps({"error": mensagem}).encode('utf-8')

    def buscar(self, id=None):
        cherrypy.response.headers['Content-Type'] = 'application/json'
        if id is None:
            return json.dumps(
                [{"id": k, **v} for k, v in self.animais.items()]
            ).encode('utf-8')
        else:
            id = int(id)
            if id in self.animais:
                return json.dumps(self.animais[id]).encode('utf-8')
            else:
                return self.formatar_erro(404, "Animal não encontrado.")

    def inserir(self):
        try:
            data = json.loads(cherrypy.request.body.read().decode('utf-8'))
        except Exception as e:
            return self.formatar_erro(400, f"Erro ao processar dados JSON: {str(e)}")

        campos_obrigatorios = ["nome", "idade", "sexo", "peso", "tamanho", "tutor_id"]
        for campo in campos_obrigatorios:
            if campo not in data:
                return self.formatar_erro(400, f"Campo '{campo}' faltando.")

        try:
            idade = int(data["idade"])
            peso = float(data["peso"])
            tamanho = float(data["tamanho"])
        except ValueError:
            return self.formatar_erro(400, "Idade, peso e tamanho devem ser numéricos.")

        if data["sexo"] not in ["m", "f"]:
            return self.formatar_erro(400, "Sexo deve ser 'm' ou 'f'.")

        tutor_id = int(data["tutor_id"])
        if tutor_id not in self.tutor_service.tutores:
            return self.formatar_erro(404, "Tutor não encontrado.")

        animal = {
            "nome": data["nome"],
            "idade": idade,
            "sexo": data["sexo"],
            "peso": peso,
            "tamanho": tamanho,
            "tutor_id": tutor_id
        }
        self.animais[self.animal_id] = animal
        self.animal_id += 1

        cherrypy.response.status = 201
        return json.dumps({"message": "Animal cadastrado com sucesso.", "id": self.animal_id - 1}).encode('utf-8')

    def atualizar(self, id):
        try:
            data = json.loads(cherrypy.request.body.read().decode('utf-8'))
        except Exception as e:
            return self.formatar_erro(400, f"Erro ao processar dados JSON: {str(e)}")

        id = int(id)
        if id not in self.animais:
            return self.formatar_erro(404, "Animal não encontrado.")

        animal = self.animais[id]
        for key, value in data.items():
            if key in animal:
                animal[key] = value

        cherrypy.response.status = 200
        return json.dumps({"message": "Animal atualizado com sucesso."}).encode('utf-8')

    def deletar(self, id):
        id = int(id)
        if id not in self.animais:
            return self.formatar_erro(404, "Animal não encontrado.")

        del self.animais[id]
        cherrypy.response.status = 200
        return json.dumps({"message": "Animal excluído com sucesso."}).encode('utf-8')


# Configuração do Dispatcher
if __name__ == '__main__':
    dispatcher = cherrypy.dispatch.RoutesDispatcher()
    tutor_service = TutorService()
    animal_service = AnimalService(tutor_service)

    # Rotas para tutores
    dispatcher.connect(name="get_tutores", route="/tutores", controller=tutor_service, action="buscar", conditions=dict(method=["GET"]))
    dispatcher.connect(name="get_tutor", route="/tutores/:id", controller=tutor_service, action="buscar", conditions=dict(method=["GET"]))
    dispatcher.connect(name="create_tutor", route="/tutores", controller=tutor_service, action="inserir", conditions=dict(method=["POST"]))
    dispatcher.connect(name="update_tutor", route="/tutores/:id", controller=tutor_service, action="atualizar", conditions=dict(method=["PUT"]))
    dispatcher.connect(name="delete_tutor", route="/tutores/:id", controller=tutor_service, action="deletar", conditions=dict(method=["DELETE"]))

    # Rotas para animais
    dispatcher.connect(name="get_animais", route="/animais", controller=animal_service, action="buscar", conditions=dict(method=["GET"]))
    dispatcher.connect(name="get_animal", route="/animais/:id", controller=animal_service, action="buscar", conditions=dict(method=["GET"]))
    dispatcher.connect(name="create_animal", route="/animais", controller=animal_service, action="inserir", conditions=dict(method=["POST"]))
    dispatcher.connect(name="update_animal", route="/animais/:id", controller=animal_service, action="atualizar", conditions=dict(method=["PUT"]))
    dispatcher.connect(name="delete_animal", route="/animais/:id", controller=animal_service, action="deletar", conditions=dict(method=["DELETE"]))

    conf = {'/': {'request.dispatch': dispatcher}}
    cherrypy.tree.mount(root=None, config=conf)
    cherrypy.config.update({'server.socket_port': 8080})
    cherrypy.engine.start()
    cherrypy.engine.block()

