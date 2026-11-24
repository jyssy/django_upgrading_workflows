# Review workflow instructions

## Purpose and authority

This repository provides a human-controlled, read-only review workflow for the Service
Index and Portal CMS application and infrastructure repositories. Its output is
advisory. A report, skill, or recommendation is not authorization to edit a target
repository or perform an operational action.

The workspace-level instructions in `../AGENTS.md` apply. Preserve all tracked,
untracked, submodule, and nested-repository work. Never inspect or emit secret material.

## Absolute target write boundary

The four reviewed repositories are permanently read-only to this workflow:

- `../service-index-uv-sand/Operations_ServiceIndex_Django`
- `../Operations_ServiceIndex_Infrastructure`
- `../Operations_PortalCMS_Django`
- `../Operations_CMS_Infrastructure`

No skill, runner, reviewer, or follow-up under this workflow may modify any file or Git
state in those repositories, including source, tests, configuration, documentation,
generated files, branches, or submodules. This remains true even if a report or a
separately approved plan recommends a change. The skills may only write proposed
enhancements to `analysis_reports/` in this repository. They must never apply a
recommendation to a reviewed repository.

Other repositories consulted for context, including the outer Service Index uv
development environment and Portal local harness, are read-only as well. The only
write destination for a periodic review run is this repository's `analysis_reports/`.
Edits to this workflow's own skills/configuration are separate maintenance work and
require an explicit user request.

## Decision gate

Recommendations remain proposals. A human may decide whether to pursue one in a
separate workflow, but this review system never edits the reviewed repositories or
turns a report into authorization. Do not infer a decision from a report, issue, prior
plan, or silence. Do not make a recommendation look decided by placing it in this file.

## Read-only review boundaries

- A human-led review may inspect relevant non-secret source files read-only and must
  first read the target repository's effective `AGENTS.md`. It must not write any file
  or change Git state in a reviewed or context repository.
- Use the three-step, script-free orchestrator procedure in `README.md`. The plan must
  include `skills/django-enhancement-recommendations.md` as explicit `--file` context,
  bind only the four configured repositories as read-only `--add-dir` contexts, and
  allow writes only to the four exact report files under one run-specific
  `analysis_reports/` directory. Never use repository-wide write patterns such as
  `--allow '**'`. The human must inspect the plan and its complete scope before running
  `orchestrate approve --latest`, then run `orchestrate execute --latest` immediately
  afterward without creating another plan in this repository. Any scope mismatch or
  failed plan/approval step must stop the workflow.
- The orchestrator CLI's Codex write-path validation is post-execution, not an
  operating-system restriction to the allowed report files. If execution reports an
  out-of-scope change, do not automatically clean or revert it; stop and ask the human
  to inspect the workflow diff. Its Git-visible check may not detect ignored files.
- The orchestrator CLI stores plan and approval records in private user-local state
  outside its target repository. These are approval metadata, not review reports; do
  not copy them into this repository. Review reports may be written only under
  `analysis_reports/`.
- Never read vault, password, credential, private-key, environment, Terraform-state,
  generated secret-bearing configuration, or other secret-bearing files. Never run a
  secret scanner over target contents as a workaround.
- Per the repository owner's clarification, production passwords are stored in
  Ansible Vault-encrypted `passwords.yml` files in the infrastructure repositories.
  Treat the encrypted files as prohibited context too: do not open, decrypt, index, or
  copy their contents. A review may assess the general secret-handling approach from
  relevant non-vault code, but must not reproduce vault values or the secret-name map.
- Reports may include only repository aliases, availability, dates, checklist text,
  safe evidence references, and sanitized recommendations. Do not include source
  excerpts, secret values, raw configuration, full hostnames, or raw command output.
- Review outputs and suggestions may be written only under this repository's
  `analysis_reports/`; never write reports into a target or context repository.
- Do not run Terraform, Ansible, vault, migration, deployment, service, or cloud
  commands. Do not commit, push, merge, tag, release, deploy, restart services, or
  access production data without separate explicit authorization.

## Review scope and run naming

- Across the four configured targets, assess security, framework-specific best
  practices, code readability and maintainability, and documentation quality, in
  addition to the applicable target-specific checklist. Apply each dimension only
  where relevant to that repository; separate verified observations, risks, and
  proposed improvements using the matching skill's finding format.
- Use one new directory per review run: `analysis_reports/<UTC-timestamp>/`. Use a
  UTC timestamp in `YYYYMMDDTHHMMSSZ` form. Put exactly one Markdown report per target
  inside it, named for the repository alias, such as `service-index-django.md` or
  `portal-cms-infrastructure.md`. If that timestamp directory already exists, choose
  a later timestamp; never reuse or overwrite a prior run directory.
- A normal review plan allows only those four exact report paths. A requested edit to
  workflow instructions or skills is separate maintenance work: scope its exact
  workflow-repository paths explicitly and do not combine it with a review run unless
  a new plan expressly includes both scopes. Target repositories remain read-only.

## Target-specific review skills

Use the matching skill file as the review checklist:

- `skills/service-index-django/SKILL.md`
- `skills/service-index-infrastructure/SKILL.md`
- `skills/portal-cms-django/SKILL.md`
- `skills/portal-cms-infrastructure/SKILL.md`

Each review must distinguish verified observations, risks, and proposed improvements.
Avoid copying current version numbers, tags, addresses, hostnames, or environment names
into durable guidance; re-check the target repository's sources of truth.

## Checks and handoff

Run only checks explicitly permitted by the applicable repository guidance. This
workflow does not validate target projects. Before handoff, re-read the diff and report
changed files, checks run and results, checks not run, failures, assumptions, and
unresolved security or operational risks.
