import packages.googler as googler

def search(s):
    opts = googler.parse_args()
    opts.keywords = s.split(" ")
    repl = googler.GooglerCmd(opts)
    repl.showing_results_for_alert(interactive=False)
    repl.fetch()

    return repl.results