# CauseChain

CauseChain is a small Python OOP project for investigating **why a problem happened** by connecting possible causes into a chain.

The main idea is simple:

> Don't stop at the visible problem. Trace it backward to understand what caused it.

---

## Problem Statement

When something fails, the first visible problem is often only a symptom.

For example:

```text
Website became slow
        ↓
API response became slower
        ↓
Database queries became slower
        ↓
Database CPU increased
        ↓
Traffic suddenly increased
```

If we only fix the website's performance without understanding the deeper cause, the same problem may happen again.

CauseChain helps organize this investigation.

---

## Project Structure

```text
CauseChain/
│
├── cause_chain.py
├── cause_chain_studio.py
├── README.md
└── .gitignore
```

---

## Features

### 1. Create a Problem

Create an investigation with:

* Problem ID
* Title
* Description

Example:

```text
ID: INC001
Title: Website became slow
Description: Customers are experiencing slow page loading.
```

---

### 2. Add Possible Causes

Multiple possible causes can be recorded for the same problem.

Each cause contains:

* Cause
* Category
* Confidence
* Supporting evidence

Example:

```text
Cause: Database queries became slower
Category: Infrastructure
Confidence: High
Evidence: Database response time increased at 10:30 AM.
```

---

### 3. Connect Causes

Causes can be connected to create a cause-and-effect relationship.

Example:

```text
Traffic Spike
      ↓
Database CPU Increased
      ↓
Database Queries Slowed
      ↓
API Response Slowed
      ↓
Website Became Slow
```

This creates a chain instead of keeping causes as unrelated notes.

---

## Confidence Levels

Every cause can have one of three confidence levels:

```text
Low
Medium
High
```

Confidence represents how strongly the current investigation supports the cause.

It does **not** mean that a high-confidence cause is automatically proven.

Evidence should still be reviewed.

---

## Evidence Gaps

CauseChain checks whether recorded causes have supporting evidence.

For example:

```text
Cause:
Server overloaded

Evidence:
Not provided
```

This becomes an evidence gap.

This is important because a suspected cause without evidence should not automatically be treated as the actual root cause.

---

## Cause Chain

The system can construct a connected chain such as:

```text
Traffic Spike
      →
Database CPU Increased
      →
Queries Became Slower
      →
API Became Slower
```

This makes the investigation easier to understand.

---

## Confidence Calculation

CauseChain calculates an overall confidence percentage from the confidence levels assigned to recorded causes.

Internally:

```text
Low    = 1
Medium = 2
High   = 3
```

The average confidence is converted into a percentage.

This provides a simple overview of how strongly the current investigation supports its recorded causes.

---

## Investigation Recommendations

CauseChain can recommend what to do next.

For example:

### No causes

```text
Start by identifying possible causes.
```

### Missing evidence

```text
Collect evidence before treating the causes as confirmed.
```

### Low confidence

```text
Investigate the recorded causes further.
```

### Shallow chain

```text
Consider asking why the identified cause happened.
```

### Strong investigation

```text
Review the deepest cause and confirm it with evidence.
```

---

## How to Run

Make sure Python 3 is installed.

Open a terminal inside the project folder and run:

```bash
python cause_chain_studio.py
```

---

## Studio Menu

```text
============================================================
CAUSECHAIN STUDIO
============================================================
1. Create Problem
2. Add Cause
3. Connect Causes
4. View All Problems
5. View Problem Details
6. Analyze Problem
7. Show Recommendation
8. Exit
============================================================
```

---

## Typical Workflow

```text
Create Problem
      ↓
Identify Possible Causes
      ↓
Add Evidence
      ↓
Assign Confidence
      ↓
Connect Related Causes
      ↓
Build Cause Chain
      ↓
Review Evidence Gaps
      ↓
Investigate Deeper
      ↓
Validate the Likely Cause
```

---

## Example Use Case

Imagine an online store reports:

```text
Problem:
Orders are being delayed.
```

Possible investigation:

```text
Orders Delayed
      ↓
Orders Not Processed Quickly
      ↓
Order Processing Queue Increased
      ↓
Processing Worker Became Slow
      ↓
Server Resources Were Exhausted
```

Each step can be recorded as a cause and connected to the next step.

The investigator can then attach evidence to each cause.

---

## Real-World Applications

### Software Incidents

Investigate:

* Application failures
* Slow APIs
* Database problems
* Deployment incidents
* Service outages

### Business Operations

Investigate:

* Missed deadlines
* Customer complaints
* Delayed orders
* Process failures
* Unexpected costs

### Project Management

Investigate:

* Why a project slipped
* Why work had to be repeated
* Why a milestone was missed
* Why a task remained blocked

### Troubleshooting

The same structure can be used for everyday technical or operational problems.

---

## OOP Concepts Used

### Class

```python
class CauseChain:
```

The main class contains the investigation logic.

### Constructor

```python
def __init__(self):
```

Initializes the collection of investigations.

### Methods

Separate methods handle:

* Problem creation
* Cause creation
* Cause relationships
* Confidence calculation
* Evidence-gap detection
* Chain construction
* Analysis
* Recommendations

### Encapsulation

Problem and cause information is maintained inside the `CauseChain` object.

### Separation of Responsibilities

```text
cause_chain.py
        ↓
Core investigation logic

cause_chain_studio.py
        ↓
Interactive interface
```

This keeps the business logic separate from the user interface.

---

## Why This Is More Than a Simple CRUD Project

CauseChain is not primarily about storing problems and causes.

Its main value is the **reasoning structure**:

```text
Problem
   ↓
Possible Cause
   ↓
Evidence
   ↓
Confidence
   ↓
Relationship
   ↓
Deeper Cause
   ↓
Investigation
```

The system also deliberately avoids claiming that the deepest recorded cause is automatically the true root cause.

That distinction matters in real investigations.

---

## Limitations

This version is intentionally small and local.

It does not currently:

* Automatically discover causes
* Automatically collect evidence
* Verify whether evidence is correct
* Persist data to a database
* Build complex branching cause trees
* Connect to monitoring systems
* Automatically determine the true root cause

The user is responsible for entering the investigation information.

---

## Future Improvements

Possible future versions could add:

* Persistent database storage
* Branching cause trees
* Multiple investigation paths
* Evidence attachments
* Timeline reconstruction
* Incident history
* Dependency relationships
* Automatic cause suggestions
* Natural-language investigation input
* AI-assisted root-cause exploration
* AI-assisted grouping of similar causes
* AI-assisted evidence analysis

For example, a future version could receive:

```text
"Our website became slow after yesterday's deployment."
```

and suggest investigation paths such as:

```text
Deployment
   ↓
Code Change
   ↓
Database Queries
   ↓
Resource Usage
```

The human investigator could then validate or reject those possibilities.

---

## Technologies

* Python 3
* Object-Oriented Programming
* Standard Python library only

No external packages are required.

---

## .gitignore

```gitignore
__pycache__/
*.py[cod]
*.pyo
.venv/
venv/
env/
.idea/
.vscode/
.DS_Store
```

---

## Project Goal

CauseChain demonstrates a practical approach to problem investigation:

> **A visible failure is not always the real cause. Trace the chain, examine the evidence, and investigate deeper before deciding what actually went wrong.**
