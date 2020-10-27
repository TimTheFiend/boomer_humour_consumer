from __future__ import annotations

from json import load as json_load

from entity import Actor
from components.ai import HostileEnemy
from components.level import Level
from components.inventory import Inventory
from components.stats import Stats


RACES: None

try:
    with open('res/races.json') as f:
        RACES = json_load(f)
except FileNotFoundError:
    raise FileNotFoundError()


HUMAN = RACES['human']


human = Actor(
    char=RACES['human']['char'],
    color=RACES['human']['color'],
    name=str(RACES['human']['name']['singular'].capitalize()),
    ai_cls=HostileEnemy,
    stats=Stats(stats=RACES['human']['stats']),
    level=Level(), # TODO
    inventory=Inventory()
)

player = Actor(
    char=RACES['human']['char'],
    color=RACES['human']['color'],
    name=str(RACES['human']['name']['singular'].capitalize()),
    ai_cls=HostileEnemy,
    stats=Stats(stats=RACES['human']['stats']),
    level=Level(), # TODO
    inventory=Inventory()
)