# Multi-Agent Campaign Execution

This document captures a representative execution of the Multi-Agent Creative
Studio using Google ADK and A2A-connected specialist agents.

The example demonstrates how the Creative Director coordinates research,
copywriting, visual generation, quality review, revision, and project planning
to produce a complete Instagram campaign.

---

## 1. Creative Director — Campaign Planning

The Creative Director received the PureBoost campaign brief and created an
execution plan across the specialist agents.

> I'll coordinate our team to create a complete Instagram campaign for
> PureBoost. Here's my plan:
>
> **Brand Strategist** will research the organic energy drink market,
> competitor landscape, and specific insights for the U.S. college student
> demographic.
>
> **Copywriter** will create 3 Instagram posts (captions and hashtags)
> designed to resonate with students' busy lifestyles.
>
> **Designer** will generate visual concepts and high-quality images for
> each post.
>
> **Critic** will review all creative work for quality and brand alignment.
>
> **Revision Round:** If the Critic identifies any issues, I will have the
> specialists revise their work.
>
> **Project Manager** will create a comprehensive project timeline and
> deliver the final campaign package.

The Creative Director then initiated the workflow with the Brand Strategist.

---

## 2. Brand Strategist — Market Research

The Brand Strategist researched the market, competitors, and target audience.

After receiving the research, the Creative Director summarized the result:

> ✓ Research complete. I received detailed insights on the **"Modern Organic"**
> whitespace, the shift toward **mindful productivity**, and the importance
> of visual wellness for the **18–24 demographic**.
>
> Now moving to Copywriter to create the 3 Instagram posts...

The research became the strategic context for the downstream creative agents.

---

## 3. Copywriter — Instagram Content

Using the Brand Strategist's research, the Copywriter generated three
Instagram post concepts.

The Creative Director reported:

> ✓ Copywriting complete. I received 3 Instagram posts focusing on
> **educational value, community engagement, and personal storytelling**,
> all aligned with the "Modern Organic" strategy.
>
> Now moving to Designer to generate the visual concepts and images...

The approved copy and strategy were then provided to the Designer.

---

## 4. Designer — Initial Visual Generation

The Designer generated visual concepts for all three Instagram posts.

The initial campaign contained three concepts:

1. **The Modern Desk**
2. **Mindful Productivity**
3. **The Natural Peak**

The Creative Director confirmed:

> ✓ Design complete. I have generated and displayed the visual concepts for
> all three posts.
>
> Now moving to Critic for a quality review of the copy and visuals...

These initial images are preserved in:

```text
generated-images/
├── modern-desk-v1.png
├── mindful-productivity-v1.png
└── natural-peak-v1.png
```

---

## 5. Critic — Initial Quality Review

The Critic independently evaluated both the written content and generated visuals.

### Copy Review

**Score: 9/10 — APPROVED**

The Critic found that the copy effectively targeted the college demographic and addressed relevant audience pain points.

### Visual Review

**Score: 6/10 — NEEDS_REVISION**

The Critic identified:

- A spelling error: **"FLANCE"**
- Anatomical distortions in **The Natural Peak**
- Minor AI-generated artifacts in the other visual concepts

The Creative Director interpreted the Critic's assessment and determined that the visual assets—not the copy—required another iteration.

> I'll work with the Designer to revise the visual concepts based on this feedback.

This demonstrates targeted revision routing: the approved copy was preserved, while the visual feedback was routed back to the Designer.

---

## 6. Designer — Revision Round

The Designer received the Critic's feedback and regenerated the visual assets.

The Creative Director reported:

> ✓ Designer completed revisions based on critic feedback. The spelling errors and anatomical issues have been corrected.
>
> Now re-running the Critic for a final quality review...

The revised images are preserved as:

```text
generated-images/
├── modern-desk-v2.png
├── mindful-productivity-v2.png
└── natural-peak-v2.png
```

The revised assets were then sent back to the Critic.

---

## 7. Critic — Final Quality Review

The Critic performed a second review after the revision round.

The Creative Director reported:

> ✓ Final Critic review complete. While the copy remains highly rated (9/10), the Critic noted that the revised visuals still contain some technical AI artifacts (Score 5/10).
>
> Per our workflow, we have completed the maximum of one revision round. I will now proceed to the Project Manager to create the final campaign timeline and package, incorporating all deliverables and the Critic's final assessment.

The workflow stopped revising after the configured maximum of one revision round and preserved the Critic's remaining concerns in the final campaign assessment.

---

## 8. Image Link Generation

Before final packaging, the workflow attempted to generate final HTTPS links for the campaign images.

The Creative Director reported:

> ⚠️ I encountered a technical issue generating the final HTTPS links for the images. However, all campaign content is complete. I'll now have the Project Manager create the final timeline and campaign summary.

The generated assets remained available through their Google Cloud Storage URIs, allowing the workflow to continue despite the link-generation issue.

---

## 9. Project Manager — Final Packaging

The Project Manager generated the final campaign timeline and campaign summary.

The final package included:

- Market research and campaign strategy
- Three Instagram posts
- Three revised visual concepts
- Critic quality assessment
- Four-week implementation timeline
- Estimated campaign budget

The complete final response is preserved in [`final-output.md`](final-output.md).

---

## Execution Summary

```text
Campaign Brief
      │
      ▼
Creative Director
      │
      ▼
Brand Strategist
      │
      ▼
Copywriter
      │
      ▼
Designer — V1 Visuals
      │
      ▼
Critic — NEEDS_REVISION
      │
      ▼
Creative Director — Routes Visual Feedback
      │
      ▼
Designer — V2 Visuals
      │
      ▼
Critic — Final Review
      │
      ▼
Project Manager
      │
      ▼
Final Campaign Package
```
