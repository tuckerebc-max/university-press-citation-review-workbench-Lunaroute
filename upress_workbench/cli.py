from __future__ import annotations

import argparse
import time

from . import config
from .pipeline import RunManager
from .state import StateStore

TERMINAL = {"complete", "partial", "failed", "cancelled", "interrupted"}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run a University Press chapter batch without opening the browser interface.")
    parser.add_argument("--input", required=True, dest="input_root")
    parser.add_argument("--output", required=True, dest="output_parent")
    parser.add_argument("--owner", required=True, dest="case_owner")
    parser.add_argument("--project", default="University Press chapter review", dest="project_label")
    parser.add_argument("--classification", choices=["public", "unpublished_approved"], default="unpublished_approved")
    parser.add_argument("--mode", choices=["baseline", "incremental", "full", "release", "proof"], default="baseline", dest="run_mode")
    parser.add_argument("--model", choices=sorted(config.ALLOWED_MODELS), default=config.DEFAULT_BATCH_MODEL)
    parser.add_argument("--concurrency", type=int, choices=range(1, config.MAX_WORKERS + 1), default=3)
    parser.add_argument("--crossref", action=argparse.BooleanOptionalAction, default=True, dest="crossref_enabled")
    parser.add_argument("--approve-lunaroute", action="store_true", dest="provider_approved", help="Required confirmation that LunaRoute is approved for every chapter in this manifest.")
    args = parser.parse_args(argv)
    if not args.provider_approved:
        parser.error("--approve-lunaroute is required before any manuscript text can leave the machine")
    config.ensure_runtime_dirs()
    store = StateStore(config.DB_PATH)
    store.recover_orphaned_runs()
    manager = RunManager(store)
    run_id = manager.create_and_start(vars(args))
    print(f"Run {run_id} created.")
    while True:
        run = store.get_run(run_id)
        if not run:
            return 2
        chapters = store.get_chapters(run_id)
        complete = sum(1 for item in chapters if item["status"] == "packet_built")
        print(f"{run['status']}: {complete}/{len(chapters)} packets", end="\r", flush=True)
        if run["status"] in TERMINAL:
            print()
            print(f"Output: {run['output_root']}")
            return 0 if run["status"] == "complete" else 1
        time.sleep(1.5)


if __name__ == "__main__":
    raise SystemExit(main())
