import typing
from stage import Stage

class Effect:
	
	def __init__(self, name: str, tags: set[str] | None = {}) -> None:
		self.name = name
		self.tags = tags
	
	def check(self, stage: Stage) -> bool:
		return False
	
	def delta(self, stage: Stage) -> None:
		pass

# ---

class DiabellHand(Effect):
	
	def __init__(self):
		super().__init__('diabell_hand', {'diabell_hand'})
	
	def check(self, stage: Stage) -> bool:
		return True
	
	def delta(self, stage: Stage) -> None:
		pass
