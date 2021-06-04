from enum import Enum


class Sex(Enum):
    MALE = 'M'
    FEMALE = 'F'


class Tree:
    def __init__(self, first_name, second_name, sex: str):
        self.first_name = first_name
        self.second_name = second_name
        self.father = None
        self.mother = None
        self.children = []
        self.date = None
        self.sex = Sex.FEMALE if sex == 'F' else Sex.MALE
        pass

    def showParents(self):
        print(str(self.father.first_name) + "\t" + str(self.mother.first_name))

    def add_child(self, child):
        self.children.append(child)

    def delete(self, root):
        if root.father:
            self.delete(root.father)
        if root.mother:
            self.delete(root.mother)
        for child in root.childer:
            self.delete(child)


    def get_birth_day(self):
        print(self.get_birth_day()) if self.date else print("There is no date ")

