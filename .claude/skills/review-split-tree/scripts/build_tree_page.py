r"""Build the split-tree review page: the tree read by ``data_foundry.curation.split_tree``, the notes into issues.

Writes ``tree-data.json`` and the page (``split_tree_review.html``) into ``--out``; publish both together, the page
fetches the data file beside it. The grammar the reader takes, and how the page shows it, are in ``../SKILL.md``.

Usage::

    python build_tree_page.py --tree .claude/skills/knowledge-curation/references/split_tree.md \\
        [--draft draft.md --draft-label "Draft"] [--notes TREE_IMPROVEMENTS.md --anchors anchors.json] \\
        --commit <sha> --out <dir>
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

from markdown_it import MarkdownIt

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "src"))  # this checkout's reader, not an installed one
from data_foundry.curation import split_tree as st
from data_foundry.schema import current_tag

MD = MarkdownIt("commonmark").enable("table")
REPO = "https://github.com/TabArena/data-foundry/blob/main/.claude/skills/knowledge-curation/references/"
PAGE = Path(__file__).resolve().parent.parent / "assets" / "tree_page.html"
SHORT_LABELS = {
    "Expanding science catalogue": "Catalogue",
    "Experimental results": "Experimental",
    "Clinical study": "Clinical",
    "Database snapshot": "Snapshot",
    "Dated event log": "Event log",
    "Panel data": "Panel",
    "Order and windows step": "Order step",
}
CHECKS = {
    "windows": ("the windows check", "windows"),
    "gap": ("the gap rules", "gap"),
    "unit": ("the unit check", "unit"),
    "groups": ("the enough-groups check", "groups"),
    "sametime": ("the same-time check", "same time"),
    "stationary": ("the stationary-relation test", "stationarity"),
}
"""The named checks of "Checks the steps cite": how the tree names each, and the chip's short label."""
GUIDE = ("How to walk it", "Who answers", "Words", "Checks the steps cite")
"""The text sections the page's guide tab shows, in order."""
TABLE = re.compile(r"(?m)^\|.*\|\n\|[-| ]+\|\n(?:^\|.*\|\n?)+")
TURN = re.compile(r"(?m)^\*\*(Lennart|Andrej|Myunghwan|Answer|Resolved|Deferred) \(([^)]*)\):\*\*[ \t]*(.*)$")


def inline(text: str) -> str:
    """Render one line of markdown, joining wrapped lines."""
    return MD.renderInline(re.sub(r"\s*\n\s*", " ", text.strip()))


def block(text: str) -> str:
    """Render markdown blocks; links to sibling reference files point to the repository."""
    html = MD.render(text)
    return re.sub(r'href="([a-z_]+\.md)(#[^"]*)?"', lambda m: f'href="{REPO}{m[1]}{m[2] or ""}" target="_blank"', html)


def plain(text: str) -> str:
    """The text without markdown emphasis, code ticks or the annotation's ``_( )_``."""
    text = re.sub(r"\s+", " ", text).replace("**", "").replace("`", "")
    return re.sub(r"(?<![A-Za-z0-9])_\(|\)_(?![A-Za-z0-9])", "", text).strip()


def slug(text: str) -> str:
    """A hash-safe view key."""
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def checks_in(text: str) -> list[str]:
    """The named checks a question's annotation or a leaf's body cites."""
    low = text.lower()
    return [key for key, (name, _) in CHECKS.items() if name in low]


def leaf_checks(leaf: st.Leaf) -> list[str]:
    """The checks a leaf takes: the gap rules under a temporal leaf, the same-time check under a fill-in leaf."""
    found = ["gap"] if leaf.family == "Temporal" else []
    found += ["sametime"] if leaf.tag and current_tag(leaf.tag) == "RetrospectiveFillIn" else []
    return found + [k for k in checks_in(leaf.body) if k not in found]


def checks_data(text: str) -> dict:
    """Each named check's bullet of "Checks the steps cite", rendered."""
    out = {}
    for key, (name, short) in CHECKS.items():
        m = re.search(r"(?ms)^\* \*\*" + re.escape(name) + r"\.?\*\*(.*?)(?=^\* \*\*|\Z)", text, re.I)
        out[key] = {"label": name[0].upper() + name[1:], "short": short, "html": block(m[1].strip()) if m else ""}
    return out


class PageNodes:
    """Turns one parsed tree into the page's nodes; a draft's ids carry a prefix so both trees share one id space."""

    def __init__(self, tree: st.SplitTree, nodes: dict, which: str, prefix: str = ""):
        """Keep the tree, the node store, the tree's name (``today`` or ``draft``) and the id prefix."""
        self.tree, self.nodes, self.which, self.prefix = tree, nodes, which, prefix
        self.roots = {name: prefix + s.root.id for name, s in tree.sections.items() if s.root is not None}
        self.codes = {name: prefix + s.root.id.split(".")[0] for name, s in tree.sections.items() if s.root is not None}

    def add(self, node: dict) -> str:
        """Store a node; ids are unique across both trees."""
        if node["id"] in self.nodes:
            raise ValueError(f"duplicate node id {node['id']}")
        node.setdefault("children", [])
        self.nodes[node["id"]] = node
        return node["id"]

    def base(self, nid: str, section: str, answer: str | None) -> dict:
        """The fields every node has: id, section, tree and the answer that leads to it."""
        return {
            "id": nid,
            "sec": self.codes[section],
            "tree": self.which,
            "answer": inline(answer) if answer else None,
            "answerPlain": plain(answer) if answer else None,
        }

    def walk(self, node: st.Node, answer: str | None, link_id: str) -> str:
        """Add a node and everything below it; a link gets ``link_id`` (its question's id and the answer's number)."""
        if isinstance(node, st.Question):
            nid = self.prefix + node.id
            q = {
                **self.base(nid, node.section, answer),
                "type": "q",
                "html": inline(node.text),
                "plain": plain(node.text),
                "reads": inline(node.reads),
                "qkind": "" if node.kind == "person decides" else node.kind,
                "person": node.kind == "person decides",
                "checks": checks_in(node.reads),
            }
            self.add(q)
            q["children"] = [self.walk(child, label, f"{nid}.{k}") for k, (label, child) in enumerate(node.answers, 1)]
            return nid
        if isinstance(node, st.Leaf):
            rest = node.title.partition(" · ")[2]
            rest = rest.replace(node.tag, f"`{node.tag}`", 1) if node.tag else rest
            return self.add(
                {
                    **self.base(self.prefix + node.id, node.section, answer),
                    "type": "leaf",
                    "family": node.family,
                    "html": inline(rest),
                    "title": node.title,
                    "plain": node.title,
                    "body": inline(node.body) if node.body else "",
                    "examples": node.examples,
                    "unreached": not node.reached,
                    "checks": leaf_checks(node),
                }
            )
        target = self.tree.section_named(node.target)
        return self.add(
            {
                **self.base(link_id, node.section, answer),
                "type": "ref",
                "target": self.roots[target.name],
                "plain": (node.target + " " + plain(node.note)).strip(),
                "examples": node.here,
                "note": inline(node.note) if node.note else "",
            }
        )

    def build(self, views: list, intros: dict) -> list[str]:
        """Add every section, its view and its intro, then the overview root; returns the roots to link parents from."""
        sections = [s for s in self.tree.sections.values() if s.root is not None]
        for s in sections:
            self.walk(s.root, s.name if s.kind == "type" else None, "")
            if s.intro:
                intros[self.roots[s.name]] = inline(" ".join(s.intro))
            label = SHORT_LABELS.get(s.name, s.name)
            key = ("draft-" if self.prefix else "") + slug(label)
            views.append(
                {"key": key, "tree": self.which, "label": label, "root": self.roots[s.name], "step": s.kind == "step"}
            )
        root = self.prefix + "ROOT"
        question = "Which data collection type does the record name?"
        self.add(
            {
                "id": root,
                "sec": root,
                "tree": self.which,
                "answer": None,
                "answerPlain": None,
                "type": "q",
                "html": question,
                "plain": question,
                "reads": "the record's collection type; each type is walked from its own first question",
                "qkind": "data and documentation",
                "person": False,
                "checks": [],
                "children": [self.roots[s.name] for s in sections if s.kind == "type"],
            }
        )
        overview = {"key": ("draft-" if self.prefix else "") + "overview", "label": "Overview", "root": root}
        views.insert(len(views) - len(sections), {**overview, "tree": self.which, "step": False})
        return [root] + [self.roots[s.name] for s in sections if s.kind == "step"]


def intro_of(text: str) -> str:
    """The text before the first ``## `` heading, without the title."""
    return re.sub(r"(?m)^# .*\n", "", re.split(r"(?m)^## ", text)[0]).strip()


def parse_question(text: str, key: str, title: str) -> dict:
    """An issue-shaped block: bullets with bold leads and one options table.

    The table's columns are ``| | Option | What it does | Pro | Con |``, as on the dataset review page.
    """
    options = []
    tm = TABLE.search(text)
    if tm:
        for row in tm[0].strip().split("\n")[2:]:
            k, name, what, pro, con = [c.strip() for c in row.strip().strip("|").split("|")][:5]
            options.append(
                {
                    "key": k,
                    "name": inline(name.replace("(implemented)", "").strip()),
                    "implemented": "(implemented)" in name,
                    "what": inline(what),
                    "pro": [inline(x) for x in pro.split("; ") if x.strip()],
                    "con": [inline(x) for x in con.split("; ") if x.strip()],
                }
            )
        text = text[: tm.start()] + text[tm.end() :]
    leads = {
        m[1].strip(): re.sub(r"(?m)^  ", "", m[2]).strip()
        for m in re.finditer(r"(?ms)^- \*\*(.+?):\*\*(.*?)(?=^- \*\*|\Z)", text)
    }
    rec = leads.pop("Recommendation", "")
    decision = ""
    dm = re.search(r"\*\*Decision:\*\*\s*(.+)$", rec, re.S)
    if dm:
        decision, rec = inline(dm[1]), rec[: dm.start()].strip()
    rk = re.match(r"\(?([A-Za-z])\)?(?=[.,;\s])", rec)
    leads.pop("Options", None)
    problem = leads.pop("Problem", "")
    return {
        "key": key,
        "title": inline(title) if title else "",
        "problem": block(problem),
        "details": [{"lead": k, "html": block(v)} for k, v in leads.items()],
        "options": options,
        "rec": rk[1] if rk else None,
        "recHtml": inline(rec),
        "decision": decision,
    }


def parse_issue(head: str, body: str) -> dict | None:
    """One ``### <ID>. <title>`` issue: its first question, the turns below it, its state and the active question."""
    hm = re.match(r"([A-Z]+\d+)\. (.+)", head.strip())
    if not hm:
        return None
    meta, _, rest = body.strip().partition("\n\n")
    merges = re.search(r"\*\*Merges:\*\*(.+?)(?:\*\*Status:\*\*|$)", meta, re.S)
    status = re.search(r"\*\*Status:\*\*\s*(.+)$", meta, re.S)
    found = list(TURN.finditer(rest))
    questions = [parse_question(rest[: found[0].start()] if found else rest, "q1", "")]
    turns = []
    for i, m in enumerate(found):
        more = rest[m.end() : found[i + 1].start() if i + 1 < len(found) else len(rest)].strip()
        kind = {"Answer": "ai", "Resolved": "resolved", "Deferred": "deferred"}.get(m[1], "person")
        turn = {"kind": kind, "who": m[1], "meta": m[2], "question": None, "html": ""}
        if kind == "ai" and TABLE.search(more):
            turn["question"] = f"q{len(questions) + 1}"
            questions.append(parse_question(more, turn["question"], m[3]))
        else:
            text = (m[3] + "\n" + more).strip()
            turn["html"] = block(text) if text and text != "(no note)" else ""
        turns.append(turn)
    status_text = status[1].strip().rstrip(".") if status else "open"
    last = turns[-1] if turns else None
    if last and last["kind"] == "resolved":
        state, active = "decided", "q1"
    elif last and last["kind"] == "ai" and last["question"]:
        state, active = "yourturn", last["question"]
    elif status_text.lower().startswith("with "):
        state, active = "elsewhere", None
    else:
        state, active = "open", questions[-1]["key"]
    merges_text = merges[1].strip() if merges else ""
    return {
        "id": hm[1],
        "title": hm[2].strip(),
        "merges": expand_ids(merges_text),
        "mergesText": inline(merges_text),
        "status": status_text,
        "questions": questions,
        "turns": turns,
        "state": state,
        "active": active,
    }


def parse_issues(notes: str, heading: str) -> tuple[str, list[dict], dict]:
    """The issues under the ``## <heading>`` section, its intro, and the evidence findings of the notes file."""
    sections = {p.partition("\n")[0].strip(): p.partition("\n")[2] for p in re.split(r"(?m)^## ", notes)[1:]}
    key = next((k for k in sections if k.startswith(heading)), None)
    if key is None:
        return "", [], {}
    chunks = re.split(r"(?m)^### ", sections[key])
    issues = [i for c in chunks[1:] if (i := parse_issue(*c.partition("\n")[::2]))]
    evidence = {}
    for k, body in sections.items():
        rm = re.match(r"(R\d+)\. (.+)", k)
        if rm:
            evidence[rm[1]] = {"id": rm[1], "title": rm[2], "tag": "", "html": block(body)}
    for para in re.split(r"\n\s*\n", notes):
        m = re.match(r"\*\*([A-Z]\d+)\. (.+?)\*\*\s*(\((verified|suspected)[^)]*\)\.?)?\s*(.*)$", para.strip(), re.S)
        if m and not m[1].startswith("T"):
            evidence[m[1]] = {"id": m[1], "title": m[2].rstrip("."), "tag": m[4] or "", "html": block(m[5])}
    return block(chunks[0]), issues, evidence


def expand_ids(text: str) -> list[str]:
    """``A1 to A3, R2`` → ``[A1, A2, A3, R2]``."""
    out = []
    for a, b in re.findall(r"\b([A-Z]\d+)(?: to ([A-Z]\d+))?\b", text):
        out += [f"{a[0]}{i}" for i in range(int(a[1:]), int(b[1:]) + 1)] if b else [a]
    return list(dict.fromkeys(out))


def select(nodes: dict, sel: dict) -> list[str]:
    """The node ids one anchor selector picks: ``id``, or ``sec``/``type``/``contains``/``title`` (tree ``today``)."""
    hits = []
    for n in nodes.values():
        if n["tree"] != sel.get("tree", "today") or ("id" in sel and n["id"] != sel["id"]):
            continue
        if ("sec" in sel and n["sec"] != sel["sec"]) or ("type" in sel and n["type"] != sel["type"]):
            continue
        hay = n["plain"] + " " + " ".join(n.get("examples", []))
        if ("contains" in sel and sel["contains"] not in hay) or ("title" in sel and n.get("title") != sel["title"]):
            continue
        hits.append(n["id"])
    if not hits:
        raise ValueError(f"anchor selector matches no node: {sel}")
    return hits


def attach_departures(nodes: dict, tree: st.SplitTree) -> list[dict]:
    """The departures table: each row put on its leaf, by the leaf's ID."""
    departures = []
    for row in tree.departures:
        leaf = nodes.get(row["leaf"])
        if leaf is None or leaf["type"] != "leaf":
            raise ValueError(f"departure {row['definition']}: no leaf {row['leaf']!r}")
        leaf.setdefault("departures", []).append(row["definition"])
        why = f"{row.get('reason', '')} ({row.get('reviewer', '')}, {row.get('date', '')})"
        departures.append(
            {
                "name": row["definition"],
                "leaf": leaf["title"],
                "leafId": leaf["id"],
                "ships": inline(row["ships"]),
                "why": inline(why),
            }
        )
    return departures


def tree_stats(nodes: dict, n_issues: int) -> dict:
    """Questions, leaves and unreached leaves per tree, and the number of issues."""
    stats = {}
    for tree in ("today", "draft"):
        qs = [n for n in nodes.values() if n["tree"] == tree and n["type"] == "q" and not n["id"].endswith("ROOT")]
        lv = [n for n in nodes.values() if n["tree"] == tree and n["type"] == "leaf"]
        stats[tree] = {"questions": len(qs), "leaves": len(lv), "unreached": sum(n["unreached"] for n in lv)}
    stats["points"] = n_issues
    return stats


def link_parents(nodes: dict, roots: list[str]) -> None:
    """Set each node's parent."""

    def walk(nid: str, parent: str | None = None) -> None:
        if parent is not None:
            nodes[nid].setdefault("parent", parent)
        for c in nodes[nid]["children"]:
            walk(c, nid)

    for r in roots:
        walk(r)


def arguments() -> argparse.Namespace:
    """The command line."""
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--tree", type=Path, required=True, help="split_tree.md")
    ap.add_argument("--draft", type=Path, help="a draft of a restructured tree, in the same grammar")
    ap.add_argument("--draft-label", default="Draft", help="the draft's name on the page")
    ap.add_argument("--notes", type=Path, help="the review notes with the issues")
    ap.add_argument("--issues-heading", default="Review points", help="the ## heading the issues sit under")
    ap.add_argument("--anchors", type=Path, help="JSON: issue id -> selectors of the nodes it concerns")
    ap.add_argument("--commit", default="", help="the commit of the tree, shown in the header")
    ap.add_argument("--out", type=Path, required=True, help="folder for tree-data.json and the page")
    return ap.parse_args()


def main() -> None:
    """Parse the inputs, check them, and write the data file and the page."""
    args = arguments()
    nodes, views, intros = {}, [], {}
    text = args.tree.read_text(encoding="utf-8")
    tree = st.parse(text)
    roots = PageNodes(tree, nodes, "today").build(views, intros)
    draft_intro = ""
    if args.draft:
        draft_text = args.draft.read_text(encoding="utf-8")
        draft_intro = intro_of(draft_text)
        roots += PageNodes(st.parse(draft_text), nodes, "draft", prefix="D-").build(views, intros)
    link_parents(nodes, roots)
    departures = attach_departures(nodes, tree)

    causes, issues, evidence = "", [], {}
    if args.notes:
        causes, issues, evidence = parse_issues(args.notes.read_text(encoding="utf-8"), args.issues_heading)
    anchors = json.loads(args.anchors.read_text(encoding="utf-8")) if args.anchors else {}
    for it in issues:
        it["anchors"] = list(dict.fromkeys(i for sel in anchors.get(it["id"], []) for i in select(nodes, sel)))
        for i in it["anchors"]:
            nodes[i].setdefault("points", []).append(it["id"])

    stats = tree_stats(nodes, len(issues))
    dep = tree.sections.get(st.DEPARTURES)
    data = {
        "commit": args.commit,
        "stats": stats,
        "views": views,
        "nodes": nodes,
        "sectionIntros": intros,
        "guide": {
            "intro": block(intro_of(text)),
            "sections": [{"title": g, "html": block(tree.sections[g].text)} for g in GUIDE if g in tree.sections],
        },
        "checks": checks_data(
            tree.sections["Checks the steps cite"].text if "Checks the steps cite" in tree.sections else ""
        ),
        "draftIntro": block(draft_intro),
        "departures": departures,
        "depIntro": inline(dep.text.split("\n\n")[0]) if dep else "",
        "causes": causes,
        "issues": issues,
        "evidence": evidence,
        "labels": {"draft": args.draft_label},
    }
    args.out.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    (args.out / "tree-data.json").write_text(payload, encoding="utf-8")
    shutil.copyfile(PAGE, args.out / "split_tree_review.html")
    print(f"{len(nodes)} nodes; today {stats['today']}; draft {stats['draft']}; {len(issues)} issues")
    for it in issues:
        keys = [q["key"] for q in it["questions"]]
        print(f"  {it['id']}: {it['state']}, {len(it['anchors'])} nodes, questions {keys}")


if __name__ == "__main__":
    main()
