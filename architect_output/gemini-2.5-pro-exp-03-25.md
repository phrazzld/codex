```mermaid
flowchart TD
    subgraph CodexRepo [codex Repository]
        direction LR

        subgraph UserFacing [User Interaction & Setup]
            style UserFacing fill:#f9f,stroke:#333,stroke-width:2px
            User[Developer/User] --> InstallScript(install.sh);
            User --> Readme(README.md);
            User --> ClaudeMD(CLAUDE.md);
            User --> Backlog(BACKLOG.md);
        end

        subgraph Configuration [Shell Configuration]
            style Configuration fill:#ccf,stroke:#333,stroke-width:2px
            Dotfiles(dotfiles/)
            Dotfiles --> Zshrc(.zshrc)
            Dotfiles --> Aliases(.aliases)
            Dotfiles --> Env(.env)
        end

        subgraph AI_Workflow [AI Workflow Components]
            style AI_Workflow fill:#9cf,stroke:#333,stroke-width:2px
            CommandsDir(claude-commands/)
            CommandsDir --> Commands[Commands (*.md)\n- /audit\n- /plan\n- /execute\n- ...]

            subgraph Documentation [Documentation & Standards]
                style Documentation fill:#fca,stroke:#333,stroke-width:2px
                DocsDir(docs/)
                DocsDir --> DevPhilosophy(DEVELOPMENT_PHILOSOPHY.md)
                DocsDir --> PromptsDir(prompts/)
                PromptsDir --> Prompts[Prompts (*.md)\n- audit.md\n- plan.md\n- execute.md\n- ...]
                DocsDir --> ProfDocsDir(professional/)
                ProfDocsDir --> CV(cv.md)
                ProfDocsDir --> Resume(resume.md)
            end
        end

        subgraph ExternalTools [External Tools]
            style ExternalTools fill:#eee,stroke:#666,stroke-width:1px,stroke-dasharray: 5 5
            Architect(architect CLI)
        end

        %% Relationships
        InstallScript -- Creates Symlinks --> Dotfiles;
        InstallScript -- Creates Symlinks --> CommandsDir;

        Commands -- Uses Templates --> Prompts;
        Commands -- Guided By --> DevPhilosophy;
        Commands -- Invokes --> Architect;
        Architect -- Generates Output For --> Commands;
        DevPhilosophy -- Informs --> Architect;

        Readme -- Describes --> CodexRepo;
        ClaudeMD -- Guides Usage Of --> CommandsDir;
        Backlog -- Informs Future --> CodexRepo;
    end

    %% Styling
    classDef default fill:#fff,stroke:#333,stroke-width:1px;
    class UserFacing fill:#e9d8fd,stroke:#8e44ad,stroke-width:1px;
    class Configuration fill:#d5f5e3,stroke:#27ae60,stroke-width:1px;
    class AI_Workflow fill:#d6eaf8,stroke:#2980b9,stroke-width:1px;
    class Documentation fill:#fdebd0,stroke:#e67e22,stroke-width:1px;
    class ExternalTools fill:#f2f3f4,stroke:#7f8c8d,stroke-width:1px;

    class InstallScript,Readme,ClaudeMD,Backlog UserFacing;
    class Dotfiles,Zshrc,Aliases,Env Configuration;
    class CommandsDir,Commands AI_Workflow;
    class DocsDir,DevPhilosophy,PromptsDir,Prompts,ProfDocsDir,CV,Resume Documentation;
    class Architect ExternalTools;
```

### Diagram Explanation

This Mermaid flowchart visualizes the structure and key relationships within the `codex` repository.

-   **User Interaction & Setup (Purple)**: Shows how a user interacts with the repository, primarily through the `README.md` for understanding, `CLAUDE.md` for AI usage guidelines, `BACKLOG.md` for future plans, and `install.sh` for setting up the environment.
-   **Shell Configuration (Green)**: Represents the `dotfiles` directory containing shell configurations (`.zshrc`, `.aliases`, `.env`) that are symlinked into the user's home directory by `install.sh`.
-   **AI Workflow Components (Blue)**: Highlights the core AI-driven workflow elements. The `claude-commands/` directory contains executable command scripts (like `/audit`, `/plan`). These commands utilize corresponding templates from `docs/prompts/` and are heavily guided by the `DEVELOPMENT_PHILOSOPHY.md`. Many commands invoke an external `architect` CLI tool for complex generation tasks.
-   **Documentation & Standards (Orange)**: Groups the essential documentation. `DEVELOPMENT_PHILOSOPHY.md` is central, defining standards used by commands and the architect tool. The `docs/prompts/` directory holds templates for the commands, and `docs/professional/` contains CV/resume templates.
-   **External Tools (Gray Dashed)**: Represents the `architect` CLI, an external dependency invoked by several Claude commands.

### Key Insights

1.  **Centrality of `DEVELOPMENT_PHILOSOPHY.md`**: This document is a core artifact, guiding both the AI commands and the external `architect` tool, ensuring consistent development practices.
2.  **Command-Prompt Relationship**: There's a direct link between the executable scripts in `claude-commands/` and the templates in `docs/prompts/`.
3.  **Automation via `install.sh`**: The script automates the setup by linking configurations (`dotfiles`) and AI commands (`claude-commands`) into the user's environment.
4.  **Architect Tool Integration**: Several commands rely on the `architect` CLI, indicating a workflow that leverages external AI processing based on local context and standards.
5.  **Structured Workflow**: The repository enforces a structured approach to development tasks (planning, executing, debugging, reviewing) through dedicated commands and prompts.