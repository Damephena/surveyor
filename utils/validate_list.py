from django.core.exceptions import ValidationError

def validate_list(args):
    
    """Verifies that there is at least two choices in choices
    :param String choices: The string representing the user choices.
    """
    values = args.split(',')

    if len(values) < 2:
        raise ValidationError(
        'A list of choices separated by "," is expected. Choices must contain more than one item.'
    )
