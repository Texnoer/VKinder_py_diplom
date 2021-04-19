import unittest
from bot_commands import Search, VkSaver
from vk_bot import VkBot


class TestVk(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        return "start testing"

    def setUp(self):
        return "start test"

    def test_add_status(self):
        self.assertEqual(Search.add_status('5'), "всё сложно")
        print(f'\n{Search.add_status.__name__} - test pass')
        self.assertEqual(Search.add_status('3'), "помолвлен(-а)")
        print(f'{Search.add_status.__name__} - test pass')

    def test_get_photo(self):
        self.assertEqual(VkSaver().get_photo(1234567, 'profile'), {})
        print(f'\n{VkSaver().get_photo.__name__} - test pass')

    def test_get_info(self):
        self.assertTrue(Search.info(), True)
        print('test pass')

    def test_get_name_from_vk(self):
        self.assertEqual(VkBot(1)._get_user_name_from_vk_id(1), 'Павел')
        print(f'\n{VkBot._get_user_name_from_vk_id.__name__} - test pass')

    def tearDown(self):
        return "stop testing"

    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == '__main__':
    unittest.main()
