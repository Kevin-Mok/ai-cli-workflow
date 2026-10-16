# Local code-review-graph checks

The graph helper checks an installed code-review-graph runtime against disposable source. It verifies caller lookup and incremental updates, or the restricted stdio MCP tool surface, without opening a model session.

The reviewed integration targets code-review-graph 2.3.9. Existing local executables and optional client declarations are preserved during migration; the original installer and MCP templates remain in the private recovery archive. The public transfer adds the reusable smoke helper rather than replacing private client configuration. Do not run upstream setup commands to reconstruct that configuration automatically.

From the checkout root, no sudo, with an existing installation:

```sh
python3 scripts/smoke_code_review_graph.py --mode cli --plain
python3 scripts/smoke_code_review_graph.py --mode mcp --plain
```

`--binary PATH` selects an isolated installation. CLI mode builds a two-function fixture, finds its caller, then verifies an incremental update. MCP mode initializes the server, checks exactly four query tools, queries callers/stats/impact, and confirms an unbuilt graph stays unbuilt. `--details` shows raw diagnostics. The helper strips inherited graph and Git routing variables before creating disposable state.

Graph queries can create local SQLite metadata and are not a filesystem sandbox. Graphs can be stale or incomplete; selected context and an empty caller result do not prove correctness or test coverage. Keep databases/exports outside Git and retain normal model/client approval requirements.
