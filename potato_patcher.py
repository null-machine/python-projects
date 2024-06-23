# py .\potato_patcher.py "C:\Program Files (x86)\VB\Voicemeeter\voicemeeter8x64.exe"

import os
import sys
import time
import subprocess
import traceback

from pymem import Pymem, process, exception

#############################################################################################
# This is an in-memory patch that launches and patches Voicemeeter Potato in memory on startup.
# It will not actually properly activate Voicemeeter but by supressing the activation popup after the trial period expires
# it behaves as if it has been activated for all intents and purposes.
#
# The most recent versions of Voicemeeter Potato validate their own binary integrity by checking the digital file signature
# so it is no longer possible to simply apply the patch to the binary itself and I couldn't be bothered to figure out how to bypass the signature check.
# This patch was developed for version 3.0.2.8 but it should work for newer versions as long as no major changes are made to the activation popup.
#
# For this to work as an autorun you can create a Task Scheduler Task with high privileges that launches this python script on logon.
# You have to pass the full exe path and file name of the Voicemeeter exe you want to patch as the only argument.
# The script will launch Voicemeeter and then immediately patch its memory.
#############################################################################################

patches = [
	("voicemeeter8x64.exe", b"\xb9\x2c\x01\x00\x00", b"\xb9\x00\x00"),
	("voicemeeter8.exe",	b"\x3d\x2c\x01\x00\x00", b"\x3d\x00\x00\x00\x00\x7e\x0a\xb8\x00\x00"),
]


def main(voicemeeter_exe_path):
	# Select the correct patch based on the executable name
	selected_patch = next((sig, patch) for handle, sig, patch in patches if handle.lower() in voicemeeter_exe_path.lower())

	# Launch Voicemeeter with idle priority
	proc = subprocess.Popen([voicemeeter_exe_path], cwd=os.path.dirname(voicemeeter_exe_path))
	pid = proc.pid

	if not selected_patch:
		print("- No patch found for the given executable.")
		return

	sig, patch = selected_patch
	try:
		pm = Pymem(pid)
	except exception.ProcessNotFound:
		print("- Process not found, even though it should have been launched.")
		return

	print(f"+ Found Voicemeeter with PID {pm.process_id}")
	for i in range(10):
		module = process.module_from_name(pm.process_handle, os.path.basename(voicemeeter_exe_path))
		if module is not None:
			break
		time.sleep(.1)
	else:
		print(f"- Could not resolve main module")
		print("* Aborting...")
		return

	address = pm.pattern_scan_module(sig, module)

	if address is None:
		print(f"- Couldn't find signature 0x{sig.hex()}")
		print("* Aborting...")
		return

	print(f"+ Found signature at address 0x{address:02x}")
	pm.write_bytes(address, patch, len(patch))
	print(f"+ Voicemeeter successfully patched")


if __name__ == '__main__':
	try:
		if len(sys.argv) > 1:
			main(' '.join(sys.argv[1:]))
		else:
			print(f"Usage: python {os.path.basename(__file__)} <path/to/voicemeeter8[x64].exe>")
	except Exception:
		traceback.print_exc()
		input()