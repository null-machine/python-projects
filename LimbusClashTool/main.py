import yaml
from os import listdir
from sinner import Sinner
from skill import Skill


files = [file for file in listdir('sinners')]

sinners = []
skills = []
s1_list = []
s2_list = []
s3_list = []
# s1_average = 0
# s2_average = 0
# s3_average = 0

print("Generating charts...")

for file in files:
	stream = open(f'sinners/{file}', 'r')
	sinner = yaml.load(stream, yaml.Loader)
	plt = sinner.gen_chart()
	plt.savefig(f'charts/{sinner.name}.png')
	plt.close()
	sinners.append(sinner)
	skills.append(sinner.s1)
	skills.append(sinner.s2)
	skills.append(sinner.s3)
	s1_list.append(sinner.s1)
	s2_list.append(sinner.s2)
	s3_list.append(sinner.s3)
	# s1_average += sinner.s1.max_aggregate
	# s2_average += sinner.s2.max_aggregate
	# s3_average += sinner.s3.max_aggregate

# s1_average /= len(s1_list)
# s2_average /= len(s2_list)
# s3_average /= len(s3_list)

print("Generating tier lists...")

sinners.sort(reverse=True)
tier_list = open('tier_lists/sinner_tier_list.txt', 'w+')
for sinner in sinners:
	tier_list.write(f'{sinner.gen_display_str()}\n')
tier_list.close()

tier_list = open('tier_lists/no_prime_no_base_sinner_tier_list.txt', 'w+')
for sinner in sinners:
	if not sinner.name.endswith('_base') and not sinner.name.endswith('_prime'):
		tier_list.write(f'{sinner.gen_display_str()}\n')
tier_list.close()

skills.sort(reverse=True)
tier_list = open('tier_lists/skill_tier_list.txt', 'w+')
for skill in skills:
	tier_list.write(f'{skill.gen_display_str()}\n')
tier_list.close()

s1_list.sort(reverse=True)
tier_list = open('tier_lists/s1_tier_list.txt', 'w+')
for skill in s1_list:
	tier_list.write(f'{skill.gen_display_str()}\n')
tier_list.close()

s2_list.sort(reverse=True)
tier_list = open('tier_lists/s2_tier_list.txt', 'w+')
for skill in s2_list:
	tier_list.write(f'{skill.gen_display_str()}\n')
tier_list.close()

s3_list.sort(reverse=True)
tier_list = open('tier_lists/s3_tier_list.txt', 'w+')
for skill in s3_list:
	tier_list.write(f'{skill.gen_display_str()}\n')
tier_list.close()

# stream = open(f'sinners/gregor_g_corp.yaml', 'r')
# sinner = yaml.load(stream, yaml.Loader)
# plt = sinner.gen_chart()
# plt.savefig(f'charts/{sinner.name}.png')
# plt.close()

print("Done!")