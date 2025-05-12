# WHITEBOARD

## GOAL
Generate creative technical brainstorming for a backlog item, exploring multiple approaches from conventional to innovative "cut the Gordian knot" solutions.

## READ
- Top item from BACKLOG.md

## WRITE
- Create `WHITEBOARD-CONTEXT.md` containing the top item from BACKLOG.md

## RUN
- Run the following command with the maximum timeout in the bash tool:
```bash
thinktank-wrapper --template whiteboard --inject WHITEBOARD-CONTEXT.md --model-set high_context --include-philosophy --include-glance ./
```