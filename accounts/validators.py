from django.core.exceptions import ValidationError


def validate_pin_length(pin):
    if len(pin) < 4 or len(pin) > 4:
        raise ValidationError("pin must be four digits")


def validate_pin(pin):
    if pin != pin:
        raise ValidationError("incorrect pin")
