class _MappingBase:
    
    def __init__(self, value: int):
        if int(value) not in self._map:
            raise ValueError(f"Invalid value: {value}")
        self.value = int(value)
        self.name = self._map[int(value)]

    def __repr__(self):
        return f"{self.name}"

    def to_int(self):
        return self.value
