from pathlib import Path
paths = Path('bank')
for path in paths.iterdir():
	print(path)