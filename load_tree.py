import gedcom
import tree as tr
import datetime
import writer as wr
import main_algo as algo

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


def make_tree_person(person):
    if not isinstance(person, gedcom.Individual):
        raise TypeError("invalid person parameter method: " + make_tree_person.__name__)
    first_name, second_name = person.name
    tree = tr.Tree(first_name, second_name, person.sex)

    if person.birth is None:
        tree.date = None
    else:
        if person.birth.birth_day is None:
            tree.date = None
            return tree
        date = person.birth.birth_day

        day = date['day'] if 'day' in date else 1
        month = date['month'] if 'month' in date else 'JAN'
        month = month_dict[month] if month else None

        if 'year' in date:
            year = date['year']
        else:
            tree.date = None
            return tree

        try:
            tree.date = datetime.date(year, month, day)
        except ValueError:
            tree.date = None

    return tree


def load_persons_as_map(file_name):
    map_tree_persons = {}
    ged_file = gedcom.parse(file_name)
    for person in ged_file.individuals:
        # check do the person exist
        if person.id not in map_tree_persons:
            # continue
            tree_person = make_tree_person(person)
            map_tree_persons[person.id] = tree_person
        else:
            tree_person = map_tree_persons[person.id]
        if person.mother:
            if person.mother.id not in map_tree_persons:
                mother = make_tree_person(person.mother)
                map_tree_persons[person.mother.id] = mother
                tree_person.mother = mother
            else:
                tree_person.mother = map_tree_persons[person.mother.id]
            map_tree_persons[person.mother.id].children.append(tree_person)

        if person.father:
            if person.father.id not in map_tree_persons:
                father = make_tree_person(person.father)
                map_tree_persons[person.father.id] = father
                tree_person.father = father
            else:
                tree_person.father = map_tree_persons[person.father.id]
            map_tree_persons[person.father.id].children.append(tree_person)

    return map_tree_persons


def convert_persons_for_write_to_file(map_person):
    if not isinstance(map_person, dict):
        raise TypeError("invalid map_person parameter method: " + convert_persons_for_write_to_file.__name__)
    map_persons = {}  # key id, value - writer.Person object
    for id_key, person in map_person.items():
        if id_key not in map_persons:
            person_to_write = wr.Person(person.first_name, person.second_name, person.sex, person.date)
            map_persons[id_key] = person_to_write
        else:
            person_to_write = map_persons[id_key]
        # а если родня мама-папа уже есть???????  ищем по iD так как перепаковывается только нода
        if person.mother:
            # если мама как личность уже присутствует в словаре
            if wr.get_key(map_person, person.mother) in map_persons:
                person_to_write.mother = map_persons[wr.get_key(map_person, person.mother)]
            else:
                mother = wr.Person(
                    person.mother.first_name,
                    person.mother.second_name,
                    person.mother.sex,
                    person.mother.date)
                map_persons[wr.get_key(map_person, person.mother)] = mother
                person_to_write.mother = mother
        if person.father:
            # если отец как личность уже присутствует в словаре
            if wr.get_key(map_person, person.father) in map_persons:
                person_to_write.father = map_persons[wr.get_key(map_person, person.father)]
            else:
                father = wr.Person(
                    person.father.first_name,
                    person.father.second_name,
                    person.father.sex,
                    person.father.date)
                map_persons[wr.get_key(map_person, person.father)] = father
                person_to_write.father = father
    return map_persons


if __name__ == '__main__':

    tree_map1 = load_persons_as_map("GED/Test_Union1.ged")

    tree_map2 = load_persons_as_map("GED/Test_Union2.ged")
    # for key, person1 in tree_map1.items():
    #     print(person1.first_name)
    # print('\n')
    # for key, person2 in tree_map2.items():
    #     print(person2.mother, end='    ')
    # print('\n')
    print(tree_map2)

    # map_name = convert_persons_for_write_to_file(tree_map2)

    map_result = algo.tree_union(tree_map1, tree_map2)
    print(map_result)

    # wr.save_to_file(map_name)

    # for key, person123 in map_result.items():
    #     print(person123.first_name + " Father is " + person123.father.first_name if person123.father else "None")
    # wr.save_to_file(map_name)
