class Household():
    def __init__(self, id, size, type, persons):
        self.id = id
        self.size = size
        self.type = type
        self.persons = persons

    def __str__(self) -> str:
        return  "{}: ({}, {}, {})".format(self.id, self.size, self.type, self.persons)

    def getdic(self) -> str:
        return {'id':self.id, 'size':self.size, 'type':self.type, 'Persons':self.persons}


# H = Household(1, 3, 'family', [1,2,3])
# print(H)