import yaml
from sinner import Sinner
from skill import Skill

un_deux = Skill("un_deux", "lcb_meursault", 2, 2, 4, 26)
nailing_fist = Skill("nailing_fist", "lcb_meursault", 5, 1, 8, 26)
des_coups = Skill("des_coups", "lcb_meursault", 4, 4, 1, 36)

meursault = Sinner("lcb_meursault", un_deux, nailing_fist, des_coups)

# print(yaml.dump(meursault))
meursault.s3.gen_breakpoints(0, 0.7)