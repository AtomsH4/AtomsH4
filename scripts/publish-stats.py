"""Stage freshly generated stats SVGs, retaining validated previous cards on failure."""

import os
from pathlib import Path
import shutil
import xml.etree.ElementTree as ET

SVG_NS = "http://www.w3.org/2000/svg"
CARD_NAMES = ("stats.svg", "top-langs.svg")
ERROR_MARKERS = (
    "something went wrong",
    "rate limit",
    "bad credentials",
    "no github api tokens",
    "an unknown error",
)


def validate_card(path):
    root = ET.parse(path).getroot()
    if root.tag != f"{{{SVG_NS}}}svg":
        raise ValueError("File is not an SVG document")
    text_nodes = root.findall(f".//{{{SVG_NS}}}text")
    if not any("".join(node.itertext()).strip() for node in text_nodes):
        raise ValueError("SVG contains no card text")
    content = " ".join(root.itertext()).lower()
    if any(marker in content for marker in ERROR_MARKERS):
        raise ValueError("SVG contains an error card")


def stage_cards(generated_dir, previous_dir, output_dir):
    selected = []
    for name in CARD_NAMES:
        source = generated_dir / name
        try:
            validate_card(source)
            status = "updated"
        except (OSError, ET.ParseError, ValueError) as error:
            print(f"::warning::{name} was not regenerated ({error}); trying the previous card.")
            source = previous_dir / name
            try:
                validate_card(source)
            except (OSError, ET.ParseError, ValueError) as previous_error:
                raise RuntimeError(
                    f"No valid {name} is available; leaving the published assets unchanged."
                ) from previous_error
            status = "retained previous card"
        selected.append((name, source, status))

    # Resolve both cards before staging either; the publish step only runs on success.
    output_dir.mkdir(parents=True, exist_ok=True)
    for name, source, status in selected:
        shutil.copyfile(source, output_dir / name)
        print(f"{name}: {status}")

    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path:
        with open(summary_path, "a", encoding="utf-8") as summary:
            summary.write("### Stats cards\n\n")
            for name, _, status in selected:
                summary.write(f"- {name}: {status}\n")


if __name__ == "__main__":
    try:
        stage_cards(Path("generated-stats"), Path("previous-assets"), Path("public"))
    except RuntimeError as error:
        raise SystemExit(f"::error::{error}") from error
