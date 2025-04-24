# backlog

- rename codex to something else

- extract hardcoded thinktank invocations from claude command files so when we change them we don't have to manually change them in every file
- it would be nice if there were a way to have claude code automatically log its activity every so often, and then automatically trigger certain actions if the last x lines / last y time blocks of activity are redundant or looped or obviously stuck eg hit /consult if it has been ten minutes and gone nowhere
- build stronger "get relevant files for context" tool
  - ... or just always throw the whole codebase at 1m+ context models
- modify resolve action to ask thinktank for help
- modify audit action to use thinktank to conduct the audit, not just draft remediation
- define precommit that sends diff and dev philosophy to flash?
