# ALIGN

## GOAL
Identify ways the codebase can better align with our development philosophy.

## READ
- DEVELOPMENT_PHILOSOPHY.md
- Any relevant language-specific appendices

## PREPARE
# Create prompt file
cat > ALIGN-PROMPT.md << 'EOL'
$(cat "docs/prompts/align.md")
EOL

## RUN
# Execute analysis with thinktank
```bash
thinktank --instructions ALIGN-PROMPT.md $THINKTANK_HIGH_CONTEXT_MODELS $THINKTANK_SYNTHESIS_MODEL $(find_glance_files) $(find_philosophy_files)
```

# Create alignment plan
Copy synthesis file to `ALIGN_PLAN.md`

## CLEANUP
rm ALIGN-PROMPT.md

