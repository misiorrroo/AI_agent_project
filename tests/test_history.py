import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import history


class HistoryTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        data_dir = Path(self.temp_dir.name) / "data"
        self.history_db_file = data_dir / "historia.db"
        self.history_file = data_dir / "historia.json"
        self.history_db_file_patch = patch.object(
            history, "HISTORY_DB_FILE", self.history_db_file
        )
        self.history_file_patch = patch.object(
            history, "HISTORY_FILE", self.history_file
        )
        self.history_db_file_patch.start()
        self.history_file_patch.start()

    def tearDown(self):
        self.history_file_patch.stop()
        self.history_db_file_patch.stop()
        self.temp_dir.cleanup()

    def test_load_history_returns_empty_list_when_database_does_not_exist(self):
        self.assertEqual(history.load_history(), [])

    def test_save_history_creates_database_file(self):
        history.save_history([{"role": "user", "content": "Cześć"}])

        self.assertTrue(self.history_db_file.exists())

    def test_saved_history_can_be_loaded_in_the_same_order(self):
        messages = [
            {"role": "system", "content": "Pomagaj użytkownikowi."},
            {"role": "user", "content": "Jak działa Python?"},
        ]

        history.save_history(messages)

        self.assertEqual(history.load_history(), messages)

    def test_migrates_existing_json_history_on_first_load(self):
        messages = [{"role": "user", "content": "Poprzednia rozmowa"}]
        self.history_file.parent.mkdir(parents=True)
        self.history_file.write_text(json.dumps(messages), encoding="utf-8")

        self.assertEqual(history.load_history(), messages)
        self.assertEqual(history.load_history(), messages)

    def test_clear_does_not_restore_migrated_json_history(self):
        messages = [{"role": "user", "content": "Poprzednia rozmowa"}]
        self.history_file.parent.mkdir(parents=True)
        self.history_file.write_text(json.dumps(messages), encoding="utf-8")
        history.load_history()

        history.clear_history()

        self.assertEqual(history.load_history(), [])

    def test_clear_history_removes_all_messages(self):
        history.save_history([{"role": "user", "content": "test"}])

        history.clear_history()

        self.assertEqual(history.load_history(), [])


if __name__ == "__main__":
    unittest.main()
