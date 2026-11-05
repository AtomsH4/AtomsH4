# Profile stats through GitHub Actions

Approved scope: generate both STATS cards in the existing assets workflow, retain the existing
appearance, and keep the previous successful SVG whenever regeneration fails.

- Run with the existing 12-hour schedule, main-branch pushes, and manual dispatch.
- Render inside the runner using its automatic GITHUB_TOKEN and a fixed Stats Action/core version.
- Generate candidates outside the publishing directory. Validate SVG structure and reject error cards.
- Read previous cards from the existing output branch. Select a valid new or previous card
  independently for stats and languages; abort publishing if either has no valid candidate.
- Serialize asset runs to prevent concurrent publication.
- Keep the snake and trophy stages, then publish all five SVGs in one output-branch update.
- Switch README URLs only after the first production workflow has published both cards.
- Replace the obsolete Vercel setup instructions with the Actions workflow and recovery steps.

Validation: lint the workflow and shell blocks, exercise success/failure/fallback cases locally,
run the actual GitHub workflow, inspect both published SVGs, then verify the README references.
