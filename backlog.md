# backlog

- current workflow is: manually modify backlog, run plan command to generate a plan file, run ticket command to turn it into a todo file, run execute to knock out tasks, run chill and consult when we encounter hiccups, run review when we finish, run address if we need to and rinse and repeat until things are looking fresh. problem: the plan command doesn't break work up often enough; our plan files are too often too broad in scope and result in huge todo files and huge pull requests which are difficult to review and qa and quite brittle to manage. we need to either modify the plan command to do a better job of breaking up bullets it fetches from the backlog, or we need to add another step after plan but before ticket that sanity checks the scope of the plan file and breaks it into multiple plan files if it's too broad

- rename codex to something else
  - this thing is my whole engineering base of operations
  - fortress of solitude
  - cloud nine
  - the lanes
  - necronomicon
  - cloaca maxima
  - grimoire

- extract hardcoded thinktank invocations from claude command files so when we change them we don't have to manually change them in every file
- it would be nice if there were a way to have claude code automatically log its activity every so often, and then automatically trigger certain actions if the last x lines / last y time blocks of activity are redundant or looped or obviously stuck eg hit /consult if it has been ten minutes and gone nowhere
- build stronger "get relevant files for context" tool
  - ... or just always throw the whole codebase at 1m+ context models
- modify resolve action to ask thinktank for help
- modify audit action to use thinktank to conduct the audit, not just draft remediation
- define precommit that sends diff and dev philosophy to flash?
