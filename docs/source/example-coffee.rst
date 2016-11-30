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
amount     99.97%
grind_size 99.97%
brew_time  99.97%
grind_type 99.97%
beans      99.97%
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
amount     96.02%
grind_size 96.02%
brew_time  96.02%
grind_type 98.57%
beans      98.57%
========== ======

We can also check the power for the interaction model:

.. code:: python

    twofi_model = "(" + '+'.join(coffee_design.columns) + ")**2"
    desc = patsy.ModelDesc.from_formula(twofi_model)
    factorial_power = dexpy.power.f_power(twofi_model, coffee_design, sn, alpha)
    factorial_power.pop(0)
    factorial_power = ['{0:.2f}%'.format(i*100) for i in factorial_power] # convert to %

===================== ======
Term                  Power
===================== ======
amount                84.33%
grind_size            84.33%
brew_time             84.33%
grind_type            90.89%
beans                 90.89%
amount:grind_size     84.33%
amount:brew_time      84.33%
amount:grind_type     84.33%
amount:beans          84.33%
grind_size:brew_time  84.33%
grind_size:grind_type 84.33%
grind_size:beans      84.33%
brew_time:grind_type  84.33%
brew_time:beans       84.33%
grind_type:beans      90.89%
===================== ======


Run Experiment
--------------

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

All that is left is to drink 24 pots of coffee and record the results.

+-----+------+-----+------+------+--------+------+
| run | hank | joe | neal | mike | martin | mean |
+=====+======+=====+======+======+========+======+
| 0   | 6    | 4   | 5    | 7    | 6      | 5.6  |
+-----+------+-----+------+------+--------+------+
| 1   | 6    | 6   | 6    | 7    | 7      | 6.4  |
+-----+------+-----+------+------+--------+------+
| 2   | 4    | 5   | 4    | 6    | 5      | 4.8  |
+-----+------+-----+------+------+--------+------+
| 3   | 6    | 7   | 3    | 5    | 6      | 5.4  |
+-----+------+-----+------+------+--------+------+
| 4   | 3    | 6   | 2    | 5    | 4      | 4    |
+-----+------+-----+------+------+--------+------+
| 5   | 5    | 7   | 7    | 5    | 5      | 5.8  |
+-----+------+-----+------+------+--------+------+
| 6   | 3    | 5   | 3    | 6    | 7      | 4.8  |
+-----+------+-----+------+------+--------+------+
| 7   | 3    | 6   | 4    | 6    | 5      | 4.8  |
+-----+------+-----+------+------+--------+------+
| 8   | 4    | 8   | 6    | 8    | 5      | 6.2  |
+-----+------+-----+------+------+--------+------+
| 9   | 5    | 8   | 5    | 5    | 6      | 5.8  |
+-----+------+-----+------+------+--------+------+
| 10  | 4    | 6   | 5    | 6    | 6      | 5.4  |
+-----+------+-----+------+------+--------+------+
| 11  | 4    | 6   | 6    | 8    | 5      | 5.8  |
+-----+------+-----+------+------+--------+------+
| 12  | 6    | 6   | 5    | 6    | 7      | 6    |
+-----+------+-----+------+------+--------+------+
| 13  | 7    | 7   | 2    | 5    | 5      | 5.2  |
+-----+------+-----+------+------+--------+------+
| 14  | 7    | 6   | 2    | 7    | 3      | 5    |
+-----+------+-----+------+------+--------+------+
| 15  | 6    | 6   | 4    | 7    | 6      | 5.8  |
+-----+------+-----+------+------+--------+------+
| 16  | 7    | 7   | 5    | 4    | 4      | 5.4  |
+-----+------+-----+------+------+--------+------+
| 17  | 6    | 7   | 3    | 5    | 4      | 5    |
+-----+------+-----+------+------+--------+------+
| 18  | 6    | 6   | 7    | 7    | 5      | 6.2  |
+-----+------+-----+------+------+--------+------+
| 19  | 8    | 6   | 4    | 5    | 5      | 5.6  |
+-----+------+-----+------+------+--------+------+
| 20  | 6    | 7   | 3    | 5    | 5      | 5.2  |
+-----+------+-----+------+------+--------+------+
| 21  | 8    | 6   | 5    | 7    | 5      | 6.2  |
+-----+------+-----+------+------+--------+------+
| 22  | 7    | 5   | 2    | 7    | 4      | 5    |
+-----+------+-----+------+------+--------+------+
| 23  | 7    | 5   | 6    | 7    | 5      | 6    |
+-----+------+-----+------+------+--------+------+

We'll store the mean for later as another column in the DataFrame.

.. code:: python

    coffee_design['taste_rating'] = [
        5.6, 6.4, 4.8, 5.4, 4, 5.8, 4.8, 4.8
        6.2, 5.8, 5.4, 5.8, 6, 5.2, 5, 5.8
        5.4, 5, 6.2, 5.6, 5.2, 6.2, 5, 6
    ]

.. [#] http://www.statease.com/publications/newsletter/stat-teaser-09-16#article1
