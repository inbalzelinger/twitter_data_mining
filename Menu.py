
class menu:

    def __init__(self):
        self.l = 'l'

    def key_words(self):
        user_input = input("enter your search key words\n")
        return user_input

    def location(self):
        user_input = input("chose tweets contry:\n"
                           "")
        return user_input

    def aggregate_by (self):
        user_input = input("aggregate by:\n")
        return user_input