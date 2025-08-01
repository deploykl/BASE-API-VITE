from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# ===== Validadores para campos específicos =====
validate_dni = RegexValidator(
    regex=r'^\d{8}$',
    message=_('El DNI debe tener exactamente 8 dígitos.'),
    code='invalid_dni'
)

validate_celular = RegexValidator(
    regex=r'^\d{9}$',
    message=_('El celular debe tener exactamente 9 dígitos.'),
    code='invalid_celular'
)
