# Course materials: how-to guide (teacher notes)

Everything for CS4040 lives in this one repository. The slides, cheat sheets
and (later) Codio lessons are plain-text `.qmd` files built with
[Quarto](https://quarto.org). They quote the real example programs at the top
of the repo and use the real asset folders, so code and images are never
copied and pasted.

**Contents:** [How it fits together](#how-it-fits-together) ·
[One-time setup](#one-time-setup) · [Everyday commands](#everyday-commands) ·
[Add a module](#add-a-new-module) · [Slide decks](#slide-decks) ·
[Cheat sheets](#cheat-sheets) · [Quoting code](#quoting-code-and-reusing-text) ·
[Build and publish the website](#build-and-publish-the-website) ·
[Codio lessons](#codio-lessons) · [Build the Codio assignment](#build-the-codio-assignment) ·
[Bring it into Codio](#bring-it-into-codio) · [Updating Codio later](#updating-codio-later) ·
[Private files](#private-files) · [Themes](#themes) · [When something breaks](#when-something-breaks)

---

## How it fits together

```text
cs4040/                         repo root: run every program from here
  e00starter.py … e18*.py       examples (public; students get these)
  l01.py, p3.py, project*.py…   lab/project solutions (PRIVATE: ignored by git)
  images/ sounds/ music/ sprites/ fonts/ maps/    the one copy of every asset
  utils/                        update.py (students' setup tool) and asset tools
  _private/                     PRIVATE: Codio questions with answers, keys
  _quarto.yml                   website: what gets built, sidebar, themes
  _variables.yml                course name, site address, doc links
  index.qmd                     the website's home page
  course/
    README.md                   this guide
    u3m1/ … u5m1/               one folder per module
      u3m1-slides.qmd           the slide deck
      u3m1-cheatsheet.qmd       the cheat sheet (web page + PDF)
      code/                     small runnable programs the slides/cheat sheet quote
      concepts/                 paragraphs shared by the slides and cheat sheet
      media/                    pictures for the slides/cheat sheet
      content/  labs/  codio/   (only once a module has Codio lessons)
    shared/
      concepts/                 paragraphs used by every module (game loop, imports…)
      styles/                   slides.scss (slides), cheatsheet.typ (PDF layout)
      templates/                starter.py, Codio settings, assignment.example.toml
    tools/
      course_filter.py          runs during every build (code quoting, Codio markup)
      build_codio.py            makes Codio assignment zips
      check_private.py          the commit check that keeps private files off GitHub
```

| You run | It makes | Goes to |
|---|---|---|
| `quarto render` | website, slides, cheat sheets (web + PDF) | `_build/site/` |
| `quarto publish gh-pages` | publishes `_build/site` | <https://dargen.io/cs4040/> |
| `python course/tools/build_codio.py` | one zip per Codio assignment | `_build/codio/` |
| students run `python3 update.py …` | newest examples/assets from GitHub `main` | their workspace or Codio box |

Module folders are named `u<unit>m<module>`: `u3m1` = Unit 3, Module 1. Every
file in a module starts with that name (`u3m1-slides.qmd`), so downloaded
files and browser tabs say which module they belong to.

## One-time setup

1. Install [Quarto](https://quarto.org/docs/get-started/) (free, open source).
   It includes everything for HTML, slides and PDFs; no LaTeX needed.
2. In VS Code, install the **Quarto** extension (preview button, syntax help).
3. Python 3.11 or newer (the tools use only the standard library).
4. In this folder, turn on the private-file check (once per clone):

   ```bash
   git config core.hooksPath .githooks
   ```

## Everyday commands

Run from the repo root:

```bash
quarto preview course/u3m2/u3m2-slides.qmd    # live preview; reloads when you save
quarto render                                 # build everything into _build/site
quarto render course/u3m2/u3m2-cheatsheet.qmd # build just one file
quarto publish gh-pages                       # put the built site online
python course/tools/build_codio.py            # build Codio zips (when there are any)
```

`_build/` and `.quarto/` are build output, ignored by git. Delete them any time.

## Add a new module

Example: Unit 5, Module 2, "Platformers".

1. **Make the folder** `course/u5m2/` with `u5m2-slides.qmd` and
   `u5m2-cheatsheet.qmd` (copy an existing module's two files and clear them
   out), plus `code/`, `concepts/` and `media/` as you need them.
   `quarto render` picks up any `course/*/*-slides.qmd` and
   `course/*/*-cheatsheet.qmd` automatically.
2. **Sidebar:** in `_quarto.yml`, under `website: sidebar: contents:`, copy
   another module's block:

   ```yaml
         - section: "U5M2 · Platformers"
           contents:
             - text: "Slides"
               href: course/u5m2/u5m2-slides.qmd
             - text: "Cheat sheet"
               href: course/u5m2/u5m2-cheatsheet.qmd
   ```
3. **Home page:** add a row to the table in `index.qmd`.
4. **Students' README:** add a row to the table in the top-level `README.md`
   (links are `https://dargen.io/cs4040/course/u5m2/u5m2-slides.html`,
   `…-cheatsheet.html` and `…-cheatsheet.pdf`).
5. `quarto render`, check it, `quarto publish gh-pages`, commit and push.

## Slide decks

`course/<module>/<module>-slides.qmd`. Builds a reveal.js deck (HTML, what you
present) and a `.pptx` (rough; for when you need PowerPoint).

````markdown
---
title: "Platformers"
subtitle: "{{< var course.code >}} · Unit 5: Advanced Games"
format:
  revealjs: default
  pptx: default
---

# Gravity                         ← "#" = section title slide

## Falling                        ← "##" = a new slide, this is its title

- Bullet points
- **bold**, `code`, [links](https://example.com)

Code quoted from a file (see "Quoting code"):

```{.python include="code/gravity.py" snippet="fall"}
```

::: notes
Speaker notes: only you see these (press S while presenting).
:::

## Two columns

:::: {.columns}
::: {.column width="50%"}
Left side
:::
::: {.column width="50%"}
![](media/jump.png)
:::
::::
````

Useful pieces:

| You want | Write |
|---|---|
| Bullets appear one at a time | `::: {.incremental}` … `:::` around the list |
| Shrink one long code block | `::: {.code-small}` … `:::` around it |
| Highlight lines 3–4 of a code block | add `code-line-numbers="3-4"` inside the `{…}` |
| An image that fills the slide | `![](media/x.png){.r-stretch}` |
| An image at a set width | `![](media/x.png){width=60%}` |
| A course-wide value | `{{< var course.code >}}`, `{{< var pgzero.docs >}}` (set in `_variables.yml`) |
| A shared paragraph | `{{< include concepts/_name.qmd >}}` |

Images for slides go in the module's `media/` folder. Sprites the code uses
come from the top-level `images/` folder, never copied.

Structure that has worked: a `#` section per big idea, one idea per `##` slide,
code on its own slide or beside one short explanation, and the docs link in
the speaker notes.

## Cheat sheets

`course/<module>/<module>-cheatsheet.qmd`. Builds a web page (with copy
buttons on the code) and a two-column landscape PDF for printing.

````markdown
---
title: "Platformers Cheat Sheet"
subtitle: "{{< var course.code >}} · Unit 5"
format:
  html:
    toc: true
    toc-depth: 2
  typst: default
---

::: {.content-visible when-format="html"}
Every code block has a copy button (top right). [Download the printable PDF](u5m2-cheatsheet.pdf).
:::

[Pygame Zero docs]({{< var pgzero.docs >}})

## Jumping: `actor.vy`          ← one "##" entry per thing students look up

One or two sentences: what it is and when to use it.

```{.python include="code/gravity.py" snippet="jump" dedent=4}
```
````

Rules that keep it working:

- **One `##` per entry**: a name students search for, a sentence or two, one
  short code block. The web page gets a table of contents from the `##`s.
- **Short code blocks.** The PDF never splits a code block across columns, so a
  long block leaves a big gap. Over ~15 lines, split it into two entries.
- **Comments on code lines** explain each line; students copy the code, and the
  comments come with it.
- The PDF layout (landscape, two columns, font sizes) is set once in
  `_quarto.yml` (`format: typst:`) and `course/shared/styles/cheatsheet.typ`.
- Explanation that also appears on a slide goes in `concepts/_name.qmd` and is
  included in both, so the two never disagree.

## Quoting code and reusing text

**Code comes from `.py` files, never pasted.** A code block with `include=`
is filled in at build time. Paths starting with `/` are from the repo root;
others are from the page's folder.

````markdown
```{.python include="/e03globalframe.py" def="update"}
```
```{.python include="/e04bouncing.py" from="# check rightmost part of Actor"}
```
```{.python include="/e05square.py" from="if state == 0:" to="state = 1"}
```
```{.python include="code/actor_basics.py" snippet="move"}
```
````

| Option | Shows |
|---|---|
| (none) | the whole file |
| `def="update"` | the whole function or class |
| `from="text"` | from the line containing `text` to the end of its block |
| `from="a" to="b"` | from the line containing `a` to the line containing `b` |
| `snippet="move"` | lines between `# start snippet move` and `# end snippet move` |
| `start-line=5 end-line=9` | a line range (breaks when the file changes; avoid) |
| `file-line-numbers="true"` | numbers the lines as they are in the file |

- **Quote the real examples** (`/e04bouncing.py`) when the slide is about that
  example. Use `def`/`from`/`to` so the example files stay clean.
- **Small demo programs** for one idea go in the module's `code/` folder. They
  must run on their own (`python course/u3m1/code/actor_basics.py`). These can
  use `snippet` markers; the markers never appear on a page.
- Indentation is removed automatically. If you change a file so the text or
  function is gone, the page shows `!! code not found` and the build prints a
  WARNING naming the page, so nothing breaks silently.

**Text you would otherwise retype** goes in a partial: a file whose name
starts with `_`, in the module's `concepts/` (or `course/shared/concepts/` if
every module uses it). Pull it in with `{{< include concepts/_tuples.qmd >}}`
or `{{< include /course/shared/concepts/_colors.qmd >}}`. Files starting with
`_` are never built on their own.

## Build and publish the website

```bash
quarto render              # everything → _build/site/  (open _build/site/index.html to check)
quarto publish gh-pages    # uploads _build/site to the gh-pages branch
```

`quarto publish gh-pages` puts only the built site on a separate `gh-pages`
branch; your `main` branch and your private files are never involved. The first
time, it asks to confirm; then in GitHub go to the repo's **Settings → Pages**
and set the source to the `gh-pages` branch, `/ (root)`. The site appears at
`https://mjdargen.github.io/cs4040/`, which your `dargen.io` domain serves as
<https://dargen.io/cs4040/>. Keep that address in `_variables.yml`
(`course.site`); Codio pages use it to link to the slides.

What gets built is listed under `render:` at the top of `_quarto.yml`. Right
now that's the home page, slides and cheat sheets.

## Codio lessons

None exist yet; the tools are ready. A module's Codio assignment is made of:

```text
course/u3m1/
  content/                 reading and example pages, in order
    _metadata.yml          (makes every page also build as Codio Markdown)
    00-overview.qmd
    01-example-0.qmd …
  labs/
    _metadata.yml
    l01-drawing/
      instructions.qmd     lab page
      demo.gif             media the page shows
  codio/
    assignment.toml        page order, Codio page ids, which file opens beside each page
_private/codio-assessments/u3m1/
  multiple-choice-365928436.json …   Check-It questions (contain answers; never pushed)
```

**1. Pages.** Each page is a normal `.qmd` with a `title:`. Number the files
so they sort in order. Put this `_metadata.yml` in `content/` and in `labs/`
so Quarto also makes the Markdown that Codio needs:

```yaml
format:
  html: default
  gfm:
    wrap: preserve
    from: markdown-smart
```

Write pages exactly like slides and cheat sheets: quote code with `include=`,
reuse `concepts/` partials, put images next to the page or in `media/`. Three
extra pieces of markup become Codio's own syntax on Codio and a readable
preview on the website:

```markdown
[Check It!]{.checkit id=multiple-choice-365928436}
[Install Pygame Zero Plus]{.codio-button run="python3 update.py pygame"}
[Slides]{.codio-embed href="../u3m1-slides.qmd"}
```

- `.checkit`: a Codio assessment, by its id.
- `.codio-button`: a button that runs a terminal command.
- `.codio-embed`: shows a page of the course website (e.g. the slides) inside Codio.

**2. Check-It questions** are written in Codio. To keep a copy (and use them
in a rebuilt assignment), export the assignment from Codio (**Project →
Export as Zip**). The questions are the files in `.guides/assessments/`. Copy
them into `_private/codio-assessments/<module>/`. The `id=` on the page is the
file name without `.json`.

**3. The assignment file.** Copy `course/shared/templates/codio/assignment.example.toml`
to `course/<module>/codio/assignment.toml` and fill it in: the title,
which examples students get (`examples = "/e0[0-5]*.py"`), lab starters, lab
solutions (private files, copied into `.guides/secure/` where only teachers
can see them), and one `[[page]]` per page in order. Each page has an `id`:
keep it the same forever so Codio keeps student progress when you rebuild.
For a new page, use any new UUID (in Python: `python -c "import uuid; print(uuid.uuid4())"`).
`open = "e04bouncing.py"` opens that file beside the page with the Graphics
Viewer; `terminal = true` opens a terminal.

**4. Turn it on.** In `_quarto.yml`, add the pages under `render:` and to the
module's sidebar section:

```yaml
  render:
    - …
    - "course/u3m1/content/*.qmd"
    - "course/u3m1/labs/*/instructions.qmd"
```

```yaml
          - section: "Lessons"
            contents:
              - auto: "course/u3m1/content/*.qmd"
          - section: "Labs"
            contents:
              - auto: "course/u3m1/labs/*/instructions.qmd"
```

and set `build = true` in its `assignment.toml`. (Leave a page out of
`render:` and it isn't built anywhere, not even as a draft. Set
`build = false` and `build_codio.py` skips the module.)

## Build the Codio assignment

```bash
quarto render                          # makes the Markdown versions of the pages
python course/tools/build_codio.py     # every module with build = true
python course/tools/build_codio.py course/u3m1   # just one
```

For each module it checks that every `.py` compiles, every Check-It id has a
question in `_private/`, every image exists and every page that opens a file
has that file. Anything wrong is listed as `PROBLEM:` and the script exits with
an error. The result is `_build/codio/<folder>/` and `_build/codio/<folder>.zip`
containing:

```text
.guides/content/      pages (.md) and Codio page settings (.json), index.json = order
.guides/img/          only the images/videos the pages use
.guides/assessments/  only the Check-It questions the pages use
.guides/secure/       lab solutions (teacher-only)
e00starter.py …       the examples, l01.py … starters, update.py, images/
.codio  .settings     Run button, Graphics Viewer, editor settings (from course/shared/templates/codio/)
```

## Bring it into Codio

First time, for a new assignment:

1. In Codio, open the course → **Edit Assignments** tab → in the module, **Add Assignment**.
2. Under **Select your Starting Point**, choose **Import**.
3. Pick a **Stack** with Python 3 (the same one your other Pygame Zero assignments use).
4. **Source:** choose **Zip file** and upload `_build/codio/<folder>.zip`.
5. Enter the name and description, then **Create**.
6. Open it, click through the pages (check the Graphics Viewer, Check-Its and
   buttons), then **Publish**. Students can't see it until it is published.

## Updating Codio later

There are two kinds of updates, and they travel differently.

**Examples and assets (most updates): students pull them.** `update.py` in
every Codio box downloads the newest files from this repo's `main` branch on
GitHub. So: fix an example or add images → commit and push to GitHub → students
click a button on a page (or run it in the terminal):

```markdown
[Get the latest examples]{.codio-button run="python3 update.py examples"}
[Get the latest images]{.codio-button run="python3 update.py assets"}
```

This works for students who already started, and never needs a re-publish.
(It overwrites the example files, so students should do their own work in
their lab files, not in the examples.)

**Pages, questions and settings: you re-publish.**

1. Edit the `.qmd` pages, then `quarto render` and `python course/tools/build_codio.py`.
2. In Codio, open the course → **Edit Assignments** → open the assignment.
3. Upload the new zip into the file tree (drag it in), then in the terminal:

   ```bash
   unzip -o pygame-zero-basics.zip && rm pygame-zero-basics.zip
   ```

   (`-o` replaces the old files. If you removed a page, also delete its two
   files from `.guides/content/`.)
4. **Publish**, and write what changed in the **Change Log**.

Once students have started an assignment, Codio warns you and won't replace
files they already have, because that would wipe their work; new files are
added. Resetting a student (course **Overview** → the assignment → the
student's **⋯** → **Reset**) gives them the new version but erases their work.
After publishing a change, open the assignment as a test student to check what
students see.

**Later, if you want one command instead of uploading.** Codio has an API for
publishing a zip to an existing assignment (your Codio admin creates a key
under **Organization → Integrations**; Codio's `codio-api-js` package and
`codio-assignment-publish-action` use it). A GitHub Action can't build these
zips, because the private files aren't on GitHub, so it would run from your
computer. See Codio's docs:
[modify assignments](https://docs.codio.com/instructors/setupcourses/modify-assignments.html),
[publishing with the API](https://docs.codio.com/common/develop/ide/tools/ghapi.html).

## Private files

The repo is public; private files stay on this computer only:

| Private thing | Where / how it is named | Kept out of git by |
|---|---|---|
| Lab solutions, in-class activities, experiments | top-level `l*.py`, `ica_*.py`, `exp_*.py`, `_*.py` | `.gitignore` |
| Project solutions | top-level `p2*.py` … `p5*.py`, `project*.py` | `.gitignore` |
| Codio questions (contain answers), answer keys | `_private/` | `.gitignore` |
| Any other file | add a line `# PRIVATE` to it | the commit check |

The commit check (`course/tools/check_private.py`, turned on in
[One-time setup](#one-time-setup)) runs on every `git commit` and stops it if
it would publish a private file, even one added with `git add -f`.

Because these files are not on GitHub, back them up some other way (OneDrive
already does, since the repo lives there).

Careful with names: a new public file whose name matches a pattern above is
silently left out of git. `git status` shows what will be committed; if a file
you expect isn't listed, check `git check-ignore -v <file>`.

## Themes

Set once in `_quarto.yml` for everything: slides use reveal.js `dracula` plus
`course/shared/styles/slides.scss`; the website uses `flatly` (light) and
`darkly` (dark), a matched pair that follows the student's light/dark setting;
the PDF cheat sheets stay light for printing
(`course/shared/styles/cheatsheet.typ`). To try another theme, change the name
and re-render (slides: `dark`, `night`, `moon`, `league`, `blood`…; website:
any [Bootswatch](https://bootswatch.com/) name).

## When something breaks

| You see | Do this |
|---|---|
| `!! code not found` on a page, WARNING in the build | the quoted text or function changed in the `.py`; update the `from=`/`to=`/`def=` |
| A page or image missing from the site | is it under `render:` in `_quarto.yml`? is the path right (case matters online)? |
| Build fails on a `.qmd` | the error names the file and line; often an unclosed `:::` or code fence |
| PDF cheat sheet has a big gap | a code block is too long to fit in the column; split it |
| `build_codio.py` says `PROBLEM:` | it names the page and the missing image, question or file |
| Commit refused with "Commit stopped" | you're committing a private file; the message names it |
| Changes don't show online | re-run `quarto render` then `quarto publish gh-pages`; refresh with Ctrl+F5 |

See `REVIEW-NOTES.md` for fixes made while converting the original slides and
cheat sheets, and open questions.
