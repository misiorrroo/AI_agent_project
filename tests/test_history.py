import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import history


class HistoryTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.history_file = Path(self.temp_dir.name) / "data" / "historia.json"
        self.history_file_patch = patch.object(
            history,
            "HISTORY_FILE",
            self.history_file,
        )
        self.history_file_patch.start()

    def tearDown(self):
        self.history_file_patch.stop()
        self.temp_dir.cleanup()

    def test_load_history_returns_empty_list_when_file_does_not_exist(self):
        self.assertEqual(history.load_history(), [])

    def test_save_history_creates_directory_and_file(self):
        messages = [{"role": "user", "content": "Cześć"}]

        history.save_history(messages)

        self.assertTrue(self.history_file.exists())

    def test_saved_history_can_be_loaded(self):
        messages = [
            {"role": "system", "content": "Pomagaj użytkownikowi."},
            {"role": "user", "content": "Jak działa Python?"},
        ]

        history.save_history(messages)

        self.assertEqual(history.load_history(), messages)


if __name__ == "__main__":
    unittest.main()
