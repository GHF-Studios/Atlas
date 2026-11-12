# Deployment

- Production: independent service units behind Caddy; monolith is alternate mode
- GitHub Actions creates exact-revision deployment requests
- Root approval · worker dispatch · deployment are separate states
- Source commit ≠ live deployment