# AI Creative Studio -- Multi-Agent Instagram Campaign Generation

## Overview

I built a distributed, multimodal **Multi-Agent Creative Studio** that
transforms a campaign brief into a complete Instagram campaign.

The system uses **Google Agent Development Kit (ADK)**, **Agent-to-Agent
(A2A) communication**, **Model Context Protocol (MCP)**, Gemini models,
Google Cloud Run, Google Cloud Storage, and Gemini Enterprise Agent
Platform Runtime.

Rather than relying on one agent to perform every task, the solution is
designed as a team of specialized AI agents. Each agent has a clearly
defined responsibility and can operate as an independent service.

The **Creative Director** is the central orchestrator. It coordinates
the specialist agents, carries campaign context through the workflow,
interprets quality-review feedback, and routes revision requests to the
appropriate specialist.

------------------------------------------------------------------------

## Architecture

The solution consists of six specialized agents:

  -----------------------------------------------------------------------
  Agent                   Platform                Responsibility
  ----------------------- ----------------------- -----------------------
  Brand Strategist        Cloud Run               Researches target
                                                  audiences, competitors,
                                                  market trends, and
                                                  strategic insights
                                                  using Google Search

  Copywriter              Cloud Run               Creates three Instagram
                                                  caption variations
                                                  using reusable ADK
                                                  Skills

  Designer                Cloud Run               Creates visual concepts
                                                  and generates campaign
                                                  images using Gemini

  Critic                  Cloud Run               Reviews captions and
                                                  generated visuals and
                                                  returns structured
                                                  quality feedback

  Project Manager         Cloud Run               Creates the campaign
                                                  timeline and tasks,
                                                  with optional Notion
                                                  integration through MCP

  Creative Director       Gemini Enterprise Agent Orchestrates the
                          Platform Runtime        workflow and
                                                  communicates with
                                                  specialist agents over
                                                  A2A
  -----------------------------------------------------------------------

Each specialist is independently deployed and exposed through an **A2A
agent interface**. The Creative Director discovers and invokes these
remote agents rather than embedding their implementations directly
inside the orchestrator.

------------------------------------------------------------------------

## Multi-Agent Workflow

A user provides a campaign brief to the Creative Director, which
coordinates the end-to-end workflow.

``` mermaid
flowchart TD
    USER[User Campaign Brief]
    CD[Creative Director<br/>Orchestrator]
    BS[Brand Strategist<br/>Audience & Market Research]
    CW[Copywriter<br/>Instagram Captions]
    DS[Designer<br/>Image Generation]
    CR[Critic<br/>Quality Review]
    ROUTE{Revision Required?}
    PM[Project Manager<br/>Campaign Timeline]

    USER --> CD

    CD --> BS
    BS --> CD

    CD --> CW
    CW --> CD

    CD --> DS
    DS --> CD

    CD --> CR
    CR --> ROUTE

    ROUTE -->|APPROVED| PM
    ROUTE -->|NEEDS_REVISION| CD

    CD -->|Copy issue| CW
    CD -->|Visual issue| DS
    CD -->|Copy + visual issues| CW
    CD -->|Copy + visual issues| DS

    CW --> CD
    DS --> CD
    CD --> CR

    PM --> CD
    CD --> USER
```

The high-level execution flow is:

1.  **Campaign Brief** -- The user provides the campaign idea, goals,
    and target audience.
2.  **Research** -- The Brand Strategist researches the audience,
    competitors, and current market trends.
3.  **Copy Generation** -- The Copywriter uses the research to generate
    three distinct Instagram caption options.
4.  **Visual Generation** -- The Designer creates matching visual
    concepts and generates campaign images.
5.  **Quality Review** -- The Critic evaluates the copy, visuals, and
    overall campaign alignment.
6.  **Revision Loop** -- If the Critic returns `NEEDS_REVISION`, its
    feedback returns to the Creative Director. The Creative Director
    determines which specialist should revise the work---for example,
    the Copywriter for copy issues, the Designer for visual issues, or
    both when necessary.
7.  **Re-review** -- Revised output is sent back to the Critic for
    another quality review.
8.  **Campaign Planning** -- Once the Critic returns `APPROVED`, the
    Project Manager creates the campaign timeline and task plan.
9.  **Final Campaign** -- The Creative Director assembles the research,
    captions, images, review result, and project plan into the final
    response.

------------------------------------------------------------------------

## Agent-to-Agent (A2A) Architecture

A key architectural feature is that the specialist agents are **not
simply Python functions running inside the Creative Director
application**.

Each specialist runs as an independent service with its own endpoint.
The Creative Director communicates with these services using the **A2A
protocol**.

``` text
                         User
                           │
                           ▼
                 ┌─────────────────┐
                 │ Creative        │
                 │ Director        │
                 │ Orchestrator    │
                 └────────┬────────┘
                          │
                          │ A2A
          ┌───────────────┼────────────────┐
          │               │                │
          ▼               ▼                ▼
   Brand Strategist   Copywriter       Designer
      Cloud Run        Cloud Run       Cloud Run
          │               │                │
          └───────────────┼────────────────┘
                          │
                          │ A2A
                    ┌─────┴─────┐
                    ▼           ▼
                  Critic    Project Manager
                Cloud Run      Cloud Run
```

This distributed design allows specialist agents to be developed,
deployed, updated, and scaled independently while the Creative Director
coordinates them as one application.

------------------------------------------------------------------------

## Brand Strategist

The Brand Strategist is responsible for **research and strategy**.

It is configured to:

-   Research the target audience using Google Search
-   Identify audience demographics, behaviors, interests, needs, and
    pain points
-   Analyze relevant competitors
-   Research current market trends
-   Produce strategic insights for downstream agents
-   Keep research current by incorporating the current year into search
    queries

The Brand Strategist intentionally does **not** generate captions or
visual designs. Its output becomes the research foundation for
downstream creative work.

------------------------------------------------------------------------

## Copywriter

The Copywriter receives the Brand Strategist's research and transforms
it into Instagram-ready content.

The agent generates:

-   Three distinct caption variations
-   Different tones and messaging approaches
-   Strong opening hooks
-   Calls to action
-   Relevant hashtags

I also integrated **ADK Skills** so reusable copywriting knowledge can
be maintained separately from the agent's primary instructions.

This keeps reusable expertise modular instead of placing every
copywriting rule inside one large system prompt.

------------------------------------------------------------------------

## Designer

The Designer converts campaign concepts into visual assets.

The Designer uses a tool-based architecture: the agent develops the
visual concept and image-generation prompt, while a dedicated
image-generation tool invokes a Gemini image model.

Generated images are uploaded to **Google Cloud Storage**, and the
Designer returns the corresponding `gcs_uri`.

``` text
Designer Agent
     │
     ▼
Creates image concept + prompt
     │
     ▼
Image Generation Tool
     │
     ▼
Gemini Image Model
     │
     ▼
Generated Image
     │
     ▼
Google Cloud Storage
     │
     ▼
gcs_uri
```

This allows downstream agents, particularly the Critic, to access
generated visuals without passing large raw image payloads between
agents.

------------------------------------------------------------------------

## Critic and Quality Gate

The Critic acts as the automated quality-control layer of the system.

It reviews:

-   Instagram copy
-   Generated campaign visuals
-   Alignment between strategy, copy, and visual content

The Critic returns a structured verdict:

``` text
APPROVED
```

or:

``` text
NEEDS_REVISION
```

When revision is required, the Critic identifies the issue that needs to
be corrected and provides feedback.

The Critic does **not** directly decide which specialist to invoke. Its
verdict and feedback return to the **Creative Director**, which
interprets the feedback and routes the revision to the appropriate
specialist.

For example:

-   Copy or messaging issue → **Copywriter**
-   Visual or image issue → **Designer**
-   Copy and visual issues → **both specialists as needed**

After revision, the Creative Director sends the updated campaign back to
the Critic for another review.

------------------------------------------------------------------------

## Automatic Revision Loop

A major feature of the system is its automated quality and revision
loop.

``` text
                 Copy + Images
                      │
                      ▼
                    Critic
                      │
                      ▼
              ┌───────────────┐
              │    Verdict    │
              └───────┬───────┘
                      │
             ┌────────┴─────────┐
             │                  │
         APPROVED        NEEDS_REVISION
             │                  │
             ▼                  ▼
     Project Manager      Creative Director
                                │
                         interprets feedback
                                │
                    ┌───────────┴───────────┐
                    ▼                       ▼
               Copywriter               Designer
                    │                       │
                    └───────────┬───────────┘
                                ▼
                         Creative Director
                                │
                                ▼
                              Critic
```

The campaign does not proceed to the Project Manager until the Critic
approves the work.

This creates an automated feedback loop in which the Critic evaluates
quality and the Creative Director handles revision routing and
orchestration.

------------------------------------------------------------------------

## Project Manager and MCP

After the campaign passes the quality gate, the Project Manager converts
the approved campaign into an actionable execution plan.

The Project Manager generates:

-   Campaign timeline
-   Tasks
-   Deliverables
-   Execution plan

The system also supports optional **Notion integration using Model
Context Protocol (MCP)**.

MCP allows the Project Manager to interact with Notion through a
standardized tool interface rather than requiring a custom Notion
integration directly inside the agent.

If Notion is unavailable, the Project Manager can still generate the
complete text-based campaign plan.

------------------------------------------------------------------------

## Technology Stack

  Layer                            Technology
  -------------------------------- ------------------------------------------
  Language                         Python 3.11 / 3.12
  Agent Framework                  Google Agent Development Kit (ADK)
  Agent Communication              A2A Protocol
  LLM                              Gemini on Vertex AI
  Image Generation                 Gemini Image Model
  External Tool Integration        Model Context Protocol (MCP)
  Specialist Deployment            Google Cloud Run
  Orchestrator Runtime             Gemini Enterprise Agent Platform Runtime
  Image Storage                    Google Cloud Storage
  Secrets                          Google Secret Manager
  Project Management Integration   Notion via MCP
  Dependency Management            uv

------------------------------------------------------------------------

## Project Structure

``` text
Multi-Agent-Creative-Studio/
├── agents/
│   ├── brand_strategist/
│   ├── copywriter/
│   │   └── skills/
│   ├── creative_director/
│   ├── critic/
│   ├── designer/
│   └── project_manager/
│
├── deploy/
│   ├── deploy_all_specialists.py
│   ├── deploy_orchestrator.py
│   ├── env_utils.py
│   └── teardown_gcp.sh
│
├── .env.example
├── .gitignore
├── google_setup.py
├── LICENSE
├── pyproject.toml
├── README.md
├── run_campaign.py
├── setup_inspector.sh
└── uv.lock
```

Each specialist agent has its own implementation, configuration,
dependencies, prompts, and tools as needed.

The `agents/creative_director/` package contains the orchestration layer
responsible for coordinating remote specialist agents and managing the
Critic-driven revision loop.

The `deploy/` directory contains deployment utilities for the specialist
services and orchestrator.

Local runtime artifacts, the virtual environment, and secrets such as
`.venv/`, `.adk/`, and `.env` are intentionally excluded from source
control.

------------------------------------------------------------------------

## Running Locally

Create the local environment from the project lockfile:

``` bash
uv sync
```

Activate the virtual environment:

``` bash
source .venv/bin/activate
```

Create your local environment configuration from the example file and
provide the required project-specific values:

``` bash
cp .env.example .env
```

Start the ADK development UI from the repository root:

``` bash
uv run adk web agents
```

Use the ADK web interface to select and test the available agents.

> Do not commit `.env`, credentials, or other secrets. Only
> `.env.example` should be used as the source-controlled configuration
> template.

------------------------------------------------------------------------

## Key Concepts Demonstrated

Through this project, I implemented and explored several Agentic AI
architecture patterns:

-   Multi-agent orchestration
-   Specialized AI agents
-   LLM-driven orchestration
-   Agent-to-Agent (A2A) communication
-   Remote agents as tools
-   Context propagation between agents
-   Multimodal AI workflows
-   Tool-based image generation
-   Automated quality gates
-   Critic-driven revision loops
-   Dynamic revision routing by the orchestrator
-   ADK Skills
-   Model Context Protocol (MCP)
-   Cloud-native agent deployment
-   Independent agent services
-   Retry and error-handling patterns

------------------------------------------------------------------------

## Reliability

Because the solution consists of distributed AI services, I incorporated
reliability considerations including:

-   Retry policies for transient failures
-   Backoff strategies
-   Tool error handling
-   Graceful handling of optional Notion integration failures
-   Configurable model and deployment settings
-   Environment-based configuration rather than hard-coded
    infrastructure values

------------------------------------------------------------------------

## What I Learned

This project helped me understand an important distinction between
building an individual AI agent and building an **agentic system**.

The primary challenge is not simply prompting individual models. It is
designing how specialized agents:

-   discover each other,
-   communicate,
-   exchange context,
-   use external tools,
-   generate multimodal outputs,
-   evaluate each other's work,
-   route and respond to revision feedback,
-   recover from failures, and
-   coordinate toward a single business outcome.

The Creative Director provides the orchestration layer, while the
specialist agents remain independently deployable services connected
through A2A.

The Critic provides the quality gate, but the Creative Director remains
responsible for orchestration: when the Critic returns `NEEDS_REVISION`,
the Creative Director interprets the feedback and determines whether the
Copywriter, Designer, or both should revise their work before another
review.

This architecture demonstrates how multiple specialized AI capabilities
can be composed into a complete end-to-end workflow rather than
implemented as one monolithic agent.
