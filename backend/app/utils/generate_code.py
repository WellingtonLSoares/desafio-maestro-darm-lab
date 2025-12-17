from random import choices
from string import digits

def generate_reset_code():
  return ''.join(choices(digits, k=6))
