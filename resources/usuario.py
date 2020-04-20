from flask_restful import Resource, reqparse
from models.usuario import UserModel

class Usuarios(Resource):
    #/usuarios/{user_id}
    def get(self):
        return {'usuarios': [usuario.json() for usuario in UserModel.query.all()]}

class User(Resource):
    @staticmethod
    def get(usuario_id):
        usuario = UserModel.find_user(usuario_id)
        if usuario:
            return usuario.json()
        return {'message': 'User not found.'}, 404 # not found

    def delete(self, usuario_id):
       usuario = UserModel.find_user(usuario_id)
       if usuario:
            try:
                usuario.delete()
            except:
                return {'message': 'An error ocurred trying to delete user.'}, 500
            return {'message': 'User deleted.'}
       return {'message': 'User not found.'}, 404

class UserRegister(Resource):
    # /cadastro
    def post(self):
        argumentos = reqparse.RequestParser()
        argumentos.add_argument('login', type=str, required=True, help="This field 'login' cannot be left empty.")
        argumentos.add_argument('senha', type=str, required=True, help="This field 'password' cannot be left empty.")
        dados = argumentos.parse_args()

        if UserModel.find_by_login(dados['login']):
            return {"message": "The login '{}' already exists.".format(dados['login'])}

        user = UserModel(**dados)
        user.save_user()
        return {'message': "User created successfully!"}, 201 #Created