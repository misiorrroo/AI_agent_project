import base64
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import media


class MediaTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.settings_file = Path(self.temp_dir.name) / "settings.json"
        self.output_dir = Path(self.temp_dir.name) / "output"
        self.settings_patch = patch.object(media, "MEDIA_SETTINGS_FILE", self.settings_file)
        self.default_dir_patch = patch.object(media, "DEFAULT_MEDIA_OUTPUT_DIR", self.output_dir)
        self.api_key_patch = patch.object(media, "API_KEY", "test-api-key")
        self.settings_patch.start()
        self.default_dir_patch.start()
        self.api_key_patch.start()

    def tearDown(self):
        self.api_key_patch.stop()
        self.default_dir_patch.stop()
        self.settings_patch.stop()
        self.temp_dir.cleanup()

    def test_generate_speech_saves_raw_pcm_and_uses_expected_payload(self):
        response = Mock(ok=True, content=b"pcm-data")

        with patch.object(media.requests, "post", return_value=response) as post:
            output_file = media.generate_speech("zajawka")

        self.assertEqual(output_file.suffix, ".pcm")
        self.assertEqual(output_file.read_bytes(), b"pcm-data")
        self.assertEqual(post.call_args.kwargs["json"], {
            "model": "heygen/heygen-voice-1-turbo:free",
            "input": "zajawka",
            "voice": "nadine",
            "response_format": "pcm",
        })

    def test_generate_image_decodes_base64_and_uses_expected_payload(self):
        response = Mock(ok=True)
        response.json.return_value = {
            "data": [{"b64_json": base64.b64encode(b"png-data").decode()}],
        }

        with patch.object(media.requests, "post", return_value=response) as post:
            output_file = media.generate_image("zielona łąka")

        self.assertEqual(output_file.suffix, ".png")
        self.assertEqual(output_file.read_bytes(), b"png-data")
        self.assertEqual(post.call_args.kwargs["json"], {
            "model": "recraft/recraft-v4.1-flash-v2:free",
            "prompt": "zielona łąka",
            "aspect_ratio": "16:9",
            "n": 1,
        })

    def test_output_directory_is_persisted(self):
        selected_dir = Path(self.temp_dir.name) / "selected"

        result = media.set_media_output_dir(selected_dir)

        self.assertEqual(result, selected_dir.resolve())
        self.assertEqual(media.get_media_output_dir(), selected_dir.resolve())


if __name__ == "__main__":
    unittest.main()
