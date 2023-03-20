class Validator:
    
  def __init__(self, value):
    self.value = value
    self.is_valid = True
    self.errors = []
    self.lowercase_alpha = 'abcdefghijklmnopqrstuvwxyz'
    self.uppercase_alpha = self.lowercase_alpha.upper()
    self.numbers = '1234567890'
    self.max_length = None
    self.max_length_error = None
    self.min_length = None
    self.min_length_error = None
    self.whitelist = None
    self.whitelist_error = None

  def set_string_name(self, string_name):
    self.string_name = string_name
    return self

  def set_max_length(self, max_length, max_length_error):
    self.max_length = max_length
    self.max_length_error = max_length_error
    return self
  
  def set_min_length(self, min_length, min_length_error):
    self.min_length = min_length
    self.min_length_error = min_length_error
    return self
  
  def set_whitelist(self, allowed_symbols, whitelist_error, allow_uppercase_letters=True, allow_lowercase_letters=True, allow_numbers=True):
    whitelist = ''
    if allow_uppercase_letters == True: whitelist += self.uppercase_alpha
    if allow_lowercase_letters == True: whitelist += self.lowercase_alpha
    if allow_numbers == True: whitelist += self.numbers
    whitelist += allowed_symbols
    self.whitelist = whitelist
    self.whitelist_error = whitelist_error
    return self

  def validate(self):
    if self.max_length != None: self.check_max_length()
    if self.min_length != None: self.check_min_length()
    if self.whitelist != None: self.check_whitelist()

  def check_max_length(self):
    if len(self.value) > self.max_length:
      self.is_valid = False
      self.errors.append(self.max_length_error)
  
  def check_min_length(self):
    if len(self.value) < self.min_length:
      self.is_valid = False
      self.errors.append(self.min_length_error)

  def check_whitelist(self):
    operation_failed = False
    for value_char in self.value:
      found_char = False
      for whitelist_char in self.whitelist:
        if value_char == whitelist_char:
          found_char = True
          break
      if found_char == False:
        self.errors.append(self.whitelist_error)
        self.is_valid = False
        break

