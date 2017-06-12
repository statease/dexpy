Example: Optimal Design
=======================

Problem Description
-------------------

A chemist is trying to improve the yield of a chemical process.

She can vary:

 * Reaction time (40-50 minutes)
 * Temperature (80-90 °C)

With one output, or `response`, variable:

 * Conversion (%)

Design Choice
-------------

Due to the expense of the experiment, only 6 runs may be performed. From prior
experimention the chemist knows to expect a quadratic effect. Standard designs
such as a two-level factorial (with center points), or a Central Composite
design have too many runs. Instead the chemist decides to use an
`optimal design <http://www.itl.nist.gov/div898/handbook/pri/section5/pri521.htm>`_,
where the factor settings are chosen in an algorithmic search, designed to
optimize some criteria. We will be using the **D-optimal** criteria, which
minimizes the joint confidence interval of the model parameters.

This can easily be done in dexpy using
:func:`build_optimal <dexpy.optimal.build_optimal>`. Note that by default the
size of the design is the minimal number of runs required to support the model
(in this case 6).

.. code:: python

  import dexpy.optimal
  from dexpy.model import ModelOrder
  reaction_design = dexpy.optimal.build_optimal(2, order=ModelOrder.quadratic)
  print(reaction_design)

+---+-------+-------+
|   | time  | temp  |
+---+-------+-------+
| 0 | 43.64 | 80.00 |
+---+-------+-------+
| 1 | 40.00 | 90.00 |
+---+-------+-------+
| 2 | 40.00 | 82.73 |
+---+-------+-------+
| 3 | 50.00 | 80.00 |
+---+-------+-------+
| 4 | 45.45 | 85.45 |
+---+-------+-------+
| 5 | 50.00 | 90.00 |
+---+-------+-------+

As you can see, the runs are arranged in a less structured manner than a
standard design. If you look at the design graphically, you can see that
the points are spread out throughout the space.

.. image:: img/optimal-6-run.svg

We can calculate the D-optimality of this design, which is just the
determinant of the information matrix :math:`|X'X|`.

.. code:: python

  from dexpy.model import make_model, ModelOrder
  from patsy import dmatrix
  import numpy as np

  quad_model = make_model(reaction_design.columns, ModelOrder.quadratic)
  X = dmatrix(quad_model, reaction_design)
  XtX = np.dot(np.transpose(X), X)
  d = np.linalg.det(XtX)

  print("|(X'X)| for optimal design: {}".format(d))

  # |(X'X)| for optimal design: 264.56712477125734

What if the chemist was able to run 10 experiments? You can give the optimal
builder a **run_count** parameter.

.. code:: python

  import dexpy.optimal
  from dexpy.model import ModelOrder
  reaction_design = dexpy.optimal.build_optimal(2, run_count=10, order=ModelOrder.quadratic)
  print(reaction_design)

+---+------+------+
|   | time | temp |
+---+------+------+
| 0 | 50.0 | 80.0 |
+---+------+------+
| 1 | 50.0 | 85.5 |
+---+------+------+
| 2 | 40.0 | 90.0 |
+---+------+------+
| 3 | 50.0 | 90.0 |
+---+------+------+
| 4 | 40.0 | 80.0 |
+---+------+------+
| 5 | 40.0 | 85.5 |
+---+------+------+
| 6 | 50.0 | 80.0 |
+---+------+------+
| 7 | 44.5 | 80.0 |
+---+------+------+
| 8 | 45.4 | 84.5 |
+---+------+------+
| 9 | 44.5 | 90.0 |
+---+------+------+

.. image:: img/optimal-10-run.svg

Notice that there appears to be only 9 runs in the image. That is because one of
the vertices (indicated in red) has been duplicated by the optimal search
algorithm. Both run 0 and run 6 have a time of 50 minutes and a temp of 80 °C.

Note that the **run_count** parameter must be greater than, or equal to, the
size of the model. In this example, the quadratic model
:math:`\hat{y} = 1 + X_1 + X_2 + {X_1}{X_2} + X_1^2 + X_2^2`
requires at least 6 runs. If you try to pass in too few runs you get an exception.

.. code:: python

  import dexpy.optimal
  from dexpy.model import ModelOrder
  reaction_design = dexpy.optimal.build_optimal(2, run_count=4, order=ModelOrder.quadratic)

Produces::

  ValueError: Can't build a design of size 4 for a model of rank 6. Model: '(X1+X2)**2+pow(X1,2)+pow(X2, 2)'

