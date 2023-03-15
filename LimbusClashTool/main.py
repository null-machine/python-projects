import yaml
from sinner import Sinner
from skill import Skill

to_pathos_mathos = Skill("to_pathos_mathos", "outis", 20, 1, 3, 21)
legerdemain = Skill("legerdemain", "gregor", 18, 1, 5, 24)

un_deux = Skill("un_deux", "lcb_meursault", 2, 2, 4, 26)
nailing_fist = Skill("nailing_fist", "lcb_meursault", 5, 1, 8, 26)
des_coups = Skill("des_coups", "lcb_meursault", 4, 4, 1, 26)
meursault = Sinner("lcb_meursault", un_deux, nailing_fist, des_coups)

sole_strike = Skill("sole_strike", "l_corp_faust", 3, 1, 6, 37)
deep_cuts = Skill("deep_cuts", "l_corp_faust", 4, 3, 3, 37)
opportunistic_slash = Skill("opportunistic_slash", "l_corp_faust", 4, 2, 11, 37)
l_corp_faust = Sinner("l_corp_faust", sole_strike, deep_cuts, opportunistic_slash)

graze_the_grass = Skill("graze_the_grass", "r_corp_heathcliff", 5, 3, 2, 41)
concentrated_fire = Skill("concentrated_fire", "r_corp_heathcliff", 5, 4, 3, 41)
quick_suppression = Skill("quick_suppression", "r_corp_heathcliff", 4, 5, 4, 41)
r_corp_heathcliff = Sinner("r_corp_heathcliff", graze_the_grass, concentrated_fire, quick_suppression)

mind_strike = Skill("mind_strike", "r_corp_ishmael", 3, 2, 5, 32)
flaying_surge = Skill("flaying_surge", "r_corp_ishmael", 6, 1, 10, 32)
mind_whip = Skill("mind_whip", "r_corp_ishmael", 2, 4, 5, 32)
r_corp_ishmael = Sinner("r_corp_ishmael", mind_strike, flaying_surge, mind_whip)

focus_strike = Skill("focus_strike", "kurokumo_ryoshu", 5, 1, 6, 38)
clean_up = Skill("clean_up", "kurokumo_ryoshu", 5, 2, 5, 38)
lenticular_swirl = Skill("lenticular_swirl", "kurokumo_ryoshu", 8, 2, 4, 38)
kurokumo_ryoshu = Sinner("kurokumo_ryoshu", focus_strike, clean_up, lenticular_swirl)

# hack = Skill("hack", "g_corp_gregor", 4, 2, 3, 41)
# dismember = Skill("dismember", "g_corp_gregor", 6, 1, 10, 41)
# eviscerate = Skill("eviscerate", "g_corp_gregor", 4, 4, 2, 41)
# g_corp_gregor = Sinner("g_corp_gregor", hack, dismember, eviscerate)

rip = Skill("rip", "w_corp_don_quixote", 5, 1, 6, 38)
leap = Skill("leap", "w_corp_don_quixote", 4, 3, 4, 38)
rip_space = Skill("rip_space", "w_corp_don_quixote", 1, 5, 6, 38)
w_corp_don_quixote = Sinner("w_corp_don_quixote", rip, leap, rip_space)

w_corp_don_quixote.show_skill_graphs()
# g_corp_gregor.show_skill_graphs()
# r_corp_ishmael.show_skill_graphs()

# print(yaml.dump(meursault))
# meursault.s3.gen_breakpoints(0)

# legerdemain.gen_breakpoints(0)

# opportunistic_slash.gen_breakpoints(30)
# deep_cuts.gen_breakpoints(30)