
class MissingDependency(Exception):
    """Raise if a program dependency is missing."""
    def __init__(self, message):
        super(MissingDependency, self).__init__(message)