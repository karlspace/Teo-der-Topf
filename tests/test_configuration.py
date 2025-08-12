import logging
import sys
import unittest
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from Application.configuration import Configuration


class TestConfiguration(unittest.TestCase):
    def test_log_level_invalid_defaults_to_info(self):
        self.assertEqual(
            Configuration.loglevel_from_string("invalid"),
            logging.INFO,
        )


if __name__ == "__main__":
    unittest.main()
