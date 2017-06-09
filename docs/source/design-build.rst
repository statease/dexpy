Building a Design
=================

First you will need to determine what kind of design suits your problem.

* :ref:`Screening (Factorial) <screening-designs>` - Used to determine what factors are important.
* :ref:`Response Surface <response-surface-designs>` - Used for optimizing a process.
* :ref:`Mixture <mixture-designs>` - Used when the components sum to a total (e.g. drug formulation).

.. _screening-designs:

=================
Screening Designs
=================

These designs are meant to be run with many factors, and are used to determine
which factors are important and which can be discarded. They typically have
fewer runs and are meant to be used with a linear or interaction model.

.. _factorial:

Two-Level Factorial
-------------------

.. automodule:: dexpy.factorial
    :members:

.. _response-surface-designs:

========================
Response Surface Designs
========================

Find the best settings for the factors with a goal to optimize the process. Use
a Response Surface Optimal designs to algorithmically find the best runs to fit
within multi-linear constraints, to custom polynomial models, and have more
flexible blocking structures.

.. _central-composite:

Central Composite
-----------------

.. autofunction:: dexpy.ccd.build_ccd

.. _mixture-designs:

===============
Mixture Designs
===============

Formulation work. If the process is a mixture, such as a drug formulation, a
chemical composition, or even how to allocate a budget, then use a Mixture
Design. These designs produce runs to model the responses in terms of the
relative proportions of the components. The sum of the component proportions is
always 1 (100% of the components being varied). As one component is increased
the sum of the other components must decrease to maintain the sum. Mixture
optimal designs are most commonly used because they allow the most flexibility
in your component ranges.

Simplex Lattice
---------------

.. autofunction:: dexpy.simplex_lattice.build_simplex_lattice

Simplex Centroid
----------------

.. autofunction:: dexpy.simplex_centroid.build_simplex_centroid


Optimal Design
==============

Optimal designs are designs built algorithmically to satisfy some criteria (e.g. D-optimality).

.. autofunction:: dexpy.optimal.build_optimal

