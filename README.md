# Django modernization review workflow

This repository holds a careful, read-only review workflow for the Service Index and
Portal CMS application and infrastructure repositories. It creates dated review packs
under `analysis_reports/`; it does not scan source contents, call a model, change a
target repository, or implement recommendations.

## Why this is a review pack generator

Periodic review is useful, but a general-purpose scanner cannot promise that arbitrary
repository text is secret-free. Entropy checks also miss secrets and flag ordinary data.
The scheduled job therefore generates bounded reviewer checklists from local profiles
without opening the target repositories. A human or separately authorized review can
use the skill instructions to inspect target source read-only. Findings must avoid
source excerpts, credentials, secret-bearing values, and unnecessary infrastructure
details.

The infrastructure repositories use Ansible Vault-encrypted `passwords.yml` files for
production passwords, according to the repository owner. The review workflow must not
open or decrypt those files. It can assess secret-handling patterns from relevant
non-vault code without copying vault values or the secret-name map into reports.

The checklists identify the high-risk interfaces documented by each repository's own
`AGENTS.md`. They are not findings or approved change plans. A reviewer must verify
current source and distinguish observed evidence from recommendations. Infrastructure
code is the source of truth for each app's OS dependencies and deployment behavior.
Reviews also consider the Ubuntu LTS lifecycle and routine apt security/package updates;
a 22.04-to-24.04 move must check compatibility of the dependencies declared in that code.

All four reviewed repositories and any other context repositories are read-only to this
workflow. Skills and scheduled runs may write proposed enhancements only to this
repository's `analysis_reports/`; they never modify target code, config, docs, tests,
Git state, or submodules, even if a recommendation is approved elsewhere.

## Targets

The paths are relative to this repository's parent workspace:

- `../service-index-uv-sand/Operations_ServiceIndex_Django`
- `../Operations_ServiceIndex_Infrastructure`
- `../Operations_PortalCMS_Django`
- `../Operations_CMS_Infrastructure`

The workflow only records whether each configured root exists. It does not traverse
these roots or inspect their contents.

## Run manually

```sh
python3 audit_runner.py
```

The runner uses only the Python standard library. Each run creates one timestamped
Markdown pack per target under `analysis_reports/`. Reports contain stable repository
aliases, root availability, review questions, and the review date. They contain no
source file paths or excerpts.

## macOS scheduling

`launchd/com.access.django-upgrading-workflows.review.plist` is a LaunchAgent template
for this checkout. It requests a run every 21 days while loaded. The runner uses only
the Python standard library, so it does not need either app's `uv` environment. It
currently generates review packs only; it does not read target source or perform a
review. This is an elapsed interval, not a fixed weekday; sleep, shutdown, and user
login state can affect when a LaunchAgent actually runs. Review the absolute paths in
the plist, then install and load it manually if scheduling is desired. The plist is not
installed or loaded by this repository's code. Logs are written under
`analysis_reports/logs/`.

## Review and decision process

Read `AGENTS.md` and the matching skill in `skills/` before a review. Keep the review
read-only. Record recommendations with evidence that is safe to share and label their
status as proposed. A recommendation becomes an implementation plan only after an
authorized human explicitly decides it; record that decision in a separate approved
plan. This repository's `AGENTS.md` governs what can happen after that point and never
turns an undecided proposal into authorization.

Do not use these reports to run Terraform, Ansible, migrations, deployments, or other
operational commands. Do not commit, push, merge, tag, release, or deploy as part of a
review.
