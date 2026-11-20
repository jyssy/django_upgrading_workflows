# Service Index infrastructure read-only review skill

Use only for `../Operations_ServiceIndex_Infrastructure`. Read its effective
`AGENTS.md`, repository status, submodule status, and relevant source-of-truth files
before forming conclusions. This and all context repositories are permanently
read-only to this workflow. Write proposals only to this repository's
`analysis_reports/`; never apply recommendations to a target, regardless of plan status.
Never inspect/decrypt vault contents,
Terraform state, credentials, private keys, or generated secret-bearing files.

Production passwords are stored in Ansible Vault-encrypted `passwords.yml` files per
the repository owner. Do not open or decrypt those files. Assess secret handling only
from relevant non-vault code, without reproducing vault values or the secret-name map.

## Review sequence

1. Establish the repository root, dirty state, and submodule boundaries without
   altering them.
2. Trace relevant infrastructure behavior through inventory, variables, playbooks,
   templates, Terraform configuration, modules, and documented interfaces.
3. Use current source files as authority for targets and release wiring; do not preserve
   transient hostnames, addresses, tags, paths, or package versions in guidance.
4. Assess concrete risks and distinguish observed configuration from an inferred
   runtime effect. Do not imply a Terraform plan or deployment was validated.
5. Present bounded proposed improvements, prerequisites, and required human checks.

## Focus areas

- Terraform backend/provider boundaries, IAM least privilege, encryption, public
  exposure, security groups, secrets references, resource lifecycle, and state safety.
- Ansible inventory/limit discipline, privilege escalation, idempotence, input
  validation, secret handling, and role/submodule provenance.
- Host baseline, patching, SSH access, TLS, certificate handling, network boundaries,
  monitoring, backup/recovery, and drift visibility.
- Ubuntu release lifecycle: deployed LTS and standard-support end, host image, and
  consistency of routine apt security updates, package upgrades, and required reboots.
- Treat infrastructure code as the source of truth for app-specific OS dependencies and
  deployment behavior. Trace declared packages, package sources, runtime configuration,
  and services there; do not invent a dependency inventory from general Django knowledge.
- For a 22.04-to-24.04 proposal, check whether those declared requirements and host image
  remain compatible, then compare a parallel image/instance rebuild with an in-place
  upgrade based on the actual infrastructure design.
- Capture the release-note review, third-party repository/package impact, likely package
  removals and config prompts, backup/restore, maintenance window, reboot, and post-change
  service validation as planning items. Do not execute these actions during review.
- Application release selection and uv environment coupling with the Django app.
- Deployment repeatability, failure handling, rollback evidence, and separation of
  bootstrap from routine deployment.

## Prohibited validation and report format

Do not run Terraform, Ansible, vault, AWS, deployment, or state commands. List any
needed syntax checks or plans as pending for an authorized human; be precise about
why the command is needed without embedding secret values or full infrastructure
inventory.

Do not run `do-release-upgrade`, apt/package upgrades, reboots, or instance replacement.
Record OS migration validation and rollout steps as pending for an authorized operator.

For each item, report: **Observation**, **safe evidence reference**, **risk**,
**suggested improvement**, **confidence**, **human validation**, and **gate**. Keep
recommendations **proposed** until separately decided and recorded by an authorized
human.
