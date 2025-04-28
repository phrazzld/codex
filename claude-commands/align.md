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
thinktank --instructions ALIGN-PROMPT.md --synthesis-model gemini-2.5-pro-preview-03-25 --model gemini-2.5-flash-preview-04-17 --model gemini-2.5-pro-preview-03-25 --model gpt-4.1 ./

# Create alignment plan
cp thinktank_output/gemini-2.5-pro-preview-03-25-synthesis.md ALIGN-PLAN.md

## CLEANUP
rm ALIGN-PROMPT.md

## REVIEW
echo "Review ALIGN-PLAN.md for actionable improvements to better align with our development philosophy."
