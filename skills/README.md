# Skills

Skills are plain Markdown runbooks, one per folder at `skills/<name>/SKILL.md`. Any agent can use them: it opens the file and follows the steps, with no plugin or loader required. Which skill runs for which request is decided by the task router table in `AGENTS.md`, so a skill is only ever reached from there or from another skill that hands off to it.
