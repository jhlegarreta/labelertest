# -*- coding: utf-8 -*-
"""Labels PRs based on title. Must be run in a github action with the
pull_request event. Does not remove any label since a PR might contain multiple
commits with different prefixes and the user might have added them manually.
Adapted from scikit-learn."""
from ghapi.all import context_github
from ghapi.all import GhApi
from ghapi.all import user_repo
from ghapi.all import github_token

from requests import HTTPError

import os
import re
import yaml

owner, repo = user_repo()

# Retrieve the PR data
pull_request = context_github.event.pull_request
title = pull_request.title

print("Title: {}".format(title))
print("PR number: {}".format(pull_request.number))

filebasename = 'title_to_labels_regex.yml'
file = os.path.join(os.path.dirname(
        os.path.dirname(os.path.realpath(__file__))), filebasename)

with open(file) as f:
    conf = yaml.safe_load(f.read())

word_boundary = r"\b"
regex_to_title_labels = [(word_boundary + key + word_boundary, val)
             for key, val in conf.items()]

# List of PR title and label pairs
#regex_to_title_labels = [
#    (r"\bDOC: \b", "type:documentation"),
#    (r"\bSTYLE: \b", "duplicate")
#]

# Find PR title and label matches
title_labels_to_add = [
    label for regex, label in regex_to_title_labels
    if re.search(regex, title)
]

# Add labels if matches were found
if title_labels_to_add:
    print("Labels to add: {}".format(title_labels_to_add))

    api = GhApi(owner=owner, repo=repo, token=github_token())
    try:
        api.issues.add_labels(
            accept="application/vnd.github.v3+json",
            issue_number=pull_request.number, labels=title_labels_to_add)
    except Exception as e:
        print("owner: {}".format(owner))
        print("repo: {}".format(repo))
        print("Exception info: {}".format(e))
        print("api: {}".format(api))
