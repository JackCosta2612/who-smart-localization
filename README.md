# who-smart-localization

This repository contains model-neutral Agent Skills for WHO SMART Guidelines localization work. The project is part of a university Natural Language Processing collaboration with the World Health Organization (WHO).

The repository now supports more than one skill. Each skill lives in its own folder under `skills/`.

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

## Project scope

The repository supports localization work around WHO SMART Guidelines and Digital Adaptation Kits (DAKs). The first planned skill is Country Profiling, which prepares a structured country context for later localization work. The existing Policy Comparison skill is kept as a separate skill because it will depend on good country context.

The skills are review aids. They do not make clinical decisions, produce final national policy, or replace WHO, country, legal, policy, or clinical experts.

## Repository structure

```text
.
├── README.md
├── SKILLS.md
├── docs/
├── shared/
│   └── assets/
└── skills/
    ├── country-profiling/
    │   ├── SKILL.md
    │   ├── README.md
    │   ├── context/
    │   ├── examples/
    │   ├── scripts/
    │   └── tests/
    └── policy-comparison/
        ├── SKILL.md
        ├── context/
        ├── examples/
        ├── scripts/
        └── tests/
```

## Skills

### Country Profiling

Given a country name and target health domain, this skill produces a structured, verifiable country profile relevant to DAK implementation. It draws from provided DAK material, WHO/open data sources, and country-specific public health documentation supplied by the user or retrieved by a future retrieval layer.

Location: `skills/country-profiling/`

### Policy Comparison

Given a WHO source statement and local policy excerpt, this skill produces a traceable localization matrix showing alignment, partial alignment, divergence, missing content, or required expert review.

Location: `skills/policy-comparison/`

## Running validators

Policy comparison matrix validator:

```bash
python3 skills/policy-comparison/scripts/validate_matrix.py skills/policy-comparison/examples/example-output-1.md
```

Country profiling output validator:

```bash
python3 skills/country-profiling/scripts/validate_profile.py skills/country-profiling/examples/example-output-1.md
```

These validators check structure only. They do not validate clinical correctness, policy correctness, or source interpretation.
