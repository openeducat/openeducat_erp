# openeducat_facility – Facility Management 🏢

## Overview

The **Facility** module tracks non-classroom school infrastructure: sports grounds, laboratories, hostels, canteens and any other bookable facility.

---

## Key Features

* Register all school facilities with descriptions and capacity
* Booking system with conflict checking
* Maintenance request logging
* Usage reporting

---

## Core Model: `op.facility`

| Field | Description |
|-------|-------------|
| `name` | Facility name |
| `type` | Sports Ground / Hostel / Lab / Canteen / Other |
| `capacity` | Maximum users |
| `state` | Operational / Under Maintenance / Closed |

---

## License

LGPL-3.0 – see repository [LICENSE](../LICENSE).
