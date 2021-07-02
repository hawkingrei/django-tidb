# Check Django compatibility before other imports which may fail if the
# wrong version of Django is installed.
from .utils import check_django_compatability

import pkg_resources

__version__ = pkg_resources.get_distribution("django-tidb").version

check_django_compatability()