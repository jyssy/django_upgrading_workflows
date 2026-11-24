#!/usr/bin/env python3
"""Run one approval-gated, read-only review of all configured repositories."""

from __future__ import annotations

from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from typing import Any

from audit_runner import ALLOWED_ROOTS, ROOT, load_profiles


OUTPUT_ROOT = ROOT / "analysis_reports"
DEFAULT_STATE_ROOT = Path.home() / ".orchestrator" / "workflow"
PLAN_ID_RE = re.compile(r"Plan ID:\s*([a-f0-9]{64})")
ANSI_RE = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")

CONSTRAINTS = (
    "Treat effective AGENTS.md guidance as authoritative. Review only the four "
    "approval-bound read-only repositories listed in the task. Read each target's "
    "effective AGENTS.md before relevant source; if none exists, note that and "
    "follow the matching workflow skill. Never read, display, index, or transmit "
    "vault, password, credential, private-key, environment, Terraform-state, "
    "generated secret-bearing, or other secret-bearing files. Never run a secret "
    "scanner over target contents. Never modify target files or Git state. Do not "
    "run Terraform, Ansible, vault, migration, deployment, service, or cloud "
    "commands. Do not run tests, linters, or static-analysis commands for this "
    "read-only review. Do not commit, push, merge, tag, release, deploy, restart "
    "services, or access production data. Write exactly one sanitized Markdown report per "
    "repository under the approved analysis_reports run directory. Reports must "
    "distinguish verified observations, risks, and proposed improvements; include "
    "only safe evidence references and sanitized recommendations, with no source "
    "excerpts, secret values, raw configuration, full hostnames, or raw command "
    "output. Recommendations remain proposals."
)


def _resolve_targets() -> dict[str, Path]:
    profiles = load_profiles()
    targets: dict[str, Path] = {}
    for profile in profiles:
        repo_id = str(profile["id"])
        candidate = ROOT.parent / ALLOWED_ROOTS[repo_id]
        if any(part.is_symlink() for part in (candidate, *candidate.parents)):
            raise RuntimeError(f"Refusing symlinked repository path: {repo_id}")
        if not candidate.is_dir():
            raise RuntimeError(f"Configured repository is unavailable: {repo_id}")
        targets[repo_id] = candidate.resolve()

    if set(targets) != set(ALLOWED_ROOTS):
        raise RuntimeError("Review profiles do not match the configured repository allowlist")
    return targets


def _state_root(targets: dict[str, Path]) -> Path:
    configured = os.environ.get("ORCHESTRATOR_STATE_DIR")
    if configured:
        state_root = Path(configured).expanduser()
        if not state_root.is_absolute():
            state_root = ROOT / state_root
    else:
        state_root = DEFAULT_STATE_ROOT
    state_root = state_root.resolve()
    protected_roots = {ROOT.resolve(), ROOT.parent.resolve(), *targets.values()}
    for protected in protected_roots:
        overlaps = (
            state_root == protected
            or state_root.is_relative_to(protected)
            or protected.is_relative_to(state_root)
        )
        if overlaps:
            raise RuntimeError(
                "Orchestrator state must be private user-local storage outside this "
                "workflow and all reviewed repositories"
            )
    return state_root


def _run(command: list[str], *, capture: bool) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHON_DOTENV_DISABLED"] = "1"
    env["NO_COLOR"] = "1"
    return subprocess.run(
        command,
        cwd=ROOT,
        env=env,
        check=False,
        text=True,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.STDOUT if capture else None,
    )


def _print_captured(result: subprocess.CompletedProcess[str]) -> None:
    if result.stdout:
        print(result.stdout, end="" if result.stdout.endswith("\n") else "\n")


def _safe_failure(output: str | None) -> str:
    normalized = ANSI_RE.sub("", output or "").lower()
    if "temporarily unavailable" in normalized:
        return "the orchestrator's model provider is temporarily unavailable"
    return "the orchestrator command failed; see its exit status"


def _run_id() -> str:
    value = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    run_directory = OUTPUT_ROOT / value
    if run_directory.exists() or run_directory.is_symlink():
        raise RuntimeError("Review output directory already exists; refusing to overwrite")
    return value


def _review_task(run_id: str) -> str:
    aliases = ", ".join(ALLOWED_ROOTS)
    report_names = ", ".join(f"{repo_id}.md" for repo_id in ALLOWED_ROOTS)
    return f"""Conduct a thorough, read-only technical and security review of the four
approval-bound application and infrastructure repositories: {aliases}.

This is an executor-led review: Codex must inspect relevant non-secret source and
infrastructure files itself. That read-only inspection is required and permitted;
do not defer it to a human or list it as a prohibited check. No target files are to
be changed, and no code fixes are to be implemented.

For each repository, read its effective AGENTS.md first, then use both the matching
questions in review_profiles.json and the detailed checklist under the workflow
repository's skills/ directory. If a target has no AGENTS.md, record that fact and
proceed under the workflow AGENTS.md and matching skill. Inspect relevant, current,
non-secret source and infrastructure code directly; do not rely only on repository-root
summaries or RAG. Compare application behavior with its related infrastructure where
relevant. Do not inspect prohibited files or run commands in the target repositories.
Do not run tests, linters, or static-analysis commands; this review requires source
inspection, not code execution.

Before writing reports, call ask_orchestrator with this exact task, the workflow
repository as repo_root, and the same effective constraints. Include relevant,
already-vetted non-secret files from the four repositories through context_paths.
Treat the orchestrator's response as advisory and verify every observation against
the local source before reporting it. If the tool remains unavailable after retrying,
stop and ask the user before writing reports.

The main repository is this workflow repository. Write exactly four Markdown
recommendation reports in its approved output directory analysis_reports/{run_id}/,
one named for each repository alias: {report_names}. Each report must separate
verified observations, risks, and proposed improvements; use safe repository-relative
evidence references; and avoid source excerpts, credentials, secret identifiers, raw
configuration, full hostnames, raw command output, and copied version pins. Label
recommendations as proposals and leave implementation decisions to a human. Do not
write any other file. Do not add a README, index, checklist pack, plan file, or any
other output. Do not assume the target repositories are clean or that the reports
directory is empty; status and report history have not been assessed for this task.
No automated tests or infrastructure checks are requested or permitted for this
read-only review."""


def _extract_plan_id(output: str) -> str:
    match = PLAN_ID_RE.search(output)
    if not match:
        raise RuntimeError("Orchestrator did not print a structured plan ID")
    return match.group(1)


def _plan_path(state_root: Path, plan_id: str) -> Path:
    path = state_root / "plans" / f"{plan_id}.json"
    if not path.is_file() or path.is_symlink():
        raise RuntimeError("Structured plan record was not found in user-local state")
    return path


def _validate_plan(
    plan_path: Path,
    *,
    run_id: str,
    targets: dict[str, Path],
    task: str,
) -> None:
    try:
        record: dict[str, Any] = json.loads(plan_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Could not validate the structured plan record: {exc}") from exc
    if not isinstance(record, dict):
        raise RuntimeError("Structured plan record is not an object")

    contexts = record.get("read_only_contexts")
    if not isinstance(contexts, list):
        raise RuntimeError("Plan has no approval-bound read-only repository list")
    actual_roots: set[str] = set()
    for context in contexts:
        repository = context.get("repository") if isinstance(context, dict) else None
        root = repository.get("repo_root") if isinstance(repository, dict) else None
        if not isinstance(root, str):
            raise RuntimeError("Plan contains an invalid read-only repository entry")
        actual_roots.add(root)
    expected_roots = {str(path) for path in targets.values()}
    expected_write_scope = [
        f"analysis_reports/{run_id}/{repo_id}.md" for repo_id in targets
    ]
    repository = record.get("repository")
    if not isinstance(repository, dict):
        raise RuntimeError("Plan has an invalid target repository entry")
    checks = {
        "workflow repository root": repository.get("repo_root") == str(ROOT.resolve()),
        "exact read-only repository set": actual_roots == expected_roots
        and len(contexts) == len(expected_roots),
        "reports-only write scope": record.get("allowed_paths") == expected_write_scope,
        "no additional denied-path mutations": record.get("denied_paths", []) == [],
        "exact approved task": record.get("task") == task,
        "plan ID matches record filename": record.get("plan_id") == plan_path.stem,
    }
    failures = [label for label, valid in checks.items() if not valid]
    if failures:
        raise RuntimeError("Plan scope mismatch: " + ", ".join(failures))


def _approval_path_for_plan(
    state_root: Path,
    plan_id: str,
    before: set[Path],
) -> Path:
    approvals_dir = state_root / "approvals"
    created = set(approvals_dir.glob("*.json")) - before
    matching: list[Path] = []
    for candidate in created:
        if candidate.is_symlink():
            continue
        try:
            approval = json.loads(candidate.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if isinstance(approval, dict) and approval.get("plan_id") == plan_id:
            matching.append(candidate)
    if len(matching) != 1:
        raise RuntimeError("Could not identify exactly one approval record for this plan")
    return matching[0]


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] in {"-h", "--help"}:
        print(
            "Usage: python3 manual_review.py\n\n"
            "Create and display a read-only review plan for the four configured "
            "repositories. Type exactly Y to approve that plan and launch the "
            "Codex executor. Reports are written under analysis_reports/."
        )
        return 0
    if len(sys.argv) > 1:
        print("This command accepts no arguments; use --help.", file=sys.stderr)
        return 2
    if not sys.stdin.isatty():
        print("A terminal is required for the explicit Y approval prompt.", file=sys.stderr)
        return 2

    orchestrate = shutil.which("orchestrate")
    if not orchestrate:
        print("The orchestrate CLI is not available on PATH.", file=sys.stderr)
        return 2
    if not shutil.which("codex"):
        print("The Codex CLI is not available on PATH.", file=sys.stderr)
        return 2

    if OUTPUT_ROOT.is_symlink() or not OUTPUT_ROOT.is_dir():
        print("analysis_reports/ must be an existing, non-symlink directory.", file=sys.stderr)
        return 2

    try:
        targets = _resolve_targets()
        state_root = _state_root(targets)
        run_id = _run_id()
    except (OSError, RuntimeError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2

    task = _review_task(run_id)
    command = [
        orchestrate,
        "plan",
        task,
        "--repo-root",
        str(ROOT),
        "--constraints",
        CONSTRAINTS,
    ]
    for repo_id in targets:
        command.extend(
            ("--allow", f"analysis_reports/{run_id}/{repo_id}.md")
        )
    for target in targets.values():
        command.extend(("--add-dir", str(target)))

    print("Generating the review plan. No review executor will start until you approve it.")
    planned = _run(command, capture=True)
    if planned.returncode != 0:
        print(
            f"Planning failed: {_safe_failure(planned.stdout)}. "
            "No approval or review execution occurred.",
            file=sys.stderr,
        )
        return planned.returncode or 1
    _print_captured(planned)

    try:
        plan_id = _extract_plan_id(planned.stdout or "")
        plan_path = _plan_path(state_root, plan_id)
        _validate_plan(plan_path, run_id=run_id, targets=targets, task=task)
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"{exc}. Nothing was approved or executed.", file=sys.stderr)
        return 2

    print("\nApproval scope:")
    print("  Read-only repositories:")
    for repo_id, target in targets.items():
        print(f"    - {repo_id}: {target}")
    print("  Report write paths:")
    for repo_id in targets:
        print(f"    - analysis_reports/{run_id}/{repo_id}.md")
    print("  Plan and approval records: private user-local orchestrator state")
    print("  Approval authorizes this review run only; recommendations remain proposals.")
    print(
        "  Review the proposal: source inspection is required; only four report "
        "files may be written. Cancel if the proposal conflicts."
    )
    print(
        "  Planning is read-only and may consult existing repository RAG; "
        "it does not refresh the index."
    )
    print(
        "  Codex writes inside this workflow repo; the orchestrator validates changed "
        "paths after execution and does not roll back scope violations."
    )
    try:
        response = input("Type exactly Y to approve this plan and run the review: ")
    except EOFError:
        response = ""
    if response != "Y":
        print(
            "Cancelled. No approval or review execution occurred; the "
            "read-only plan remains in user-local state."
        )
        return 0

    approvals_dir = state_root / "approvals"
    before_approvals = set(approvals_dir.glob("*.json")) if approvals_dir.exists() else set()
    approved = _run([orchestrate, "approve", str(plan_path)], capture=True)
    if approved.returncode != 0:
        print(
            f"Approval failed: {_safe_failure(approved.stdout)}. "
            "The review executor was not launched.",
            file=sys.stderr,
        )
        return approved.returncode or 1
    _print_captured(approved)

    try:
        approval_path = _approval_path_for_plan(state_root, plan_id, before_approvals)
    except (OSError, RuntimeError) as exc:
        print(f"{exc}. The executor was not launched.", file=sys.stderr)
        return 2

    print("Launching the approved Codex review. Only the four reports are in scope.")
    completed = _run(
        [orchestrate, "execute", str(plan_path), str(approval_path), "--executor", "codex"],
        capture=False,
    )
    run_directory = OUTPUT_ROOT / run_id
    if run_directory.is_symlink():
        print("Review output directory is a symlink; inspect manually.", file=sys.stderr)
        return completed.returncode or 1
    expected_reports = [run_directory / f"{repo_id}.md" for repo_id in targets]
    missing = [path.name for path in expected_reports if path.is_symlink() or not path.is_file()]
    if missing:
        print(
            "Review execution ended without all expected reports: " + ", ".join(missing),
            file=sys.stderr,
        )
        return completed.returncode or 1
    expected_names = {path.name for path in expected_reports}
    actual_names = {path.name for path in run_directory.iterdir()}
    unexpected = sorted(actual_names - expected_names)
    if unexpected:
        print(
            "Unexpected files appeared in the run directory: " + ", ".join(unexpected),
            file=sys.stderr,
        )
        return completed.returncode or 1
    if completed.returncode != 0:
        print(
            "The orchestrator returned a nonzero status. Review its scope-validation "
            "message and inspect the workflow diff; no changes were rolled back.",
            file=sys.stderr,
        )
        return completed.returncode
    print(f"Review reports are in analysis_reports/{run_id}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
