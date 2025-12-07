class Sensor:
    def __init__(self, name, unit, lower_limit, upper_limit):
        assert isinstance(lower_limit, (float, int))
        assert isinstance(upper_limit, (float, int))
        assert upper_limit > lower_limit

        self.name = name
        self.unit = unit
        self.range = (lower_limit, upper_limit)
        self.__raw = None
        self.offset = 0
        self.gain = 1

    def set_raw(self, raw):
        self.__raw = raw

    def calibrate(self, offset, gain):
        self.offset = offset
        self.gain = gain

    def read(self):
        if self.__raw is None:
            return None

        read = (self.__raw + self.offset) * self.gain

        if read > self.range[0] and read < self.range[1]:
            return read
        else:
            return None
