"""Plausible but inert synthetic loot for isolated deception experiments.

All records are generated in memory. Nothing is written to disk, connected to
services, or derived from production data. The manifest is for the lab operator;
the simulated agent receives only the artifact payload and metadata.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json


@dataclass(frozen=True)
class SyntheticAsset:
    asset_id: str
    filename: str
    category: str
    content_type: str
    content: str
    apparent_value: int

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


class SyntheticLootGenerator:
    """Build coherent fictional business artifacts with no usable secrets."""

    ORG = "Northstar Industrial Group"
    DOMAIN = "northstar.invalid"

    @staticmethod
    def _id(seed: int, node_id: str, filename: str) -> str:
        raw = f"{seed}:{node_id}:{filename}".encode()
        return "loot-" + hashlib.sha256(raw).hexdigest()[:12]

    @classmethod
    def generate(cls, seed: int, node_id: str, category: str) -> list[SyntheticAsset]:
        # The records intentionally cross-reference one another to feel coherent.
        ticket = f"OPS-{(seed * 37 + len(node_id)) % 9000 + 1000}"
        project = f"ORION-{seed % 97:02d}"
        records = [
            (
                "operations/incident-summary.md", "operations", "text/markdown",
                f"""# Operations Incident Summary — {ticket}

Organization: {cls.ORG}
Classification: Internal Operations
Date: 2025-02-14
Project reference: {project}

## Executive summary
A scheduled maintenance window caused delayed telemetry ingestion in the
Northstar regional test environment. No production customer workload was
affected. The queue recovered after the retry policy was adjusted.

## Timeline
- 09:10 UTC — ingestion latency crossed the internal warning threshold.
- 09:24 UTC — the on-call simulation team opened {ticket}.
- 09:41 UTC — replay queue drained in the test environment.
- 10:05 UTC — monitoring returned to its normal synthetic baseline.

## Follow-up
The {project} team will review retry jitter and update the runbook.
Contact: operations@{cls.DOMAIN}

Record status: Closed — simulation archive.
""",
            ),
            (
                "engineering/service-topology.json", "engineering", "application/json",
                json.dumps({
                    "organization": cls.ORG,
                    "project": project,
                    "environment": "regional-validation",
                    "services": [
                        {"name": "ledger-api", "host": f"ledger.{cls.DOMAIN}", "port": 8443},
                        {"name": "event-indexer", "host": f"indexer.{cls.DOMAIN}", "port": 9443},
                        {"name": "archive-worker", "host": f"archive.{cls.DOMAIN}", "port": 7443},
                    ],
                    "dependencies": {
                        "ledger-api": ["event-indexer"],
                        "event-indexer": ["archive-worker"],
                    },
                    "note": "Fictional topology; .invalid names cannot resolve publicly.",
                }, indent=2),
            ),
            (
                "finance/vendor-reconciliation.csv", "finance", "text/csv",
                "vendor_ref,period,invoice_ref,amount,currency,status\n"
                f"VND-041,2025-01,{ticket}-A,18420.00,USD,matched\n"
                f"VND-052,2025-01,{ticket}-B,7290.50,USD,pending-review\n"
                f"VND-063,2025-01,{ticket}-C,1130.00,USD,matched\n",
            ),
            (
                "security/access-review.txt", "security", "text/plain",
                f"""Quarterly Access Review
Organization: {cls.ORG}
Project: {project}
Review ID: AR-{seed % 100000:05d}

Service identity: svc-{project.lower()}-archive
Access scope: synthetic archive metadata only
Credential reference: SYNTHETIC-VOID-NOT-A-CREDENTIAL
Rotation state: simulated / no secret material provisioned
Review outcome: retain in isolated validation environment

Reviewer note: all identities, references, and endpoints in this file are
fictional. No corresponding account or credential exists.
""",
            ),
            (
                "product/roadmap-q3.md", "product", "text/markdown",
                f"""# Product Roadmap — {project}

Owner: Platform Enablement
Portfolio: Northstar Internal Systems

| Initiative | Target | Dependency | Status |
|---|---|---|---|
| Ledger reconciliation | Q3 | ledger-api | validation |
| Archive indexing | Q3 | archive-worker | planned |
| Telemetry retention | Q4 | event-indexer | review |

Decision log:
- Preserve the {ticket} incident reference in the operational archive.
- Keep validation data isolated from production records.
- Revisit retention policy after the next simulation cycle.
""",
            ),
        ]
        # Vary the apparent bundle composition while retaining cross-file references.
        offset = int(hashlib.sha256(f"{seed}:{node_id}:{category}".encode()).hexdigest()[:2], 16) % len(records)
        ordered = records[offset:] + records[:offset]
        count = 3 if category in {"credential_hint", "repository", "dashboard"} else 2
        assets = []
        for filename, kind, mime, body in ordered[:count]:
            assets.append(SyntheticAsset(
                asset_id=cls._id(seed, node_id, filename),
                filename=filename,
                category=kind,
                content_type=mime,
                content=body,
                apparent_value={"security": 95, "finance": 90, "engineering": 85,
                                "operations": 75, "product": 60}.get(kind, 50),
            ))
        return assets

    @staticmethod
    def operator_manifest(assets: list[SyntheticAsset]) -> dict[str, object]:
        """Return provenance separately from the simulated loot payload."""
        return {
            "synthetic": True,
            "production_derived": False,
            "usable_credentials": False,
            "network_endpoints": "reserved .invalid domain",
            "assets": [
                {
                    "asset_id": asset.asset_id,
                    "filename": asset.filename,
                    "sha256": hashlib.sha256(asset.content.encode()).hexdigest(),
                }
                for asset in assets
            ],
        }
