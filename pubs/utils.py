# Function here may belong somewhere else. In the mean time...

from . import color
from . import pretty

def resolve_citekey(repo, citekey, ui=None, exit_on_fail=True):
    """Check that a citekey exists, or autocompletes it if not ambiguous."""
    # FIXME. Make me optionally non ui interactive/exiting
    citekeys = repo.citekeys_from_prefix(citekey)
    if len(citekeys) == 0:
        if ui is not None:
            ui.error("No citekey named or beginning with '{}'".format(color.dye_out(citekey, 'citekey')))
            if exit_on_fail:
                ui.exit()
    elif len(citekeys) == 1:
        if citekeys[0] != citekey:
            if ui is not None:
                ui.warning("Provided citekey '{}' has been autocompleted into '{}'".format(color.dye_out(citekey, 'citekey'), color.dye_out(citekeys[0], 'citekey')))
            citekey = citekeys[0]
    elif citekey not in citekeys:
        if ui is not None:
            citekeys = sorted(citekeys)
            ui.error("Be more specific; Provided citekey '{}' matches multiples citekeys:".format(
                     citekey))
            for c in citekeys:
                p = repo.pull_paper(c)
                ui.message(u'    {}'.format(pretty.paper_oneliner(p)))
            if exit_on_fail:
                ui.exit()
    return citekey


def resolve_citekey_list(repo, citekeys, ui=None, exit_on_fail=True):
    shutdown = False
    keys = []
    for key in citekeys:
        try:
            keys.append(resolve_citekey(repo, key, ui, exit_on_fail))
        except SystemExit:
            shutdown = exit_on_fail

    if shutdown and ui is not None:
        ui.exit()
    else:
        return keys
