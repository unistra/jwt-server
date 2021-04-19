import os
import sys

import django
from django.test.runner import DiscoverRunner

os.environ["DJANGO_SETTINGS_MODULE"] = "jwtserver.settings.unittest"
django.setup()


"""
Run tests script
"""
test_runner = DiscoverRunner(
    pattern="test_*.py", verbosity=2, interactive=True, failfast=False
)

test_apps = ["jwtserver"]
test_apps = test_apps if len(sys.argv) <= 1 else sys.argv[1:]
failures = test_runner.run_tests(test_apps)
sys.exit(failures)
