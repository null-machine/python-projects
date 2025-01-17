import base64
from collections.abc import Mapping
import datetime
import json
import re
from ipaddress import ip_address
from logging import getLogger
from typing import Any
from board import Board

import wsproto.frame_protocol
from mitmproxy import http

from majsoulrpa.common import validate_user_port

from protobuf_liqi import liqi_pb2
from google.protobuf.message_factory import GetMessageClass
import google.protobuf.json_format

logger = getLogger(__name__)

_message_pattern = re.compile(b"^(?:\x01|\x02..)\n.(.*?)\x12", flags=re.DOTALL)
_response_pattern = re.compile(b"^\x03..\n\x00\x12", flags=re.DOTALL)
_heartbeat_pattern = re.compile(b"<= heartbeat -", flags=re.DOTALL)

class Sniffer:
	
	def __init__(self) -> None:
		self.board = None
		self._message_queue: dict[int, dict] = {}
		self._message_type_map: dict = {}
		for sdesc in liqi_pb2.DESCRIPTOR.services_by_name.values():
			for mdesc in sdesc.methods:
				self._message_type_map["." + mdesc.full_name] = (
					GetMessageClass(mdesc.input_type),
					GetMessageClass(mdesc.output_type),
				)
		for tdesc in liqi_pb2.DESCRIPTOR.message_types_by_name.values():
			self._message_type_map["." + tdesc.full_name] = (
				GetMessageClass(tdesc),
				None,
			)
		self._MESSAGE_TYPE_MAP = {}
		for tdesc in liqi_pb2.DESCRIPTOR.message_types_by_name.values():
			self._MESSAGE_TYPE_MAP["." + tdesc.full_name] = GetMessageClass(tdesc)
	
	def websocket_message(self, flow: http.HTTPFlow) -> None:  # noqa: C901
		
		websocket_data = flow.websocket
		if websocket_data is None:
			msg = "`websocket_data is None`"
			raise RuntimeError(msg)

		# Get the last message of WebSocket.
		if len(websocket_data.messages) == 0:
			msg = "`len(websocket_data.messages) == 0`"
			raise RuntimeError(msg)

		message = websocket_data.messages[-1]
		if message.type != wsproto.frame_protocol.Opcode.BINARY:
			msg = f"{message.type}: An unsupported WebSocket message type."
			raise RuntimeError(msg)

		direction = "outbound" if message.from_client else "inbound"

		content = message.content # byte string

		if _heartbeat_pattern.search(content) is not None:
			return # Ignore the heartbeats exchanged in the tournament room

		m = _message_pattern.search(content)
		if m is not None:
			type_ = content[0]
			assert type_ in [1, 2]

			number = None
			name = m.group(1).decode(encoding="utf-8")

			if type_ == 2:
				# Processing request messages
				# that expect response messages.
				# Store messages in a queue until
				# a corresponding response message is found.
				number = int.from_bytes(content[1:2], byteorder="little")
				if number in self._message_queue:
					prev_request = self._message_queue[number]
					msg = (
						"There is not any response message"
						" for the following WebSocket request message:\n"
						f"direction: {prev_request['direction']}\n"
						f"content: {prev_request['request']}"
					)
					logger.warning(msg)

				self._message_queue[number] = {
					"direction": direction,
					"name": name,
					"request": content,
				}

				return

			# Processing request messages that do not require a response
			assert type_ == 1
			assert number is None

			request_direction = direction
			request = content

			if request_direction == "outbound":
				direction = "inbound"
			else:
				assert request_direction == "inbound"
				direction = "outbound"
			response = None

		else:
			# Response message.
			# Find the corresponding request message from the queue.
			m = _response_pattern.search(content)
			if m is None:
				msg = (
					"An unknown WebSocket message:\n"
					f"direction: {direction}\n"
					f"content: {content!r}"
				)
				raise RuntimeError(msg)
			
			number = int.from_bytes(content[1:2], byteorder="little")
			if number not in self._message_queue:
				msg = (
					"An WebSocket response message"
					" that does not match to any request message:\n"
					f"direction: {direction}\n"
					f"content: {content!r}"
				)
				raise RuntimeError(msg)

			request_direction = self._message_queue[number]["direction"]
			name = self._message_queue[number]["name"]
			request = self._message_queue[number]["request"]
			response = content
			del self._message_queue[number]

		
		# Check that the directions of
		# the request and response are consistent.
		if request_direction == "inbound":
			if direction == "inbound":
				msg = (
					"Both request and response WebSocket messages are inbound."
				)
				raise RuntimeError(msg)
			assert direction == "outbound"
		else:
			assert request_direction == "outbound"
			if direction == "outbound":
				msg = (
					"Both request and response WebSocket messages"
					" are outbound."
				)
				raise RuntimeError(msg)
			assert direction == "inbound"
		
		def unwrap_message(message: bytes) -> tuple[str, bytes]:
			wrapper = liqi_pb2.Wrapper()  # type: ignore[attr-defined]
			wrapper.ParseFromString(message)
			return (wrapper.name, wrapper.data)
		
		match request[0]:
			# A request message that does not require a response
			# is missing the two bytes of the message number.
			case 1:
				name, request_data = unwrap_message(request[1:])
			# A request message that has a corresponding
			# response message, there are 2 bytes to store
			# the message number, and the name must be extracted to
			# parse the response message.
			case 2:
				name, request_data = unwrap_message(request[3:])
			case _:
				msg = f"{request[0]}: unknown request type."
				raise RuntimeError(msg)
		
		if response is not None:
			if response[0] != 3:  # noqa: PLR2004
				msg = f"{response[0]}: unknown response type."
				raise RuntimeError(msg)
			response_name, response_data = unwrap_message(response[3:])
			if response_name != "":
				msg = f"{response_name}: unknown response name."
				raise RuntimeError(msg)
		else:
			response_data = b""
		
		# Convert Protocol Buffers messages to JSONizable object format
		def jsonize(
			name: str,
			data: bytes,
			*,
			is_response: bool,
		) -> dict[str, Any]:
			if is_response:
				try:
					parser = self._message_type_map[name][1]()
				except IndexError as ie:
					now = datetime.datetime.now(datetime.UTC)
					file_name = now.strftime(f"%Y-%m-%d-%H-%M-%S-{name}.bin")
					with Path(file_name).open("wb") as fp:
						fp.write(data)
					msg = (
						"A new API found:\n"
						f"  name: {name}\n"
						f"Raw data was saved to {file_name}.\n"
						"Please cooperate by providing data. "
						"Thank you for your cooperation."
					)
					raise RuntimeError(msg) from ie
			else:
				try:
					parser = self._message_type_map[name][0]()
				except KeyError as ke:
					now = datetime.datetime.now(datetime.UTC)
					file_name = now.strftime(f"%Y-%m-%d-%H-%M-%S-{name}.bin")
					with Path(file_name).open("wb") as fp:
						fp.write(data)
					msg = (
						"A new API found:\n"
						f"  name: {name}\n"
						f"Raw data was saved to {file_name}.\n"
						"Please cooperate by providing data. "
						"Thank you for your cooperation."
					)
					raise RuntimeError(msg) from ke

			parser.ParseFromString(data)

			return google.protobuf.json_format.MessageToDict(
				parser,
				always_print_fields_with_no_presence=True,
				preserving_proto_field_name=True,
			)

		jsonized_request = jsonize(name, request_data, is_response=False)
		if response is not None:
			jsonized_response = jsonize(name, response_data, is_response=True)
		else:
			jsonized_response = None
		
		# print(f'\n{name}\njson req: {jsonized_request}\njson resp: {jsonized_response}\nrequest data:{request_data}')
		
		def _decode_bytes(buf: bytes) -> bytes:
			keys = [132, 94, 78, 66, 57, 162, 31, 96, 28]
			decode = bytearray()
			for i, _byte in enumerate(buf):
				mask = ((23 ^ len(buf)) + 5 * i + keys[i % len(keys)]) & 255
				_byte ^= mask
				decode += _byte.to_bytes(1, "little")
			return bytes(decode)
		
		def parse_action(
			message: Mapping,
			*,
			restore: bool = False,
		) -> tuple[int, str, dict[str, Any]]:
			step: int = message["step"]
			name: str = message["name"]
			encoded_data: str = message["data"]
			data: bytes = base64.b64decode(encoded_data)

			if not restore:
				data = _decode_bytes(data)

			parser = self._MESSAGE_TYPE_MAP[f".lq.{name}"]()
			parser.ParseFromString(data)
			result = google.protobuf.json_format.MessageToDict(
				parser,
				always_print_fields_with_no_presence=True,
				preserving_proto_field_name=True,
			)

			return step, name, result
		
		# if name == ".lq.FastTest.checkNetworkDelay" or name == ".lq.FastTest.inputOperation":
		# 	return
		
		match name:
			case ".lq.ActionPrototype":
				if jsonized_request is not None:
					request_step, request_name, request_result = parse_action(jsonized_request)
					print(f'#### {request_step} {request_name} {request_result}')
					match request_name:
						case "ActionNewRound":
							self.board = Board(request_result)
						case "ActionDiscardTile":
							self.board.process_discard(request_result)
						case "ActionChiPengGang":
							self.board.process_meld(request_result)
					

addons = [Sniffer()]