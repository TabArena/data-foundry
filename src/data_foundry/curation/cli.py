"""Command-line entry point for the curation backlog.

Subcommands::

    data-foundry-curation serve                         # local editing dashboard
    data-foundry-curation build-site OUT_DIR            # read-only static site + guidelines (GitHub Pages)
    data-foundry-curation validate                      # check records against the vocab
    data-foundry-curation sync-notebooks [--check]      # refresh each record's notebook_path and v2_path
    data-foundry-curation export --format csv OUT.csv   # flat snapshot (csv|parquet)
    data-foundry-curation export --format gsheet --spreadsheet <id-or-url>
    data-foundry-curation dataset {list,check,build,new}   # v2 dataset folders (see data_foundry.v2.cli)
    data-foundry-curation claims {list,claim,release,renew,check,sync,import-records,init}   # live claims board

Run ``python -m data_foundry.curation.cli <subcommand> -h`` for details.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Callable
from dataclasses import asdict

from data_foundry.curation import claims, exporter
from data_foundry.curation._paths import records_dir, skills_dir
from data_foundry.curation.app import serve
from data_foundry.curation.notebooks import sync_notebook_paths, sync_v2_paths
from data_foundry.curation.record import ACCEPTED_SUGGESTIONS, load_vocabularies
from data_foundry.curation.site import build_site
from data_foundry.curation.store import load_all, load_index
from data_foundry.v2.cli import add_dataset_parser


def _cmd_serve(args: argparse.Namespace) -> int:
    serve(host=args.host, port=args.port, directory=args.records_dir)
    return 0


def _cmd_build_site(args: argparse.Namespace) -> int:
    out = build_site(args.output, args.records_dir)
    n_docs = len(json.loads((out / "docs" / "manifest.json").read_text(encoding="utf-8"))["docs"])
    print(
        f"Built read-only static site in {out}/ (index.html, guidelines.html, schema.json, records.json, "
        f"docs/manifest.json + {n_docs} guideline markdown files)."
    )
    if not n_docs:
        print(f"warning: no guideline files under {skills_dir()}; the Guidelines page links to GitHub instead.")
    return 0


def _cmd_validate(args: argparse.Namespace) -> int:
    vocab = load_vocabularies()
    records = load_all(args.records_dir)
    flagged = {r.unique_name: r.unknown_vocab_values(vocab) for r in records}
    flagged = {k: v for k, v in flagged.items() if v}
    print(f"Loaded {len(records)} records from {args.records_dir or records_dir()}.")
    if not flagged:
        print("All dropdown values are in the vocabulary. ✓")
        return 0
    print(f"{len(flagged)} record(s) carry values not in vocabularies.yaml:")
    for name, fields in list(flagged.items())[:40]:
        print(f"  {name}: " + "; ".join(f"{f}={vals}" for f, vals in fields.items()))
    if len(flagged) > 40:
        print(f"  … and {len(flagged) - 40} more")
    return 1 if args.strict else 0


def _cmd_sync_notebooks(args: argparse.Namespace) -> int:
    drift = False
    for label, sync in (("notebook_path", sync_notebook_paths), ("v2_path", sync_v2_paths)):
        changed = sync(args.records_dir, check=args.check)
        if not changed:
            print(f"Every record's {label} matches the datasets tree. ✓")
            continue
        drift = True
        verb = "would change" if args.check else "updated"
        print(f"{len(changed)} record(s) {verb} ({label}):")
        for name, (stored, resolved) in list(changed.items())[:40]:
            print(f"  {name}: {stored or '(unset)'} -> {resolved or '(unset)'}")
        if len(changed) > 40:
            print(f"  … and {len(changed) - 40} more")
    return 1 if (args.check and drift) else 0


def _cmd_export(args: argparse.Namespace) -> int:
    if args.format == "csv":
        print("Wrote", exporter.export_csv(args.output, args.records_dir))
    elif args.format == "parquet":
        print("Wrote", exporter.export_parquet(args.output, args.records_dir))
    elif args.format == "xlsx":
        print("Wrote", exporter.export_xlsx(args.output, args.records_dir))
    elif args.format == "gsheet":
        if not args.spreadsheet:
            print("error: --spreadsheet is required for --format gsheet", file=sys.stderr)
            return 2
        n = exporter.push_to_gsheet(
            args.spreadsheet,
            args.worksheet,
            service_account_file=args.service_account_file,
            directory=args.records_dir,
        )
        print(f"Pushed {n} rows to '{args.spreadsheet}' / {args.worksheet}.")
    return 0


def _print_claims(items: list[claims.Claim]) -> None:
    if not items:
        return
    width = max(len(c.name) for c in items)
    for c in items:
        until = c.expires_at[:10] + (" EXPIRED" if c.expired() else "")
        print(f"  {c.name:<{width}}  {c.holder:<8} {c.stage:<7} {c.claimed_at[:10]} -> {until:<18} {c.note}".rstrip())


def _board_age(board: claims.Board) -> str:
    age = board.age()
    return "just now" if age < 5 else f"{age:.0f} s ago" if age < 120 else f"{age / 60:.0f} min ago"


def _load_board(args: argparse.Namespace) -> claims.Board:
    if getattr(args, "offline", False):
        board = claims.cached_board()
        if board is None:
            raise claims.ClaimsError("No cached board yet; run once without --offline.")
        return board
    return claims.load(max_age=getattr(args, "max_age", 0.0))


def _cmd_claims_list(args: argparse.Namespace) -> int:
    board = _load_board(args)
    me = claims.configured_curator()
    items = sorted(board.claims.values(), key=lambda c: (c.holder, c.name))
    if args.mine:
        items = [c for c in items if c.holder == me]
    elif args.others:
        items = [c for c in items if c.holder != me]
    if args.json:
        print(json.dumps([asdict(c) | {"expired": c.expired()} for c in items], ensure_ascii=False, indent=1))
        return 0
    tip = board.tip[:8] if board.tip else "no branch yet"
    print(f"{len(items)} claim(s) on {board.remote}/{board.branch} ({tip}, fetched {_board_age(board)}):")
    _print_claims(items)
    return 0


def _stage_for(record: object, stage: str | None) -> str:
    if stage:
        return stage
    return "add" if getattr(record, "suggestion", None) in ACCEPTED_SUGGESTIONS else "triage"


def _report(outcome: claims.Outcome, verb: str) -> None:
    if outcome.changed:
        print(f"{verb} {len(outcome.changed)}: {', '.join(outcome.changed)}")
    for name, reason in outcome.skipped.items():
        print(f"skipped {name}: {reason}")


def _sync_names(args: argparse.Namespace, outcome: claims.Outcome) -> None:
    if args.no_sync or not outcome.changed:
        return
    changed = claims.mirror_to_records(outcome.board, outcome.changed, args.records_dir)
    if changed:
        print(f"records updated (claimed_by, WIP): {', '.join(changed)}")


def _cmd_claims_claim(args: argparse.Namespace) -> int:
    index = load_index(args.records_dir)
    unknown = [n for n in args.names if n not in index]
    if unknown and not args.allow_unknown:
        print(f"error: no record for {', '.join(unknown)} (create the record first, or pass --allow-unknown)")
        return 2
    groups: dict[str, list[str]] = {}
    for name in args.names:
        groups.setdefault(_stage_for(index.get(name), args.stage), []).append(name)
    complete = True
    for stage, names in groups.items():
        outcome = claims.claim(names, stage=stage, note=args.note, ttl_days=args.ttl, steal=args.steal)
        _report(outcome, f"claimed ({stage})")
        _sync_names(args, outcome)
        complete &= not outcome.skipped
    return 0 if complete else 1


def _cmd_claims_release(args: argparse.Namespace) -> int:
    outcome = claims.release(args.names, force=args.force)
    _report(outcome, "released")
    _sync_names(args, outcome)
    return 0 if not outcome.skipped else 1


def _cmd_claims_renew(args: argparse.Namespace) -> int:
    outcome = claims.renew(args.names or None, ttl_days=args.ttl)
    _report(outcome, f"renewed for {args.ttl:g} days")
    return 0 if not outcome.skipped else 1


def _cmd_claims_check(args: argparse.Namespace) -> int:
    board = _load_board(args)
    me = claims.configured_curator()
    for name in args.names:
        c = board.claims.get(name)
        if c is None:
            print(f"{name}: free")
        elif c.holder == me:
            print(f"{name}: yours ({c.describe()})")
        else:
            print(
                f"WARNING {name}: claimed by {c.describe()}" + (" - can be taken over (--steal)" if c.expired() else "")
            )
    return 0  # advisory: the check warns, it never blocks


def _cmd_claims_sync(args: argparse.Namespace) -> int:
    board = _load_board(args)
    changed = claims.mirror_to_records(board, None, args.records_dir, write=not args.check)
    if not changed:
        print("Every record's claimed_by and WIP value match the claims board. ✓")
        return 0
    verb = "would change" if args.check else "updated"
    print(f"{len(changed)} record(s) {verb} (claimed_by before -> after):")
    for name, (before, after) in changed.items():
        print(f"  {name}: {before or '(none)'} -> {after or '(none)'}")
    return 1 if args.check else 0


def _cmd_claims_import(args: argparse.Namespace) -> int:
    outcome = claims.import_from_records(args.records_dir, ttl_days=args.ttl)
    _report(outcome, "imported")
    return 0


def _cmd_claims_init(args: argparse.Namespace) -> int:
    outcome = claims.init_branch(pages_dispatch=args.pages_dispatch)
    board = outcome.board
    print(f"Claims board: {board.remote}/{board.branch} at {board.tip[:8] if board.tip else '-'}.")
    return 0


def _run_claims(func: Callable[[argparse.Namespace], int]) -> Callable[[argparse.Namespace], int]:
    """Turn a :class:`~data_foundry.curation.claims.ClaimsError` into one line on stderr and exit code 2."""

    def run(args: argparse.Namespace) -> int:
        try:
            return func(args)
        except claims.ClaimsError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 2

    return run


def _add_claims_parser(sub: argparse._SubParsersAction) -> None:
    p_claims = sub.add_parser(
        "claims", help="The live claims board: who works on which dataset (a branch of the remote, pushed directly)."
    )
    csub = p_claims.add_subparsers(dest="claims_command", required=True)

    def board_options(p: argparse.ArgumentParser) -> None:
        p.add_argument("--offline", action="store_true", help="Use the cached board of the last fetch.")
        p.add_argument("--max-age", type=float, default=0.0, help="Reuse a cached board up to this many seconds old.")

    p = csub.add_parser("list", help="Show the claims (fetches the board).")
    board_options(p)
    who = p.add_mutually_exclusive_group()
    who.add_argument("--mine", action="store_true")
    who.add_argument("--others", action="store_true")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=_run_claims(_cmd_claims_list))

    ttl = {"type": float, "default": claims.DEFAULT_TTL_DAYS, "help": "Days until the claim expires."}
    no_sync = {"action": "store_true", "help": "Leave the records' claimed_by and WIP value alone."}

    p = csub.add_parser("claim", help="Claim datasets (skips the ones someone else holds; exit 1 then).")
    p.add_argument("names", nargs="+")
    p.add_argument("--stage", choices=claims.STAGES, help="Default: add for an accepted record, else triage.")
    p.add_argument("--note", default="", help="What you are doing, shown on the board.")
    p.add_argument("--ttl", **ttl)
    p.add_argument("--steal", action="store_true", help="Take over expired claims of others.")
    p.add_argument("--allow-unknown", action="store_true", help="Claim names that have no record yet.")
    p.add_argument("--no-sync", **no_sync)
    p.set_defaults(func=_run_claims(_cmd_claims_claim))

    p = csub.add_parser("release", help="Release your claims.")
    p.add_argument("names", nargs="+")
    p.add_argument("--force", action="store_true", help="Release another curator's claim (logged).")
    p.add_argument("--no-sync", **no_sync)
    p.set_defaults(func=_run_claims(_cmd_claims_release))

    p = csub.add_parser("renew", help="Extend your claims (all, or the names given).")
    p.add_argument("names", nargs="*")
    p.add_argument("--ttl", **ttl)
    p.set_defaults(func=_run_claims(_cmd_claims_renew))

    p = csub.add_parser("check", help="Say for each dataset whether it is free, yours or someone else's (exit 0).")
    p.add_argument("names", nargs="+")
    board_options(p)
    p.set_defaults(func=_run_claims(_cmd_claims_check))

    p = csub.add_parser("sync", help="Mirror the board into the records' claimed_by and WIP values.")
    p.add_argument("--check", action="store_true", help="Report drift and exit non-zero instead of writing.")
    board_options(p)
    p.set_defaults(func=_run_claims(_cmd_claims_sync))

    p = csub.add_parser("import-records", help="Once: put the claims the records carry on the board.")
    p.add_argument("--ttl", **ttl)
    p.set_defaults(func=_run_claims(_cmd_claims_import))

    p = csub.add_parser("init", help="Create the claims branch if missing.")
    p.add_argument(
        "--pages-dispatch",
        action="store_true",
        help="Also put the workflow on the branch that rebuilds the GitHub Pages dashboard on every claim.",
    )
    p.set_defaults(func=_run_claims(_cmd_claims_init))


def build_parser() -> argparse.ArgumentParser:
    """Construct the ``data-foundry-curation`` argument parser."""
    parser = argparse.ArgumentParser(prog="data-foundry-curation", description=__doc__.splitlines()[0])
    parser.add_argument("--records-dir", default=None, help="Override the records directory.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_serve = sub.add_parser("serve", help="Run the local editing dashboard.")
    p_serve.add_argument("--host", default="127.0.0.1")
    p_serve.add_argument("--port", type=int, default=8765)
    p_serve.set_defaults(func=_cmd_serve)

    p_site = sub.add_parser("build-site", help="Compile a read-only static site (for GitHub Pages).")
    p_site.add_argument("output", help="Output directory (e.g. _site); created if missing.")
    p_site.set_defaults(func=_cmd_build_site)

    p_validate = sub.add_parser("validate", help="Check records against the vocabulary.")
    p_validate.add_argument("--strict", action="store_true", help="Exit non-zero if any value is unmapped.")
    p_validate.set_defaults(func=_cmd_validate)

    p_sync = sub.add_parser(
        "sync-notebooks", help="Refresh each record's notebook_path and v2_path from the datasets tree."
    )
    p_sync.add_argument("--check", action="store_true", help="Report drift and exit non-zero instead of writing.")
    p_sync.set_defaults(func=_cmd_sync_notebooks)

    p_export = sub.add_parser("export", help="Compile records into a flat snapshot.")
    p_export.add_argument("--format", choices=("csv", "parquet", "xlsx", "gsheet"), default="csv")
    p_export.add_argument("output", nargs="?", help="Output path (for csv/parquet).")
    p_export.add_argument("--spreadsheet", help="Sheet id/URL (for gsheet).")
    p_export.add_argument("--worksheet", default="Main")
    p_export.add_argument("--service-account-file", default=None)
    p_export.set_defaults(func=_cmd_export)

    add_dataset_parser(sub)
    _add_claims_parser(sub)

    return parser


def main(argv: list[str] | None = None) -> int:
    """Parse ``argv`` and dispatch to the selected subcommand."""
    args = build_parser().parse_args(argv)
    # Thread the top-level --records-dir into subcommands that take it.
    if not hasattr(args, "records_dir"):
        args.records_dir = None
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
