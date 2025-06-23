import re

def is_valid_https(url: str) -> bool:
  patren = r'^https:\/\/[^\s]+$'
  return re.match(patren, url) is not None