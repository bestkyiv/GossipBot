import configparser

class Config:
	__BOT_TOKEN_PATH = ('TELEGRAM', 'bot_token')
	__CHAT_ID_PATH = ('CHAT', 'chat_id')
	__CHAT_ACCESS_PATH = ('CHAT', 'access_check')
	__CHAT_PUBLIC_PASSWORD_PATH = ('CHAT', 'public_password')
	__DEBUG_PATH = ('DEBUG', 'debug')

	def __init__(self):
		config = configparser.ConfigParser()
		config.read('config.ini')
		self.__forwarding_enabled = True

		# todo add check for missing keys, raise error
		section, key = self.__BOT_TOKEN_PATH
		self.__api_key = config.get(section, key)

		section, key = self.__CHAT_ACCESS_PATH
		self.__access_check = config.getboolean(section, key)

		section, key = self.__CHAT_ID_PATH
		self.__chat_id = config.getint(section, key)

		section, key = self.__CHAT_PUBLIC_PASSWORD_PATH
		self.__public_password = config.get(section, key)

		section, key = self.__DEBUG_PATH
		self.__debug = config.getboolean(section, key)

	def get_access_token(self) -> str:
		return self.__api_key

	def get_chat_id(self) -> str:
		return self.__chat_id
	
	def get_public_password(self) -> str:
		return self.__public_password

	def is_access_check_enable(self) -> bool:
		return self.__access_check

	def is_debug(self) -> bool:
		return self.__debug
	
	def set_forvarding(self, value: bool):
		self.__forwarding_enabled = value

	def is_forwarding_enable(self) -> bool:
		return self.__forwarding_enabled
