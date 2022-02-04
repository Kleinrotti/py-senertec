class canipError(object):
    """Represents an error of a board."""
    boardName = str()
    """Name of the board."""
    counter = int()
    """Counter how often the error occured."""
    currentError = bool()
    """Is the error still present."""
    code = str()
    """Error code."""
    errorTranslation = str()
    """Human readable error code."""
    errorCategory = str()
    """Human readable error category."""
    timestamp = str()
    """Timestamp when the error happened."""
