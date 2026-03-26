---
name: training-curriculum
description: Design training curricula with learning objectives, module sequencing, hands-on exercises, assessment methods, and progression milestones — using learning science principles for effective knowledge transfer.
metadata:
  displayName: "Training Curriculum"
  categories: ["communication"]
  tags: ["training", "curriculum", "learning", "education", "onboarding", "skill-development"]
  worksWellWithAgents: ["instructional-designer"]
  worksWellWithSkills: ["onboarding-plan"]
---

# Training Curriculum

## Before you start

Gather the following from the user. Items 1-4 are required before proceeding:

1. **What skill or knowledge should learners have after completing this curriculum?** Be specific. "Understand Kubernetes" is vague. "Deploy, scale, and troubleshoot containerized applications on Kubernetes" is actionable.
2. **Who are the learners?** Role, experience level, and what they already know. A curriculum for senior engineers differs fundamentally from one for new hires.
3. **How much time is available?** Total hours, session length, and whether it is self-paced or instructor-led. This constrains scope.
4. **What does success look like?** How will you know learners achieved the objective — certification exam, project delivery, observed behavior change?
5. **What resources exist already?** Existing docs, recordings, mentors, sandboxes, or lab environments that can be incorporated.
6. **Are there prerequisites?** What must learners know before starting? Be explicit to avoid wasting time on mismatched cohorts.

If the user says "create a training program on X," push back: "Who is the audience, what should they be able to do afterward, and how much time do we have?"

## Curriculum design template

### 1. Curriculum Overview

Write a short summary covering:
- **Target outcome**: One sentence describing what learners can do after completing the curriculum
- **Audience**: Role and prerequisite knowledge
- **Format**: Self-paced, instructor-led, cohort-based, or blended
- **Duration**: Total hours and recommended schedule (e.g., 2 hours/week for 6 weeks)

### 2. Learning Objectives

Write objectives using the format: "By the end of [module/curriculum], learners will be able to [observable verb] [specific outcome]."

Use Bloom's Taxonomy verbs matched to the appropriate level:

| Level | Verbs | Example |
|-------|-------|---------|
| Remember | List, define, identify | List the five components of a Kubernetes pod spec |
| Understand | Explain, summarize, compare | Explain the difference between a Deployment and a StatefulSet |
| Apply | Implement, configure, use | Configure a HorizontalPodAutoscaler for a deployment |
| Analyze | Debug, differentiate, investigate | Debug a CrashLoopBackOff by analyzing pod logs and events |
| Evaluate | Assess, recommend, justify | Evaluate whether a workload should use Deployments or DaemonSets |
| Create | Design, build, architect | Design a multi-namespace cluster architecture for a microservices application |

Avoid vague verbs: "understand," "learn," "know," "be familiar with." These are not observable or measurable.

### 3. Module Sequence

Structure modules in a dependency-ordered sequence. Each module builds on the previous one.

| Module | Title | Duration | Objectives (from Section 2) | Format |
|--------|-------|----------|---------------------------|--------|
| 1 | Foundations | 2 hours | Objectives 1-3 | Lecture + guided walkthrough |
| 2 | Core Workflows | 3 hours | Objectives 4-6 | Hands-on lab |
| 3 | Troubleshooting | 2 hours | Objectives 7-8 | Scenario-based exercises |
| 4 | Advanced Patterns | 3 hours | Objectives 9-10 | Project work |
| 5 | Capstone | 2 hours | All objectives | Assessment project |

Sequencing rules:
- Concepts before procedures. Teach the "why" before the "how."
- Simple before complex. Start with isolated tasks, then combine into workflows.
- Scaffolded practice. Early modules have guided exercises; later modules are increasingly open-ended.

### 4. Module Detail

For each module, specify:

- **Pre-work**: Reading, video, or setup tasks to complete before the session (max 30 minutes)
- **Content outline**: Key topics in delivery order (bullet list, not paragraphs)
- **Hands-on exercise**: A concrete task learners perform during the module. Include the scenario, expected deliverable, and estimated time.
- **Key takeaways**: 2-3 sentences summarizing what learners should remember. These double as review material.

### 5. Exercises and Labs

Every exercise follows this structure:

```
Exercise: [Title]
Scenario: [Real-world context — why would someone need to do this?]
Task: [Specific steps or open-ended problem to solve]
Expected outcome: [What the completed exercise looks like]
Time: [Estimated duration]
Hints: [Optional progressive hints for self-paced learners]
```

Exercises must practice the stated learning objective, not adjacent skills. If the objective is "configure autoscaling," the exercise should not be "write a Dockerfile."

### 6. Assessment Methods

| Assessment | When | What It Measures | Pass Criteria |
|-----------|------|-----------------|--------------|
| Knowledge check quiz | End of each module | Recall and comprehension | 80% correct |
| Hands-on lab review | End of Modules 2-4 | Application of skills | Functional deliverable matching requirements |
| Capstone project | End of curriculum | Synthesis of all objectives | Peer review + rubric score of 3/5 or higher |

For each assessment, provide the rubric or answer key. Subjective assessments need a scoring rubric with concrete criteria at each level.

### 7. Progression Milestones

Define checkpoints where learners should self-assess readiness to continue:

- **After Module 1**: "I can explain [core concepts] to a colleague without notes."
- **After Module 3**: "I can complete [core workflow] independently within [time limit]."
- **After Module 5**: "I can solve a novel problem in this domain using the tools and patterns from this curriculum."

## Quality checklist

Before delivering the curriculum, verify:

- [ ] Every learning objective uses an observable, measurable verb — not "understand" or "learn"
- [ ] Modules are sequenced by dependency — no module requires knowledge from a later module
- [ ] Each module has at least one hands-on exercise that directly practices its stated objective
- [ ] Assessments exist for each major objective with defined pass criteria
- [ ] Total time adds up correctly and fits within the stated time budget
- [ ] Prerequisites are explicit — a learner can self-assess whether they are ready to start
- [ ] Exercises use realistic scenarios, not abstract toy problems

## Common mistakes to avoid

- **Objectives without assessments.** If you state an objective but never test it, you cannot know whether learners achieved it. Every objective needs at least one corresponding assessment or exercise.
- **All lecture, no practice.** Adults retain ~10% of what they hear and ~75% of what they practice. Allocate at least 50% of time to exercises.
- **Skipping prerequisites.** A curriculum that assumes too little bores advanced learners. One that assumes too much loses beginners. State prerequisites explicitly and offer a self-assessment.
- **Modules that are too long.** Sessions over 90 minutes without a break cause attention to drop sharply. Break long modules into segments with varied formats.
- **No sequencing logic.** Randomly ordered modules force learners to hold too much in working memory. Sequence from simple to complex, concrete to abstract.
