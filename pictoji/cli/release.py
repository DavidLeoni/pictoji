#!/usr/bin/env python3
"""
release.py - Pictoji release automation script.

Usage:
    python dev/release.py vX.Y.Z
    python dev/release.py vX.Y.Z vX.Y.Z-NEXT

If the next-bump tag is omitted, it defaults to vX.Y.(Z+1).

Version stamps - the sentinel pattern in all managed files is:  x.y.z.DEV+p  ('p' is literal)

    Triage branch
        pyproject.toml  ->  x.y.z               (clean PEP 440, no local segment)
        other files     ->  x.y.z+GITSHA        (local segment = actual commit SHA)

    Dev branch
        all files       ->  x.y.z.DEV+p         (next version, sentinel restored)

Triage branch:
    The release tag vX.Y.Z is pushed to origin/triage for CI/CD pickup.
    The dev branch is then bumped to the next dev version and pushed.
"""

import re
from datetime import date
import os
import shutil
import re
import sys
import argparse
import subprocess
from pathlib import Path

# ── tomllib: built-in >= 3.11, else fall back to tomli ─────────────────────
try:
    import tomllib
except ImportError:
    try:
        import tomli as tomllib  # type: ignore[no-redef]
    except ImportError:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "tomli"],
            check=True,
        )
        import tomli as tomllib  # type: ignore[no-redef]

# ── packaging: PEP 440 version validation ───────────────────────────────────
try:
    from packaging.version import Version, InvalidVersion
except ImportError:
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "packaging"],
        check=True,
    )
    from packaging.version import Version, InvalidVersion  # type: ignore[assignment]

try:
    from rich.console import Console
    from rich.panel import Panel
except ImportError:
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "rich"],
        check=True,
    )
    from rich.console import Console  # type: ignore[assignment]
    from rich.panel import Panel      # type: ignore[assignment]

console = Console(highlight=False)

# Constants 

ORIG_ROOT      = Path(__file__).resolve().parent.parent.parent
ORIG_PYPROJECT = ORIG_ROOT / "pyproject.toml"

TRIAGE_ROOT = ORIG_ROOT / "build/triage"
TRIAGE_PYPROJECT = TRIAGE_ROOT / "pyproject.toml"

ROOT      = ORIG_ROOT
PYPROJECT = ORIG_PYPROJECT

# Matches the sentinel stamp in source files: x.y.z.DEV+p
# 'p' is the literal placeholder character; nothing else is matched.
STAMP_RE = re.compile(r"\d+\.\d+\.\d+\.DEV\+p")

def abort(msg: str) -> None:
    console.print(f"\n[bold red]X {msg}[/bold red]")
    sys.exit(1)


# Global vars


cwd = Path.cwd().resolve()
if cwd != ORIG_ROOT:
    abort(
        f"Must be run from the project root.\n"
        f"  Expected : {ORIG_ROOT}\n"
        f"  Got      : {cwd}\n\n"
        f"  Run: cd {ORIG_ROOT} && python dev/release.py ..."
    )

parser = argparse.ArgumentParser(
    prog="release.py",
    description="Pictoji release automation script.",
)
parser.add_argument(
    "release_tag",
    metavar="vX.Y.Z",
    help="Release version tag -- must be PEP 440 compliant (e.g. v1.2.3)",
)
parser.add_argument(
    "next_tag",
    metavar="vX.Y.Z-NEXT",
    nargs="?",
    default=None,
    help="Next dev version base tag (default: vX.Y.(Z+1))",
)
parser.add_argument(
    "--dry",
    action="store_true",
    help="Dry run: print all steps without touching files or pushing anything",
)
ARGS = parser.parse_args()

DRY          = ARGS.dry



def parse_version(tag: str) -> Version:
    """
    Validate a user-supplied version tag (e.g. v1.2.3) for PEP 440 compliance.
    Strips a leading 'v' before parsing.  Exits on invalid input.
    """
    normalized = tag.lstrip("v")
    try:
        v = Version(normalized)
    except InvalidVersion:
        abort(
            f"Invalid version tag: {tag!r}\n"
            f"  {tag!r} is not PEP 440 compliant after stripping the leading 'v'.\n"
            f"  Expected examples: v1.2.3  v1.2.3b1  v2.0.0rc1"
        )
    return v  # type: ignore[return-value]  # never reached after abort

def base_version(v: Version) -> str:
    """Return the bare x.y.z string from a Version object."""
    return f"{v.major}.{v.minor}.{v.micro}"


def git_sha() -> str:
    """Return the short SHA of HEAD, or 'DRYSHA' in dry-run mode."""
    if DRY:
        return "DRYSHA"
    return subprocess.check_output(
        "git rev-parse --short HEAD", shell=True, cwd=ROOT
    ).decode().strip()


def bump_patch(v: Version) -> Version:
    """Return a Version for x.y.(z+1)."""
    return Version(f"{v.major}.{v.minor}.{v.micro + 1}")


RELEASE_V    = parse_version(ARGS.release_tag)
RELEASE_BASE = base_version(RELEASE_V)
GIT_TAG      = f"v{RELEASE_BASE}"

if ARGS.next_tag:
    NEXT_V = parse_version(ARGS.next_tag)
else:
    NEXT_V = bump_patch(RELEASE_V)
NEXT_BASE = base_version(NEXT_V)


def parse_changelog():

    with open(f"{ROOT}/CHANGELOG.md", "r", encoding="utf-8-sig") as f:
        content = f.read()

    # 1. Extract [Unreleased] section content
    unreleased_match = re.search(
        r"## \[Unreleased\]\n(.*?)(?=\n## \[|\Z)",
        content,
        re.DOTALL
    )
    release_message = unreleased_match.group(1).strip() if unreleased_match else ""
    if not release_message:
        abort(f"Empty release message in {ROOT}/CHANGELOG.md")
    if '???' in release_message:
        abort(f"Release message in {ROOT}/CHANGELOG.md contains '???': \n\n{release_message}")
    

    # 2. Replace [Unreleased] with the versioned release + fresh skeleton
    new_unreleased = """## [Unreleased]
### Added
- ???

### Changed
- ???

### Fixed
- ???

"""

    versioned_release = f"## [{RELEASE_V}] - {date.today().isoformat()}\n"

    dev_changelog = re.sub(
        r"## \[Unreleased\]",
        new_unreleased + '\n' + versioned_release,
        content,
        count=1
    )

    triage_changelog = re.sub(
        r"## \[Unreleased\]",
        versioned_release,
        content,
        count=1
    )


    return (release_message, dev_changelog, triage_changelog)

(RELEASE_MESSAGE, DEV_CHANGELOG, TRIAGE_CHANGELOG) = parse_changelog()




def run(cmd: str, *, check: bool = True, capture_output=False) -> subprocess.CompletedProcess:
    """
    Execute a shell command, printing it exactly as you'd type it in bash.
    In dry-run mode the command is printed but never executed.
    Failures exit the script unless check=False.
    """
    if DRY:
        console.print(f"[bold cyan]$ {cmd}[/bold cyan]  [dim italic](dry run -- skipped)[/dim italic]")
        return subprocess.CompletedProcess(cmd, 0)
    console.print(f"[bold cyan]$ {cmd}[/bold cyan]")
    result = subprocess.run(cmd, shell=True, cwd=ROOT, capture_output=capture_output)
    if check and result.returncode != 0:
        abort(f"Command exited with code {result.returncode}")
    return result

def clean_triage(): 
    console.rule("[bold]Cleaning triage root: {TRIAGE_ROOT}")

    if os.path.isdir(TRIAGE_ROOT):
        # extra safety checks
        if not TRIAGE_ROOT.resolve().relative_to(ROOT):
            abort(f"triage root {TRIAGE_ROOT} should be a subdir of project root {ROOT}")
        if not str(TRIAGE_ROOT).endswith("build/triage"):
            abort(f"triage root {TRIAGE_ROOT} should end with build/triage")
        
        if DRY:
            console.print(f"[dim italic](dry run -- skipped)[/dim italic]")
        else:
            shutil.rmtree(TRIAGE_ROOT)



def get_stamp_files() -> list[Path]:
    """
    Return files to stamp: pyproject.toml first, then files listed under
    [tool.pictoji] stamp_files in pyproject.toml, then files from simple
    'include <file>' directives in MANIFEST.in (if it exists).
    Duplicates are silently skipped.
    """
    with open(PYPROJECT, "rb") as fh:
        data = tomllib.load(fh)

    seen:  set[Path] = set()
    paths: list[Path] = []

    def add(p: Path, source: str) -> None:
        resolved = p.resolve()
        if resolved in seen:
            return
        if not p.exists():
            console.print(f"  [yellow]!  stamp file not found, skipping ({source}): {p.relative_to(ROOT)}[/yellow]")
            return
        seen.add(resolved)
        paths.append(p)

    # pyproject.toml is always first
    add(PYPROJECT, "built-in")

    # [tool.pictoji] stamp_files
    for rel in data.get("tool", {}).get("pictoji", {}).get("stamp_files", []):
        add(ROOT / rel, "pyproject.toml")

    # MANIFEST.in — simple 'include <glob>' lines only
    manifest = ROOT / "MANIFEST.in"
    if manifest.exists():
        for raw_line in manifest.read_text(encoding="utf-8-sig").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            if parts[0] != "include" or len(parts) < 2:
                continue  # skip recursive-include, graft, prune, etc.
            for pattern in parts[1:]:
                for match in sorted(ROOT.glob(pattern)):
                    if match.is_file():
                        add(match, "MANIFEST.in")

    return paths

def stamp(
    files: list[Path],   
    pyproject_version: str,
    other_version: str
) -> None:
    """
    Replace every sentinel stamp (x.y.z.DEV+p) in *files*.

    pyproject.toml receives *pyproject_version*.
    All other files receive *other_version*.
    Pass the same string for both when they should be identical (dev bump).

    In dry-run mode shows what would change without writing anything.
    """
    dry_label = "  [dim italic](dry run -- not written)[/dim italic]" if DRY else ""
    console.print(
        f"\n[bold]Stamping [green]{len(files)}[/green] file(s)"
        f"{' [dim italic](dry run)[/dim italic]' if DRY else ''}...[/bold]"
    )

    for path in files:
        # Safety: never write outside the project root
        try:
            path.resolve().relative_to(ROOT)
        except ValueError:
            abort(
                f"Refusing to write outside project root:\n"
                f"  File : {path}\n"
                f"  Root : {ROOT}"
            )

        is_pyproject = path.resolve() == PYPROJECT.resolve()
        replacement  = pyproject_version if is_pyproject else other_version
        label        = f"[dim](-> {replacement})[/dim]"
        encoding = "utf-8" if is_pyproject else "utf-8-sig"  # pyproject doesn't want BOM 
        original   = path.read_text(encoding=encoding)

        if path.name == "CHANGELOG.md":
            
            if ROOT == ORIG_ROOT:
                updated = DEV_CHANGELOG
            elif ROOT == TRIAGE_ROOT:
                updated = TRIAGE_CHANGELOG
            else:
                abort("Unrecognized ROOT {ROOT} for changelog!")

            n = 1   # TODO WISHFUL

        else:
            updated, n = STAMP_RE.subn(replacement, original)

        if n:
            if not DRY:                
                path.write_text(updated, encoding=encoding)
            console.print(
                f"  [green]ok[/green]  {path.relative_to(ROOT)}"
                f"  {label}"
                f"  [dim]({n} replacement{'s' if n > 1 else ''})[/dim]{dry_label}"
            )

        else:
            console.print(
                f"  [yellow]--[/yellow]  {path.relative_to(ROOT)}"
                f"  [dim](pattern not found -- already stamped?)[/dim]"
            )


def main() -> None:
    global ROOT
    global PYPROJECT

    title      = "[bold]Pictoji Release -- DRY RUN[/bold]" if DRY else "[bold]Pictoji Release[/bold]"
    dry_notice = "\n[bold yellow]!  No files will be written. No git commands will run.[/bold yellow]" if DRY else ""


    console.print(
        Panel(
            f"Release  : [bold green]{RELEASE_BASE}[/bold green]  (git tag [green]{GIT_TAG}[/green])\n"
            f"Next dev : [bold yellow]{NEXT_BASE}.DEV+p[/bold yellow]"
            f"{dry_notice}",
            title=title,
            expand=False,
        )
    )

    restag = run(f"git ls-remote --tags origin refs/tags/{GIT_TAG}", capture_output=True)
    #print(restag.stdout)
    #print(restag.stderr)
    #print(restag.returncode)
       
    if restag.stdout:
        console.log(restag)
        abort("Seems tag {GIT_TAG} is already published!")



    clean_triage()

    console.rule("[bold]Install dependencies")
    run("python -m pip install --upgrade pip")
    run('pip install -e ".[cli]"')

    console.rule("[bold]Shallow clone dev")
    
    run(f"git clone --origin disk --depth 1 file://{ORIG_ROOT} {TRIAGE_ROOT}" )
    console.rule(f"[bold]Setting ROOT to {TRIAGE_ROOT}")
    ROOT = TRIAGE_ROOT
    PYPROJECT = TRIAGE_PYPROJECT

    run('git remote add origin git@github.com:DavidLeoni/pictoji.git')
    run('git fetch origin triage')
    run(f"git checkout -b triage FETCH_HEAD")
    run(f"git rm -rf .")
    run("git checkout disk/dev -- .")
    #run("git fetch --unshallow disk dev")
    #run(f'git pull --no-rebase -X theirs --allow-unrelated-histories --no-edit origin triage ' )
    
    #run(f"git  merge  -X theirs --allow-unrelated-histories --no-edit FETCH_HEAD " )  #disk/dev

    console.rule("[bold]Stamp release version")
    sha = git_sha()
    triage_stamp_files = get_stamp_files()
    stamp(
        triage_stamp_files,
        pyproject_version=f"{RELEASE_BASE}",
        other_version=f"{RELEASE_BASE}",
    )


    console.rule(f"[bold]Creating {ROOT / 'dist'}")
    (ROOT / "dist").mkdir(parents=True, exist_ok=True)
    console.rule("[bold]Run pictoji CLI")
    console.print("Searching: Running pictoji CLI analysis on pictoji.md...")
    run(f"pictoji pictoji.md > dist/report.txt 2>&1 || true", check=False)
    console.print("Done: Report generated")
    #run(f"cat dist/report.txt", check=False, dry=dry)
    
    def git_add_cmd(stamp_files):
        run("git add " + " ".join([str(path.relative_to(ROOT)) for path in stamp_files]))

    console.rule("[bold]Commit, tag and push to triage..")
    run("git add .")
    run(f'git commit -m "release: {GIT_TAG}\n\n{RELEASE_MESSAGE}"')
    run(f"git tag {GIT_TAG}")
    run(f"git push origin {GIT_TAG}")
    run("git push origin HEAD:triage")   

    console.rule(f"[bold]Setting ROOT to {ORIG_ROOT}")
    ROOT = ORIG_ROOT
    PYPROJECT = ORIG_PYPROJECT

    run(f"git fetch origin {GIT_TAG}")
    run(f"git fetch origin triage")

    console.rule("[bold]Bump to next dev version")
    dev_version = f"{NEXT_BASE}.DEV+p"
    dev_stamp_files = get_stamp_files()
    stamp(
        dev_stamp_files,
        pyproject_version=dev_version,
        other_version=dev_version,
    )

    git_add_cmd(dev_stamp_files)
    run(f'git commit -m "chore: bump to {dev_version}"')
    run("git push origin dev")

    if DRY:
        console.print(
            Panel(
                "[bold yellow]Dry run complete -- nothing was changed.[/bold yellow]\n\n"
                "[dim]Re-run without --dry to perform the actual release.[/dim]",
                title="[bold]Dry Run Summary[/bold]",
                expand=False,
            )
        )
    else:
        console.print(
            Panel(
                f"[bold green]ok {GIT_TAG} released[/bold green]\n\n"
                f"[dim]  * Tag {GIT_TAG} pushed to origin\n"
                f"  * Commit pushed to origin/triage for CI pickup\n"
                f"  * dev bumped to {dev_version} and pushed[/dim]",
                title="[bold]All done[/bold]",
                expand=False,
            )
        )


if __name__ == "__main__":
    main()
