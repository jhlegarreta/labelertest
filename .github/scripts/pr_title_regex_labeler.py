# -*- coding: utf-8 -*-
"""Labels PRs based on title. Must be run in a github action with the
pull_request event. Does not remove any label since a PR might contain multiple
commits with different prefixes and the user might have added them manually.
Adapted from scikit-learn."""
from ghapi.all import context_github
from ghapi.all import GhApi
from ghapi.all import user_repo
from ghapi.all import github_token
import re

owner, repo = user_repo()

# Retrieve the PR data
pull_request = context_github.event.pull_request
title = pull_request.title

# List of PR title and label pairs
regex_to_title_labels = [
    (r"\bDOC: \b", "type:documentation"),
    (r"\bSTYLE: \b", "duplicate")
]

# Find PR title and label matches
title_labels_to_add = [
    label for regex, label in regex_to_title_labels
    if re.search(regex, title)
]

# Add labels if matches were found
if title_labels_to_add:

    api = GhApi(owner=owner, repo=repo, token=github_token())
    api.issues.add_labels(pull_request.number, labels=title_labels_to_add)
