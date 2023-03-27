class Person():
    def __init__(self, id, age, sex, ethnicity, religion, status):
        self.id = id
        self.age = age
        self.sex = sex
        self.ethnicity = ethnicity
        self.religion = religion
        self.status = status

    def __eq__(self, other) -> bool:
        return (self.age, self.sex, self.ethnicity, self.religion, self.status) == (other.age, other.sex, other.ethnicity, other.religion, other.status)

    def __str__(self) -> str:
        return  "[{}: {}, {}, {}, {}, {}]".format(self.id, self.age, self.sex, self.ethnicity, self.religion, self.status)

    def getdic(self) -> str:
        return {'id':self.id, 'age':self.age, 'sex':self.sex, 'ethnicity':self.ethnicity, 'religion':self.religion, 'status': self.status}

# p = Person(1, 24, 'Male', 'White', 'Muslim', 'Single')
# p2 = Person(2, 24, 'Male', 'White', 'Muslim', 'Single')
# q = Person(2, 20, 'Female', 'Asian', 'Sikh', 'Single')
# r = Person(3, 55, 'Male', 'Asian', 'Hindu', 'Married')
# print(p)
# Persons = []
# Persons.append(p)
# Persons.append(q)
# Persons.append(r)
# s = Person(4,20, 'Female', 'Asian', 'Sikh')

# print(p.getdic())
# print(p==p2)