# Makefile for generating professional PDFs from Markdown
# Uses md-to-pdf with custom CSS styling

.PHONY: all resume cv meta clean watch-resume watch-cv watch-meta help

# Default target
all: resume cv meta

# Individual document targets
resume: resume.pdf

cv: cv.pdf

meta: resume-meta.pdf

# PDF generation rules
resume.pdf: resume.md styles/resume.css styles/base.css
	@echo "Generating resume.pdf..."
	@md-to-pdf resume.md
	@echo "✓ Generated resume.pdf"

cv.pdf: cv.md styles/cv.css styles/base.css
	@echo "Generating cv.pdf..."
	@md-to-pdf cv.md
	@echo "✓ Generated cv.pdf"

resume-meta.pdf: resume-meta.md styles/resume.css styles/base.css
	@echo "Generating resume-meta.pdf..."
	@md-to-pdf resume-meta.md
	@echo "✓ Generated resume-meta.pdf"

# Watch mode for live updates
watch-resume:
	@echo "Watching resume.md for changes..."
	@md-to-pdf resume.md --watch

watch-cv:
	@echo "Watching cv.md for changes..."
	@md-to-pdf cv.md --watch

watch-meta:
	@echo "Watching resume-meta.md for changes..."
	@md-to-pdf resume-meta.md --watch

# Clean generated PDFs
clean:
	@echo "Removing generated PDFs..."
	@rm -f resume.pdf cv.pdf resume-meta.pdf
	@echo "✓ Cleaned"

# Help target
help:
	@echo "Professional Document PDF Generator"
	@echo ""
	@echo "Usage:"
	@echo "  make all          Generate all PDFs (resume, CV, Meta resume)"
	@echo "  make resume       Generate resume.pdf"
	@echo "  make cv           Generate cv.pdf"
	@echo "  make meta         Generate resume-meta.pdf"
	@echo "  make clean        Remove all generated PDFs"
	@echo ""
	@echo "Watch mode (auto-regenerate on changes):"
	@echo "  make watch-resume    Watch resume.md"
	@echo "  make watch-cv        Watch cv.md"
	@echo "  make watch-meta      Watch resume-meta.md"
	@echo ""
	@echo "Files:"
	@echo "  resume.md         General-purpose resume"
	@echo "  cv.md             Comprehensive curriculum vitae"
	@echo "  resume-meta.md    Meta/Facebook-tailored resume"
	@echo ""
	@echo "Styling:"
	@echo "  styles/base.css   Shared base styles"
	@echo "  styles/resume.css Resume-specific styles (compact)"
	@echo "  styles/cv.css     CV-specific styles (detailed)"
