class Person():
    def __init__(self, id, age, sex, ethnicity, religion):
        self.id = id
        self.age = age
        self.sex = sex
        self.ethnicity = ethnicity
        self.religion = religion

    def __eq__(self, other) -> bool:
        return (self.age, self.sex, self.ethnicity, self.religion) == (other.age, other.sex, other.ethnicity, other.religion)

    def __str__(self) -> str:
        return  "[{}: {}, {}, {}, {}]".format(self.id, self.age, self.sex, self.ethnicity, self.religion)

    def getdic(self) -> str:
        return {'id':self.id, 'age':self.age, 'sex':self.sex, 'ethnicity':self.ethnicity, 'religion':self.religion}

# p = Person(1, 24, 'Male', 'White', 'Muslim')
# q = Person(2, 20, 'Female', 'Asian', 'Sikh')
# r = Person(3, 55, 'Male', 'Asian', 'Hindu')
# print(p)
# Persons = []
# Persons.append(p)
# Persons.append(q)
# Persons.append(r)
# s = Person(4,20, 'Female', 'Asian', 'Sikh')

# print(p.getdic())