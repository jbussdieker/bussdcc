# BussDCC

![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.11%2B-brightgreen)

**bussdcc** is a strongly-typed cybernetic kernel for building durable, event-driven systems in Python.

It provides a minimal but complete coordination core for systems that manage:

* **Devices** (hardware, boundaries, external resources)
* **Processes** (event-driven logic)
* **Interfaces** (human/network adapters)
* **Services** (time-driven supervised workers)

The kernel defines **contracts, lifecycle, dispatch authority, and supervision** — but leaves application policy to you.

## Why BussDCC?

Modern Python systems often grow into tangled combinations of:

* Threads
* Callbacks
* Background loops
* Signal handlers
* Implicit global state

bussdcc enforces:

* **Explicit lifecycles**
* **Authoritative message dispatch**
* **Typed events**
* **Supervised background services**
* **Deterministic boot and shutdown**

It is not an application framework.

It is a **coordination kernel**.

# Quick Start

```python
from bussdcc import Runtime, message
from bussdcc.device import Device
from bussdcc.process import Process
from bussdcc.service import Service

class MySensor(Device):
    kind = "sensor"

    def connect(self):
        print("Sensor online")

    def disconnect(self):
        print("Sensor offline")


class Logger(Process):
    name = "logger"

    def handle_event(self, ctx, evt):
        print(evt.payload.name, evt.payload.to_dict())


class Heartbeat(Service):
    name = "heartbeat"
    interval = 2.0

    def tick(self, ctx):
        ctx.emit(message.SystemSignal(signal=0, action="heartbeat"))


rt = Runtime()
rt.attach_device(MySensor(id="sensor-1"))
rt.register_process(Logger())
rt.register_service(Heartbeat())

rt.boot()
```

# Architectural Model

At its core, bussdcc is built around a single invariant:

> **All coordination flows through typed `Message` events.**
> The `Runtime` is the authoritative dispatcher.

Everything else supports that invariant.

# Core Concepts

## Runtime

The `Runtime` is the coordination authority.

It:

* Owns the `Context`
* Owns the event dispatch loop
* Controls boot and shutdown order
* Supervises services
* Routes every `Message` to:

  * Processes
  * Interfaces
  * Services (event-driven side)

Boot order is deterministic:

1. Devices attach
2. Processes attach and start
3. Interfaces attach and start
4. Services attach and begin supervised execution

Shutdown reverses this order.

The runtime emits lifecycle messages:

* `runtime.booting`
* `runtime.booted`
* `runtime.shutting_down`
* `runtime.shutdown`

The runtime is also usable as a context manager:

```python
with Runtime() as rt:
    ...
```

## Context

The `Context` is a minimal capability container.

It exposes:

* `clock` — time abstraction
* `events` — event bus
* `state` — thread-safe hierarchical state
* `runtime` — runtime access
* `emit(message)` — authoritative message emission

The context is intentionally small and infrastructure-focused.

## Messages

Messages are:

* Frozen dataclasses
* Strictly typed
* Assigned a severity level

Example:

```python
@dataclass(slots=True, frozen=True)
class ProcessError(Message):
    name = "process.error"
    severity = Severity.ERROR
```

Every message becomes an `Event[Message]` when emitted.

Severity levels:

* `DEBUG`
* `INFO`
* `WARNING`
* `ERROR`
* `CRITICAL`

Severity protects the system from infinite error recursion during failure cascades.

## Event Engine

The `EventBus` is:

* Synchronous
* Thread-safe
* In-process
* Typed

Handlers run in the emitter’s thread.

Subscriber failures are isolated and converted into `event.subscriber_error` messages (unless already error-level).

This is coordination — not distributed messaging middleware.

## Devices

Devices represent hardware or external boundaries.

Lifecycle:

```
attach(ctx) → connect()
detach()   → disconnect()
```

Devices emit:

* `device.attached`
* `device.detached`
* `device.failed`

Devices are expected to fail honestly.

## Processes

Processes are synchronous, event-driven logic units.

They:

* Attach to the runtime
* Start during boot
* Receive every emitted `Message`
* React via `handle_event`

Lifecycle:

* `attach(ctx)`
* `start(ctx)`
* `handle_event(ctx, evt)`
* `stop(ctx)`
* `detach()`

Errors are isolated and converted into `process.error`.

## Interfaces

Interfaces are processes by role.

They typically:

* Translate external input (HTTP, CLI, UI, network) into `Message`s
* Present system state outward

They follow the same lifecycle as processes but are registered separately for clarity.

## Services

Services are supervised, time-driven components.

They:

* Run in dedicated threads
* Execute `tick(ctx)` on an interval
* May restart automatically
* May be marked `critical`

Execution model:

```
start()
loop:
    tick()
    sleep(interval)
stop()
```

Supervisor messages:

* `service.started`
* `service.stopped`
* `service.error`
* `service.restart`
* `service.failure`

Critical failures can halt the supervisor.

## State

The `StateStore` is:

* Thread-safe
* Hierarchical
* Dot-path addressable

Example:

```python
ctx.state.set("system.clock.uptime", 42)
value = ctx.state.get("system.clock.uptime")
```

It intentionally provides:

* No schema
* No persistence
* No policy

It is coordination state — not storage.

## Clock Abstraction

Time is abstracted via `ClockProtocol`.

Default: `SystemClock`

Provides:

* `now_utc()`
* `monotonic()`
* `sleep(seconds, cancel=Event)`

Custom clocks (simulated, deterministic, test clocks) can be injected.

# Runtime Variants

### `Runtime`

Standard synchronous kernel.

### `ThreadedRuntime`

Owns a background execution thread.
Provides `.run()` which blocks until shutdown.

### `SignalRuntime`

Adds POSIX signal supervision:

* `SIGINT` → shutdown
* `SIGTERM` → shutdown
* `SIGHUP` → reload
* `SIGUSR1`, `SIGUSR2` → user-defined message events

Signals are converted into typed system messages.

# Design Principles

* **Authoritative dispatch** — only the runtime routes messages.
* **Typed contracts over inheritance depth**
* **Infrastructure replaceable by protocol**
* **Explicit lifecycle ordering**
* **Failure isolation**
* **mypy --strict compatibility**

# What BussDCC Is

* A cybernetic coordination kernel
* A durable event-driven runtime
* Suitable for:

  * IoT systems
  * Robotics
  * Hardware control
  * Automation engines
  * Control planes
  * Edge services

# What BussDCC Is Not

* Not Django
* Not FastAPI
* Not Celery
* Not a rules engine
* Not a persistence layer
* Not a distributed system

It is the thing you build those systems on top of.

# Status

**Alpha**

Core architecture is stabilizing.
APIs may evolve, but the dispatch model and lifecycle ordering are solidifying.

# Installation

```bash
pip install bussdcc
```

Requires Python 3.11+

# License

MIT License


> Durable systems start with explicit contracts, supervised execution, and honest failure boundaries.
