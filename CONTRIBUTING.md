# General Contributing Guidelines

1. Contribute using the
   [fork](https://docs.github.com/en/pull-requests/how-tos/work-with-forks/fork-a-repo) and
   [pull request](https://docs.github.com/en/pull-requests/how-tos/create-pull-requests/creating-a-pull-request?tool=webui)
   workflow. Creating development branches in the main repository is discouraged.
2. Pull requests are merged via a
   [merge queue](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue#about-merge-queues)
   using a [merge commit](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/about-merge-methods-on-github).
   1. Commit history matters. You may be asked to clean up your commits or split a large pull
      request before it is merged.
   2. If a merge queue check fails, rebase your branch on the target branch and resolve any
      conflicts.
3. All commits must have a
   [verified signature](https://docs.github.com/en/authentication/managing-commit-signature-verification/about-commit-signature-verification).

## Target Branches

Currently, all development targets the `main` branch.

| Branch | Status | Target RHEL Version | Notes |
| :--- | :--- | :--- | :--- |
| `main`| Active development | RHEL 10.4+ | Default target for new features and fixes
