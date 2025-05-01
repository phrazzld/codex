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
# Execute analysis with thinktank-wrapper
```bash
thinktank-wrapper --model-set high_context --include-glance --include-philosophy --instructions ALIGN-PROMPT.md ./
```

# Create alignment plan
Copy synthesis file to `ALIGN_PLAN.md`

## CLEANUP
rm ALIGN-PROMPT.md

