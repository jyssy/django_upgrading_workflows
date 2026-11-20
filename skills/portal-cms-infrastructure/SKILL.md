# Portal CMS infrastructure read-only review skill

Use only for `../Operations_CMS_Infrastructure`. Read its effective `AGENTS.md`, full
repository status, and submodule status before inspection. Preserve all existing work.
This and all context repositories are permanently read-only to this workflow. Write
proposals only to this repository's `analysis_reports/`; never apply recommendations
to a target, regardless of plan status.

Production passwords are stored in Ansible Vault-encrypted `passwords.yml` files per
the repository owner. Do not open or decrypt those files. Assess secret handling only
from relevant non-vault code, without reproducing vault values or the secret-name map.

## Review sequence

1. Establish repository and submodule boundaries and inspect only relevant source files.
2. Trace deployment behavior across inventory, variable files, playbooks, templates,
   Terraform, and shared-role references. Treat current source as authoritative.
3. Never read/decrypt vaults, Terraform state, credentials, private keys, or generated
   files that can contain runtime secrets.
4. Distinguish code facts from inferred production effects; avoid copying hostnames,
   addresses, tags, environment values, or versions into durable recommendations.
5. Write proposed actions with precise scope, prerequisites, and human validation gates.

## Focus areas

- Terraform provider/backend, IAM, encryption, network exposure, resource lifecycle,
  secrets references, state handling, and drift controls.
- Ansible targeting, inventory safety, privilege boundaries, input checks, secret
  references, idempotence, and shared-role/submodule provenance.
- Nginx/Gunicorn hardening, PostgreSQL connectivity boundaries, TLS/certificate
  lifecycle, host patching, backups, monitoring, and recovery.
- Ubuntu LTS lifecycle: deployed release and standard-support end, host image, and
  consistency of routine apt security updates, package upgrades, and required reboots.
- Treat infrastructure code as the source of truth for app-specific OS dependencies and
  deployment behavior. Trace its declared packages, package sources, runtime config, and
  services; do not infer an unlisted app dependency inventory.
- For a 22.04-to-24.04 proposal, check compatibility of those declared requirements and
  the host image, then compare parallel instance replacement with in-place upgrade using
  the real Terraform/Ansible design and service availability.
- Include release-note and third-party package review, package removals/config prompts,
  backup/restore, maintenance window, reboot, and post-upgrade checks in planning. Do not
  execute OS upgrades or infrastructure changes during review.
- Application release selection and configuration contract with Portal CMS Django.
- Explicit separation and safe defaults for migration enablement, static collection,
  service restarts, rollout scope, and rollback behavior.

## Prohibited validation and report format

Never run Terraform, Ansible, vault, cloud, migration, deployment, certificate, or
service commands. Never run `do-release-upgrade`, apt/package upgrades, or reboots. State
required syntax checks, plans, and OS migration validation as pending for an authorized
operator. Do not expose vault-name mappings alongside values, infrastructure inventory,
secret identifiers, or raw command output.

For each item, report: **Observation**, **safe evidence reference**, **risk**,
**suggested improvement**, **confidence**, **human validation**, and **gate**. Keep
recommendations **proposed** until an authorized human explicitly decides them and
records a separate approved implementation plan.
