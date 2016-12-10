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
taste tests. We want to add 8 center point runs to check for curvature,
bringing the total number of runs up to 36.  We can only do 3 per day, so as
not to over-caffienate our testers, and can only do the tests on days when all
5 testers are in the office. That means the test will probably take a month or
so.

We can calculate the power of a full factorial using dexpy, assuming a signal
to noise ratio of 2:

.. code:: python

    coffee_design = dexpy.factorial.build_factorial(5, 2**5)
    center_points = [
        [0, 0, 0, -1, -1],
        [0, 0, 0, -1, 1],
        [0, 0, 0, 1, -1],
        [0, 0, 0, 1, 1]
    ]
    coffee_design = coffee_design.append(pd.DataFrame(center_points * 2, columns=coffee_design.columns))
    coffee_design.index = np.arange(0, len(coffee_design))

    factorial_power = dexpy.power.f_power(model, coffee_design, sn, alpha)
    factorial_power.pop(0) # remove intercept
    factorial_power = ['{0:.2f}%'.format(i*100) for i in factorial_power] # convert to %

========== ======
Term       Power
========== ======
amount     99.98%
grind_size 99.98%
brew_time  99.98%
grind_type 99.99%
beans      99.99%
========== ======

This means we have a 99.97% chance of detecting a change of 2 taste rating,
assuming a standard deviation of 1 taste rating for the experiment. This is
high enough that we decide to run a fraction instead, and get the experiment
done more quickly. We can create a 2\ :sup:`5-1` fractional factorial, which
will have 16 runs, along with the 4 center points for a total of 20. As you can
see the power is still quite good.

.. code:: python

    coffee_design = dexpy.factorial.build_factorial(5, 2**(5-1))
    coffee_design.columns = ['amount', 'grind_size', 'brew_time', 'grind_type', 'beans']
    center_points = [
        [0, 0, 0, -1, -1],
        [0, 0, 0, -1, 1],
        [0, 0, 0, 1, -1],
        [0, 0, 0, 1, 1]
    ]

    coffee_design = coffee_design.append(pd.DataFrame(center_points * 2, columns=coffee_design.columns))
    coffee_design.index = np.arange(0, len(coffee_design))

    model = ' + '.join(coffee_design.columns)
    factorial_power = dexpy.power.f_power(model, coffee_design, sn, alpha)
    factorial_power.pop(0) # remove intercept
    factorial_power = ['{0:.2f}%'.format(i*100) for i in factorial_power] # convert to %

========== ======
Term       Power
========== ======
amount     96.55%
grind_size 96.55%
brew_time  96.55%
grind_type 99.61%
beans      99.61%
========== ======

We can also check the power for the interaction model:

.. code:: python

    twofi_model = "(" + '+'.join(coffee_design.columns) + ")**2"
    factorial_power = dexpy.power.f_power(twofi_model, coffee_design, sn, alpha)
    factorial_power.pop(0)
    factorial_power = ['{0:.2f}%'.format(i*100) for i in factorial_power] # convert to %

===================== ======
Term                  Power
===================== ======
amount                93.67%
grind_size            93.67%
brew_time             93.67%
grind_type            98.91%
beans                 98.91%
amount:grind_size     93.67%
amount:brew_time      93.67%
amount:grind_type     93.67%
amount:beans          93.67%
grind_size:brew_time  93.67%
grind_size:grind_type 93.67%
grind_size:beans      93.67%
brew_time:grind_type  93.67%
brew_time:beans       93.67%
grind_type:beans      98.91%
===================== ======


Run the Experiment
------------------

We can build the 2\ :sup:`5-1` design using :ref:`build_factorial <factorial>`,
then appending the 8 center point runs. We actually already did this to evaluate
the power, but here is the code again.

.. code:: python

    coffee_design = dexpy.factorial.build_factorial(5, 2**(5-1))
    coffee_design.columns = ['amount', 'grind_size', 'brew_time', 'grind_type', 'beans']
    center_points = [
        [0, 0, 0, -1, -1],
        [0, 0, 0, -1, 1],
        [0, 0, 0, 1, -1],
        [0, 0, 0, 1, 1]
    ]

    coffee_design = coffee_design.append(pd.DataFrame(center_points * 2, columns=coffee_design.columns))
    coffee_design.index = np.arange(0, len(coffee_design))

It is convenient to print out the design in actual values, rather than the
coded -1 and +1 values, for when we make the coffee.

.. code:: python

    actual_lows = { 'amount' : 2.5, 'grind_size' : 8, 'brew_time': 3.5,
                    'grind_type': 'burr', 'beans': 'light' }
    actual_highs = { 'amount' : 4, 'grind_size' : 10, 'brew_time': 4.5,
                     'grind_type': 'blade', 'beans': 'dark' }
    actual_design = dexpy.design.coded_to_actual(coffee_design, actual_lows, actual_highs)

+-----+--------+------------+-----------+------------+-------+
| run | amount | grind_size | brew_time | grind_type | beans |
+=====+========+============+===========+============+=======+
| 0   | 2.5    | 8          | 3.5       | burr       | dark  |
+-----+--------+------------+-----------+------------+-------+
| 1   | 2.5    | 8          | 3.5       | blade      | light |
+-----+--------+------------+-----------+------------+-------+
| 2   | 2.5    | 8          | 4.5       | burr       | light |
+-----+--------+------------+-----------+------------+-------+
| 3   | 2.5    | 8          | 4.5       | blade      | dark  |
+-----+--------+------------+-----------+------------+-------+
| 4   | 2.5    | 10         | 3.5       | burr       | light |
+-----+--------+------------+-----------+------------+-------+
| 5   | 2.5    | 10         | 3.5       | blade      | dark  |
+-----+--------+------------+-----------+------------+-------+
| 6   | 2.5    | 10         | 4.5       | burr       | dark  |
+-----+--------+------------+-----------+------------+-------+
| 7   | 2.5    | 10         | 4.5       | blade      | light |
+-----+--------+------------+-----------+------------+-------+
| 8   | 4      | 8          | 3.5       | burr       | light |
+-----+--------+------------+-----------+------------+-------+
| 9   | 4      | 8          | 3.5       | blade      | dark  |
+-----+--------+------------+-----------+------------+-------+
| 10  | 4      | 8          | 4.5       | burr       | dark  |
+-----+--------+------------+-----------+------------+-------+
| 11  | 4      | 8          | 4.5       | blade      | light |
+-----+--------+------------+-----------+------------+-------+
| 12  | 4      | 10         | 3.5       | burr       | dark  |
+-----+--------+------------+-----------+------------+-------+
| 13  | 4      | 10         | 3.5       | blade      | light |
+-----+--------+------------+-----------+------------+-------+
| 14  | 4      | 10         | 4.5       | burr       | light |
+-----+--------+------------+-----------+------------+-------+
| 15  | 4      | 10         | 4.5       | blade      | dark  |
+-----+--------+------------+-----------+------------+-------+
| 16  | 3.25   | 9          | 4         | burr       | light |
+-----+--------+------------+-----------+------------+-------+
| 17  | 3.25   | 9          | 4         | burr       | dark  |
+-----+--------+------------+-----------+------------+-------+
| 18  | 3.25   | 9          | 4         | blade      | light |
+-----+--------+------------+-----------+------------+-------+
| 19  | 3.25   | 9          | 4         | blade      | dark  |
+-----+--------+------------+-----------+------------+-------+
| 20  | 3.25   | 9          | 4         | burr       | light |
+-----+--------+------------+-----------+------------+-------+
| 21  | 3.25   | 9          | 4         | burr       | dark  |
+-----+--------+------------+-----------+------------+-------+
| 22  | 3.25   | 9          | 4         | blade      | light |
+-----+--------+------------+-----------+------------+-------+
| 23  | 3.25   | 9          | 4         | blade      | dark  |
+-----+--------+------------+-----------+------------+-------+

All that is left is to drink 24 pots of coffee and record the results. Note
that, while the tables in this example are in a sorted order, the actual
experiment was run in random order. This is done to reduce the possibility
of incidental variables influencing the results. For example, if the
temperature in the office for the first 8 runs was cold, the testers may
have rated the taste higher. Hot coffee being more pleasing in a cold
environment. If the first 8 runs were the only runs where amount was at its
low setting, as it is in the sorted table above, we would confound the low
amount effect with the effect of the cold office, and incorrectly conclude
that a lower amount of coffee is better.

+-----+------+-----+------+------+--------+------+
| run | hank | joe | neal | mike | martin | mean |
+=====+======+=====+======+======+========+======+
| 0   | 4    | 4   | 4    | 5    | 5      | 4.4  |
+-----+------+-----+------+------+--------+------+
| 1   | 5    | 6   | 6    | 7    | 5      | 5.8  |
+-----+------+-----+------+------+--------+------+
| 2   | 7    | 7   | 6    | 7    | 7      | 6.8  |
+-----+------+-----+------+------+--------+------+
| 3   | 4    | 5   | 3    | 6    | 5      | 4.6  |
+-----+------+-----+------+------+--------+------+
| 4   | 1    | 3   | 1    | 5    | 3      | 2.6  |
+-----+------+-----+------+------+--------+------+
| 5   | 7    | 7   | 4    | 2    | 5      | 5.0  |
+-----+------+-----+------+------+--------+------+
| 6   | 7    | 5   | 5    | 5    | 9      | 6.2  |
+-----+------+-----+------+------+--------+------+
| 7   | 1    | 4   | 2    | 5    | 5      | 3.4  |
+-----+------+-----+------+------+--------+------+
| 8   | 5    | 7   | 5    | 6    | 5      | 5.6  |
+-----+------+-----+------+------+--------+------+
| 9   | 2    | 7   | 3    | 8    | 5      | 5.0  |
+-----+------+-----+------+------+--------+------+
| 10  | 2    | 8   | 4    | 9    | 6      | 5.8  |
+-----+------+-----+------+------+--------+------+
| 11  | 6    | 6   | 7    | 7    | 7      | 6.6  |
+-----+------+-----+------+------+--------+------+
| 12  | 8    | 6   | 5    | 5    | 7      | 6.2  |
+-----+------+-----+------+------+--------+------+
| 13  | 4    | 6   | 2    | 3    | 2      | 3.4  |
+-----+------+-----+------+------+--------+------+
| 14  | 5    | 6   | 3    | 7    | 4      | 5.0  |
+-----+------+-----+------+------+--------+------+
| 15  | 7    | 5   | 4    | 7    | 9      | 6.4  |
+-----+------+-----+------+------+--------+------+
| 16  | 7    | 6   | 6    | 6    | 5      | 6.0  |
+-----+------+-----+------+------+--------+------+
| 17  | 7    | 6   | 6    | 6    | 5      | 6.0  |
+-----+------+-----+------+------+--------+------+
| 18  | 7    | 8   | 5    | 8    | 6      | 6.8  |
+-----+------+-----+------+------+--------+------+
| 19  | 6    | 7   | 4    | 6    | 7      | 6.0  |
+-----+------+-----+------+------+--------+------+
| 20  | 7    | 7   | 6    | 5    | 5      | 6.0  |
+-----+------+-----+------+------+--------+------+
| 21  | 6    | 7   | 5    | 7    | 6      | 6.2  |
+-----+------+-----+------+------+--------+------+
| 22  | 5    | 7   | 3    | 6    | 4      | 5.0  |
+-----+------+-----+------+------+--------+------+
| 23  | 7    | 6   | 6    | 6    | 7      | 6.4  |
+-----+------+-----+------+------+--------+------+

We'll store the mean for later as another column in the DataFrame.

.. code:: python

    coffee_design['taste_rating'] = [
        4.4, 5.8, 6.8, 4.6, 2.6, 5, 6.2, 3.4,
        5.6, 5, 5.8, 6.6, 6.2, 3.4, 5, 6.4,
        6, 6, 6.8, 6, 6, 6.2, 5, 6.4
    ]


Fit a Model
-----------

The statsmodels package has an OLS fitting routine that takes a patsy formula:

.. code:: python

  lm = statsmodels.formula.api.ols("taste_rating ~" + twofi_model, data=coffee_design).fit()
  print(lm.summary2())

We can reduce this model by removing terms that have a p-value above 0.05:

.. code:: python

  reduced_model = "amount + grind_size + brew_time + grind_type + amount:grind_type + grind_size:brew_time + grind_size:grind_type"
  lm = statsmodels.formula.api.ols("taste_rating ~" + reduced_model, data=coffee_design).fit()
  print(lm.summary2())

.. [#] http://www.statease.com/publications/newsletter/stat-teaser-09-16#article1
