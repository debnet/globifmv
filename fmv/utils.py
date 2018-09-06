# coding: utf-8
import re
from bs4 import BeautifulSoup
from lxml import etree


REGEX_LINK = re.compile(r'\[{2}(.|[^<>|\[\]]+)(?:(<-|->|\|)(.*))?\]{2}')


def import_scenario(file_path):
    """
    Permet d'importer un fichier de Twine au format Harlowe
    :param file_path: Chemin du fichier
    :return: Liste des scènes
    """
    with open(file_path, 'r') as file:
        soup = BeautifulSoup(file, 'lxml')
    story = soup.find('tw-storydata')
    tree = etree.fromstring(story.prettify())
    story_name, intro_pid, intro_name = tree.attrib['name'], tree.attrib['startnode'], None
    passages = tree.findall('tw-passagedata')
    by_pid, by_name = {}, {}

    def add_scene(pid, name, text):
        data = dict(pid=pid, name=name, text=text.replace("//", "").strip(), next=[])
        by_pid[pid] = data
        by_name[name] = data
        if pid == intro_pid:
            global intro_name
            intro_name = name
        for match in (REGEX_LINK.findall(text) or ()):
            left, op, right = match
            if not op:
                if left == intro_name:
                    continue
                data['next'].append((left, left))
            elif op in ('->', '|'):
                if right == intro_name:
                    continue
                data['next'].append((right, left))
            elif op in ('<-', ):
                if left == intro_name:
                    continue
                data['next'].append((left, right))
        return data

    for passage in passages:
        pid, name = passage.attrib['pid'], passage.attrib['name']
        add_scene(pid, name, passage.text)

    from fmv.models import Scenario, Scene, Choice

    scenario = Scenario.objects.create(name=story_name)
    for data in by_name.values():
        scene = Scene.objects.create(scenario=scenario, name=data['name'], description=data['text'])
        data['scene'] = scene
    for data in by_name.values():
        scene_from = data['scene']
        for code, name in data['next']:
            scene_to = by_name.get(code)
            if not scene_to:
                continue
            scene_to = scene_to['scene']
            Choice.objects.create(name=name, scene_from=scene_from, scene_to=scene_to)
    scenario.intro = by_pid[intro_pid]['scene']
    scenario.save()
