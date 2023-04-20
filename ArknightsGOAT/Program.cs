using System;
using System.Collections.Generic;

namespace GOAT
{
	public class Program
	{

		static List<Unit> Units = new List<Unit>();

		public static void Main(string[] args)
		{
			Console.WriteLine($"Buff Efficiency is the multiplier that is applied to an additive buff to get the resultant DPS increase.\nThe number in brackets is the base attack used to calculate an percentile additive buff.\n");

			Unit thorns = new Unit("Thorns S3");
			thorns.Attack = 711f;
			thorns.TrustBonus = 30f;
			thorns.ApplyBaseAttack();
			thorns.Interval = 1.3f;
			thorns.OnSkill.AdditivePercent = 120f;
			thorns.OnSkill.Speed = 50f;
			thorns.DamageOverTime = 125f;
			Units.Add(thorns);

			Unit ayer = new Unit("Ayerscarpe S1");
			ayer.SkillCost = 3.9f;
			ayer.SkillDuration = 1.3f;
			ayer.Attack = 670f;
			ayer.TrustBonus = 75f;
			ayer.ApplyBaseAttack();
			ayer.Interval = 1.3f;
			ayer.OnSkill.Multiplier = 160f;
			ayer.OnSkill.Targets = 3;
			Units.Add(ayer);

			Unit gavialter = new Unit("Gavialter S3"); // note: block count atk scaling not accounted for
			gavialter.Attack = 766f;
			gavialter.TrustBonus = 50f;
			gavialter.ApplyBaseAttack();
			gavialter.SkillCost = 35f;
			gavialter.SkillDuration = 25f;
			gavialter.Interval = 1.2f;
			gavialter.AdditivePercent = 10f;
			gavialter.OnSkill.AdditivePercent = 10f + 140f;
			gavialter.OnSkill.Speed = 100f;
			gavialter.OnSkill.Targets = 5;
			gavialter.OffSkill.Targets = 3;
			Units.Add(gavialter);

			Unit blaze = new Unit("Blaze S2");
			blaze.Attack = 765f;
			blaze.TrustBonus = 60f;
			blaze.ApplyBaseAttack();
			blaze.Interval = 1.2f;
			blaze.OnSkill.AdditivePercent = 100f;
			blaze.OnSkill.Targets = 3;
			Units.Add(blaze);

			Unit specter = new Unit("Specter S2");
			specter.Attack = 725f;
			specter.TrustBonus = 80f;
			specter.ApplyBaseAttack();
			specter.SkillCost = 40f;
			specter.SkillDuration = 15f;
			specter.Interval = 1.2f;
			specter.OnSkill.AdditivePercent = 160f;
			specter.Targets = 3;
			Units.Add(specter);

			Unit weedy = new Unit("Weedy S2");
			weedy.Attack = 677f;
			weedy.TrustBonus = 45f;
			weedy.ApplyBaseAttack();
			weedy.Interval = 1.2f;
			weedy.OnSkill.IntervalModifier = 2.2f;
			weedy.OnSkill.AdditivePercent = 200f;
			weedy.Targets = 2;
			Units.Add(weedy);

			Unit gladiia = new Unit("Gladiia S1");
			gladiia.Attack = 492f;
			gladiia.TrustBonus = 50f;
			gladiia.ApplyBaseAttack();
			gladiia.SkillCost = 3f;
			gladiia.SkillDuration = 1f;
			gladiia.Interval = 1.8f;
			gladiia.Multiplier = 136f;
			gladiia.OnSkill.Multiplier = 210f * 1.36f;
			Units.Add(gladiia);

			Unit gladiia2 = new Unit("Gladiia S2");
			gladiia2.Attack = 492f;
			gladiia2.TrustBonus = 50f;
			gladiia2.ApplyBaseAttack();
			gladiia2.SkillCost = 25f;
			gladiia2.SkillDuration = 20f;
			gladiia2.Interval = 1.8f;
			gladiia2.Multiplier = 136f;
			gladiia2.OnSkill.Interval = 1.8f + 0.5f;
			gladiia2.OnSkill.Multiplier = 180f * 1.36f;
			gladiia2.OnSkill.Targets = 2;
			Units.Add(gladiia2);

			Unit lappland = new Unit("Lappland S1");
			lappland.Attack = 685f;
			lappland.TrustBonus = 75f;
			lappland.ApplyBaseAttack();
			lappland.Interval = 1.3f;
			lappland.OnSkill.AdditivePercent = 70f;
			Units.Add(lappland);

			Unit lappland2 = new Unit("Lappland S2");
			lappland2.Attack = 685f;
			lappland2.TrustBonus = 75f;
			lappland2.ApplyBaseAttack();
			lappland2.Interval = 1.3f;
			lappland2.SkillCost = 1.3f * 17f;
			lappland2.SkillDuration = 20f;
			lappland2.OnSkill.AdditivePercent = 120f;
			lappland2.OnSkill.Targets = 2;
			Units.Add(lappland2);

			Unit silverash = new Unit("SilverAsh S3");
			silverash.Attack = 713f;
			silverash.TrustBonus = 50f;
			silverash.ApplyBaseAttack();
			silverash.SkillCost = 90f;
			silverash.SkillDuration = 30f;
			silverash.Interval = 1.3f;
			silverash.AdditivePercent = 10f;
			silverash.OnSkill.AdditivePercent = 10f + 200f;
			silverash.OnSkill.Targets = 6;
			Units.Add(silverash);

			Unit mlynar = new Unit("Mlynar S3");
			mlynar.Attack = 335f;
			mlynar.TrustBonus = 30f;
			mlynar.ApplyBaseAttack();
			mlynar.SkillCost = 42f; // 40s required for max scaling
			mlynar.SkillDuration = 28f;
			mlynar.Interval = 1.2f;
			mlynar.OffSkill.Speed = -100f;
			mlynar.OnSkill.AdditivePercent = 400f + 12f; // scales from 0f to 200f
			mlynar.OnSkill.Targets = 5;
			mlynar.OnSkill.Multiplier = 180f * 1.1f;
			Units.Add(mlynar);

			Unit surtr = new Unit("Surtr S3");
			surtr.Attack = 671f;
			surtr.TrustBonus = 100f;
			surtr.ApplyBaseAttack();
			surtr.Interval = 1.25f;
			surtr.OffSkill.Speed = -100f;
			surtr.OnSkill.AdditivePercent = 330f;
			surtr.OnSkill.Targets = 4;
			surtr.OnSkill.Multiplier = 100f / 0.8f;
			Units.Add(surtr);

			Unit irene = new Unit("Irene S3");
			irene.Attack = 621f;
			irene.TrustBonus = 80f;
			irene.ApplyBaseAttack();
			irene.SkillCost = 24f;
			irene.SkillDuration = 3f;
			irene.SkillRestorationRate = 2f / 1.3f;
			irene.Interval = 1.3f;
			irene.OffSkill.Speed = 136f;
			irene.OnSkill.MultiHit = 13f / 3f;
			irene.OnSkill.Multiplier = (300f + 250f * 12f) / 13f;
			Units.Add(irene);

			Unit exusiai = new Unit("Exusiai S3");
			exusiai.Attack = 540f;
			exusiai.TrustBonus = 90f;
			exusiai.ApplyBaseAttack();
			exusiai.SkillCost = 30f;
			exusiai.SkillDuration = 15f;
			exusiai.Interval = 1f;
			exusiai.AdditivePercent = 6f;
			exusiai.Speed = 12f;
			exusiai.OnSkill.Multiplier = 110f;
			exusiai.OnSkill.IntervalModifier = -0.22f;
			exusiai.OnSkill.MultiHit = 5f;
			Units.Add(exusiai);

			Unit mountain = new Unit("Mountain S2");
			mountain.Attack = 587f;
			mountain.TrustBonus = 45f;
			mountain.ApplyBaseAttack();
			mountain.Interval = 0.78f;
			mountain.OnSkill.AdditivePercent = 80f;
			mountain.OnSkill.Targets = 2;
			mountain.CritChance = 20f;
			mountain.CritMultiplier = 165f;
			Units.Add(mountain);

			Unit bagpipe = new Unit("Bagpipe S3");
			bagpipe.Attack = 586f;
			bagpipe.TrustBonus = 85f;
			bagpipe.ApplyBaseAttack();
			bagpipe.SkillCost = 40f;
			bagpipe.SkillDuration = 20f;
			bagpipe.Interval = 1f;
			bagpipe.AdditivePercent = 6f;
			bagpipe.OnSkill.AdditivePercent = 120f;
			bagpipe.OnSkill.IntervalModifier = 0.7f;
			bagpipe.OnSkill.MultiHit = 3;
			bagpipe.CritChance = 25f;
			bagpipe.CritMultiplier = 130f;
			Units.Add(bagpipe);

			foreach (Unit unit in Units) {
				Console.WriteLine(unit);
			}
		}
	}
}
