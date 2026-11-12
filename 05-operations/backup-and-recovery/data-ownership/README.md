# Data Ownership

> **Status:** Draft — every stateful service needs one canonical owner.

Map state to the service or repository that owns its schema, writes, export/import, and recovery. Dashboards and aggregate backups may present or compose state without becoming a second authority.

Keep product-domain ownership in the service contracts and link to them from the operational map.
