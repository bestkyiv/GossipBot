import configparser

class Settings:
	__BOT_TOKEN_PATH = ('TELEGRAM', 'bot_token')
	__CHAT_ID_PATH = ('CHAT', 'chat_id')
	__CHAT_ACCESS_PATH = ('CHAT', 'access_check')

	def __init__(self):
		config = configparser.ConfigParser()
		config.read('settings.ini')

		# todo add check for missing keys, raise error
		section, key = self.__BOT_TOKEN_PATH
		self.__api_key = config.get(section, key)

		section, key = self.__CHAT_ACCESS_PATH
		self.__access_check = config.getboolean(section, key)
		if self.__access_check:
			raise NotImplementedError("Access check is not implemented yet")

		section, key = self.__CHAT_ID_PATH
		self.__chat_id = config.getint(section, key)

	def get_access_token(self) -> str:
		return self.__api_key

	def get_chat_id(self) -> str:
		return self.__chat_id

	def is_access_check_enable(self) -> bool:
		return self.__access_check