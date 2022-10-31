# investment-portfolio

I just want to manage my investment portfolio via a simple cli

## Roadmap

0. Create skeleton of the project (package, docs, unittests, ...)
1. cli implementation to create projects, add standard investment strategy (passive, active) with %, add stocks, amount, value , rm stocks, ...
2. Ability to see the deltas between your investment sheet and your stocks
3. Ability to update your stocks value
4. Ability to cope with currencies
5. Ability to load from yahoo the stock history
6. Ability to document why you bought the stocks you wanted
7. Ability to define optimization methods for your portfolio e.g. with the integration of https://github.com/tradytics/eiten
8. Ability to measure the deltas between your portfolio and the "optimized one" to be able to react to it
9. Ability to setup a simple selling strategy (when your stock grow disproportionate, etc...
10. Ability to setup more complex selling strategies (algorithm based) - do not know yet how to do it.
11. Export possibilities to excel or else

## Improvements to work on
1. **portfolio_plan_cli:** consistent visualization with rich
2. **portfolio_plan_cli:** in `visualize-allocation`, show allocation errors with colors!

## Should

- Use prompt (https://python-prompt-toolkit.readthedocs.io/en/master/pages/asking_for_input.html) to have autocompletion instead of click

## Warning

I'm not in the financial domain. I just try to help myself building my portfolio and I do not want to use excel to handle it.
