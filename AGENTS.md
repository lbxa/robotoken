# Repository Guidelines

## Project Structure & Module Organization

- `report/robotoken.tex` is the authoritative, self-contained manuscript; `robotoken.pdf` is the publication artifact.
- `report/plot_scales.py` generates Matplotlib figures; `report/figures/` holds the LaTeX PGF output.
- `website/src/pages/index.astro` assembles the site. Components, styles, and ordered MDX sections live in `website/src/components/`, `styles/`, and `content/sections/`.
- `website/public/` contains figures, the PDF download, and BibTeX. `website/dist/` and `report/build/` are generated directories.
- Follow the additional guidance in `website/AGENTS.md` for website changes.

## Build, Test, and Development Commands

Run website commands from `website/`:

- `bun install --frozen-lockfile`: install locked dependencies.
- `bun run dev`: start local development.
- `bun run build`: generate the static site; `bun run preview` serves it locally.
- `bun run typecheck` and `bun run lint`: check TypeScript, Astro, and ESLint rules.
- `bun run deploy:check`: build and validate Wrangler without publishing.
- `bun run deploy`: build and publish to `robotoken.lbxa.net`. Confirm the account with `bunx wrangler whoami` first; keep credentials out of Git.

From the repository root, `make -C report` compiles and copies the PDF into website downloads; it requires `latexmk` and BibTeX. `uv run report/plot_scales.py` regenerates figures. Embed the generated PGF into the manuscript's marked block as described in `report/README.md`.

## Coding Style & Naming Conventions

Use two-space indentation for Astro/TypeScript/configuration and four spaces for Python. Follow surrounding quote conventions, strict TypeScript, and ESLint; prefer `const`. Use PascalCase component names and numbered MDX filenames such as `03-acquisition.mdx`, with stable kebab-case slugs and explicit frontmatter ordering.

## Testing Guidelines

No automated test framework, test naming convention, or coverage threshold is configured. Run build, typecheck, and lint for website changes. Inspect desktop/mobile rendering, equations, tables, links, and figures. For manuscript changes, compile the existing document, inspect the PDF, and verify references and website parity.

## Research & Editing Constraints

Keep manuscript and web content synchronized, including figures, captions, assumptions, and caveats. Preserve the template's exact infinity header, typography, and spacing. Publish PDF and BibTeX only. Distinguish scenario assumptions from measured evidence. Author documents directly; use Context7 for current library/API documentation.

## Commit & Pull Request Guidelines

History currently contains only `init`; no established commit convention exists. Use concise imperative subjects. PRs should explain the change, relevant issues, validation, and screenshots for visual changes. Record durable decisions in the affected README changelog.
