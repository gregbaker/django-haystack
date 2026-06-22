import os
import unittest

from django.conf import settings

from haystack.utils import log as logging


def load_tests(loader, standard_tests, pattern):
    log = logging.getLogger("haystack")
    try:
        import opensearchpy
        from opensearchpy import OpenSearch, exceptions
    except ImportError:
        log.error(
            "Skipping OpenSearch tests: 'opensearch-py' not installed."
        )
        raise unittest.SkipTest("'opensearch-py' not installed.")

    url = settings.HAYSTACK_CONNECTIONS["elasticsearch"]["URL"]
    es = OpenSearch(url)
    try:
        es.info()
    except exceptions.ConnectionError as e:
        log.error("opensearch not running on %r" % url, exc_info=True)
        raise unittest.SkipTest("opensearch not running on %r" % url, e)

    package_tests = loader.discover(
        start_dir=os.path.dirname(__file__), pattern=pattern
    )
    standard_tests.addTests(package_tests)
    return standard_tests
