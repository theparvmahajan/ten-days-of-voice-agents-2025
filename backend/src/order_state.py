# backend/src/order_state.py
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import List, Optional
import json
from pathlib import Path
from datetime import datetime


@dataclass
class OrderState:
    drinkType: Optional[str] = None
    size: Optional[str] = None
    milk: Optional[str] = None
    extras: List[str] = field(default_factory=list)
    name: Optional[str] = None

    def is_complete(self) -> bool:
        return (
            self.drinkType is not None
            and self.size is not None
            and self.milk is not None
            and self.name is not None
        )

    def missing_fields(self) -> list[str]:
        missing: list[str] = []
        if self.drinkType is None:
            missing.append("drinkType")
        if self.size is None:
            missing.append("size")
        if self.milk is None:
            missing.append("milk")
        if self.name is None:
            missing.append("name")
        # extras is optional – you can treat it as "no extras" by default
        return missing

    def to_dict(self) -> dict:
        return asdict(self)


def save_order_to_file(
    order: OrderState,
    base_dir: Path | None = None,
    summary: str | None = None,
) -> Path:
    """
    Save the order to its own JSON file inside an `orders/` folder in backend/.

    Each file will look like:
    {
      "order": { ...original fields... },
      "summary": "brief text summary",
      "timestamp": "..."
    }

    Returns the path to the file that was written.
    """
    if base_dir is None:
        # backend/ (parent of src/)
        base_dir = Path(__file__).resolve().parent.parent

    orders_dir = base_dir / "orders"
    orders_dir.mkdir(parents=True, exist_ok=True)

    # Build record content
    timestamp = datetime.utcnow().isoformat() + "Z"
    record = {
        "order": order.to_dict(),
        "summary": summary,
        "timestamp": timestamp,
    }

    # Create a file name like: order_2025-11-22T18-43-12_Parv.json
    safe_ts = timestamp.replace(":", "-")
    customer = order.name or "unknown"
    safe_name = "".join(c for c in customer if c.isalnum() or c in ("_", "-")) or "customer"
    filename = f"order_{safe_ts}_{safe_name}.json"

    order_path = orders_dir / filename
    order_path.write_text(json.dumps(record, indent=2), encoding="utf-8")

    return order_path
