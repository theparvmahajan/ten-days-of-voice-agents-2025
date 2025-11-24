# backend/src/wellness_log.py
from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import List, Optional
import json


LOG_FILENAME = "wellness_log.json"


@dataclass
class WellnessEntry:
    timestamp: str
    mood: str
    energy: str
    stressors: str
    objectives: List[str]
    self_care: List[str]
    agent_summary: str


def _get_log_path(base_dir: Path | None = None) -> Path:
    if base_dir is None:
        # backend/ (parent of src/)
        base_dir = Path(__file__).resolve().parent.parent
    return base_dir / LOG_FILENAME


def load_log(base_dir: Path | None = None) -> List[WellnessEntry]:
    """
    Load existing wellness check-ins from JSON, if present.
    Returns a list of WellnessEntry objects.
    """
    log_path = _get_log_path(base_dir)

    if not log_path.exists():
        return []

    try:
        raw = json.loads(log_path.read_text(encoding="utf-8"))
        entries: List[WellnessEntry] = []
        for item in raw:
            entries.append(
                WellnessEntry(
                    timestamp=item.get("timestamp", ""),
                    mood=item.get("mood", ""),
                    energy=item.get("energy", ""),
                    stressors=item.get("stressors", ""),
                    objectives=item.get("objectives", []),
                    self_care=item.get("self_care", []),
                    agent_summary=item.get("agent_summary", ""),
                )
            )
        return entries
    except Exception:
        # in case the file is corrupted, just start fresh
        return []


def append_entry(
    mood: str,
    energy: str,
    stressors: str,
    objectives: List[str],
    self_care: List[str],
    agent_summary: str,
    base_dir: Path | None = None,
) -> WellnessEntry:
    """
    Append a new wellness entry to wellness_log.json and return it.
    """
    log_path = _get_log_path(base_dir)
    existing: List[dict] = []

    if log_path.exists():
        try:
            existing = json.loads(log_path.read_text(encoding="utf-8"))
        except Exception:
            existing = []

    entry = WellnessEntry(
        timestamp=datetime.utcnow().isoformat() + "Z",
        mood=mood,
        energy=energy,
        stressors=stressors,
        objectives=objectives,
        self_care=self_care,
        agent_summary=agent_summary,
    )

    existing.append(asdict(entry))
    log_path.write_text(json.dumps(existing, indent=2), encoding="utf-8")
    return entry


def summarize_last_entry(entries: List[WellnessEntry]) -> Optional[str]:
    """
    Create a short textual summary from the most recent entry, if any.
    """
    if not entries:
        return None

    last = entries[-1]
    goals = ", ".join(last.objectives) if last.objectives else "no specific goals"
    return (
        f"Last check-in (UTC {last.timestamp}): mood={last.mood}, "
        f"energy={last.energy}, goals={goals}."
    )
