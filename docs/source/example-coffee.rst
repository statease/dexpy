Example: Coffee Taste Test
==========================

Problem Description
-------------------

A coffee taste test was conducted at the Stat-Ease office to improve the taste
of the coffee [#]_. This example uses a simplified version of that experiment.

We will look at 5 input factors:

 * Amount of Coffee (2.5 to 4.0 oz.)
 * Grind size (8-10mm)
 * Brew time (3.5 to 4.5 minutes)
 * Grind Type (burr vs blade)
 * Coffee beans (light vs dark)

With one output, or `response`, variable:

 * Average overall liking (1-9)

The liking is an average of the scores of a panel of 5 office coffee drinkers.

Design Choice
-------------

A `full factorial <http://www.itl.nist.gov/div898/handbook/pri/section3/pri3332.htm>`_,
that is, running all combinations of lows and highs, would take 2\ :sup:`5` = 32
taste tests. We want to add 4 center point runs to check for curvature,
bringing the total number of runs up to 36.  We can only do 3 per day, so as
not to over-caffienate our testers, and can only do the tests on days when all
5 testers are in the office. That means the test will probably take a month or
so.

We can calculate the power of a full factorial using dexpy, assuming a signlat to noise
ratio of 2:

.. code:: python

    coffee_design = dexpy.factorial.build_factorial(5, 2**(5-1))
    center_points = [
        [0, 0, 0, -1, -1],
        [0, 0, 0, -1, 1],
        [0, 0, 0, 1, -1],
        [0, 0, 0, 1, 1]
    ]
    coffee_design = coffee_design.append(pd.DataFrame(center_points * 2, columns=coffee_design.columns))
    coffee_design.index = np.arange(0, len(coffee_design))

    factorial_power = dexpy.power.f_power(model, coffee_design, sn, alpha)
    factorial_power.pop(0)
    factorial_power = ['{0:.2f}%'.format(i*100) for i in factorial_power] # convert to %

========== =====
Term       Power
========== =====
amount     99.97%
grind_size 99.97%
brew_time  99.97%
grind_type 99.97%
beans      99.97%
========== =====

.. [#] http://www.statease.com/publications/newsletter/stat-teaser-09-16#article1
