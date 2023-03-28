class Person():
    def __init__(self, id, age, sex, ethnicity, religion, status, qualification):
        self.id = id
        self.age = age
        self.sex = sex
        self.ethnicity = ethnicity
        self.religion = religion
        self.status = status
        self.qualification = qualification

    def __eq__(self, other) -> bool:
        return (self.age, self.sex, self.ethnicity, self.religion, self.status, self.qualification) == (other.age, other.sex, other.ethnicity, other.religion, other.status, other.qualification)

    def __str__(self) -> str:
        return  "[{}: {}, {}, {}, {}, {}, {}]".format(self.id, self.age, self.sex, self.ethnicity, self.religion, self.status, self.qualification)

    def getdic(self) -> str:
        return {'id':self.id, 'age':self.age, 'sex':self.sex, 'ethnicity':self.ethnicity, 'religion':self.religion, 'status': self.status, 'qualification': self.qualification}

# p = Person(1, 24, 'Male', 'White', 'Muslim', 'Single', 'level1')
# p2 = Person(2, 24, 'Male', 'White', 'Muslim', 'Single')
# q = Person(2, 20, 'Female', 'Asian', 'Sikh', 'Single')
# r = Person(3, 55, 'Male', 'Asian', 'Hindu', 'Married')
# print(p)
# Persons = []
# Persons.append(p)
# Persons.append(q)
# Persons.append(r)
# s = Person(4,20, 'Female', 'Asian', 'Sikh')
# print(p==p2)