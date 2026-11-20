# Read-only review pack: Service Index Infrastructure

Generated: 2026-11-19 20:34 UTC
Configured root available: yes

This pack contains review questions, not findings or an approved change plan.
Use the matching skill and the target repository's current guidance. Inspect
relevant non-secret source read-only. Do not include source excerpts or secrets.

## Review questions

- [ ] Do Terraform provider/backend/resource patterns follow current least-privilege, encryption, network exposure, and state-handling practices?
- [ ] Do Ansible roles, inventory boundaries, privilege escalation, idempotency, and secret references follow current safe patterns?
- [ ] Are deployment inputs and application release selection traceable to their sources of truth without hardcoded environment details?
- [ ] What Ubuntu LTS release and support window do the managed hosts use, and are standard apt security updates, routine package upgrades, and required reboots handled consistently?
- [ ] Is Ubuntu 24.04 still the right destination, or should the currently supported LTS target also be compared for support runway and compatibility?
- [ ] If considering Ubuntu 22.04 to 24.04, do the infrastructure-declared app dependencies, packages, services, configuration, and host image remain compatible; what release-note or package-source changes need attention?
- [ ] Does the infrastructure code support a parallel host/image rebuild or an in-place release upgrade, and has the chosen approach included backup/restore, maintenance window, reboot, rollback, and post-upgrade service checks in a human-reviewed plan?
- [ ] Are host hardening, patching, TLS, backups, monitoring, and recovery documented with evidence?
- [ ] Which recommendations require Terraform or Ansible validation that the reviewer is prohibited from running?

## Reviewer notes

Record only sanitized observations, safe evidence references, and proposed
improvements. Label each item proposed. An authorized human must decide
whether to create a separate implementation plan.
