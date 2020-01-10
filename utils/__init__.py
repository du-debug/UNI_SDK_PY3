"""
用到一些工具类在此
"""
import unicodedata

def to_utf8(v):
    if isinstance(v, str):
        return v
    else:
        return v.encode("utf8")
