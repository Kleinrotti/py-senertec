class energyUnit(object):
    """Represents an energy unit."""

    def __init__(self):
        self.serial = str()
        """Serial number of energy unit."""
        self.itemNumber = str()
        """Item number if energy unit."""
        self.model = str()
        """Model name of energy unit."""
        self.connected = bool()
        """Indicates if the unit is connected."""
        self.online = bool()
        """Indicates wether the unit is online or not."""
        self.contact = str()
        """Contact person of the unit."""
        self.city = str()
        """City where the unit is located."""
        self.street = str()
        """Street where the unit is located."""
        self.postalCode = str()
        """Post code where the unit is located."""
        self.locationName = str()
        """Location name of the unit."""
        self.productGroup = str()
