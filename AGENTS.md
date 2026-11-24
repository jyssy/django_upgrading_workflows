# Review workflow instructions

## Purpose and authority

This repository creates read-only review packs for the Service Index and Portal CMS
application and infrastructure repositories. Its output is advisory. A report,
checklist, skill, or recommendation is not authorization to edit a target repository
or perform an operational action.

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

- `audit_runner.py` is a checklist-only runner. It may check only whether configured
  repository roots exist; it must not traverse them, read source/configuration, invoke
  Git, invoke a model, or execute repository commands.
- A human-led review may inspect relevant non-secret source files read-only and must
  first read the target repository's effective `AGENTS.md`. It must not write any file
  or change Git state in a reviewed or context repository.
- `manual_review.py` is the manually started, approval-gated entry point for a
  human-led review. It must use `orchestrate plan` with only the four configured
  repositories as approval-bound read-only `--add-dir` contexts, and allow writes only
  beneath the run-specific `analysis_reports/` directory in this repository. It must
  display the plan and complete scope, then require an exact uppercase `Y` before
  creating a single-use approval and launching Codex. Any scope mismatch, missing
  repository, missing CLI, or failed planning/approval step must stop before review
  execution. Do not use repository-wide write patterns such as `--allow '**'`; allow
  only the four exact report-file paths in that run directory.
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

Run only checks explicitly permitted by the applicable repository guidance. The review
pack generator does not validate target projects. Before handing off any change in this
repository, re-read the diff and report changed files, checks run and results, checks
not run, failures, assumptions, and unresolved security or operational risks.
