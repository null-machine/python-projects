import yaml
from sinner import Sinner
from skill import Skill

print('''Sinner Ultimate Scientific Analysis Model Of Generally Unknown Strategies
- Generates charts of skill clash ranges.
- Enemy offense level is assumed to be 30.
- Y-axis represents the chance of winning on any coin in the clash.
- X-axis represents the power of an enemy skill that always rolls the same thing.
- Cyan, yellow and magenta are associated a chance of 0.7, 0.5 and 0.3 of rolling heads respectively.
''')

# file = open('sinners/w_corp_don_quixote.yaml', 'w+')
# file.write(yaml.dump(w_corp_don_quixote))
# file.close()

stream = open('sinners/w_corp_don_quixote.yaml', 'r')
sinner = yaml.load(stream, yaml.Loader)
fig = sinner.gen_charts()
fig.savefig(f'charts/{sinner.name}.png')