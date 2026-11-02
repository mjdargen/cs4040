// Print layout shared by every cheat sheet (loaded in the header, before
// Quarto's template): landscape letter, compact text and code.
#set page(flipped: true)
#set par(justify: false)
// keep every code block and table in one piece (never split across columns/pages)
#set block(breakable: false)
#show heading.where(level: 2): it => block(above: 0.9em, below: 0.4em, text(size: 10.5pt, weight: "bold", it.body))
#show raw.where(block: true): set text(size: 7.4pt)
#show raw.where(block: true): set par(justify: false)
#show raw.where(block: true): it => block(spacing: 0.5em, breakable: false, it)
