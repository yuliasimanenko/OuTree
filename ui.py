from graphviz import Digraph
import wx, os
import pathlib
import eel
import main_algo as algo
import load_tree as convert


def get_key(dictionary, val):
    for key, value in dictionary.items():
        if val == value:
            return key


def change_key_values(bad_dict: dict) -> dict:
    new_dict = {}
    for key, value in bad_dict.items():
        new_dict[value] = key
    return new_dict


def paint_tree(map_family: dict):
    map_family = change_key_values(map_family)
    os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin/'
    tree = Digraph('main', comment="Main Tree")
    tree.attr(rank='same')
    ready_nodes = set()
    for key_id, family in map_family.items():
        if key_id in ready_nodes:
            continue
        fam = Digraph(key_id)
        if family.mother:
            fam.node(family.mother, r'{0} {1}'.format(family.mother, family.mother), fillcolor="#ff7e40", style='filled')
        if family.father:
            fam.node(family.father, r'{0} {1}'.format(family.father, family.father), fillcolor="#fa9940", style='filled')
        if family.children:
            for child in family.children:
                fam.node(child, r'{0} {1}'.format(child, child))
        if family.mother and family.father:
            marriage_code = str(hash(family.mother) + hash(family.father))
            fam.node(marriage_code, label='', fixedsize='false', width='0', height='0', shape='none')
            fam.edge(family.mother, marriage_code, arrowhead='none')
            fam.edge(marriage_code, family.father, arrowhead='none')
            if family.children:
                for child in family.children:
                    fam.edge(marriage_code, child, arrowhead='none')
        else:
            if family.mother and family.children:
                for child in family.children:
                    fam.edge(family.mother, child, arrowhead='none')
            if family.father and family.children:
                for child in family.children:
                    fam.edge(family.father, child, arrowhead='none')
        tree.subgraph(fam)
    tree.format = 'svg'
    tree.render('tree', view=True)
    os.remove('tree')
    pass


def test_print1():
    os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin/'
    tree = Digraph("main")
    grand_parents = Digraph("grand")
    parents = Digraph("parents")
    me = Digraph('me')
    uncle = Digraph("uncle")

    uncle.node("Дядя", r'Литвиненко\nДенис', fillcolor="#fa9940", style='filled')

    grand_parents.node("Бабушка", r'Литвиненко\nЛюдмила', fillcolor="#ff7e40", style='filled')
    grand_parents.node("Дедушка", r'Литвиненко\nВасилий', fillcolor="#fa9940", style='filled')
    grand_parents.node('FM', label='', fixedsize='false', width='0', height='0', shape='none')
    tree.attr(rank='same')

    tree.edge("Бабушка", "FM", arrowhead='none')
    tree.edge("FM", "Дедушка", arrowhead='none')
    tree.edge("FM", "Дядя", arrowhead='none')

    parents.node("Мама", r'Литвиненко\nИрина', fillcolor="#ff7e40", style='filled')
    parents.node("Папа", r'Симаненко\nАлександр', fillcolor="#fa9940", style='filled')
    parents.node('FM2', label='', fixedsize='false', width='0', height='0', shape='none')
    tree.attr(rank='same')

    tree.edge("Мама", "FM2", arrowhead='none')
    tree.edge("FM2", "Папа", arrowhead='none')
    tree.edge("FM", "Мама", arrowhead='none')

    me.node("Я", r'Симаненко\nЮлия', fillcolor="#ff7e40", style='filled')

    tree.edge("FM2", "Я", arrowhead='none')

    tree.subgraph(grand_parents)
    tree.subgraph(uncle)
    tree.subgraph(parents)
    tree.subgraph(me)

    tree.format = 'svg'
    tree.render('left_tree_part', view=True)
    os.remove('left_tree_part')


def test_print2():
    os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin/'
    tree = Digraph("main")
    grand_parents = Digraph("grand")
    parents = Digraph("parents")
    me = Digraph('me')
    uncle = Digraph("uncle")

    grand_parents.node("Бабушка", r'Шапкина\nЛюбовь', fillcolor="#ff7e40", style='filled')
    grand_parents.node("Дедушка", r'Симаненко\nВладимир', fillcolor="#fa9940", style='filled')
    grand_parents.node('FM', label='', fixedsize='false', width='0', height='0', shape='none')
    tree.attr(rank='same')

    tree.edge("Бабушка", "FM", arrowhead='none')
    tree.edge("FM", "Дедушка", arrowhead='none')

    parents.node("Мама", r'Литвиненко\nИрина', fillcolor="#ff7e40", style='filled')
    parents.node("Папа", r'Симаненко\nАлександр', fillcolor="#fa9940", style='filled')
    parents.node('FM2', label='', fixedsize='false', width='0', height='0', shape='none')
    tree.attr(rank='same')

    tree.edge("Мама", "FM2", arrowhead='none')
    tree.edge("FM2", "Папа", arrowhead='none')
    tree.edge("FM", "Папа", arrowhead='none')

    me.node("Я", r'Симаненко\nЮлия', fillcolor="#ff7e40", style='filled')

    tree.edge("FM2", "Я", arrowhead='none')

    tree.subgraph(grand_parents)
    tree.subgraph(uncle)
    tree.subgraph(parents)
    tree.subgraph(me)

    tree.format = 'svg'
    tree.render('right_tree_part', view=True)
    os.remove('right_tree_part')


def most_tree():
    os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin/'
    tree = Digraph("main")
    grand_parents1 = Digraph("grand1")
    grand_parents = Digraph("grand")
    parents = Digraph("parents")
    me = Digraph('me')
    uncle = Digraph("uncle")

    uncle.node("Дядя", r'Литвиненко\nДенис', fillcolor="#fa9940", style='filled')

    grand_parents.node("Бабушка", r'Литвиненко\nЛюдмила', fillcolor="#ff7e40", style='filled')
    grand_parents.node("Дедушка", r'Литвиненко\nВасилий', fillcolor="#fa9940", style='filled')
    grand_parents.node('FM', label='', fixedsize='false', width='0', height='0', shape='none')
    tree.attr(rank='same')

    grand_parents1.node("Бабушка1", r'Шапкина\nЛюбовь', fillcolor="#ff7e40", style='filled')
    grand_parents1.node("Дедушка1", r'Симаненко\nВладимир', fillcolor="#fa9940", style='filled')
    grand_parents1.node('FM1', label='', fixedsize='false', width='0', height='0', shape='none')

    tree.edge("Бабушка1", "FM1", arrowhead='none')
    tree.edge("FM1", "Дедушка1", arrowhead='none')

    tree.edge("Бабушка", "FM", arrowhead='none')
    tree.edge("FM", "Дедушка", arrowhead='none')
    tree.edge("FM", "Дядя", arrowhead='none')

    parents.node("Мама", r'Литвиненко\nИрина', fillcolor="#ff7e40", style='filled')
    parents.node("Папа", r'Симаненко\nАлександр', fillcolor="#fa9940", style='filled')
    parents.node('FM2', label='', fixedsize='false', width='0', height='0', shape='none')
    tree.attr(rank='same')

    tree.edge("Папа", "FM2", arrowhead='none')
    tree.edge("FM2", "Мама", arrowhead='none')

    tree.edge("FM", "Мама", arrowhead='none')
    tree.edge("FM1", "Папа", arrowhead='none')

    me.node("Я", r'Симаненко\nЮлия', fillcolor="#ff7e40", style='filled')

    tree.edge("FM2", "Я", arrowhead='none')

    tree.subgraph(grand_parents)
    tree.subgraph(uncle)
    tree.subgraph(parents)
    tree.subgraph(me)
    tree.subgraph(grand_parents1)

    tree.format = 'svg'
    tree.render('picture', view=True)
    os.remove('picture')




# if __name__ == '__main__':
    # tree = convert.load_persons_as_map('GED/Test_Union1.ged')
    # paint_tree(tree)


"""
WINDOW
"""

eel.init("web")


@eel.expose
def union_tree(path1, path2):
    tree_map1 = convert.load_persons_as_map(path1)
    tree_map2 = convert.load_persons_as_map(path2)
    union = algo.tree_union(tree_map1, tree_map2)
    print(union)
    if isinstance(union, int):
        return union


@eel.expose
def pythonFunction(wildcard="*"):
    app = wx.App(None)
    style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
    dialog = wx.FileDialog(None, 'Open', wildcard=wildcard, style=style)
    if dialog.ShowModal() == wx.ID_OK:
        path = dialog.GetPath()
    else:
        path = None
    dialog.Destroy()
    print(path)

    return path if test_open_files(path) else False


def test_open_files(file_path) -> bool:
    if pathlib.Path(file_path).suffix in ('.ged', '.GED'):
        return True
    else:
        print("Not GED file")
        return False


eel.start("index.html", size=(900, 760))
