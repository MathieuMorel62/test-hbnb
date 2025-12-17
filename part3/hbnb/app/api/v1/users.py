from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace('users', description="Users operations")

user_model = api.model('User', {
    'first_name': fields.String(required=True, description="First name of the user"),
    'last_name': fields.String(required=True, description="Last name of the user"),
    'email': fields.String(required=True, description="Email of the user")
})

user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(required=False, description="First name of the user"),
    'last_name': fields.String(required=False, description="Last name of the user"),
    'email': fields.String(required=False, description="Email of the user"),
    'password': fields.String(required=False, description="Password of user")
})

user_model_with_password = api.model('UserWithPassword', {
    "first_name": fields.String(required=True, description="First name of the user"),
    "last_name": fields.String(required=True, description="Last name of the user"),
    "email": fields.String(required=True, description="Email of the user"),
    "password": fields.String(required=True, description="Password of the user")
})

@api.route('/')
class UserList(Resource):
    @jwt_required()
    @api.expect(user_model_with_password, validate=True)
    @api.response(201, "User successfully created")
    @api.response(400, "Email already registered")
    @api.response(400, "Invalid input data")
    @api.response(401, "Unauthorized")
    @api.response(403, "Admin privileges required")
    def post(self):
        """
        Crée un nouvel utilisateur.

        Args:
            user_data (dict): Données de l'utilisateur à créer.
        
        Returns:
            tuple: Données de l'utilisateur et code HTTP.
        """
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        if not is_admin:
            return {'error': "Admin privileges required"}, 403

        user_data = api.payload

        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': "Email already registered"}, 400
        
        try:
            new_user = facade.create_user(user_data)
            return {
                'id': new_user.id,
                'first_name': new_user.first_name,
                'last_name': new_user.last_name,
                'email': new_user.email
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400
        
    @api.response(200, "List of users retrieved successfully")
    def get(self):
        """
        Récupère tous les utilisateurs.

        Returns:
            list: Liste des utilisateurs.
        """
        users = facade.get_all_users()
        return [
            {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            } for user in users
        ], 200


@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, "User details retrieved successfully")
    @api.response(404, "User not found")
    def get(self, user_id):
        """
        Récupère les détails d'un utilisateur.

        Args:
            user_id (str): Identifiant de l'utilisateur.
            
        Returns:
            tuple: Données de l'utilisateur et code HTTP.
        """
        user = facade.get_user(user_id)
        if not user:
            return {'error': "User not found"}, 404
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200

    @jwt_required()
    @api.expect(user_update_model, validate=False)
    @api.response(200, "User successfully updated")
    @api.response(404, "User not found")
    @api.response(400, "Invalid input data")
    @api.response(400, "Email already registered")
    @api.response(400, 'You cannot modify email or password')
    @api.response(403, 'Unauthorized action')
    @api.response(401, 'Unauthorized')
    def put(self, user_id):
        """
        Met à jour les détails d'un utilisateur.

        Args:
            user_id (str): Identifiant de l'utilisateur.
            user_data (dict): Données de l'utilisateur à mettre à jour.
                
        Returns:
            tuple: Données de l'utilisateur et code HTTP.
        """
        current_user = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        
        # Vérifie d'abord si l'utilisateur existe
        user = facade.get_user(user_id)
        if not user:
            return {'error': "User not found"}, 404

        # Vérifie l'autorisation : admin OU propriétaire
        if not is_admin and current_user != user_id:
            return {'error': "Unauthorized action"}, 403

        user_data = api.payload.copy()

        # Si ce n'est pas un admin, bloque la modification d'email/password
        if not is_admin:
            if 'email' in user_data:
                return {'error': 'You cannot modify email or password'}, 400
            if 'password' in user_data:
                return {'error': 'You cannot modify email or password'}, 400
        else:
            # Si c'est un admin, vérifie l'unicité de l'email si modifié
            if 'email' in user_data:
                existing_user = facade.get_user_by_email(user_data['email'])
                if existing_user and existing_user.id != user_id:
                    return {'error': "Email already registered"}, 400

        try:
            updated_user = facade.update_user(user_id, user_data)
            if not updated_user:
                return {'error': "User not found"}, 404

            return {
                'id': updated_user.id,
                'first_name': updated_user.first_name,
                'last_name': updated_user.last_name,
                'email': updated_user.email
            }, 200

        except ValueError as e:
            return {'error': str(e)}, 400
