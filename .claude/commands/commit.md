---
description: Create atomic commit with appropriate tag
---

Create a new commit for all of our uncommitted changes.

Run `git status && git diff HEAD && git status --porcelain` to see what files are uncommitted.

Add the untracked and changed files.

Create an atomic commit message with an appropriate message.

Add a tag such as "feat", "fix", "docs", "refactor", "test", "chore", etc. that reflects our work.

**Format:**
```
<tag>(<scope>): <short description>

<optional body with more details>
```

**Examples:**
- `feat(auth): add user login endpoint`
- `fix(api): handle null response from external service`
- `docs(readme): update installation instructions`
- `refactor(services): extract common validation logic`
