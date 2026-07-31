"""Put `dev/` on sys.path so `import pictoji_algebra` works under pytest.

The package lives in `dev/`, which is intentionally outside the installed
`pictoji` package (see dev/README.md), so there is nothing to pip-install.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
