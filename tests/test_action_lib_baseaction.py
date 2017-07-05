from men_and_mice_base_action_test_case import MenAndMiceBaseActionTestCase
from mock import patch

from lib.run_operation import RunOperation
from st2actions.runners.pythonrunner import Action

class TestActionLibBaseAction(MenAndMiceBaseActionTestCase):
    __test__ = True
    action_cls = RunOperation

    def test_init(self):
        action = self.get_action_instance({})
        self.assertIsInstance(action, RunOperation)
        self.assertIsInstance(action, Action)

    def test_camel_to_snake_lower(self):
        action = self.get_action_instance({})
        camel = "camelCaseString"
        snake = "camel_case_string"
        result = action.camel_to_snake(camel)
        self.assertEqual(result, snake)

    def test_camel_to_snake_upper(self):
        action = self.get_action_instance({})
        camel = "CamelCaseString"
        snake = "camel_case_string"
        result = action.camel_to_snake(camel)
        self.assertEqual(result, snake)

    def test_camel_to_snake_multiple_upper(self):
        action = self.get_action_instance({})
        camel = "GetADComputer"
        snake = "get_ad_computer"
        result = action.camel_to_snake(camel)
        self.assertEqual(result, snake)

    def test_snake_to_camel(self):
        action = self.get_action_instance({})
        snake = "snake_case_string"
        camel = "snakeCaseString"
        result = action.snake_to_camel(snake)
        self.assertEqual(result, camel)

    def test_get_del_arg_present(self):
        action = self.get_action_instance({})
        test_dict = {"key1": "value1",
                     "key2": "value2"}
        test_key = "key1"
        expected_dict = {"key2": "value2"}
        expected_value = test_dict["key1"]
        result_value = action.get_del_arg(test_key, test_dict)
        self.assertEqual(result_value, expected_value)
        self.assertEqual(test_dict, expected_dict)

    def test_get_del_arg_missing(self):
        action = self.get_action_instance({})
        test_dict = {"key1": "value1",
                     "key2": "value2"}
        test_key = "key3"
        expected_dict = test_dict
        expected_value = None
        result_value = action.get_del_arg(test_key, test_dict)
        self.assertEqual(result_value, expected_value)
        self.assertEqual(test_dict, expected_dict)
