# Live i3 verification hit the sandbox boundary

The initial `i3-msg -t get_bar_config` probe reported “Operation not
permitted” opening the live i3 socket. This prevented monitor routing
verification inside the default sandbox.

Postmortem lookup for “i3 ipc socket operation not permitted” returned i3
runtime checks. The earlier i3 Q incident also documents an i3 runtime
path denied in the sandbox. No code change was needed for IPC access.

With approved desktop access, the read-only query mapped HDMI-0, DVI-D-0,
and DP-2 to their status commands. After the scoped config update, i3
reload succeeded, all three wrapper processes were running, and each
installed status command emitted Redshift first at 2300 K. Physical
monitor inspection and wheel gestures remain manual.
