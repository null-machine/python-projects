import pathlib
import sys
import time
import random

# Weird thing i have to do because Python (not needed when using the library)
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import sam

sam.log(
	"Hello World!",
	onFinished=lambda: sam.log("You can customize me with sam.Settings() or with the arguments", sam.Settings(pitch=-30))
)