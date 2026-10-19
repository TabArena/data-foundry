# Reaching the sources

Recipes for sources a plain web fetch cannot read. Why the discussions and notebooks matter is in the general
[provenance.md](../../knowledge-curation/references/provenance.md), "Competition pages are claims".

## Kaggle

Kaggle pages do not render for a plain fetch (JavaScript only, reCAPTCHA), so read them through the `kaggle` command
line. The credentials are in `~/.kaggle/`. Use kaggle 2.2.2 or newer through `uvx`, so the project venv is not
touched: the 2.2.0 in the venv gets a 403 from the discussions API.

```bash
K="uvx --from kaggle==2.2.2 kaggle -W"
$K datasets metadata <owner>/<slug> -p .          # data card text (description, licence) as JSON
$K datasets files <owner>/<slug>                  # file names, sizes, upload dates
$K datasets topics list <owner>/<slug>            # Discussion tab: id, title, author, comments, votes
$K datasets topics show <owner>/<slug> <topic_id> # one thread with all its comments
$K competitions topics list <competition>         # the same for a competition (and `topics show`)
$K kernels list --dataset <owner>/<slug> --sort-by voteCount   # Code tab, by votes
$K kernels list --user <owner>                    # the uploader's own notebooks
$K kernels pull <owner>/<kernel> -p <dir> -m      # a notebook's source and metadata
```

Ask the curator for a page only when the command line cannot reach it, and say explicitly when this check was
skipped.

## Other sources

* PubChem's literature endpoint (`sdq/sdqagent.cgi`) answers automated requests with a reCAPTCHA page after a few
  calls. Use PUG REST (`https://pubchem.ncbi.nlm.nih.gov/rest/pug/...`) and PUG-View (`.../rest/pug_view/...`) instead,
  at most 5 requests per second.
* Zindi needs a login, and some competitions were open only to participants of one country; whether an account can
  download is a question for the curator.
* SEC EDGAR refuses bulk requests without a User-Agent naming an organisation and a contact address. Ask the curator
  for both; never put a personal address into a request on your own.
* Paywalled papers: search for a free copy first, then ask the curator
  ([provenance.md](../../knowledge-curation/references/provenance.md), "Citing papers"). ResearchGate and SciSpace
  return 403 to automated fetches.
