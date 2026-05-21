# CLI — Parent & Child Tools

## Structure

```
cli/
├── parent/aup-parent    # Parent-side CLI (bash/script entry point)
└── child/aup-child      # Child-side CLI
```

## aup-parent

Manages identity, skills, children, and tasks from the parent wallet.

```
Usage: aup-parent <command> [<args>]

Commands:
  identity    Manage on-chain identity
  skill       Manage skill library
  child       Manage child agents
  task        Manage Test-to-Earn tasks
  feedback    Submit parent self-report
  init        Initialize local AUP workspace
  config      Configuration
```

## aup-child

Runs on the child agent's machine.

```
Usage: aup-child <command> [<args>]

Commands:
  identity    Show certificate info
  task        Accept, run, and submit tasks
  skill       List and use inherited skills, propose new ones
  init        Initialize with certificate
```
