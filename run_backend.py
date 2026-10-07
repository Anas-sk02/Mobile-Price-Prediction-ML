"""
SmartPrice - Root Backend Launcher
Supports dynamic cloud port ($PORT) and production/dev modes.
"""

import os
import sys
from pathlib import Path
import uvicorn

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    is_prod = os.environ.get("ENV", "development") == "production" or "PORT" in os.environ

    uvicorn.run(
        "backend.app.main:app",
        host="0.0.0.0",
        port=port,
        reload=not is_prod,
        app_dir=str(PROJECT_ROOT)
    )
