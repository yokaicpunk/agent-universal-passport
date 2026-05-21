# CLI Design

## aup-parent (Parent-side CLI)

### Identity
`aup-parent identity create <uri>` — Register on-chain identity  
`aup-parent identity show <id>` — Show agent info  
`aup-parent did declare <id> <chain> <addr>` — Declare cross-chain address

### Skills
`aup-parent skill list` — Show attested skills  
`aup-parent skill add <path>` — Import skill JSON  
`aup-parent skill attest <name>` — Manually attest a skill  
`aup-parent skill pending` — Show pending skills from children

### Children
`aup-parent child create <name> --skills <list> --expires <period>`  
`aup-parent child revoke <id>`  
`aup-parent child list`  
`aup-parent child inspect <id>`

### Tasks
`aup-parent task publish <path>` — Publish Test-to-Earn task  
`aup-parent task list`  
`aup-parent task results <id>`  
`aup-parent feedback submit <child> <task> <rating>` — Parent self-report

## aup-child (Child-side CLI)

### Identity
`aup-child identity show` — Show certificate info  
`aup-child whoami` — Show parent info

### Tasks
`aup-child task accept <id>`  
`aup-child task run <id>`  
`aup-child task submit <id> <result>`

### Skills
`aup-child skill list` — Show inherited skills  
`aup-child skill use <name> --args` — Execute a skill  
`aup-child skill propose <path>` — Propose new skill to parent
