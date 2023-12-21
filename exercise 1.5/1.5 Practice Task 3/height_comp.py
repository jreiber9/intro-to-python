class Height(object):
    def __init__(self, feet, inches):
        self.feet = feet
        self.inches = inches

    def __lt__(self, other):
        height_inches_A = self.feet * 12 + self.inches
        height_inches_B = other.feet * 12 + other.inches
        return height_inches_A < height_inches_B

    def __le__(self, other):
        height_inches_A = self.feet * 12 + self.inches
        height_inches_B = other.feet * 12 + other.inches
        return height_inches_A <= height_inches_B

    def __eq__(self, other):
        height_inches_A = self.feet * 12 + self.inches
        height_inches_B = other.feet * 12 + other.inches
        return height_inches_A == height_inches_B
    
    def __gt__(self, other):
        height_inches_A = self.feet * 12 + self.inches
        height_inches_B = other.feet * 12 + other.inches
        return height_inches_A > height_inches_B
    
    def __ge__(self, other):
        height_inches_A = self.feet * 12 + self.inches
        height_inches_B = other.feet * 12 + other.inches
        return height_inches_A >= height_inches_B

    def __ne__(self, other):
        height_inches_A = self.feet * 12 + self.inches
        height_inches_B = other.feet * 12 + other.inches
        return height_inches_A != height_inches_B

# height cases
print(Height(4, 6) > Height(4, 5))
print(Height(4, 5) >= Height(4, 5))
print(Height(5, 9) != Height(5, 10))
    




