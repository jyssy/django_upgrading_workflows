# Django Enhancement Recommendations

## Purpose

Use this brief to plan and run a read-only technical and security review of the four
configured Service Index and Portal CMS repositories. The four target repositories are
inspection-only. During a review run, the only permitted project writes are four
sanitized recommendation reports inside this workflow repository, one per target,
under a new run-specific directory in `analysis_reports/`. The orchestrator may also
store plan and single-use approval metadata in its private user-local state; those are
control records, not project files or review reports. Separately requested workflow
maintenance is governed by the scope in “Workflow maintenance” below.

## Review scope

Review exactly these repositories as read-only contexts:

- `service-index-django`: `../service-index-uv-sand/Operations_ServiceIndex_Django`
- `service-index-infrastructure`: `../Operations_ServiceIndex_Infrastructure`
- `portal-cms-django`: `../Operations_PortalCMS_Django`
- `portal-cms-infrastructure`: `../Operations_CMS_Infrastructure`

Before inspecting a target, read its effective `AGENTS.md`. Then use its matching
target-specific checklist under `skills/`. Inspect relevant non-secret source only.
Compare application behavior with its related infrastructure where useful.

Across the four targets, assess the following dimensions where they apply, in addition
to the target-specific checklist:

- **Security:** authentication and authorization, input handling, safe configuration
  and secret references, data exposure, and the security boundaries described by the
  target's instructions.
- **Framework and platform practices:** appropriate Django patterns for application
  repositories; maintainable, repeatable, and least-privilege practices for
  infrastructure repositories. Use current repository sources rather than generic
  assumptions.
- **Readability and maintainability:** clear organization, focused responsibilities,
  understandable names and error paths, and avoidable duplication or complexity.
- **Documentation quality:** whether relevant code, project, and operational
  documentation is clear and consistent with verified source behavior.

Report concrete observations with safe evidence references. Separate verified facts,
risks, and **proposed** improvements using the matching target skill's finding format.
Do not infer noncompliance solely from style preference or the absence of a particular
tool, test, or documentation format.

Never read, display, decrypt, index, copy, or transmit vault, password, credential,
private-key, environment, Terraform-state, generated secret-bearing, or other
secret-bearing files. Do not run a secret scanner over target contents. Do not run
tests, linters, static analysis, Terraform, Ansible, migrations, deployment, service,
cloud, or production-data commands. Do not change target files or Git state, and do not
write anywhere else in the workspace.

## Report outputs

Write exactly these four files under one new directory for the run. Use the UTC run
timestamp as the directory name in `YYYYMMDDTHHMMSSZ` form; use the repository alias
as each report filename. If that directory already exists, select a later timestamp
and do not overwrite it:

- `analysis_reports/<UTC-timestamp>/service-index-django.md`
- `analysis_reports/<UTC-timestamp>/service-index-infrastructure.md`
- `analysis_reports/<UTC-timestamp>/portal-cms-django.md`
- `analysis_reports/<UTC-timestamp>/portal-cms-infrastructure.md`

Each report must separate verified observations, risks, and proposed improvements.
Use sanitized recommendations and safe repository-relative evidence references. Do not
include source excerpts, secret values or identifiers, raw configuration, full
hostnames, raw command output, or copied version pins. Recommendations are proposals,
not decisions or authorization to implement changes.

## Manual orchestrator sequence

These commands use absolute paths for this checkout and can be run from any current
directory. Use exact report-file paths in the `--allow` options. Do not use
`--allow '**'` or any repository-wide write pattern.

First choose a new UTC timestamp and build the read-only plan. This passes this file as
explicit planning context with `--file` and binds only the four target repositories as
read-only contexts:

```sh
review_run_id="$(date -u +%Y%m%dT%H%M%SZ)"
while [ -e "analysis_reports/$review_run_id" ]; do
  sleep 1
  review_run_id="$(date -u +%Y%m%dT%H%M%SZ)"
done

orchestrate plan "Conduct a strictly read-only technical and security review of exactly the four repositories in the attached Django Enhancement Recommendations skill. Read each target's AGENTS.md first and use its matching checklist. Write only four sanitized reports in this workflow repository's analysis_reports run directory; do not modify any reviewed repository or any other path. Label improvements as proposals." \
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

Inspect the full plan before continuing. Confirm it names exactly the four read-only
repositories and the four report files above. Stop if the plan scope differs. Running
the approve command below is the explicit human approval. Run the two commands
immediately and do not create another plan in this repository between them:

```sh
orchestrate approve --latest --repo-root "/Users/jelambeadmin/Documents/access-sysops/django_upgrading_workflows"
```

```sh
orchestrate execute --latest --repo-root "/Users/jelambeadmin/Documents/access-sysops/django_upgrading_workflows" --executor codex
```

The approval is single-use. If approval or execution fails, stop and review the CLI
message and workflow diff. Do not clean up or revert unexpected changes automatically.

## Workflow maintenance

Changes to this brief, other workflow skills, `AGENTS.md`, or `README.md` are separate
maintenance tasks. Make them only when explicitly requested and scope the exact
workflow-repository paths for that task. A normal review plan must continue to allow
writes only to its four report files; target repositories remain read-only in either
workflow.
