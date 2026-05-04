from __future__ import annotations

import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]


class SkillDistributionLayoutTests(unittest.TestCase):
    def test_skill_distribution_layout_exists(self) -> None:
        skill_root = ROOT_DIR / "skills" / "baibaiaigc"

        self.assertTrue((skill_root / "SKILL.md").exists())
        self.assertTrue((skill_root / "agents" / "openai.yaml").exists())
        self.assertTrue((skill_root / "prompts" / "baibaiaigc1.md").exists())
        self.assertTrue((skill_root / "prompts" / "baibaiaigc2.md").exists())
        self.assertTrue((skill_root / "prompts" / "baibaiaigc-en.md").exists())
        self.assertTrue((skill_root / "references" / "checklist.md").exists())
        self.assertTrue((skill_root / "references" / "usage.md").exists())


if __name__ == "__main__":
    unittest.main()
