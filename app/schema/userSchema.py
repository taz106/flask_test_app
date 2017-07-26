from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    name = fields.String(
        required=True,
        error_messages={'required': 'Name is required.'} 
    )
    age = fields.Integer(
        required=True,
        error_messages={'required': 'Age is required.'}
    )
    city = fields.String(
        required=True,
        error_messages={'required': {'message': 'City required', 'code': 400}}
    )
    email = fields.Email(
        required=True,
        error_messages={'required': {'message': 'Not a Valid Email', 'code': 400}}
    )