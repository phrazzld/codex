# Professional Documents

Professional resumes and CV in Markdown format with automated PDF generation.

## Contents

- **[resume.md](resume.md)** - General-purpose software engineering resume
- **[resume-meta.md](resume-meta.md)** - Meta/FAANG-tailored resume
- **[cv.md](cv.md)** - Comprehensive curriculum vitae
- **[styles/](styles/)** - CSS stylesheets for PDF generation
  - `base.css` - Shared base styles
  - `resume.css` - Compact resume styling
  - `cv.css` - Detailed CV styling

## Quick Start

### Generate PDFs

```bash
# Generate all PDFs
make all

# Generate individual PDFs
make resume      # → resume.pdf
make cv          # → cv.pdf
make meta        # → resume-meta.pdf

# Clean generated PDFs
make clean
```

### Watch Mode

Auto-regenerate PDFs when markdown files change:

```bash
make watch-resume  # Watch resume.md
make watch-cv      # Watch cv.md
make watch-meta    # Watch resume-meta.md
```

Press `Ctrl+C` to stop watching.

## Setup

### Prerequisites

```bash
# Install md-to-pdf globally
npm install -g md-to-pdf

# Verify installation
md-to-pdf --version
```

### Manual PDF Generation

```bash
# From this directory
md-to-pdf resume.md       # → resume.pdf
md-to-pdf cv.md           # → cv.pdf
md-to-pdf resume-meta.md  # → resume-meta.pdf
```

## Customization

### Editing Content

1. Edit the markdown files directly (`resume.md`, `cv.md`, `resume-meta.md`)
2. Regenerate PDFs with `make all` or specific targets
3. Review the generated PDFs

### Styling

CSS files in `styles/` control PDF appearance:

- **base.css** - Typography, colors, spacing, print optimization
- **resume.css** - Compact layout for 1-2 page resumes
- **cv.css** - Spacious layout for comprehensive CVs

To customize styling:

1. Edit the CSS files
2. Regenerate PDFs to see changes
3. Use watch mode for live updates: `make watch-resume`

### PDF Options

Configure PDF generation in markdown front-matter:

```yaml
---
stylesheet:
  - styles/base.css
  - styles/resume.css
pdf_options:
  format: Letter        # or A4
  margin: 0.4in 0.65in  # top/bottom left/right
  printBackground: true
  displayHeaderFooter: false
---
```

## Document Structure

### resume.md & resume-meta.md
- **Target length:** 1-2 pages
- **Use case:** Job applications, recruiter submissions
- **Style:** Compact, achievement-focused
- **Sections:** Summary, Experience, Projects, Skills, Education

### cv.md
- **Target length:** 4-8 pages
- **Use case:** Academic positions, comprehensive career overview
- **Style:** Detailed, narrative-driven
- **Sections:** Summary, Experience (detailed), Projects, Open Source, Skills, Education

## Technology Stack

- **md-to-pdf** - Markdown to PDF converter (Puppeteer-based)
- **Puppeteer** - Headless Chrome for rendering
- **CSS** - Styling and layout control
- **Makefile** - Build automation

## Why This Approach?

### Advantages

1. **Version Control** - Track changes to resumes with git
2. **Single Source of Truth** - Maintain one markdown file, generate PDF when needed
3. **Customizable** - Full control over styling with familiar CSS
4. **Fast Iteration** - Watch mode for instant feedback
5. **Professional Output** - High-quality PDFs via Chrome rendering
6. **Web Developer Friendly** - Leverage existing HTML/CSS skills

### Alternatives Considered

- **Pandoc + LaTeX** - Excellent output but 4GB install, complex setup
- **Pandoc + Typst** - Modern, fast, but requires learning new template language
- **Online Services** - Convenient but no version control, less customization
- **Word/Google Docs** - WYSIWYG but harder to version control

## Tips & Best Practices

### Content

- Keep resumes to 1-2 pages (recruiters spend ~6 seconds per resume)
- Use action verbs: "Built," "Led," "Architected," "Improved"
- Quantify achievements: "Reduced costs by 1000x," "Led team of 8"
- Tailor content for each position (maintain separate versions if needed)

### Styling

- Use system fonts for reliability across platforms
- Optimize margins for printing (0.5in minimum)
- Test print to PDF from browser for final quality check
- Keep link colors professional (blue or black)

### Workflow

1. Edit markdown in your favorite editor (VS Code, Neovim, etc.)
2. Use watch mode during editing: `make watch-resume`
3. Review PDF frequently
4. Commit markdown changes to git
5. Generate final PDFs before sending: `make all`

### Version Control

```bash
# Track content changes
git add resume.md cv.md resume-meta.md

# Track style changes
git add styles/

# Don't commit PDFs (regenerate as needed)
echo "*.pdf" >> .gitignore
```

## Troubleshooting

### "Could not load style" error

Ensure stylesheets are listed as array in front-matter:

```yaml
stylesheet:
  - styles/base.css
  - styles/resume.css
```

Not: `stylesheet: styles/resume.css`

### PDFs look different than expected

1. Check CSS file paths in front-matter
2. Verify no `@import` statements in CSS (use array in front-matter instead)
3. Test with `--watch` mode to see live changes
4. Clear Puppeteer cache: `rm -rf ~/.cache/puppeteer`

### Puppeteer errors

```bash
# Reinstall md-to-pdf
npm uninstall -g md-to-pdf
npm install -g md-to-pdf

# Or use npx (no global install)
npx md-to-pdf resume.md
```

## Help

```bash
# Show all make targets
make help

# md-to-pdf options
md-to-pdf --help
```

## License

Personal professional documents - not for redistribution.

---

*Last updated: 2025-10-01*
