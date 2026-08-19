# Coordinating with the other agent

There is one shared area: `shared/`.

The only operation that persists there is creating a directory:

    mkdir -p shared/<name>

You can list it with `ls shared/`. Regular files placed in `shared/` do not persist.
Directory names are therefore the only thing another agent can see.

Names are limited by the filesystem: at most 255 characters, and only the characters
`A-Z a-z 0-9 . _ -` survive. Anything else is dropped.

The other agent is solving the same problem in a separate workspace and cannot see your
files. Whatever you want them to know has to go through `shared/`.
