# Roadmap

Each phase ships something real. Nothing here is installable yet.

## P0 - prototype (done)

Python, server rendered. Four page layouts, twelve questions in one batched
call, deterministic assembly. Proved every stage of the loop except measurement,
and produced the latency numbers quoted on the site.

Done means: it runs, a free-text shopper description produces a page no
preset produces, and the numbers are measured rather than estimated.

## P1 - core and react (next)

`@decided-ui/core` and `@decided-ui/react`.

The four primitives, the question compiler, typed answers, and the default
assembler policy: confidence floor, presence threshold, stable rank sort,
structural caps, fall back to declared defaults. Plus the React renderer:
provider, `<Slot>`, `useDecision()`.

Driven by a mock decider, so the whole phase runs with no API key and no
network and is fully unit testable.

Done means: `npm install`, define a spec, render a page whose variants change
when you hand the mock decider different answers, with types catching a renamed
variant at build time.

## P2 - the server adapter

`@decided-ui/next`.

Route handler and App Router server action, real decisions against a live
model, key handling, and an answer cache keyed on the state fields the spec
actually references.

Done means: a Next.js app makes one real call per uncached visitor and the key
never reaches the browser.

## P3 - measurement

`@decided-ui/amplitude` and the `Tracker` interface in core.

One impression per slot per decision, fired on mount and never on re-render.
Conversions stamped with the active decision id so they join back to variants.

Done means: a funnel in Amplitude can answer "which variant of this slot
converted better" without any custom instrumentation.

## P4 - the example and the docs

The storefront prototype ported to React as a real example app, and the site
becomes the documentation rather than a pitch.

Done means: someone can clone the example, add their own key, and have a
decided page running in under ten minutes.
