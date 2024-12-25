from pathlib import Path
from subprocess import Popen

from mitmproxy import SNIFFER_PATH
from impl.browser import (
	BrowserBase,
	DesktopBrowser,
	RemoteBrowser,
)
from impl.zmq_client import ZMQClient

class Main:
	
	def __init__(
		self,
		*,
		user_data_dir: str | Path | None = None,
	) -> None:
		self.proxy_port = 23334
		self.remote_port = 34445
		self.message_queue_port = 45556
		self.proxy_process: Popen[bytes] | None = None
		
		sniffer_args: list[str | Path] = [
			"mitmdump",
			"-s",
			SNIFFER_PATH,
			"-p",
			f"{self.proxy_port}",
			"--set",
			f"port={self.message_queue_port}",
		]
		
		self.mitmproxy_process = Popen(sniffer_args)
		self.browser = DesktopBrowser(
			self.proxy_port,
			0, # initial left position of window
			0, # initial top position of window
			1280, # window viewport width
			720, # window viewport height
			headless=False,
			user_data_dir=None, # none means private browsing
		)
		self.message_queue_client = ZMQClient(
			port=self.message_queue_port,
		)
	
	def __exit__(self, exc_type, exc_value, traceback) -> None:
		if self.browser is not None:
			self.browser.close()
			self.browser = None
		if self.mitmproxy_process is not None:
			if self.mitmproxy_process.poll() is None:
				self.mitmproxy_process.kill()
			self.mitmproxy_process = None

main = Main()

line = ""
while line != "exit":
	line = input()

if main.mitmproxy_process is not None:
	if main.mitmproxy_process.poll() is None:
		main.mitmproxy_process.kill()
	main.mitmproxy_process = None