# -*- coding: utf-8 -*-
"""Labels issue based on title. Must be run in a github action with the
issue event. Does not remove any label since a PR might contain multiple
commits with different prefixes and the user might have added them manually.
Adapted from scikit-learn."""
from ghapi.all import context_github
from ghapi.all import GhApi
from ghapi.all import user_repo
from ghapi.all import github_token
import os
import re
import yaml

owner, repo = user_repo()

# Retrieve the issue data
issue = context_github.event.issue
title = issue.title

print(title)
print(issue.number)

filebasename = 'title_to_labels_regex.yml'
file = os.path.join(os.path.dirname(
        os.path.dirname(os.path.realpath(__file__))), filebasename)

with open(file) as f:
    conf = yaml.safe_load(f.read())

word_boundary = r"\b"
regex_to_title_labels = [(word_boundary + key + word_boundary, val)
             for key, val in conf.items()]

# List of issue title and label pairs
#regex_to_title_labels = [
#    (r"\bWONTFIX: \b", "type:wontfix"),
#    (r"\bSTYLE: \b", "duplicate")
#]

# Find PR title and label matches
title_labels_to_add = [
    label for regex, label in regex_to_title_labels
    if re.search(regex, title)
]

print(title_labels_to_add)

# Add labels if matches were found
if title_labels_to_add:

    api = GhApi(owner=owner, repo=repo, token=github_token())
    api.issues.add_labels(issue.number, labels=title_labels_to_add)
