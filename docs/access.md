# Warehouse access

Status: not set up

Written by `skills/setup/SKILL.md` and rewritten whenever the connection changes. When the connection is recorded and one test query has run, setup changes the status line to `Status: set up YYYY-MM-DD`.

This file says how the agent reaches the warehouse, never what it logs in with. No password, key, token or connection string with a secret in it is ever written here or anywhere else in the repo. The credential lives where the connection method keeps it (the MCP server's config, the CLI's own login, an environment variable outside the repo).

## Connection

- Method: [MCP server | vendor CLI | script | file exports]
- Name or command: [the MCP server name, the CLI command, the script path, or the export folder]
- Warehouse and SQL dialect: [the warehouse product and the dialect the agent writes]
- Projects, databases or schemas in scope: [what the agent may read]

## Running a query

[The exact steps the agent takes to run one read query and get the rows back: the tool or command, how the SQL is passed, the output format, and where results are written.]

## Estimating cost before a run

[How to get a scan size or cost estimate without running the query, such as a dry run or an explain plan, and how to read it. Or: "not available".]

## Limits

- Rows returned to the session per query: [a number]
- Scan or cost per query: [a number, or "none set"]
- When a query would exceed a limit: [ask the user first | do not run it]

## How read-only is guaranteed

- Credential scope: [the role or grants the credential holds, as the user describes them]
- Provisioned by: [the user | their admin]
- Can this credential write? [no, confirmed by the scope above | unknown | yes]

The rule in `AGENTS.md` (hard rule 1) is a prompt rule. It is not a guarantee: an agent can make a mistake, and a prompt can be overridden. The only real guarantee is a credential that cannot write. If the answer above is "unknown" or "yes", the user has been told so and this line says so.

## Last verified

[YYYY-MM-DD: the test query that ran and what it returned]
