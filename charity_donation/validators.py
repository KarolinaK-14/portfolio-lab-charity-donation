from django.core.exceptions import ValidationError

class CustomPasswordValidator():

    def __init__(self, min_length=1):
        self.min_length = min_length

    def validate(self, password, user=None):
        special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"
        if not any(char.isdigit() for char in password):
            raise ValidationError('Hasło musi zawierać co najmniej %(min_length)d cyfrę.' % {'min_length': self.min_length})
        if not any(char.isupper() for char in password):
            raise ValidationError('Hasło musi zawierać co najmniej %(min_length)d wielką literę.' % {'min_length': self.min_length})
        if not any(char.islower() for char in password):
            raise ValidationError('Hasło musi zawierać co najmniej %(min_length)d małą literę.' % {'min_length': self.min_length})
        if not any(char in special_characters for char in password):
            raise ValidationError('Hasło musi zawierać co najmniej %(min_length)d znak specjalny.' % {'min_length': self.min_length})

    def get_help_text(self):
        return ""