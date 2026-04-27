# who-smart-localization

## Team workflow

This repository is meant to stay approachable for the full project team, including teammates with limited coding experience.

### Before you start

You need:

- a GitHub account;
- Git installed on your computer;
- access to this repository on GitHub.

If you have never used Git before, follow the steps below exactly in order.

### Step 1: Copy the repository to your computer

This is called "cloning" the repository. It creates a local copy on your machine so you can edit files safely.

First, open Terminal and move to the folder where you want the repository to be saved on your computer.

For example, if you want to put it on your Desktop, run:

```bash
cd ~/Desktop
```

If you want it in another folder, go to that folder instead.

After that, run:

```bash
git clone https://github.com/JackCosta2612/who-smart-localization.git
```

Then move into the project folder:

```bash
cd who-smart-localization
```

### Step 2: Make sure you are on the main project branch

The `main` branch is the central version of the project. You should not edit directly on it.

Run:

```bash
git checkout main
```

If this works, Git has switched you to the main branch.

### Step 3: Download the newest version of the project

Before starting your own work, download the latest changes from GitHub so your copy is up to date.

Run:

```bash
git pull origin main
```

This updates your local `main` branch with the newest version from GitHub.

### Step 4: Create your own branch for your change

A branch is your personal work area. It lets you make changes without affecting the main project until the team reviews them.

Create a branch with a short name that describes your task:

```bash
git checkout -b short-description
```

Replace `short-description` with your own branch name.

Good examples:

- `readme-update`
- `example-matrix`
- `validator-fixes`

Try to keep the name short and descriptive.

### Step 5: Edit the files you need

Make your changes in the project files.

Common example:

- update a markdown file;
- add an example;
- improve documentation;
- fix a script.

### Step 6: Check which files you changed

Before saving your work to Git, check what changed.

Run:

```bash
git status
```

This shows:

- which files were changed;
- which branch you are on;
- whether Git is ready for the next step.

### Step 7: Add your changed files

This tells Git which files should be included in your next saved version.

To add everything you changed:

```bash
git add .
```

If you only want to add one file, you can use:

```bash
git add README.md
```

### Step 8: Save your work with a commit

A commit is a saved checkpoint with a short message explaining what you changed.

Run:

```bash
git commit -m "Short description of my change"
```

Example:

```bash
git commit -m "Update README workflow instructions"
```

### Step 9: Upload your branch to GitHub

This is called "pushing". It sends your branch and commits from your computer to GitHub.

Run:

```bash
git push -u origin short-description
```

Use the same branch name you created in Step 4.

### Step 10: Open a pull request

A pull request is a request for the team to review your branch before it is merged into `main`.

After pushing:

1. Open the repository on GitHub.
2. GitHub will usually show a button to create a pull request for your branch.
3. Click that button.
4. Make sure your branch is being compared into `main`.
5. Write a short title and a short explanation of what you changed.
6. Create the pull request.
7. Ask a teammate to review it.

### Step 11: Wait for review before merging

Do not merge your own changes unless the team has agreed on that workflow.

Normally the process is:

1. Open a branch.
2. Make changes.
3. Commit and push.
4. Open a pull request.
5. Wait for review.
6. Merge only after approval.

## Project summary

This repository contains a model-neutral Agent Skill for WHO SMART Guidelines localization. The goal is to compare WHO global guidance or structured SMART Guideline content with country-specific policy material and produce a traceable, human-reviewable localization matrix.

The project is part of a university Natural Language Processing collaboration with the World Health Organization (WHO). It is intentionally lightweight: mostly documentation, examples, and a small validation script.

## Scope

The skill is designed to help a reviewer answer questions such as:

- Does the local policy align with the WHO source?
- Is the local policy more specific or more restrictive?
- Is a WHO element missing from the local excerpt?
- Is the relationship too unclear to classify without expert review?

The output is a structured markdown matrix rather than a free-form summary.

## What the skill does

- Compares a WHO source statement with a local policy statement.
- Assigns a controlled alignment category.
- Records evidence from both sources.
- Preserves traceability and uncertainty.
- Flags rows that need expert follow-up.

## What the skill does not do

- It does not make clinical decisions.
- It does not produce final national policy.
- It does not replace WHO or country experts.
- It does not validate clinical correctness.
- It does not assume missing local policy text when evidence is absent.

## Repository structure

```text
.
├── README.md
├── SKILL.md
├── SKILLS.md
├── assets/
├── context/
│   ├── localization-categories.md
│   ├── output-schema.md
│   └── who-smart-context.md
├── examples/
│   ├── example-input-1.md
│   ├── example-input-2.md
│   ├── example-output-1.md
│   └── example-output-2.md
├── scripts/
│   └── validate_matrix.py
└── tests/
    ├── evaluation-notes.md
    ├── test-case-1.md
    └── test-case-2.md
```

## How the examples and tests are organized

- `examples/` contains toy inputs and toy outputs for structural testing only.
- `tests/` contains simple validation-oriented cases and evaluation notes.
- `context/` holds reusable definitions so `SKILL.md` stays concise.
- `scripts/validate_matrix.py` checks whether a markdown matrix follows the expected structure.

## Running the validator

The validator is structural only. It does not assess medical or policy correctness.

```bash
python3 scripts/validate_matrix.py examples/example-output-1.md
```

Expected behavior:

- exits with `0` when the matrix structure is valid;
- exits non-zero when required columns or controlled values are invalid;
- prints a reminder that the check is not a clinical review.

## Current status

This first implementation pass provides:

- a canonical `SKILL.md` file for the Agent Skill;
- core project documentation in `context/`;
- clearly labeled toy examples;
- a lightweight validator for markdown localization matrices.

Real WHO and country policy excerpts can be added later under `assets/` and referenced by future examples once the team has approved source material.
