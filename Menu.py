import country_bounding_box
class menu:

    def __init__(self):
        self.l = 'l'

    def key_words(self):
        user_input = input("enter your search key words\n")
        lst = [user_input]
        return lst

    def location(self):
        user_input = input("chose tweets country:\nEG for Egypt\nSA for Saudi Arabia\nLB for Lebanon\n")
        return country_bounding_box.country_bounding_boxes.get(user_input)[1]

    def aggregate_by (self):
        user_input = input("aggregate by:\n")
        return user_input
