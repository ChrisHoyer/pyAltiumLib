# Set up logging
import logging
logger = logging.getLogger(__name__)

class MappingBase:
    """
    Base class for mapping integer values to corresponding string 
    representations. This class provides a common structure for
    handling mapped values.

    :param int value: The integer value to be mapped.
    :raises ValueError: If the provided value is not found in the `_map` dictionary.

    """ 
    
    def __init__(self, value: int):
        if int(value) not in self._map:
            logger.error(f"Failed to map value {value}")
            
        self.value = int(value)
        self.name = self._map[int(value)]

    def __repr__(self):
        """
        Returns the string representation of the mapped value.
        
        :return: The name corresponding to the integer value.
        :rtype: str
        """
        return f"{self.name}"

    def to_int(self):
        """
        Returns the integer value of the mapped object.

        :return: The integer representation.
        :rtype: int
        """
        return self.value

    @classmethod
    def from_name(cls, name: str):
        """
        Construct an instance by name string instead of integer value.

        :param str name: The name string as it appears in the mapping.
        :return: An instance of the class, or None if not found.
        """
        for value, mapped in cls._map.items():
            n = mapped if isinstance(mapped, str) else mapped.get("name", "")
            if n == name:
                return cls(value)
        logger.error(f"Failed to find name '{name}' in {cls.__name__}")
