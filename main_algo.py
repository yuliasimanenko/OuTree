import tree as tr
import writer as wr
from transliterate import translit


def tree_analysis(tree_nodes1, tree_nodes2) -> (int, bool):
    """
    Returns the tree compatibility value as a percentage
    :param dict tree_nodes1: map {id_key : tree_person} of first tree persons
    :param dict tree_nodes2: map {id_key : tree_person} of second tree persons
    :returns: tuple the value as a percentage of tree compatibility and union ability
    :rtype: int, bool
    """
    compatibility = 0
    union = True
    for id_key1, person1 in tree_nodes1.items():
        for id_key2, person2 in tree_nodes2.items():
            compare_result = compare_person(person1, person2)
            if compare_result >= 0.5:
                if not compare_parent(person1, person2):
                    union = False
            compatibility += compare_result

    min_size_dict = len(tree_nodes1) if len(tree_nodes1) < len(tree_nodes2) else len(tree_nodes2)
    compatibility = round(compatibility * 100 / min_size_dict)
    print("Result is " + str(compatibility))
    print("Union ability is " + str(union))
    return compatibility, union


def compare_person(person1: tr.Tree, person2: tr.Tree) -> float:
    """
    :param person1: Tree person from first tree
    :param person2: Tree person from second tree
    :return: The probability of a match [0;1]
    """
    probability = 0
    value = 1 / 4
    if translit(person1.first_name, "ru") != translit(person2.first_name, "ru"):
        return 0
    else:
        probability += value

    if person1.sex != person2.sex:
        return 0
    else:
        probability += value

    if translit(person1.second_name, "ru") == translit(person2.second_name, "ru"):
        probability += value
    if person1.date == person2.date:
        probability += value
    else:
        if person1.date and person2.date:
            if person1.date.year == person2.date.year:
                probability += value / 2

    return probability


def compare_parent(person1: tr.Tree, person2: tr.Tree) -> bool:
    """

    :param person1:
    :param person2:
    :return:
    """
    # сравнить даты, чтобы родители родились раньше детей

    # print(person1.first_name + "\t" + person2.first_name)
    if person1.mother:
        if person1.mother.date and person1.date:
            if person1.mother.date > person1.date:
                return False
        if person2.mother:
            if person2.mother.date and person2.date:
                if person2.mother.date > person2.date:
                    return False
            #     если есть сравнить мам
            if compare_person(person1.mother, person2.mother) < 0.5:
                return False

    if person1.father:
        if person1.father.date and person1.date:
            if person1.father.date > person1.date:
                return False
        if person2.father:
            if person2.father.date and person2.date:
                if person2.father.date > person2.date:
                    return False
            #     если есть сравнить пап
            if compare_person(person1.father, person2.father) < 0.5:
                return False

    return True


def find_person(person: tr.Tree, map_tree: dict):
    for key, person_to_com in map_tree.items():
        if compare_person(person_to_com, person) >= 0.5:
            return key, person_to_com
    return None, None


def tree_union(map_tree1: dict, map_tree2: dict):
    compatibility, union = tree_analysis(map_tree1, map_tree2)
    if not union or compatibility <= 1 or compatibility >= 99:
        return compatibility
    id_key = 0
    ready_nodes = set()
    for key2, person2 in map_tree2.items():
        if key2 in ready_nodes:
            continue
        # поискать есть ли в дереве уже такой персонаж
        key21, person2_in_tree1 = find_person(person2, map_tree1)
        if person2_in_tree1 is None:
            new_person = tr.Tree(person2.first_name, person2.second_name, person2.sex)
            map_tree1[id_key] = new_person
            id_key += 1

        ready_nodes.add(key2)

        key, person = find_person(person2, map_tree1)
        if person2.children:
            parent = person
            for child2 in person2.children:
                if wr.get_key(map_tree2, child2) in ready_nodes:
                    continue
                key, child1 = find_person(child2, map_tree1)
                if child1 is None:
                    new_child = tr.Tree(child2.first_name, child2.second_name, child2.sex)
                    map_tree1[id_key] = new_child
                    id_key += 1
                    if person2.sex == tr.Sex.FEMALE:
                        new_child.mother = parent
                    else:
                        new_child.father = parent
                else:
                    # проверить есть ли связь, если нет то создать
                    if parent.sex == tr.Sex.FEMALE:
                        if child1.mother != parent:
                            child1.mother = parent
                    else:
                        if child1.father != parent:
                            child1.father = parent
        if person2.mother:
            if wr.get_key(map_tree2, person2.mother) not in ready_nodes:
                key_id, parent = find_person(person2.mother, map_tree1)
                if parent is None:
                    new_parent = tr.Tree(person2.mother.first_name, person2.mother.second_name, person2.mother.sex)
                    map_tree1[id_key] = new_parent
                    id_key += 1
                    person.mother = new_parent
                else:
                    if person.mother != parent:
                        person.mother = parent
        if person2.father:
            if wr.get_key(map_tree2, person2.father) not in ready_nodes:
                key_id, parent = find_person(person2.father, map_tree1)
                if parent is None:
                    new_parent = tr.Tree(person2.father.first_name, person2.father.second_name, person2.father.sex)
                    map_tree1[id_key] = new_parent
                    id_key += 1
                    person.father = new_parent
                else:
                    if person.father != parent:
                        person.father = parent
    return map_tree1


def merge_node(person1: tr.Tree, person2: tr.Tree) -> tr.Tree:
    """
    найти все уникальные ноды во втором дереве
    проверить родителей и детей
    если есть в первом дереве аналог - добавить
    :return:
    """
    # Second Name
    # if person1.second_name != person2.second_name:
    union_person = tr.Tree(person1.first_name, person1.second_name, person1.sex)
    # Date
    if person1.date or person2.date:
        if person1.date == person2.date:
            union_person.date = person1.date
        else:
            union_person.date = person1.date
    return union_person
