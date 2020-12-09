# parts of regex
all_letters = "a-zA-ZàâäôéèëêïîçùûüÿæœÀÂÄÔÉÈËÊÏÎŸÇÙÛÜÆŒäöüßÄÖÜẞąćęłńóśźżĄĆĘŁŃÓŚŹŻàèéìíîòóùúÀÈÉÌÍÎÒÓÙÚáéíñóúüÁÉÍÑÓÚÜ"

# english, polish, french, german, italian, spanish letters
letters_only = rf"^[{all_letters}]+$"

letters_spaces_dot = rf"^([{all_letters}.]| )+$"

numbers_only = r"^\d+$"

number_VAT = rf"^[{all_letters}\d+*]+$"
