import datetime
import six
import tree as tr
# import ui

month_dict = {
    'JAN': 1,
    'FEB': 2,
    'MAR': 3,
    'APR': 4,
    'MAY': 5,
    'JUN': 6,
    'JUL': 7,
    'AUG': 8,
    'SEP': 9,
    'OCT': 10,
    'NOV': 11,
    'DEC': 12
}


def get_key(dictionary, val):
    for key, value in dictionary.items():
        if val == value:
            return key


class Person:
    def __init__(self, first_name: str, second_name: str, sex: tr.Sex, date):
        self.first_name = first_name
        self.second_name = second_name
        self.sex = sex
        self.birthday = date
        self.mother = None
        self.father = None
        self.family_from = None
        self.family_self = []

    def add_family_self(self, family_id: str) -> None:
        self.family_self.append(family_id)

    def add_family_from(self, family_id: str) -> None:
        self.family_from = family_id


class Family(object):
    def __init__(self, mother_id: str, father_id: str):
        self.mother = mother_id
        self.father = father_id
        self.children = []

    def add_child(self, person_id: str):
        self.children.append(person_id)


class GedFile(object):
    """
    Custom header info values (if there isn't  info in a file)
    """
    now = datetime.datetime.today()
    now_date = "1 DATE {0} {1} {2}".format(now.day, get_key(month_dict, now.month), now.year)
    header = '0 HEAD\n1 GEDC\n2 VERS 5.5.1\n1 CHAR UTF-8\n{0}\n'.format(now_date)
    tail = '0 TRLR\n'

    def __init__(self):
        self.persons = {}  # key is a person, value is ID
        self.families = {}  # key is a family, value is a Family
        self.free_id_F = 1
        self.free_id_I = 1

    def add_person(self, person: Person) -> None:
        self.persons[person] = r"@I{0}@".format(self.free_id_I)
        self.free_id_I += 1

    def add_family(self, family: Family) -> None:
        self.families[family] = r"@F{0}@".format(self.free_id_F)
        self.free_id_F += 1

    def check_family_exist(self, person: Person) -> Family:
        for family, family_id in self.families.items():
            mother = self.persons[person.mother] if person.mother else None
            father = self.persons[person.father] if person.father else None
            if family.mother == mother and family.father == father:
                return family

    def create_families(self):
        for person, person_id in self.persons.items():
            # if your family already exist
            checked_family = self.check_family_exist(person)
            if checked_family:
                checked_family.add_child(person_id)
            else:
                if person.father or person.mother:
                    mother = self.persons[person.mother] if person.mother else None
                    father = self.persons[person.father] if person.father else None

                    family = Family(mother, father)
                    family.add_child(person_id)
                    self.add_family(family)

    def update_persons(self):
        for person, person_id in self.persons.items():
            for family, family_id in self.families.items():
                if family.mother == person_id or family.father == person_id:
                    person.family_self.append(family_id)
                if person_id in family.children:
                    person.family_from = family_id

    @staticmethod
    def print_person(person: Person, id_key: str) -> str:
        s = ''
        s += '0 {0} INDI\n'.format(id_key)
        s += '1 NAME {0} /{1}/\n'.format(person.first_name, person.second_name)
        s += '2 GIVN {0}\n'.format(person.first_name)
        s += '2 SURN {0}\n'.format(person.second_name)
        s += '1 SEX {0}\n'.format(person.sex.value)
        if person.birthday:
            s += '1 BIRT\n2 DATE {0} {1} {2}\n'.format(person.birthday.day,
                                                       get_key(month_dict, person.birthday.month),
                                                       person.birthday.year)
        if person.family_from:
            s += '1 FAMC {0}\n'.format(person.family_from)
        if person.family_self:
            for family in person.family_self:
                s += '1 FAMS {0}\n'.format(family)
        return s

    @staticmethod
    def print_family(family: Family, id_key: str) -> str:
        s = ''
        s += '0 {0} FAM\n'.format(id_key)
        if family.mother:
            s += '1 WIFE {0}\n'.format(family.mother)
        if family.father:
            s += '1 HUSB {0}\n'.format(family.father)
        for child in family.children:
            s += '1 CHIL {0}\n'.format(child)
        return s

    def save(self, file_name) -> bool:
        if isinstance(file_name, six.string_types):
            with open(file_name, 'a', encoding='utf-8') as gedcom_file:
                return self.save(gedcom_file)

        file_name.write(self.header)
        for person, key in self.persons.items():
            file_name.write(self.print_person(person, key))
        for family, key in self.families.items():
            file_name.write(self.print_family(family, key))
        file_name.write(self.tail)
        return True


def save_to_file(person_map, file_name='Test.ged'):
    ged_file = GedFile()

    for key_person, person in person_map.items():
        ged_file.add_person(person)

    ged_file.create_families()
    ged_file.update_persons()
    # ui.paint_tree(ged_file.families)
    # ged_file.save(file_name)

