# OBS_director — Original Prompts

Append-only log of the user's original prompts, verbatim, most recent last. Appended by the
`documenter` agent after each change is implemented.

## 2026-09-02 — Set up the coordinator agent workflow

> I want to create a director tool for OBS. This is mainly divided into 2 parts:
> * one called `screen` that is a transparent screen that I can add to an OBS scene so that I
>   can make visual effect appear while I am recording (OBS lets a browser window being
>   overlapped on the screen to create the scene)
> * one called `admin` in which there are a lot of tools to create visual effects to appear on
>   the `screen`
> This is a python application that is generating a web page that I can access through a
> browser or with OBS.
>
> To setup this new project, I need the following Claude agents:
> * a coordinator - this is what I call every time I need to implement something new
>     * a product owner - this uses the document `./docs/product.md` and analyse the new
>       changes and produce a Product briefing with all the product details and how the new
>       changes would impact the product in detail. It also generates acceptance criteria and
>       questions
>     * an architect - this uses the document `./docs/architecture.md` and analyse the new
>       changes and produce an Architecture briefing with all the architecture details and how
>       the new changes would impact the architecture of the code in detail. It also produces
>       mermeid diagrams and questions
>     * a developer - this uses the document `./docs/code.md` and analyse the new changes and
>       produce a code change briefing with all the code changes details and how the new
>       changes would impact the previous code in detail. It also generates questions
>     * a tester - this uses the document `./docs/code.md` and analyse the new changes and
>       produce a test plan. It also generates questions
> * after getting an input from every other agent, the coordinator generates a plan with the
>   details of the change in the form of
> ```
> # <TITLE OF THE CHANGE> - <DATETIME>
> ## Context of the changes
> <product owner input>
> ## Architectural Impact
> <architect input>
> ## Code changes
> <developer input>
> ## Testing information
> <tester input>
>
> # Deep Dives
> <Most important questions>
> ```
> * the coordinator estimates if there is any need of asking questions to the user. It uses
>   only questions from the other agents. If possible, it answer itself questions using the
>   input of the other agents
> * the coordinator asks an advisor to estimate if the plan makes sense, if there are other
>   questions to ask to the user, and if that is the case, it asks these questions
> * then the coordinator start the following two agent, in this order
>     * the implementer: this takes the plan and implements it, silently
>     * the documenter: takes the plan and updates all the documents: 1. `./docs/product.md`,
>       2. `./docs/architecture.md`, 3. `./docs/code.md`, 4. `./docs/plans.md` (by appending the
>       last plan to the file), 5. `./docs/original_prompts.md` with all the user prompts (this
>       included)
>
> This is the first task for you. Feel free to ask my any question to clarify, but don't do
> that if it is not strictly needed for solving ambiguities
