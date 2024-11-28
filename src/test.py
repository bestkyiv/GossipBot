from env_config import Config 
import unittest

SETTINGS = Config()

class TestSettings(unittest.TestCase):
    def test_get_access_token(self):
        self.__test_settings_value(SETTINGS.get_access_token)
    def test_get_chat_id(self):
        self.__test_settings_value(SETTINGS.get_chat_id)
    def test_access_check(self):
        self.__test_settings_value(SETTINGS.is_access_check_enable)
    def test_coreteam_people(self):
        self.__test_settings_value(SETTINGS.get_coreteam_people)

    def __test_settings_value(self, func):
        value = func()
        self.assertIsNotNone(value)
        print("Value: ", value)

if __name__ == '__main__':
    unittest.main()