#!/usr/bin/env python3

# Copyright 2020 Google LLC.

# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

import math
import os
import random
import time

with open("django_test_apps.txt", "r") as file:
    all_apps = file.read().split("\n")

print("test apps: ", all_apps)

if not all_apps:
    exit()


os.system(
    """DJANGO_TEST_APPS="{apps}" bash ./django_test_suite.sh""".format(
        apps=" ".join(all_apps)
    )
)
