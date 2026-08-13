"""Command-line entry point for the curation backlog.

Subcommands::

    data-foundry-curation serve                         # local editing dashboard
    data-foundry-curation build-site OUT_DIR            # read-only static site (GitHub Pages)
    data-foundry-curation validate                      # check records against the vocab
    data-foundry-curation sync-notebooks [--check]      # refresh each record's notebook_path
    data-foundry-curation export --format csv OUT.csv   # flat snapshot (csv|parquet)
    data-foundry-curation export --format gsheet --spreadsheet <id-or-url>

Run ``python -m data_foundry.curation.cli <subcommand> -h`` for details.
"""

from __future__ import annotations

import argparse
import sys

from data_foundry.curation import exporter
from data_foundry.curation._paths import records_dir
from data_foundry.curation.app import serve
from data_foundry.curation.notebooks import sync_notebook_paths
from data_foundry.curation.record import load_vocabularies
from data_foundry.curation.site import build_site
from data_foundry.curation.store import load_all


def _cmd_serve(args: argparse.Namespace) -> int:
    serve(host=args.host, port=args.port, directory=args.records_dir)
    return 0


def _cmd_build_site(args: argparse.Namespace) -> int:
    out = build_site(args.output, args.records_dir)
    print(f"Built read-only static site in {out}/ (index.html, schema.json, records.json).")
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
    changed = sync_notebook_paths(args.records_dir, check=args.check)
    if not changed:
        print("Every record's notebook_path matches the datasets tree. ✓")
        return 0
    verb = "would change" if args.check else "updated"
    print(f"{len(changed)} record(s) {verb}:")
    for name, (stored, resolved) in list(changed.items())[:40]:
        print(f"  {name}: {stored or '(unset)'} -> {resolved}")
    if len(changed) > 40:
        print(f"  … and {len(changed) - 40} more")
    return 1 if args.check else 0


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

    p_sync = sub.add_parser("sync-notebooks", help="Refresh each record's notebook_path from the datasets tree.")
    p_sync.add_argument("--check", action="store_true", help="Report drift and exit non-zero instead of writing.")
    p_sync.set_defaults(func=_cmd_sync_notebooks)

    p_export = sub.add_parser("export", help="Compile records into a flat snapshot.")
    p_export.add_argument("--format", choices=("csv", "parquet", "xlsx", "gsheet"), default="csv")
    p_export.add_argument("output", nargs="?", help="Output path (for csv/parquet).")
    p_export.add_argument("--spreadsheet", help="Sheet id/URL (for gsheet).")
    p_export.add_argument("--worksheet", default="Main")
    p_export.add_argument("--service-account-file", default=None)
    p_export.set_defaults(func=_cmd_export)

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
