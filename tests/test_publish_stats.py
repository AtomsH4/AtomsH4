from contextlib import redirect_stdout
import importlib.util
import io
from pathlib import Path
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location(
    "publish_stats", Path(__file__).resolve().parents[1] / "scripts/publish-stats.py"
)
publisher = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(publisher)

VALID_SVG = '<svg xmlns="http://www.w3.org/2000/svg"><text>{}</text></svg>'


class PublishStatsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.generated = self.root / "generated"
        self.previous = self.root / "previous"
        self.output = self.root / "public"
        self.generated.mkdir()
        self.previous.mkdir()

    def write_cards(self, directory, label):
        for name in publisher.CARD_NAMES:
            (directory / name).write_text(VALID_SVG.format(label), encoding="utf-8")

    def stage(self):
        # Expected failures in fixtures must not create GitHub Actions warnings.
        with redirect_stdout(io.StringIO()):
            publisher.stage_cards(self.generated, self.previous, self.output)

    def test_fresh_cards_replace_previous_cards(self):
        self.write_cards(self.generated, "Fresh stats")
        self.write_cards(self.previous, "Previous stats")
        self.stage()
        for name in publisher.CARD_NAMES:
            self.assertEqual(
                (self.output / name).read_bytes(), (self.generated / name).read_bytes()
            )

    def test_missing_candidates_retain_previous_cards(self):
        self.write_cards(self.previous, "Previous stats")
        self.stage()
        for name in publisher.CARD_NAMES:
            self.assertEqual(
                (self.output / name).read_bytes(), (self.previous / name).read_bytes()
            )

    def test_error_card_never_replaces_previous_card(self):
        self.write_cards(self.generated, "Fresh stats")
        self.write_cards(self.previous, "Previous stats")
        (self.generated / "stats.svg").write_text(
            VALID_SVG.format("Something went wrong! GitHub API rate limiting"),
            encoding="utf-8",
        )
        self.stage()
        self.assertEqual(
            (self.output / "stats.svg").read_bytes(),
            (self.previous / "stats.svg").read_bytes(),
        )
        self.assertEqual(
            (self.output / "top-langs.svg").read_bytes(),
            (self.generated / "top-langs.svg").read_bytes(),
        )

    def test_invalid_candidate_types_fall_back(self):
        for content in ("<svg", "<html>Unavailable</html>",
                        '<svg xmlns="http://www.w3.org/2000/svg"/>'):
            with self.subTest(content=content):
                self.write_cards(self.generated, "Fresh stats")
                self.write_cards(self.previous, "Previous stats")
                (self.generated / "stats.svg").write_text(content, encoding="utf-8")
                self.stage()
                self.assertEqual(
                    (self.output / "stats.svg").read_bytes(),
                    (self.previous / "stats.svg").read_bytes(),
                )

    def test_first_run_failure_stages_neither_card(self):
        (self.generated / "stats.svg").write_text(
            VALID_SVG.format("Fresh stats"), encoding="utf-8"
        )
        with self.assertRaises(RuntimeError):
            self.stage()
        self.assertFalse(self.output.exists())

    def test_invalid_previous_card_also_stops_publication(self):
        self.write_cards(self.previous, "Bad credentials")
        with self.assertRaises(RuntimeError):
            self.stage()
        self.assertFalse(self.output.exists())


if __name__ == "__main__":
    unittest.main()
