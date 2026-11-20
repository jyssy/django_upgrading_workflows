# Read-only review pack: Portal CMS Infrastructure

Generated: 2026-11-19 20:34 UTC
Configured root available: yes

This pack contains review questions, not findings or an approved change plan.
Use the matching skill and the target repository's current guidance. Inspect
relevant non-secret source read-only. Do not include source excerpts or secrets.

## Review questions

- [ ] Do Terraform resources and backends use least privilege, encryption, narrow network exposure, and safe state practices?
- [ ] Do Ansible deployment tasks use safe secret references, explicit targeting, idempotent configuration, and bounded privilege?
- [ ] What Ubuntu LTS release and support window do the managed hosts use, and are standard apt security updates, routine package upgrades, and required reboots handled consistently?
- [ ] Is Ubuntu 24.04 still the right destination, or should the currently supported LTS target also be compared for support runway and compatibility?
- [ ] If considering Ubuntu 22.04 to 24.04, do the infrastructure-declared app dependencies, packages, services, configuration, and host image remain compatible; what release-note or package-source changes need attention?
- [ ] Does the infrastructure code support a parallel host/image rebuild or an in-place release upgrade, and has the chosen approach included backup/restore, maintenance window, reboot, rollback, and post-upgrade service checks in a human-reviewed plan?
- [ ] Are migration enablement, static collection, and service restart behavior clearly separated and controlled?
- [ ] Are Nginx, Gunicorn, PostgreSQL connectivity, TLS/certificate handling, patching, backups, and monitoring aligned with current practices?
- [ ] Which follow-up validations are explicitly forbidden to the reviewer and must remain pending for an authorized operator?

## Reviewer notes

Record only sanitized observations, safe evidence references, and proposed
improvements. Label each item proposed. An authorized human must decide
whether to create a separate implementation plan.
