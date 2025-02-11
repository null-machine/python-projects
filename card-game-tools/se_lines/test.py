import typing

from stage import Stage
from effect import *

stage = Stage()

stage.add('field', 'amogus')

print(stage.to_string())

effect: Effect = DiabellHand()
print(effect.name, effect.check(None))