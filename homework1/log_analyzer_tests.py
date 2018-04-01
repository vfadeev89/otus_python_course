import unittest
import os
import log_analyzer


class LogAnalyzerTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_correct_loading_default_config_file(self):
        expected = log_analyzer.config
        actual = log_analyzer.load_config(os.path.join("./configs/corrupted_config.json"))
        self.assertEqual(expected, actual)

    def test_correct_loading_custom_config_file(self):
        expected = log_analyzer.config
        actual = log_analyzer.load_config("./configs/config.json")
        self.assertNotEqual(expected, actual)

    def test_correct_getting_last_log_file(self):
        expected = "./log/nginx-access-ui.log-20170630.gz"
        actual = log_analyzer.get_latest_log_file_path(log_analyzer.config["LOG_DIR"],
                                                       log_analyzer.config["LOG_NAME_PATTERN"])
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
