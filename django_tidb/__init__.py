# Check Django compatibility before other imports which may fail if the
# wrong version of Django is installed.
import pkg_resources

from .utils import check_django_compatability

__version__ = pkg_resources.get_distribution("django-tidb").version

check_django_compatability()
