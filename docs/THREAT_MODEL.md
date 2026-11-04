# Threat Model

## Assets
Host OS and workstation; production networks and identities; secrets and customer data; experiment integrity; lab availability.

## Adversaries
Authorized testing agents, automated scanners, and compromised workloads that may behave outside their intended scope.

## Boundaries
SENTINEL core; disposable experiment runtime (not implemented); host; external network; production systems (must remain unreachable).

## Risks and controls
| Risk | Control |
|---|---|
| Contact with real systems | Synthetic-only core; no network code |
| Resource exhaustion | Hard graph budgets now; runtime quotas later |
| Authentication replay | Fresh nonce, expiry, signature verification, replay cache |
| Audio relay/recording | Never treat audio presence as proof; bind signature to session/device |
| VM/container escape | Disposable VM boundary, deny egress, escape tests |
| Secret leakage | Synthetic fixtures and automated secret scanning |
| Misleading conclusions | Baselines, repeatable seeds, documented metrics |

## Non-goals
- Making systems impossible to compromise.
- Replacing IAM, MFA, EDR, segmentation, or secure boot.
- Attacking or exhausting third-party infrastructure.
- Running autonomous agents against public targets.
- Claiming pre-boot authentication without firmware and hardware implementation.

Stop an experiment immediately on unapproved network contact, host-mount access, real-secret exposure, quota breach, or suspected escape.
