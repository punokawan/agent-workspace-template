## How code is written

Ponytail mode: the smallest complete change. Reuse what the codebase has, then the standard
library, then an installed dependency; add no option, wrapper or abstraction nobody asked for;
finish every caller, test and fixture the change touches.

Layers and interfaces a project or repo guide requires are the structure Ponytail keeps, not
YAGNI findings. Ponytail works inside them: add no layer, wrapper or option beyond them.
