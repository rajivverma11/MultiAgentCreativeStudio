# AI Creative Studio – Multi-Agent Instagram Campaign Generation

## Overview

I built a distributed, multimodal **Multi-Agent Creative Studio** that transforms a simple campaign brief into a complete Instagram campaign.

The system uses **Google Agent Development Kit (ADK)**, **Agent-to-Agent (A2A) communication**, **Model Context Protocol (MCP)**, Gemini models, Google Cloud Run, and Gemini Enterprise Agent Platform Runtime.

Instead of relying on a single agent to perform every task, I designed the solution as a team of specialized AI agents. Each agent has a clearly defined responsibility and runs as an independent service.

The **Creative Director** acts as the orchestrator, coordinating the specialist agents and carrying context through the entire campaign workflow.

---

## Architecture

The solution consists of six specialized agents:

| Agent | Platform | Responsibility |
|---|---|---|
| Brand Strategist | Cloud Run | Researches target audiences, competitors, market trends, and strategic insights using Google Search |
| Copywriter | Cloud Run | Creates three Instagram caption variations using reusable ADK Skills |
| Designer | Cloud Run | Creates visual concepts and generates real campaign images using Gemini |
| Critic | Cloud Run | Reviews captions and generated visuals and provides structured quality feedback |
| Project Manager | Cloud Run | Creates the campaign timeline and tasks, with optional Notion integration through MCP |
| Creative Director | Gemini Enterprise Agent Platform Runtime | Orchestrates the complete workflow and communicates with specialist agents over A2A |

Each specialist is independently deployed and exposed through an **A2A agent interface**. The Creative Director discovers and invokes these agents remotely rather than embedding their implementation directly into the orchestrator.

---

## Multi-Agent Workflow

A user provides a single campaign brief to the Creative Director.

The Creative Director then coordinates the complete campaign generation process:

```mermaid
flowchart TD
    USER[User Campaign Brief]

    CD[Creative Director<br/>Orchestrator]

    BS[Brand Strategist<br/>Audience & Market Research]

    CW[Copywriter<br/>Instagram Captions]

    DS[Designer<br/>Image Generation]

    CR[Critic<br/>Quality Review]

    PM[Project Manager<br/>Campaign Timeline]

    REV{Approved?}

    USER --> CD
    CD --> BS
    BS --> CD

    CD --> CW
    CW --> CD

    CD --> DS
    DS --> CD

    CD --> CR
    CR --> REV

    REV -->|YES| PM
    REV -->|NO| CD

    PM --> CD
    CD --> USER
```

The high-level execution flow is:

1. **Campaign Brief** – The user provides the campaign idea and target audience.
2. **Research** – The Brand Strategist researches the audience, competitors, and current market trends.
3. **Copy Generation** – The Copywriter uses the research to generate three distinct Instagram captions.
4. **Visual Generation** – The Designer creates matching visual concepts and generates real campaign images.
5. **Quality Review** – The Critic evaluates both the captions and generated images.
6. **Revision Loop** – If the Critic returns `NEEDS_REVISION`, the Creative Director routes the feedback back to the appropriate specialist and requests another review.
7. **Campaign Planning** – Once the campaign receives `APPROVED`, the Project Manager creates the campaign timeline and task plan.
8. **Final Campaign** – The Creative Director assembles the research, captions, images, review results, and project plan into the final response.

---

## Agent-to-Agent (A2A) Architecture

One of the key parts of this project is that the specialist agents are **not Python functions running inside the Creative Director application**.

Each specialist runs as an independent service with its own endpoint.

The Creative Director communicates with them using the **A2A protocol**.

```text
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
     Cloud Run        Cloud Run        Cloud Run
          │               │                │
          └───────────────┼────────────────┘
                          │
                          │ A2A
                    ┌─────┴─────┐
                    ▼           ▼
                  Critic    Project Manager
                Cloud Run      Cloud Run
```

This distributed design allows each agent to be developed, deployed, updated, and scaled independently.

---

## Brand Strategist

The Brand Strategist is responsible exclusively for **research and strategy**.

I configured this agent to:

- Research the target audience using Google Search
- Identify audience demographics, behaviors, interests, needs, and pain points
- Analyze relevant competitors
- Research current market trends
- Produce strategic insights for downstream agents
- Keep research current by incorporating the current year into search queries

The Brand Strategist intentionally does **not** generate captions or visual designs. Its output becomes the research foundation for the rest of the campaign.

---

## Copywriter

The Copywriter receives the Brand Strategist's research and transforms it into Instagram-ready content.

The agent generates:

- Three distinct caption variations
- Different tones and messaging approaches
- Strong opening hooks
- Calls to action
- Relevant hashtags

I also integrated **ADK Skills** so reusable copywriting knowledge can be maintained separately from the agent's primary system instructions.

This keeps reusable expertise modular instead of placing every copywriting rule inside one large prompt.

---

## Designer

The Designer converts campaign concepts into actual visual assets.

The Designer uses a tool-based architecture where the text agent creates the image concept and prompt, while a separate Gemini image model performs the image generation.

The generated images are uploaded to **Google Cloud Storage**, and the Designer returns the corresponding `gcs_uri`.

```text
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

This allows downstream agents, particularly the Critic, to access the generated visual without passing large raw image payloads between agents.

---

## Critic and Quality Gate

The Critic acts as the automated quality-control layer of the system.

It reviews:

- Instagram copy
- Generated campaign visuals
- Alignment between the campaign strategy, copy, and visual content

The Critic produces a structured verdict:

```text
APPROVED
```

or

```text
NEEDS_REVISION
```

When revisions are required, the Critic identifies the most important issue that needs to be corrected.

The Creative Director uses this result to determine whether the campaign can continue to project planning or whether work must be sent back for revision.

---

## Automatic Revision Loop

A major feature I implemented is an automated quality and revision loop.

```text
             Copy + Images
                   │
                   ▼
                Critic
                   │
                   ▼
          ┌─────────────────┐
          │    Verdict      │
          └────────┬────────┘
                   │
          ┌────────┴─────────┐
          │                  │
      APPROVED        NEEDS_REVISION
          │                  │
          ▼                  ▼
 Project Manager      Creative Director
                             │
                             ▼
                   Appropriate Specialist
                             │
                             ▼
                           Critic
```

The campaign does not proceed to the Project Manager until the Critic approves the work.

This creates an automated feedback loop without requiring a human to manually move feedback between agents.

---

## Project Manager and MCP

After the campaign passes the quality gate, the Project Manager converts the approved campaign into an actionable execution plan.

The Project Manager generates:

- Campaign timeline
- Tasks
- Deliverables
- Execution plan

I also support optional **Notion integration using Model Context Protocol (MCP)**.

MCP allows the Project Manager to interact with Notion through a standardized tool interface rather than implementing a custom Notion integration directly inside the agent.

The Project Manager still generates the complete text-based campaign plan when Notion is unavailable.

---

## Technology Stack

| Layer | Technology |
|---|---|
| Language | Python 3.11 / 3.12 |
| Agent Framework | Google Agent Development Kit (ADK) |
| Agent Communication | A2A Protocol |
| LLM | Gemini on Vertex AI |
| Image Generation | Gemini Image Model |
| External Tool Integration | Model Context Protocol (MCP) |
| Specialist Deployment | Google Cloud Run |
| Orchestrator Runtime | Gemini Enterprise Agent Platform Runtime |
| Image Storage | Google Cloud Storage |
| Secrets | Google Secret Manager |
| Project Management Integration | Notion via MCP |
| Dependency Management | uv |

---

## Project Structure

```text
workshop/
├── diagrams/
├── setup_inspector.sh
└── starter/
    ├── agents/
    │   ├── brand_strategist/
    │   ├── copywriter/
    │   ├── designer/
    │   ├── critic/
    │   ├── project_manager/
    │   └── creative_director/
    │
    └── deploy/
```

Each agent contains its own configuration, prompts, tools, and service implementation.

This separation keeps the architecture modular and allows each specialist to operate as an independently deployable service.

---

## Key Concepts Demonstrated

Through this project, I implemented and explored several important Agentic AI architecture patterns:

- Multi-agent orchestration
- Specialized AI agents
- LLM-driven orchestration
- Agent-to-Agent (A2A) communication
- Remote agents as tools
- Context propagation between agents
- Multimodal AI workflows
- Tool-based image generation
- Automated quality gates
- Agent revision loops
- ADK Skills
- Model Context Protocol (MCP)
- Cloud-native agent deployment
- Independent agent services
- Retry and error-handling patterns

---

## Reliability

Because the solution consists of distributed AI services, I incorporated reliability considerations including:

- Retry policies for transient failures
- Backoff strategies
- Tool error handling
- Graceful handling of optional Notion integration failures
- Configurable model and deployment settings
- Environment-based configuration rather than hard-coded infrastructure values

---

## What I Learned

This project helped me understand an important distinction between building an individual AI agent and building an **agentic system**.

The primary challenge is not simply prompting individual models. It is designing how specialized agents:

- discover each other,
- communicate,
- exchange context,
- use external tools,
- generate multimodal outputs,
- evaluate each other's work,
- recover from failures, and
- coordinate toward a single business outcome.

The Creative Director provides the orchestration layer, while the specialist agents remain independently deployable services connected through A2A.

This architecture demonstrates how multiple specialized AI capabilities can be composed into a complete end-to-end workflow rather than implemented as one monolithic agent.