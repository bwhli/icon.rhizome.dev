import asyncio
import builtins

import rich
import uvloop

# Set event loop policy.
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

# Replace built-in print with Rich's print.
builtins.print = rich.print
