# Robotoken

**What Would a GPT-3-Scale Robotics Dataset Cost?**  
A research preprint by Lucas Barbosa (NYU), September 2026.

Robotoken estimates the cost of collecting robotics data through a five-year teleoperation program. It compares public data scales, makes acquisition assumptions explicit, and examines the limits of equating language tokens with robot experience. Scenario totals are not validated capability thresholds; costs exclude model training compute.

[Website](https://robotoken.lbxa.net) · [Report PDF](report/robotoken.pdf) · [BibTeX](website/public/files/robotoken.bib) · [Contributor guide](AGENTS.md)

## Repository layout

| Path | Purpose |
| --- | --- |
| `report/robotoken.tex` | Authoritative, self-contained manuscript with embedded bibliography, style, and figure |
| `report/plot_scales.py` | Matplotlib source for the report and website figures |
| `website/src/content/sections/` | Manually maintained MDX web edition |
| `website/src/pages/`, `website/src/components/`, `website/src/styles/` | Astro page, reusable components, and shared research styling |
| `website/public/` | Published PDF, citation, and desktop/mobile figures |
| `website/wrangler.jsonc` | Cloudflare Worker and custom-domain configuration |

## Run the website

Use Bun and Node.js 22.12 or newer. From the repository root:

```sh
cd website
bun install --frozen-lockfile
bun run dev
```

Astro normally serves the site at `http://localhost:4321`. From `website/`, run:

```sh
bun run typecheck
bun run lint
bun run build
bun run preview
```

There is no automated test suite yet. Inspect desktop and mobile layouts, equations, tables, downloads, and figure labels when changing content or presentation.

## Build the report and figures

The existing `report/robotoken.tex` can be edited and compiled in Codex's LaTeX editor. To produce the publication PDF with TeX Live or MacTeX, run from the repository root:

```sh
make -C report
```

This requires `latexmk` and BibTeX and copies the resulting PDF to `website/public/files/robotoken.pdf`.

To regenerate the Matplotlib artwork, use `uv` and a TeX installation with `pdflatex` available:

```sh
uv run report/plot_scales.py
```

The script declares its Python dependencies and produces website SVG/PNG assets plus LaTeX PGF. Follow [report/README.md](report/README.md) to embed the generated PGF in the manuscript before compiling. Keep web text, figures, captions, tables, and caveats synchronized with the report; the two editions are maintained separately.

## Deploy to Cloudflare

From `website/`:

```sh
bun run deploy:check
bunx wrangler login
bunx wrangler whoami
bun run deploy
```

Login is a one-time local setup. The dry run validates without publishing; deployment builds and uploads the static site to the `robotoken` Worker and `robotoken.lbxa.net`. Use the Cloudflare account containing the active `lbxa.net` zone. Deployment uses the existing PDF and does not compile LaTeX. See [website/README.md](website/README.md) for CI authentication and domain details.

## Contributing and citation

Read [AGENTS.md](AGENTS.md) and [website/AGENTS.md](website/AGENTS.md). Preserve the shared template's header, typography, and spacing. Keep the editable TeX source in `report/`; website downloads expose PDF and BibTeX only.

Cite the preprint as: Lucas Barbosa. *What Would a GPT-3-Scale Robotics Dataset Cost?* Robotoken, September 2026. https://robotoken.lbxa.net. Citation metadata is available in [CITATION.cff](CITATION.cff) and the [BibTeX file](website/public/files/robotoken.bib).

## License and attribution

Robotoken-authored material is released under the [MIT License](LICENSE). Third-party material retains its own license and notices, including the embedded arXiv-style template and bundled contributor skills. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## Changelog

### 2026-09-29

- Use the author-supplied name Lucas Barbosa and affiliation NYU consistently across the report, website, and citation metadata.
- Added repository setup, citation metadata, editor conventions, and an MIT license for original material while preserving third-party attribution.
- Ignore local secrets, caches, and build intermediates; retain reviewed PDFs, figure exports, and the Bun lockfile for reproducible publication.
