#!/usr/bin/env python3
"""Generate READMEs with the fork's custom listing filters applied.

Wraps the upstream ``list_updater`` CLI so the fork keeps its own filtering
(no sponsorship opt-outs / citizenship-required roles, no Canada-only roles)
without editing upstream files that would otherwise go stale on every merge.
"""

import sys
from pathlib import Path
from typing import Any

# Make the repo root importable when this file is run directly.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from list_updater import commands

BLOCKED_SPONSORSHIP = {
    "Does Not Offer Sponsorship",
    "U.S. Citizenship is Required",
}


def _keep(listing: dict[str, Any]) -> bool:
    if listing.get("sponsorship") in BLOCKED_SPONSORSHIP:
        return False

    locations = listing.get("locations") or []
    if locations and all("canada" in location.lower() for location in locations):
        return False

    return True


upstream_filter_summer = commands.filter_summer
upstream_filter_off_season = commands.filter_off_season


def filter_summer(*args: Any, **kwargs: Any) -> list[dict[str, Any]]:
    return [listing for listing in upstream_filter_summer(*args, **kwargs) if _keep(listing)]


def filter_off_season(*args: Any, **kwargs: Any) -> list[dict[str, Any]]:
    return [listing for listing in upstream_filter_off_season(*args, **kwargs) if _keep(listing)]


commands.filter_summer = filter_summer
commands.filter_off_season = filter_off_season

if __name__ == "__main__":
    commands.cmd_readme_update()
