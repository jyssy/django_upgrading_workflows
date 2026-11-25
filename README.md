# Django enhancement review workflow

This repository contains the human-controlled review brief and report destination for
the Service Index and Portal CMS application and infrastructure repositories. The four
reviewed repositories are read-only. Review findings and proposed improvements are
written only to four matching report files under `analysis_reports/` in this repository.

Use [`skills/django-enhancement-recommendations.md`](skills/django-enhancement-recommendations.md)
as the complete review brief. Pass it to `orchestrate plan` with `--file`; the short
task prompt below only tells the planner to use that file. Do not replace the exact
report-file `--allow` paths with `--allow '**'` or another broad write pattern.

## Three-step review

These commands use absolute paths for this checkout, so they can be run from any
current directory. They use shell tools only; no Python wrapper is required.

Set a UTC timestamp for this run immediately before planning. The report filenames
identify the four repositories; the directory identifies the shared run. If a directory
with the chosen timestamp already exists, wait for the next UTC second and choose a new
timestamp. Never reuse a run directory.

```sh
review_run_id="$(date -u +%Y%m%dT%H%M%SZ)"
while [ -e "analysis_reports/$review_run_id" ]; do
  sleep 1
  review_run_id="$(date -u +%Y%m%dT%H%M%SZ)"
done
```

### 1. Create the plan

The skill file is supplied as explicit context. It defines the review dimensions and
target-specific checklists. The `--allow` list contains only the four report files this
run may write. The `--add-dir` entries are the four read-only review repositories.

```sh
review_run_id="$(date -u +%Y%m%dT%H%M%SZ)"
orchestrate plan "Load and follow skills/django-enhancement-recommendations.md as the complete review brief. Plan a strictly read-only evaluation of its four configured repositories and write only the four sanitized report files listed in the allowed paths." \
  --repo-root "/Users/jelambeadmin/Documents/access-sysops/django_upgrading_workflows" \
  --file "/Users/jelambeadmin/Documents/access-sysops/django_upgrading_workflows/skills/django-enhancement-recommendations.md" \
  --allow "analysis_reports/$review_run_id/service-index-django.md" \
  --allow "analysis_reports/$review_run_id/service-index-infrastructure.md" \
  --allow "analysis_reports/$review_run_id/portal-cms-django.md" \
  --allow "analysis_reports/$review_run_id/portal-cms-infrastructure.md" \
  --add-dir "/Users/jelambeadmin/Documents/access-sysops/service-index-uv-sand/Operations_ServiceIndex_Django" \
  --add-dir "/Users/jelambeadmin/Documents/access-sysops/Operations_ServiceIndex_Infrastructure" \
  --add-dir "/Users/jelambeadmin/Documents/access-sysops/Operations_PortalCMS_Django" \
  --add-dir "/Users/jelambeadmin/Documents/access-sysops/Operations_CMS_Infrastructure"
```

Read the full plan before continuing. Confirm it includes exactly the four read-only
repositories and the four report files for this run. Stop if anything differs. Do not
create another plan in this repository before completing steps 2 and 3.

The review covers security, Django or infrastructure best practices as applicable,
code readability and maintainability, and documentation quality, alongside each
target-specific checklist. Findings stay advisory and must use the matching skill's
format. Do not run target tests or validation commands as part of this review.

### 2. Approve the plan

Running this command is your explicit approval of the plan you just inspected:

```sh
orchestrate approve --latest --repo-root "/Users/jelambeadmin/Documents/access-sysops/django_upgrading_workflows"
```

### 3. Execute the approved plan

```sh
orchestrate execute --latest --repo-root "/Users/jelambeadmin/Documents/access-sysops/django_upgrading_workflows" --executor codex
```

The executor writes the four reports only in this repository. The orchestrator stores
plan and single-use approval metadata in private user-local state. If planning fails,
the plan scope differs, or approval/execution reports an error, stop; do not run a
later step or clean up unexpected changes automatically.

Edits to `AGENTS.md`, `README.md`, or files under `skills/` are separate workflow
maintenance tasks, not part of a periodic review. Perform them only when explicitly
requested, with their exact paths included in the maintenance task's scope. Keep target
repositories read-only during that work.
