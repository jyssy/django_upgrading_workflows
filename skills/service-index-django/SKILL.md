# Service Index Django application review skill

Use this skill for read-only review of `../service-index-uv-sand/Operations_ServiceIndex_Django`.
The application repository is nested inside the uv-managed development repository.
Keep the app source, the outer local-development environment, and
`../Operations_ServiceIndex_Infrastructure` as separate repositories and sources of
truth. They are always read-only to this workflow. Write proposed improvements only to
`analysis_reports/` in this repository; never apply them to a reviewed repository,
regardless of approval or plan status.

## Before reviewing

1. Read the effective instructions for the outer development repository, the nested
   application repository, and the paired infrastructure repository. Inspect Git status
   at each relevant root and preserve all existing work.
2. Treat the app repository as the authority for application behavior and tests. Treat
   the outer `pyproject.toml`/lock as the local development environment, not proof of
   what production runs.
3. For deployed runtime and dependency questions, read current infrastructure sources of
   truth: inventory selection, application variables/tasks, selected uv project and
   lock, and relevant service/config templates. Derive the active release and selected
   uv configuration from those files at review time. Do not copy current tags, host
   labels, paths, package versions, or addresses into durable guidance.
4. Never read local runtime configuration, `.env` files, databases, logs, vault/password
   files, Terraform state, credentials, or generated secret-bearing configuration. The
   infrastructure repositories use Ansible Vault-encrypted `passwords.yml`; do not
   open or decrypt it. Never run a secret scanner over repository contents.

## Application map and contracts

- The Django project and `services` app live under
  `Operations_ServiceIndex_Django/Operations_ServiceIndex_Django/`. Read its current
  README, root URLs/settings code, `services/models.py`, serializers, views, URLs,
  signals, admin, and tests as the concern requires.
- The core domain is a service inventory: services, hosts, sites, availability/support,
  staff contacts, links, edit locks, operational events, per-host event status, and
  activity logs. Review foreign-key deletion behavior, validation, audit history,
  personal contact data, and operational host metadata together.
- The `services/api/hosts/` endpoint is a read-only JSON interface using HTTP Basic
  authentication and viewer/editor group authorization. Its serializer includes host
  inventory fields and named primary/backup contacts. Treat both authorization and
  response shape/data exposure as a security and consumer contract; never include real
  host, address, or contact values in a report. The nested service serializer currently
  follows all model fields, so assess whether an explicit response-field allowlist is
  needed to prevent future model additions from silently expanding the API.
- The app also has browser views, admin, export/listing/PDF paths, and event workflows.
  Trace route method, login/group checks, object scope, CSRF behavior, and output
  encoding for every proposed change; do not assume API protections automatically
  cover browser views or exports.
- Authentication includes allauth/CILogon and the external `access_django_user_admin`
  package. Signup policy and login routes are explicit behavior. Treat changes to
  provider policy, groups, the external package interface, or API authentication as
  high-risk producer/consumer changes.
- Treat schema and migration changes as high risk. The workspace guidance identifies
  per-schema migration behavior; establish the current migration procedure and data
  boundaries from current non-secret source before proposing any schema work.

## Review focus

- Check that authorization remains fail-closed across anonymous, authenticated,
  inactive, viewer, and editor users, especially for the Basic-auth API, data exports,
  logs, staff information, and state-changing event/service views.
- Trace every route to its actual decorators and method checks. In particular, inspect
  legacy login/logout and lock-cleanup handlers, commented-out auth decorators, and any
  username-based privilege shortcuts; prove whether each helper is reachable or dead
  before describing its risk.
- Review form/model validation for host names/IP-address fields, staff/contact data,
  editable URLs, arbitrary ordering/filter inputs, and cross-record references.
- Check audit logs and login/request logging for untrusted proxy headers, sensitive
  values, retention, access controls, and safe error handling.
- Review ORM query counts and pagination for inventory, host, contact, event, and log
  views; assess export size and serialization as the dataset grows.
- Review schema and data migrations against the multi-schema contract, rollback limits,
  and consumer compatibility. Do not infer production data shape from source alone.
- Compare dependency changes with both the local uv environment and the exact
  infrastructure-selected uv project/lock. The infrastructure code defines the
  deployed app-specific dependencies and runtime services; general OS maintenance is
  handled through normal apt security/basic upgrades.
- Keep deployment behavior in the infrastructure repository. Do not move Ansible,
  Terraform, systemd, AWS, or release-selection logic into this app.

## Tests and prohibited actions

The current app tests include signup-policy checks and API authentication/authorization,
response-shape, inactive-user, and method checks. Trace affected tests and gaps, but do
not run them as part of a review unless a separate task explicitly requests permitted
checks with safe configuration.

Never run `manage.py` commands, migrations, database tools, app services, deployment,
Ansible, Terraform, vault, cloud, or production data operations during this review.
The target instructions prohibit running checks with ambiguous config or config that
could reach production database/OAuth. If a later approved task needs validation, use
only the commands and deliberately nonproduction configuration permitted by the
current target `AGENTS.md`; report all skipped checks clearly.

## Findings format

For each finding, include **Observation**, **safe evidence reference**, **risk**,
**proposed improvement**, **confidence**, **affected contract**, and **human gate**.
Use source paths/line numbers only when safe. Do not copy runtime values, contact data,
host metadata, credentials, tokens, raw logs, or config contents. Clearly separate
verified code behavior from inference and mark every recommendation **proposed** until
an authorized human records a separate implementation plan.
