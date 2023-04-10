from datetime import datetime, timezone


class canipError(object):
    """Represents an error of a board."""

    def __init__(self):
        self.__boardName__ = str()
        """Name of the board."""
        self.__counter__ = int()
        """Counter how often the error occured."""
        self.__currentError__ = bool()
        """Is the error still present."""
        self.__code__ = str()
        """Error code."""
        self.__errorTranslation__ = str()
        """Human readable error code."""
        self.__errorCategory__ = str()
        """Human readable error category."""
        self.__timestamp__ = str()
        """Epoch timestamp when the error happened."""

    @property
    def boardName(self):
        """Return the board name."""
        return self.__boardName__

    @property
    def counter(self):
        """Return how often the error occured."""
        return self.__counter__

    @property
    def currentError(self):
        """Return if the error is currently present."""
        return self.__currentError__

    @property
    def code(self):
        """Return the error code."""
        return self.__code__

    @property
    def errorTranslation(self):
        """Return human readable error message."""
        return self.__errorTranslation__

    @property
    def errorCategory(self):
        """Return human readable error category."""
        return self.__errorCategory__

    @property
    def timestamp(self):
        """Return the timestamp when the error happened."""
        return datetime.fromtimestamp(int(self.__timestamp__) / 1000, timezone.utc)
