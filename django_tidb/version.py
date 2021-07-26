# TiDBVersion deal with tidb's version string.
# Our tidb version string is got from ```select version();```
# it look like this:
#    5.7.25-TiDB-v5.1.0-64-gfb0eaf7b4
# or 5.7.25-TiDB-v5.2.0-alpha-385-g0f0b06ab5
class TiDBVersion:
    _version = (0, 0, 0)

    def match(self, version):
        version_list = version.split('-')
        if len(version_list) > 3:
            return False
        tidb_version_list = version_list[2].split('.')
        self._version = tuple(int(x) for x in tidb_version_list)
        return True

    @property
    def version(self):
        return self._version
