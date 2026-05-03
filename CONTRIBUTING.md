# Contributing to AutoViron

First off, thank you for considering contributing to AutoViron! It's people like you that make AutoViron such a great tool.

## Where do I go from here?

If you've noticed a bug or have a feature request, make sure to check our [Issues](https://github.com/Atharva1399/autoviron/issues) first to see if someone else has already created a ticket. If not, go ahead and [make one](https://github.com/Atharva1399/autoviron/issues/new)!

## Fork & create a branch

If this is something you think you can fix, then fork AutoViron and create a branch with a descriptive name.

## Get the test suite running

1. Ensure you have Python 3.9+ installed.
2. Clone your fork and install the requirements:
   ```bash
   pip install -e ".[dev]"
   ```
3. Run the tests using `pytest`:
   ```bash
   pytest tests/
   ```

## Implement your fix or feature

At this point, you're ready to make your changes. Feel free to ask for help; everyone is a beginner at first 😸

## Make a Pull Request

At this point, you should switch back to your master branch and make sure it's up to date with AutoViron's master branch:

```bash
git remote add upstream git@github.com:Atharva1399/autoviron.git
git checkout master
git pull upstream master
```

Then update your feature branch from your local copy of master, and push it!

```bash
git checkout 325-add-new-plugin
git rebase master
git push --set-upstream origin 325-add-new-plugin
```

Finally, go to GitHub and make a Pull Request.

## Code Style
We use `black` for formatting and `flake8` for linting. Please ensure your code passes both before submitting a PR.