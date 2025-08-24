from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_dni(value):
    if value is None or value == '':
        return  # Permitir vacío
    if not value.isdigit() or len(value) != 8:
        raise ValidationError(
            _('El DNI debe tener exactamente 8 dígitos.'),
            code='invalid_dni'
        )

def validate_celular(value):
    if value is None or value == '':
        return  # Permitir vacío
    if not value.isdigit() or len(value) != 9:
        raise ValidationError(
            _('El celular debe tener exactamente 9 dígitos.'),
            code='invalid_celular'
        )