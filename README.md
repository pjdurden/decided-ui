# decided-ui

**The model chooses among interfaces you wrote.** Not generated markup: named
variants, type-checked against your components, and measured so you learn which
one actually won.

Read the full writeup: **https://pjdurden.github.io/decided-ui/**

## Status

Design and working prototype. The loop is proven end to end in a Python
prototype and the measurements on the site are real. **The TypeScript framework
described here is not built yet.** Nothing is installable today. See
[ROADMAP.md](ROADMAP.md).

## Documentation

| Page | |
| --- | --- |
| [Overview](https://pjdurden.github.io/decided-ui/) | the idea, the loop, the prototype |
| [Concepts](https://pjdurden.github.io/decided-ui/concepts.html) | slots, primitives, criteria, decisions, gating |
| [Spec API](https://pjdurden.github.io/decided-ui/spec.html) | `defineSpec`, `variant`, `presence`, `rank`, `intensity` |
| [Architecture](https://pjdurden.github.io/decided-ui/architecture.html) | packages, request lifecycle, caching, failure behaviour |
| [Jev](https://pjdurden.github.io/decided-ui/jev.html) | the decision engine, and why not an LLM |
| [Measurement](https://pjdurden.github.io/decided-ui/measurement.html) | the `Tracker` contract and closing the loop |
| [Comparison](https://pjdurden.github.io/decided-ui/comparison.html) | against generative UI, A/B tests, flags, personalisation |
| [Roadmap](https://pjdurden.github.io/decided-ui/roadmap.html) | phases, and what done means for each |

## The idea in one comparison

Generative UI has the model write the interface. That costs seconds, has to be
validated before it can render, and produces something different every time, so
there is nothing to compare and nothing to learn.

Decided UI has the model pick among variants you already built. One round trip.
It cannot produce an interface that does not exist. And because every choice has
a name, you can ask which name converted better.

That last point is the argument. A generated interface cannot be A/B tested even
in principle, because the thing it produced will never be produced again. A
decided interface is a variant with an id, which every analytics tool already
knows how to count.

## What you write

1. **Define the spec.** Slots, their variants, and a plain-English criterion per
   variant. The criterion is both the documentation and the question the model
   is asked.
2. **Write the components.** Ordinary React, one per variant. Nothing in them
   knows a model exists.
3. **Write the assembler, or skip it.** Confidence floors, caps, ordering,
   fallbacks. A working default ships.
4. **Wire the decider.** One line in a route handler. The key stays server side.
5. **Read the results.** Impressions and conversions land in your analytics tool
   joined by a decision id.

Decisions are made by [Jev](https://typesafe.ai), TypeSafe's System One model, which
returns typed answers with calibrated probabilities rather than text. One call answers
every question about a visitor in parallel.

## Four primitives

| Primitive | The question it asks |
| --- | --- |
| `variant()` | which version of this component |
| `presence()` | should this appear at all |
| `rank()` | what order should these go in |
| `intensity()` | how strongly, along a described scale |

Page layout is not a fifth primitive. It is a `variant()` whose chosen value
becomes a class name rather than a component.

## What this is not

Not an experimentation platform: it emits events and leaves assignment, storage
and reporting to the tool you already pay for. Not a component library: you
write the components. Not a way to avoid design work: someone still has to build
every variant, and writing criteria that genuinely discriminate is the real
labour.

## Building the docs

The site is generated from fragments so the nav and sidebar cannot drift:

    python3 docs/_build.py

Edit `docs/_content/<page>.html`, rebuild, and commit both.

## Licence

MIT. See [LICENSE](LICENSE). Site assets are credited in
[docs/CREDITS.md](docs/CREDITS.md).
