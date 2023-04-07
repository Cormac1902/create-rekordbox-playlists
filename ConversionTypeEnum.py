from enum import Flag, auto


class ConversionType(Flag):
    NONE = auto()
    DOWNSAMPLE = auto()
    WAV = auto()
    BIT_24 = auto()
