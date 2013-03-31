from verwatch.fetch import VersionFetcher
from verwatch.util import run, parse_nvr
import re


class KojiFetcher(VersionFetcher):
    name = 'koji'

    def get_version(self, pkg_name, branch):
        cmd = "koji latest-pkg \"%s\" \"%s\"" % (branch, pkg_name)
        errc, out, err = run(cmd)
        if errc:
            return {'error': err or out}
        lines = out.strip().split("\n")[2:]
        if not lines:
            return {'error': 'No results. Bad package name?'}
        if len(lines) > 1:
            return {'error': "`koji latest-pkg` returned more than one result. WAT?"}
        line = lines[0]
        cols = re.split(' +', line)
        if len(cols) == 1:
            return {'error': 'Koji output parsing failed: %s' % line}
        return parse_nvr(cols[0], pkg_name)