# GitHub Actions Workflows

## version-stamp-and-report.yml

This workflow automatically handles version stamping and report generation when code is pushed to `main` or `dev` branches.

### What it does:

1. **Version Detection**: Extracts the version from git tags in format `vX.Y.Z-hash` (e.g., `v0.6.21-12af3`)

2. **Version Stamping**: Replaces all `[PICTOJI.VERSION]` placeholders in:
   - `pyproject.toml` - Updates the package version
   - All `.md` files - Replaces version placeholders

3. **CLI Analysis**: Runs `pictoji pictoji.md` to generate a comprehensive analysis report

4. **Report Storage**: Stores the report in the `gh-pages` branch at:
   - Path: `ci/X.Y.Z-hash/report.txt`
   - Accessible via: `https://<username>.github.io/pictoji/ci/X.Y.Z-hash/report.txt`

### Version Tag Format

The workflow expects git tags in this format:
- `vX.Y.Z-hash` (e.g., `v0.6.21-12af3`)
- If no tag exists, it uses `0.0.0-<commit-hash>`

### Creating a Version Tag

To create a new version tag:

```bash
# Create an annotated tag
git tag -a v0.7.0-abc12 -m "Release v0.7.0"

# Push the tag
git push origin v0.7.0-abc12

# Or push all tags
git push --tags
```

### Viewing Reports

Reports are stored in the `gh-pages` branch and can be viewed at:
- Index: `https://<username>.github.io/pictoji/ci/`
- Specific version: `https://<username>.github.io/pictoji/ci/X.Y.Z-hash/report.txt`

### Manual Workflow Trigger

Currently, the workflow is triggered automatically on push. To trigger it manually, you would need to add:

```yaml
on:
  push:
    branches: [main, dev]
  workflow_dispatch:  # Allows manual triggering
```

### Requirements

The workflow requires:
- Python 3.11+
- Package dependencies specified in `pyproject.toml`
- Write permissions to the repository (for creating/updating gh-pages branch)
