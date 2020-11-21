from github import Github

import os
import json
import subprocess
import pprint
import time


def print_error(output_str: str):
    print(output_str)
    exit(1)

def make_manual_api_call(url: str):
    checks_api_call = subprocess.run(
        'curl -H "Accept: application/vnd.github.v3+json" {}'.format(url),
        capture_output=True,
        shell=True
    )

    checks_string = checks_api_call.stdout.decode("utf-8")

    return json.loads(checks_string)

REPOSITORY_SLUG = os.getenv("GITHUB_REPOSITORY")
event_name = os.getenv("GITHUB_EVENT_NAME")
event_path = os.getenv("GITHUB_EVENT_PATH")
event_ref = os.getenv("GITHUB_REF")
event_sha = os.getenv("GITHUB_SHA")
print("REPOSITORY_SLUG: {}".format(REPOSITORY_SLUG))
print("event_name: {}".format(event_name))
print("event_path: {}".format(event_path))
print("event_ref: {}".format(event_ref))
print("event_sha: {}".format(event_sha))
print("")
print("")

if not "BOT_GITHUB_TOKEN" in os.environ or os.getenv("BOT_GITHUB_TOKEN") == "":
    print("Env variable BOT_GITHUB_TOKEN not available. This is probably an external pull request.")
    exit(0)

g = Github(os.getenv("BOT_GITHUB_TOKEN"))
repo = g.get_repo(REPOSITORY_SLUG)

if not event_name in ["workflow_run", "pull_request_review", "check_suite", "schedule"]:
    print_error("Unexpected event_name which triggered this workflow run: {}".format(event_name))

event_data = {}
with open(os.getenv("GITHUB_EVENT_PATH"), mode="r") as payload:
    event_data = json.load(payload)
    # pprint.pprint(event_data)


pull_request_numbers = []
if event_name == "workflow_run" or event_name == "check_suite":
    if len(event_data[event_name]["pull_requests"]) != 1:
        print("This {} is either connected to several pull requests or none. Nothing to merge.".format(event_name))
        exit(0)
    pull_request_numbers.append(event_data[event_name]["pull_requests"][0]["number"])
elif event_name == "pull_request_review":
    pull_request_numbers.append(event_data["pull_request"]["number"])
elif event_name == "schedule":
    last_updated_prs = make_manual_api_call("https://api.github.com/repos/{}/pulls?state=open&sort=updated&direction=desc&per_page=10".format(REPOSITORY_SLUG))
    for pr in last_updated_prs:
        pull_request_numbers.append(pr["number"])


print("pull_request_numbers:")
print(pull_request_numbers)

if len(pull_request_numbers) == 0:
    print_error("No pull_requests_numbers detected")

for pull_request_number in pull_request_numbers:
    # Workaround the problem that GitHub is only calculating "mergeable" on request
    # and only keeps the value for a short time
    repo.get_pull(pull_request_number)

time.sleep(2)

for pull_request_number in pull_request_numbers:
    print("")
    print("Evaluting PR # {}".format(pull_request_number))
    print("")
    pr = repo.get_pull(pull_request_number)

    if not pr.mergeable:
        print("According to GitHub the pull request is not mergeable right now. Are there conflicts?")
        continue

    pr_latest_commit = pr.head.sha

    print("latest commit in pull request: {}".format(pr_latest_commit))

    reviews = pr.get_reviews()
    collaborators = repo.get_collaborators()

    print("all reviews on latest commit from collaborators:")

    print("")

    changes_requested = False
    approvals_on_latest_commit = 0
    approvals_required = 1

    latest_review_by_collaborators = {}
    for review in reviews:
        if review.user in collaborators:
            # We only care about APPROVED, CHANGES_REQUESTED and DISMISSED
            if review.state != "COMMENTED":
                latest_review_by_collaborators[review.user.login] = review

    for _, review in latest_review_by_collaborators.items():
        # CHANGES_REQUESTED should be always dismissed or changed to an APPROVAL
        # Even if the CHANGES_REQUESTED do not happen on the latest commit,
        # they should be respected
        if review.state == "CHANGES_REQUESTED":
            changes_requested = True

        if review.commit_id == pr_latest_commit:
            print("{}: {} on commit: {}".format(review.user, review.state, review.commit_id))

            if review.state == "APPROVED":
                approvals_on_latest_commit = approvals_on_latest_commit + 1

    print("")
    print("")
    print("approvals_on_latest_commit: {}".format(approvals_on_latest_commit))
    print("approvals_required: {}".format(approvals_required))
    print("")
    print("")

    if changes_requested:
        print("The pull request contains at least one request for changes. This has to be addressed first.")
        continue

    if approvals_on_latest_commit < approvals_required:
        print("The amount of required approvals are not reached yet.")
        continue

    print("Required approvals reached and no request for changes. Checking latest commit status...")
    print("")

    # There is a difference in commit statuses and checks
    # Our CI runs are all qualifing as checks
    # Since PyGithub is not yet supporting checks, we have to use something else here
    # https://github.com/PyGithub/PyGithub/issues/1621
    # TODO: Use only PyGithub once it supports checks

    checks = {}

    # Read up to 1000 checks
    for page in range(1, 10):
        checks_on_page = make_manual_api_call(
            'https://api.github.com/repos/{}/commits/{}/check-runs?per_page=100&page={}'.format(REPOSITORY_SLUG, pr_latest_commit, page))
        checks.update(checks_on_page)


    checks_successful = 0
    # All checks have to be successful except Auto Merge checks
    checks_successful_required = checks["total_count"]
    checks_not_completed = 0
    for check in checks["check_runs"]:
        if check["name"] != "Auto Merge Pull Requests":
            if check["status"] == "completed" and check["conclusion"] == "success":
                checks_successful = checks_successful + 1
            else:
                print("The check {} is {}".format(check["name"], check["status"]))
                if check["status"] != "completed":
                    checks_not_completed = checks_not_completed + 1
        else:
            print("The check {} with id {} is {}".format(check["name"], check["id"], check["status"]))
            checks_successful_required = checks_successful_required - 1

    if checks_not_completed != 0:
        print("There are still checks running.")
        continue

    print("checks_successful: {}".format(checks_successful))
    print("checks_successful_required: {}".format(checks_successful_required))
    print("")

    if checks_successful < checks_successful_required:
        print("Not all checks have passed. More work required 🙂")
        continue

    print("")
    print("All checks passed. Merging...")

    pr.merge(merge_method="squash")
