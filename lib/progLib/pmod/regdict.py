
import re

###########
# NUMERIC #
###########

RE_INT      = re.compile(r'([+-]*\d+)')
RE_DIGITS   = re.compile(r"(\d+)")
RE_DIGITSPC = re.compile(DIGIT+r"\s+")

RE_FLOAT        = re.compile(r'([+-]*\d+\.*\d*)')
RE_SCIFLOAT     = re.compile(r'(?:[+-]*\d+\.*\d*)+(?:[edED]+[+-]*\d+)?')
RE_CHARFLOAT    = re.compile(r'(?:[a-zA-Z]+)?(?:[+-]*\d+\.*\d*)+')
RE_CHARSCIFLOAT = re.compile(r'(?:[a-zA-Z]+)?(?:[+-]*\d+\.*\d*)+(?:[edED]+[+-]*\d+)?')

RE_BOOL = re.compile(r'(?:TRUE|True|true|FALSE|False|false)')
RE_BOOL_FR = re.compile(r'(?:VRAI|Vrai|vrai|FAUX|Faux|faux)')


###########
# STRINGS #
###########

RE_SPCSPLIT = re.compile(r'(\S+)+')