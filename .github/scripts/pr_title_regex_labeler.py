# -*- coding: utf-8 -*-
"""Labels PRs based on title. Must be run in a github action with the
pull_request event. Removes labels if no matches are found. Adapted from
scikit-learn."""
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
    (r"\bDOC: \b", "documentation"),
    (r"\bSTYLE: \b", "duplicate")
]

# Find PR title and label matches
title_labels_to_add = [
    label for regex, label in regex_to_title_labels
    if re.search(regex, title)
]

print(title_labels_to_add)

api = GhApi(owner=owner, repo=repo, token=github_token())

# Add labels if matches were found; otherwise remove the appropriate PR title
# labels
if title_labels_to_add:
    api.issues.add_labels(pull_request.number, labels=title_labels_to_add)
else:
    # Get the available title labels
    title_labels = [label for _, label in regex_to_title_labels]

    # Find the labels on PR
    labels_on_issue = api.issues.list_labels_on_issue(pull_request.number)

    print(labels_on_issue)

    # Get the title labels to be removed
    labels_to_remove = list(set(title_labels).intersection(labels_on_issue))

    # Remove the labels
    for label in labels_to_remove:
        labels_on_issue = api.issues.remove_label(
            pull_request.number, name=labels=label)
