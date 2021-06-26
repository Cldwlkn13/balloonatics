from django.core.validators import RegexValidator

alpha = RegexValidator(r'^[a-zA-Z ]*$', 'Only letters are allowed.')
alphanumeric = RegexValidator(r'^[0-9a-zA-Z ]*$', 'Only alphanumeric characters are allowed.')
numeric = RegexValidator(r'^[0-9]*$', 'Only numbers are allowed.')
phone = RegexValidator(r'^[0-9+]{10,13}$', 'Invalid Phone Number format.')

