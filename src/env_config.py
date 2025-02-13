import os
from dotenv import load_dotenv

class Config:
	__TELEGRAM_BOT_TOKEN_ENV = "TELEGRAM_BOT_TOKEN"
	__TELEGRAM_BOT_TOKEN_DEV_ENV = "TELEGRAM_BOT_TOKEN_DEV"
	__ACCESS_CHECK_ENV = "ACCESS_CHECK"
	__DEBUG_ENV = "DEBUG"
	__LOCAL_CHAT_ID_ENV = "LOCAL_CHAT_ID"
	__STAGE_CHAT_ID_ENV = "STAGE_CHAT_ID"
	__LOG_CHAT_ID_ENV = "LOG_CHAT_ID"
	__CORETEAM_PEOPLE_ENV = "CORETEAM_PEOPLE"

	def __init__(self):
		self.__forwarding_enabled = True

		# environment variables
		load_dotenv()
		self.__log_chat_id = os.getenv(self.__LOG_CHAT_ID_ENV)
		self.__debug = get_env_bool(self.__DEBUG_ENV)
		self.__access_check = get_env_bool(self.__ACCESS_CHECK_ENV)
		self.__coreteam_people = get_env_list(self.__CORETEAM_PEOPLE_ENV)

		if self.__debug is True:
			self.__chat_id = os.getenv(self.__LOCAL_CHAT_ID_ENV)
			self.__access_token = os.getenv(self.__TELEGRAM_BOT_TOKEN_DEV_ENV)
		else:
			self.__chat_id = os.getenv(self.__STAGE_CHAT_ID_ENV)
			self.__access_token = os.getenv(self.__TELEGRAM_BOT_TOKEN_ENV)

	def get_access_token(self) -> str:
		return self.__access_token

	def get_chat_id(self) -> str:
		return self.__chat_id

	def is_access_check_enable(self) -> bool:
		return self.__access_check

	def get_log_chat_id(self) -> str:
		return self.__log_chat_id

	def get_coreteam_people(self) -> list:
		return self.__coreteam_people

	def set_forvarding(self, value: bool):
		self.__forwarding_enabled = value

	def is_forwarding_enable(self) -> bool:
		return self.__forwarding_enabled

def get_env_bool(env_var, default=False) -> bool:
	value = os.getenv(env_var, str(default)).lower()
	return value in ("true", "1", "yes", "on")

def get_env_list(env_var, default=[]) -> list:
	value = os.getenv(env_var, default)
	return value.split(',')