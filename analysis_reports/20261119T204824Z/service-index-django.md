# Service Index Django review

Review date: 2026-11-19 20:48 UTC  
Scope: read-only review of relevant Service Index Django and infrastructure source.  
Status: advisory proposals only; no target-repository changes were made.

## Review boundaries applied

- Read relevant application and infrastructure source and effective repository guidance only.
- Did not open encrypted `passwords.yml` files or other credential-bearing material. The owner identifies encrypted Ansible Vault password files as the only credentials in these repositories; they remain prohibited review context.
- Did not run application commands, tests, infrastructure commands, migrations, or production operations.
- Infrastructure source is the authority for app-specific runtime dependencies and deployment shape. Ubuntu host review is limited to requirements evidenced there; otherwise the baseline assumed is standard apt-managed security and basic upgrades.
- Findings below are recommendations for human consideration, not approved implementation work.

## Findings and proposed enhancements

### 1. Enforce the deprecation privilege in the server-side view

**Priority:** High  
**Confidence:** High

The service update view requires editor access, but its deprecation branch accepts a submitted `deprecated` field without enforcing the stronger privilege represented by the UI helper. That helper only controls presentation, so an editor able to submit a crafted request may reach the state change even when the interface hides it.

**Evidence:** `services/views.py`, around lines 173–175 and 346–353; `services/views.py`, around lines 59–60 and template use around line 366.

**Proposal:** Add a server-side authorization check to the deprecation transition, using a named permission or group policy rather than a UI-only username flag. Add view tests for ordinary editors, authorized privileged users, and missing/forged form fields. Preserve the existing edit workflow for unrelated service fields.

**Decision impact:** Changes the authorization contract for deprecation and may require identifying the intended privileged role before implementation.

### 2. Harden legacy login and edit-lock cleanup endpoints

**Priority:** Medium  
**Confidence:** High

The legacy login endpoint has no active authentication decorator or method restriction and records the request identity/address. The lock-cleanup endpoint is also not restricted to authenticated POST requests, while deleting a lock is a state change. Forwarded client-address headers may be supplied by an untrusted caller unless the proxy boundary is configured and trusted.

**Evidence:** `services/urls.py`, around lines 22 and 31; `services/views.py`, around lines 894–911.

**Proposal:** Decide whether the legacy login route is still needed; otherwise retire it through an explicit compatibility plan. Require authentication and POST with CSRF protection for lock cleanup. Derive client addresses only through trusted proxy configuration and minimize stored request metadata. Add tests for anonymous access, GET behavior, CSRF, and lock ownership.

**Decision impact:** May affect existing login/logout links or integrations and should be checked against current route consumers before changing.

### 3. Make the host API response schema explicit

**Priority:** Medium  
**Confidence:** High

The service serializer uses all model fields, while the host serializer includes operational identity and contact attributes. Adding a model field can therefore expand the service API automatically; the host payload also includes sensitive operational data whose exposure should be intentional and contract-tested.

**Evidence:** `services/serializers.py`, around lines 5–40; `services/views.py`, around lines 1085–1092.

**Proposal:** Replace implicit all-field serialization with explicit field allowlists, document the authenticated group contract and intended host/contact fields, and add response-schema tests that fail when a model change expands the API. Review API consumers before narrowing any existing payload.

**Decision impact:** API consumers may depend on current fields; inventory those consumers and stage any schema change through an approved plan.

### 4. Check local dependency reproducibility against infrastructure-selected environment

**Priority:** Low  
**Confidence:** Medium

The local root project appears not to declare a user-admin package that the application root URL configuration imports. The infrastructure-selected environment appears to account for that dependency separately. This could make a fresh local sync incomplete even if the deployed environment resolves it.

**Evidence:** Local `pyproject.toml`, around lines 7–16; application `urls.py`, around line 17; selected environment is defined by infrastructure source. Transient environment names and version pins are intentionally omitted.

**Proposal:** Document the supported developer setup and ensure a clean local environment installs the same application-level dependency set as the infrastructure-selected environment, while keeping deployment-specific pins sourced from infrastructure. Add a permitted local environment check only after an implementation plan authorizes it.

**Decision impact:** Dependency ownership may span the outer development harness and infrastructure manifests; do not modify either target repository under this review workflow.

### 5. Validate ordering fields to avoid avoidable server errors

**Priority:** Low  
**Confidence:** Medium

The hosts listing route accepts a word-like ordering parameter and passes it into ORM ordering. Unsupported field names can produce an error instead of a controlled response.

**Evidence:** `services/urls.py`, around line 14; `services/views.py`, around line 582.

**Proposal:** Restrict ordering to a fixed allowlist and return a safe default or validation response for unsupported values; add tests for allowed and invalid inputs.

## Infrastructure and Ubuntu context

Use the infrastructure repository as the source of truth for deployed application dependencies and runtime wiring. No additional OS-level application requirement was established by this source-only pass. The report therefore does not propose Ubuntu-specific package changes beyond the standard apt-managed security and basic-upgrade baseline supplied by the owner. Reassess this if infrastructure source introduces a concrete OS dependency or Ubuntu 24 compatibility change.

## Checks and limitations

No tests, app management commands, dependency installation, Terraform, Ansible, vault, database, or service commands were run. Findings are based on inspected source and have not been confirmed against a live deployment, runtime configuration, proxy settings, or external API consumers. All recommendations require explicit human selection and a separate implementation plan before any change.
