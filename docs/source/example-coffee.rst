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

  import dexpy.factorial
  import dexpy.power
  import pandas as pd
  import numpy as np

  coffee_design = dexpy.factorial.build_factorial(5, 2**5)
  center_points = [
      [0, 0, 0, -1, -1],
      [0, 0, 0, -1, 1],
      [0, 0, 0, 1, -1],
      [0, 0, 0, 1, 1]
  ]
  coffee_design = coffee_design.append(pd.DataFrame(center_points * 2, columns=coffee_design.columns))
  coffee_design.index = np.arange(0, len(coffee_design))

  sn = 2.0
  alpha = 0.05
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
    sn = 2.0
    alpha = 0.05
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
    sn = 2.0
    alpha = 0.05
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
| 1   | 3    | 3   | 3    | 3    | 1      | 2.6  |
+-----+------+-----+------+------+--------+------+
| 2   | 2    | 3   | 3    | 2    | 2      | 2.4  |
+-----+------+-----+------+------+--------+------+
| 3   | 9    | 9   | 9    | 8    | 8      | 8.6  |
+-----+------+-----+------+------+--------+------+
| 4   | 1    | 3   | 1    | 2    | 1      | 1.6  |
+-----+------+-----+------+------+--------+------+
| 5   | 2    | 6   | 1    | 2    | 3      | 2.8  |
+-----+------+-----+------+------+--------+------+
| 6   | 7    | 6   | 6    | 8    | 9      | 7.2  |
+-----+------+-----+------+------+--------+------+
| 7   | 1    | 4   | 2    | 5    | 5      | 3.4  |
+-----+------+-----+------+------+--------+------+
| 8   | 5    | 7   | 8    | 6    | 8      | 6.8  |
+-----+------+-----+------+------+--------+------+
| 9   | 2    | 6   | 3    | 5    | 1      | 3.4  |
+-----+------+-----+------+------+--------+------+
| 10  | 2    | 5   | 4    | 5    | 3      | 3.8  |
+-----+------+-----+------+------+--------+------+
| 11  | 9    | 9   | 9    | 9    | 9      | 9    |
+-----+------+-----+------+------+--------+------+
| 12  | 8    | 3   | 4    | 4    | 7      | 5.2  |
+-----+------+-----+------+------+--------+------+
| 13  | 4    | 6   | 2    | 4    | 2      | 3.6  |
+-----+------+-----+------+------+--------+------+
| 14  | 9    | 8   | 8    | 8    | 8      | 8.2  |
+-----+------+-----+------+------+--------+------+
| 15  | 7    | 6   | 5    | 8    | 9      | 7    |
+-----+------+-----+------+------+--------+------+
| 16  | 7    | 6   | 4    | 5    | 5      | 5.4  |
+-----+------+-----+------+------+--------+------+
| 17  | 7    | 7   | 7    | 7    | 6      | 6.8  |
+-----+------+-----+------+------+--------+------+
| 18  | 7    | 2   | 2    | 4    | 3      | 3.6  |
+-----+------+-----+------+------+--------+------+
| 19  | 6    | 6   | 4    | 5    | 6      | 5.4  |
+-----+------+-----+------+------+--------+------+
| 20  | 7    | 4   | 4    | 3    | 6      | 4.8  |
+-----+------+-----+------+------+--------+------+
| 21  | 6    | 7   | 5    | 7    | 6      | 6.2  |
+-----+------+-----+------+------+--------+------+
| 22  | 5    | 4   | 3    | 6    | 4      | 4.4  |
+-----+------+-----+------+------+--------+------+
| 23  | 7    | 6   | 4    | 5    | 7      | 5.8  |
+-----+------+-----+------+------+--------+------+

We'll store the mean for later as another column in the DataFrame.

.. code:: python

  coffee_design['taste_rating'] = [
      4.4, 2.6, 2.4, 8.6, 1.6, 2.8, 7.2, 3.4,
      6.8, 3.4, 3.8, 9.0, 5.2, 3.6, 8.2, 7.0,
      5.4, 6.8, 3.6, 5.4, 4.8, 6.2, 4.4, 5.8
  ]


Fit a Model
-----------

The statsmodels package has an OLS fitting routine that takes a patsy formula:

.. code:: python

  from statsmodels.formula.api import ols

  lm = ols("taste_rating ~" + twofi_model, data=coffee_design).fit()
  print(lm.summary2())

+-----------------------+---------+----------+---------+------------+---------+---------+
| term                  | Coef.   | Std.Err. | t       | P>|t|      | [0.025  | 0.975]  |
+=======================+=========+==========+=========+============+=========+=========+
| Intercept             | 5.1     | 0.1434   | 35.5718 | 0          | 4.7694  | 5.4306  |
+-----------------------+---------+----------+---------+------------+---------+---------+
| amount                | 0.875   | 0.1756   | 4.9831  | **0.0011** | 0.4701  | 1.2799  |
+-----------------------+---------+----------+---------+------------+---------+---------+
| grind_size            | -0.125  | 0.1756   | -0.7119 | 0.4968     | -0.5299 | 0.2799  |
+-----------------------+---------+----------+---------+------------+---------+---------+
| brew_time             | 1.2     | 0.1756   | 6.8339  | **0.0001** | 0.7951  | 1.6049  |
+-----------------------+---------+----------+---------+------------+---------+---------+
| grind_type            | -0.1333 | 0.1434   | -0.93   | 0.3796     | -0.4639 | 0.1973  |
+-----------------------+---------+----------+---------+------------+---------+---------+
| beans                 | 0.45    | 0.1434   | 3.1387  | **0.0138** | 0.1194  | 0.7806  |
+-----------------------+---------+----------+---------+------------+---------+---------+
| amount:grind_size     | 0.25    | 0.1756   | 1.4237  | 0.1923     | -0.1549 | 0.6549  |
+-----------------------+---------+----------+---------+------------+---------+---------+
| amount:brew_time      | -0.075  | 0.1756   | -0.4271 | 0.6806     | -0.4799 | 0.3299  |
+-----------------------+---------+----------+---------+------------+---------+---------+
| amount:grind_type     | -0.175  | 0.1756   | -0.9966 | 0.3481     | -0.5799 | 0.2299  |
+-----------------------+---------+----------+---------+------------+---------+---------+
| amount:beans          | -1.325  | 0.1756   | -7.5458 | **0.0001** | -1.7299 | -0.9201 |
+-----------------------+---------+----------+---------+------------+---------+---------+
| grind_size:brew_time  | 0.375   | 0.1756   | 2.1356  | 0.0652     | -0.0299 | 0.7799  |
+-----------------------+---------+----------+---------+------------+---------+---------+
| grind_size:grind_type | -0.725  | 0.1756   | -4.1288 | **0.0033** | -1.1299 | -0.3201 |
+-----------------------+---------+----------+---------+------------+---------+---------+
| grind_size:beans      | 0.375   | 0.1756   | 2.1356  | 0.0652     | -0.0299 | 0.7799  |
+-----------------------+---------+----------+---------+------------+---------+---------+
| brew_time:grind_type  | 0.75    | 0.1756   | 4.2712  | **0.0027** | 0.3451  | 1.1549  |
+-----------------------+---------+----------+---------+------------+---------+---------+
| brew_time:beans       | 0.15    | 0.1756   | 0.8542  | 0.4178     | -0.2549 | 0.5549  |
+-----------------------+---------+----------+---------+------------+---------+---------+
| grind_type:beans      | 0.0833  | 0.1434   | 0.5812  | 0.5771     | -0.2473 | 0.4139  |
+-----------------------+---------+----------+---------+------------+---------+---------+

We can reduce this model by keeping only terms that have a p-value below 0.05
(bolded in the table above):

.. code:: python

  # this gets the pvalues dataframe from the RegressionResults
  # and slices out the rows with p < 0.05
  pvalues = lm.pvalues[1:]
  reduced_model = '+'.join(pvalues.loc[pvalues < 0.05].index)
  # you could also just specify it by hand:
  # reduced_model = "amount + brew_time + beans + amount:beans + " \
  #                 "grind_size:grind_type + brew_time:grind_type"
  lm = ols("taste_rating ~" + reduced_model, data=coffee_design).fit()
  print(lm.summary2())

+-----------------------+----------+----------+---------+--------+---------+---------+
|                       | Coef.    | Std.Err. | t       | P>|t|  | [0.025  | 0.975]  |
+=======================+==========+==========+=========+========+=========+=========+
| Intercept             | 5.1      | 0.1659   | 30.7405 | 0      | 4.75    | 5.45    |
+-----------------------+----------+----------+---------+--------+---------+---------+
| amount                | 0.875    | 0.2032   | 4.3063  | 0.0005 | 0.4463  | 1.3037  |
+-----------------------+----------+----------+---------+--------+---------+---------+
| brew_time             | 1.2      | 0.2032   | 5.9058  | 0      | 0.7713  | 1.6287  |
+-----------------------+----------+----------+---------+--------+---------+---------+
| beans                 | 0.45     | 0.1659   | 2.7124  | 0.0148 | 0.1     | 0.8     |
+-----------------------+----------+----------+---------+--------+---------+---------+
| amount:beans          | -1.325   | 0.2032   | -6.5209 | 0      | -1.7537 | -0.8963 |
+-----------------------+----------+----------+---------+--------+---------+---------+
| grind_size:grind_type | -0.725   | 0.2032   | -3.5681 | 0.0024 | -1.1537 | -0.2963 |
+-----------------------+----------+----------+---------+--------+---------+---------+
| brew_time:grind_type  | 0.75     | 0.2032   | 3.6911  | 0.0018 | 0.3213  | 1.1787  |
+-----------------------+----------+----------+---------+--------+---------+---------+

.. [#] http://www.statease.com/publications/newsletter/stat-teaser-09-16#article1
