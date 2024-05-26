from django.core.exceptions import ValidationError


class ContainsLetterValidator:
    def validate(self, password, user=None):
        if not any(char.isalpha() and char.isupper() for char in password):
            raise ValidationError(
                'Le mot de passe doit contenir une lettre', code='password_no_letters')

    def get_help_text(self):
        return 'Votre mot de passe doit contenir au moins une lettre Majuscule .'

class ContainsNumberValidator:
    def validate(self, password, user=None):
        if not any(character.isdigit() for character in password):
            raise ValidationError(
                'Le mot de passe doit contenir un Chiffre', code='password_no_number')
    def get_help_text(self):
        return 'Votre mot de passe doit contenir au moins un Chiffre .'

class CointainsUppercaseValidator:
    """
    verifie si le nom contient une lettre Majuscule

    """
    def validate(self, username, user=None):
        if not any(characte.isupper() for characte in username):
            raise ValidationError(
                'Le Username doit contenir une lettre Majuscule', code='username_no_upper')

    def get_help_text(self):
        return 'Votre Nom doit contenir au moins une lettre Majuscule .'