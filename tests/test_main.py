import tempfile
import unittest
from pathlib import Path

from main import build_message, load_recipients


class QuoteEmailerTests(unittest.TestCase):
    def test_load_recipients(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "recipients.csv"
            path.write_text("name,email\nAda,ada@example.com\n", encoding="utf-8")
            self.assertEqual(load_recipients(path), [("Ada", "ada@example.com")])

    def test_csv_columns_are_required(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "recipients.csv"
            path.write_text("address\na@example.com\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                load_recipients(path)

    def test_message_headers(self):
        message = build_message("from@example.com", "to@example.com", "Ada", "Keep going.")
        self.assertEqual(message["To"], "to@example.com")
        self.assertIn("Keep going.", message.get_content())


if __name__ == "__main__":
    unittest.main()
