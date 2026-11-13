"""Run the GeoPulse analytics pipeline from raw GPS data."""
from pathlib import Path
import os
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent

STAGES = [
    ("Data validation", "geopulse.analytics.data_validation"),
    ("Preprocessing", "geopulse.analytics.preprocessing"),
    ("Movement analytics", "geopulse.geospatial.movement_analysis"),
    ("Movement patterns", "geopulse.geospatial.movement_patterns"),
    ("Clustering", "geopulse.analytics.clustering"),
    ("Visualizations", "geopulse.analytics.visualization"),
]

def main():
    env = os.environ.copy()
    source_path = str(ROOT / "src")
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = (
        source_path + os.pathsep + existing if existing else source_path
    )

    print("=" * 60)
    print("GEOPULSE - END-TO-END ANALYTICS PIPELINE")
    print("=" * 60)

    started = time.perf_counter()

    for index, (name, module) in enumerate(STAGES, start=1):
        print(f"\n[{index}/{len(STAGES)}] Running: {name}", flush=True)
        result = subprocess.run(
            [sys.executable, "-m", module],
            cwd=ROOT,
            env=env,
            check=False,
        )

        if result.returncode != 0:
            print(
                f"\nFAILED: {name} (exit code {result.returncode})",
                file=sys.stderr,
            )
            return result.returncode

        print(f"PASSED: {name}", flush=True)

    elapsed = time.perf_counter() - started
    print("\n" + "=" * 60)
    print(f"PIPELINE COMPLETED IN {elapsed:.1f} SECONDS")
    print("=" * 60)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
