## Outward-facing actions need confirmation

Ask the user before pushing, deploying, releasing, publishing, sending any message, or
changing a remote service (DNS, hosting, databases, stores). Approval for one action does
not carry over to the next.

**Production data.** The agent never writes to a production database or store — no update,
insert, delete, backfill, seed, migration deploy, or script run with production credentials.
It prepares the write and the owner runs it.

- A write script is dry-run by default and writes only with an explicit `--apply`. State the
  tables, fields, row count, value source and rollback. Never commit a script whose default
  run writes.
- A statement of what the data should be is a requirement, not approval. Only an explicit
  "run it" or "apply it" is.
- Reading production (SELECT through an MCP server or a read replica) needs no approval;
  anything that mutates it does.
