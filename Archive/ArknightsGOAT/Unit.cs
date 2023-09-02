using System;
using System.Text;

namespace GOAT
{
	class Stats
	{
		internal float BaseAttack;

		internal int Targets = 1;
		internal float MultiHit = 1f;

		internal float TrustBonus = 0f;
		internal float Interval;

		internal float Speed = 0f;
		internal float IntervalModifier = 0f;
		internal float AdditivePercent = 0f;
		internal float AdditiveScalar = 0f;
		internal float Multiplier = 100f;

		internal float CritChance = 0f;
		internal float CritMultiplier = 100f;
		internal float DamageOverTime = 0f; // bp, thorns

		internal float AttacksPerSecond => (1f + Speed / 100f) / (Interval + IntervalModifier) * MultiHit;
		internal float DamagePerHit => (BaseAttack + BaseAttack * AdditivePercent / 100f + AdditiveScalar) * Multiplier / 100f;
		internal float DamagePerCrit => DamagePerHit * CritMultiplier / 100f;
		internal float AverageHit => DamagePerHit * (1f - CritChance / 100f) + DamagePerCrit * CritChance / 100f;

		internal float MinDamagePerSecond => AttacksPerSecond * DamagePerHit + DamageOverTime;
		internal float MaxDamagePerSecond => AttacksPerSecond * DamagePerCrit + DamageOverTime;
		internal float AverageDPS => MinDamagePerSecond * (1f - CritChance / 100f) + MaxDamagePerSecond * CritChance / 100f;
		internal float MaxTargetDamagePerSecond => AverageDPS * Targets;

		internal float AdditiveBuffEfficiency => (Multiplier / 100f * (1f - CritChance / 100f) + Multiplier / 100f * CritMultiplier / 100f * CritChance / 100f) * AttacksPerSecond;
		internal float MaxAdditiveBuffEfficiency => AdditiveBuffEfficiency * Targets;

	}

	class Unit
	{
		internal string Name;

		internal Stats OffSkill = new Stats();
		internal Stats OnSkill = new Stats();

		internal float Attack;
		internal float TrustBonus;
		internal float BaseAttack => Attack + TrustBonus;

		internal void ApplyBaseAttack()
		{
			OffSkill.BaseAttack = BaseAttack;
			OnSkill.BaseAttack = BaseAttack;
		}

		internal float SkillCost = 0f;
		internal float SkillDuration = 1f;
		internal float SkillRestorationRate = 1f;
		internal float SkillUptime => SkillDuration / (SkillCost / SkillRestorationRate + SkillDuration);

		internal float AverageDPS => OffSkill.AverageDPS * (1f - SkillUptime) + OnSkill.AverageDPS * SkillUptime;
		internal float AverageHit => OffSkill.DamagePerHit * (1f - SkillUptime) + OnSkill.AverageHit * SkillUptime;
		internal float AdditiveBuffEfficiency => OffSkill.AdditiveBuffEfficiency * (1f - SkillUptime) + OnSkill.AdditiveBuffEfficiency * SkillUptime;
		internal float MaxAdditiveBuffEfficiency => OffSkill.MaxAdditiveBuffEfficiency * (1f - SkillUptime) + OnSkill.MaxAdditiveBuffEfficiency * SkillUptime;

		internal Unit(string name)
		{
			Name = name;
		}

		public override string ToString()
		{
			StringBuilder result = new StringBuilder();
			result.AppendLine($"---------\n");
			result.AppendLine($"{Name}");

			if (OffSkill.Speed == -100f) {
				result.AppendLine($"\nCycle Information");
				result.AppendLine($"Skill Uptime: {SkillUptime}");
				result.AppendLine($"Skill Duration: {SkillDuration}");

				result.AppendLine($"\nOn Skill");
				result.AppendLine($"Average DPS: {OnSkill.AverageDPS}");
				result.AppendLine($"Average Hit Damage: {OnSkill.AverageHit}");
				result.AppendLine($"Buff Efficiency: {OnSkill.AdditiveBuffEfficiency} ({BaseAttack})");
				result.AppendLine($"Targets: {OnSkill.Targets}");
				result.AppendLine($"Max Targets DPS: {OnSkill.MaxTargetDamagePerSecond}");
				result.AppendLine($"Max Targets Buff Efficiency: {OnSkill.MaxAdditiveBuffEfficiency} ({BaseAttack})");
			} else if (SkillCost == 0) {
				result.AppendLine($"\nPost-Scaling");
				result.AppendLine($"Average DPS: {AverageDPS}");
				result.AppendLine($"Average Hit Damage: {AverageHit}");
				result.AppendLine($"Buff Efficiency: {AdditiveBuffEfficiency} ({BaseAttack})");
				result.AppendLine($"Targets: {OnSkill.Targets}");
				result.AppendLine($"Max Targets DPS: {OnSkill.MaxTargetDamagePerSecond}");
				result.AppendLine($"Max Targets Buff Efficiency: {OnSkill.MaxAdditiveBuffEfficiency} ({BaseAttack})");
			} else {
				result.AppendLine($"\nCycle Information");
				result.AppendLine($"Skill Uptime: {SkillUptime}");
				result.AppendLine($"Skill Duration: {SkillDuration}");

				result.AppendLine($"\nFull Cycle");
				result.AppendLine($"Average DPS: {AverageDPS}");
				result.AppendLine($"Average Hit Damage: {AverageHit}");
				result.AppendLine($"Buff Efficiency: {AdditiveBuffEfficiency} ({BaseAttack})");
				result.AppendLine($"Max Targets Buff Efficiency: {MaxAdditiveBuffEfficiency} ({BaseAttack})");

				result.AppendLine($"\nOn Skill");
				result.AppendLine($"Average DPS: {OnSkill.AverageDPS}");
				result.AppendLine($"Average Hit Damage: {OnSkill.AverageHit}");
				result.AppendLine($"Buff Efficiency: {OnSkill.AdditiveBuffEfficiency} ({BaseAttack})");
				result.AppendLine($"Targets: {OnSkill.Targets}");
				result.AppendLine($"Max Targets DPS: {OnSkill.MaxTargetDamagePerSecond}");
				result.AppendLine($"Max Targets Buff Efficiency: {OnSkill.MaxAdditiveBuffEfficiency} ({BaseAttack})");

				result.AppendLine($"\nOff Skill");
				result.AppendLine($"Average DPS: {OffSkill.AverageDPS}");
				result.AppendLine($"Average Hit Damage: {OffSkill.AverageHit}");
				result.AppendLine($"Buff Efficiency: {OffSkill.AdditiveBuffEfficiency} ({BaseAttack})");
				result.AppendLine($"Targets: {OffSkill.Targets}");
				result.AppendLine($"Max Targets DPS: {OffSkill.MaxTargetDamagePerSecond}");
				result.AppendLine($"Max Targets Buff Efficiency: {OffSkill.MaxAdditiveBuffEfficiency} ({BaseAttack})");
			}

			return result.ToString();
		}

		internal float Interval
		{
			set
			{
				OffSkill.Interval = value;
				OnSkill.Interval = value;
			}
		}

		internal float Speed
		{
			set
			{
				OffSkill.Speed = value;
				OnSkill.Speed = value;
			}
		}

		internal float IntervalModifier
		{
			set
			{
				OffSkill.IntervalModifier = value;
				OnSkill.IntervalModifier = value;
			}
		}

		internal float AdditivePercent
		{
			set
			{
				OffSkill.AdditivePercent = value;
				OnSkill.AdditivePercent = value;
			}
		}

		internal float AdditiveScalar
		{
			set
			{
				OffSkill.AdditiveScalar = value;
				OnSkill.AdditiveScalar = value;
			}
		}

		internal float Multiplier
		{
			set
			{
				OffSkill.Multiplier = value;
				OnSkill.Multiplier = value;
			}
		}

		internal float CritChance
		{
			set
			{
				OffSkill.CritChance = value;
				OnSkill.CritChance = value;
			}
		}

		internal float CritMultiplier
		{
			set
			{
				OffSkill.CritMultiplier = value;
				OnSkill.CritMultiplier = value;
			}
		}

		internal float DamageOverTime
		{
			set
			{
				OffSkill.DamageOverTime = value;
				OnSkill.DamageOverTime = value;
			}
		}

		internal int Targets
		{
			set
			{
				OffSkill.Targets = value;
				OnSkill.Targets = value;
			}
		}
	}
}
