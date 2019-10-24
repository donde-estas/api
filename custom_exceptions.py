class EmptyNameError(Exception):

    """Exception for when an empty name is given to a new person creator."""

    def __init__(self):
        message = 'EmptyNameError: Cannot parse an empty name'
        super().__init__(message)


class InvalidMailError(Exception):

    """Exception for when a mail does not match with the mail regex."""

    def __init__(self, invalid_mail):
        message = f'InvalidMailError: Invalid mail format: {invalid_mail}'
        super().__init__(message)
