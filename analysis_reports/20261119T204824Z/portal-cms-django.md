# Portal CMS Django review

Review date: 2026-11-19 20:48 UTC  
Scope: read-only review of relevant Portal CMS Django and infrastructure source.  
Status: advisory proposals only; no target-repository changes were made.

## Review boundaries applied

- Read relevant application and infrastructure source and effective repository guidance only.
- Did not open encrypted `passwords.yml` files or other credential-bearing material. The owner identifies encrypted Ansible Vault password files as the only credentials in these repositories; they remain prohibited review context.
- Did not run application commands, tests, infrastructure commands, migrations, or production operations.
- Infrastructure source is the authority for app-specific runtime dependencies and deployment shape. Ubuntu host review is limited to requirements evidenced there; otherwise the baseline assumed is standard apt-managed security and basic upgrades.
- Findings below are recommendations for human consideration, not approved implementation work.

## Findings and proposed enhancements

### 1. Verify identity claims before linking social login to an existing account

**Priority:** High, conditional impact  
**Confidence:** High for observed code path; provider assurance is unverified

The social-login signal selects the first email address on the provider response and links a new social login to an existing local user with that address. The inspected handler does not itself check that the selected address is verified. The settings also disable email-verification requirements for the configured account flows. Whether this creates an account-takeover risk depends on CILogon’s guarantees for the email claim and the exact allauth/provider response behavior; those guarantees were not established in this review.

**Evidence:** `portal/signals.py`, around lines 90–135; `settings.py`, around lines 699–702.

**Proposal:** Confirm the provider’s documented and configured assurance for email claims. Require a verified, trusted identity claim before automatic linking, or replace implicit linking with a secure explicit account-linking flow. Add tests for verified, unverified, absent, and duplicate email claims, including a provider response with multiple addresses.

**Decision impact:** Authentication and account recovery behavior changes. Confirm provider configuration and user-support policy before selecting an implementation.

### 2. Preserve stable, collision-resistant external identity

**Priority:** Medium  
**Confidence:** Medium

The username signal derives a local username from only the portion of the CILogon subject before an `@` separator. If distinct provider identities share that portion, the local username may collide or cease to represent the provider’s stable identity.

**Evidence:** `portal/signals.py`, around lines 46–66.

**Proposal:** Verify uniqueness assumptions for the subject values the provider actually supplies. Prefer retaining the complete stable issuer/subject pair in the social-account identity and avoid deriving a globally unique local username from a potentially shared handle. Add collision and subject-change tests before any migration or account remapping.

**Decision impact:** Could affect usernames, account lookup, and existing social-account mappings; any remapping requires an explicit migration and compatibility plan.

### 3. Review authentication log data and forwarded-address trust

**Priority:** Medium  
**Confidence:** High that the fields are logged; operational exposure/retention unverified

Authentication signal handlers log provider subject, user/email details, and request address. These are personal identifiers. Forwarded-address data should be trusted only when requests pass through configured trusted proxies; log retention and access controls were not verified.

**Evidence:** `portal/signals.py`, around lines 66–73 and 125–137.

**Proposal:** Minimize or pseudonymize identity fields in routine logs, avoid recording full email/subject unless justified, and confirm trusted-proxy handling, log access, and retention. Keep security-relevant event auditing while reducing unnecessary personal data.

**Decision impact:** Logging changes should preserve incident-response needs and comply with the organization’s retention requirements.

### 4. Confirm whether social token persistence is required

**Priority:** Low to medium  
**Confidence:** Medium; usage not established

The settings enable social account token storage. The reviewed application Python source did not show direct token consumption, while infrastructure-selected dependencies include token-auth integration. The review did not verify library behavior or the runtime integration path, so necessity and exposure are unresolved.

**Evidence:** `settings.py`, around line 703; infrastructure-selected application dependency manifest; no direct token use identified in reviewed app Python files.

**Proposal:** Trace the integration’s actual token use and storage lifecycle; if token persistence is not required, propose disabling it and removing unused integration dependencies through a separately approved change. If required, document access controls, retention, and rotation expectations. Do not change this setting based on this finding alone.

**Decision impact:** Could affect authentication integrations and stored credential material; validate behavior against the current supported library documentation and deployment wiring before deciding.

### 5. Keep health and data-sync behavior observable without leaking details or mutating unexpectedly

**Priority:** Low  
**Confidence:** High for reviewed code/documentation behavior

The health endpoint performs a database readiness check and returns a generic failure response. The resource sync path validates upstream data and uses transactional updates, while its dry-run mode still calls external APIs; stale-group pruning can delete local projection rows. Existing integration scripts may mutate whichever database the runtime configuration selects.

**Evidence:** `portal` health view and `dev_documentation/CURRENT_STATE.md`; resource sync service and management-command implementation; `tests/README.md` describes integration scripts and configuration requirements.

**Proposal:** Keep health responses generic and add operational documentation that distinguishes liveness/readiness and the external dependencies involved. Make dry-run semantics explicit in command help and logs, and require deliberate non-production configuration before any sync/test execution. Review stale-group pruning with its data owner and add preview/impact reporting before enabling it operationally.

**Decision impact:** Sync and pruning changes can affect local membership/resource projections. This review did not run any command or inspect runtime configuration.

## Infrastructure and Ubuntu context

Use infrastructure source as the authority for app-specific dependencies, runtime configuration wiring, and deployment behavior. The reviewed documentation identifies loopback restriction for health access, but this was not checked against a live host. No additional OS-level application requirement was established by this source-only pass. The report therefore does not propose Ubuntu-specific package changes beyond the standard apt-managed security and basic-upgrade baseline supplied by the owner. Reassess if infrastructure source introduces a concrete OS dependency or Ubuntu 24 compatibility change.

## Checks and limitations

No tests, app management commands, dependency installation, Terraform, Ansible, vault, database, or service commands were run. Findings have not been verified against live CILogon configuration, runtime settings, external consumers, proxy behavior, log retention, or deployed dependencies. Any library-specific token-storage mechanics need confirmation from current official documentation before implementation. All recommendations require explicit human selection and a separate implementation plan before any change.
