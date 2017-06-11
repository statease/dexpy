"""Functions to build factorial designs."""

import itertools
import pandas as pd
import dexpy.design as design


def build_full_factorial(factor_count):
    """Builds a full 2^K factorial design.

    The resulting design will contain every combination of -1 and +1 for the
    number of factors given.
    """
    factor_data = []
    for run in itertools.product([-1, 1], repeat=factor_count):
        factor_data.append(list(run))
    return factor_data


def build_factorial(factor_count, run_count):
    """Builds a regular two-level design based on a number of factors and runs.

    Full two-level factorial designs may be run for up to 9 factors. These
    designs permit estimation of all main effects and all interaction effects.
    If the number of runs requested is a 2^factor_count, the design will be a
    full factorial.

    If the number of runs is less than 2^factor_count (it still must be a power
    of two) a fractional design will be created. Not all combinations of runs
    and factor counts will result in a design. Use the
    :ref:`alias list<alias-list>` method to see what terms are estimable in
    the resulting design.

    :param factor_count: The number of factors to build for.
    :type factor_count: int
    :param run_count: The number of runs in the resulting design. Must be a power of 2.
    :type run_count: int
    :returns: A pandas.DataFrame object containing the requested design.
    """
    # store minimum aberration generators for factors from 3 to max_factors
    # these are from Design-Expert
    generator_list = {
        3: {4: ["C=AB"]},
        4: {8: ["D=ABC"]},
        5: {8: ["D=AB", "E=AC"], 16: ["E=ABCD"]},
        6: {8: ["D=AB", "E=AC", "F=BC"], 16: ["E=ABC", "F=BCD"], 32: ["F=ABCDE"]},
        7: {8: ["D=AB", "E=AC", "F=BC", "G=ABC"], 16: ["E=ABC", "F=BCD", "G=ACD"], 32: ["F=ABCD", "G=ABCE"],64: ["G=ABCDEF"]},
        8: {16: ["E=ABC", "F=BCD", "G=ACD", "H=ABD"], 32: ["F=ABC", "G=ABD", "H=BCDE"], 64: ["G=ABCD", "H=ABEF"], 128: ["H=ABCDEFG"]},
        9: {16: ["E=ABC", "F=BCD", "G=ACD", "H=ABD", "J=ABCD"], 32: ["F=ABCD", "G=ABCE", "H=ABDE", "J=ACDE"], 64: ["G=ABCD", "H=ACEF", "J=CDEF"], 128: ["H=ABCDE", "J=ABCFG"], 256: ["J=ABCDEFGH"]}, # noqa
        10: {16: ["E=ABC", "F=BCD", "G=ACD", "H=ABD", "J=ABCD", "K=AB"], 32: ["F=ABCD", "G=ABCE", "H=ABDE", "J=ACDE", "K=BCDE"], 64: ["G=ABCD", "H=ABCE", "J=ADEF", "K=BDEF"], 128: ["H=ABCG", "J=BCDE", "K=ACDF"], 256: ["J=ABCDEF", "K=ABCDGH"], 512: ["K=ABCDEFGHJ"]}, # noqa
        11: {16: ["E=ABC", "F=BCD", "G=ACD", "H=ABD", "J=ABCD", "K=AB", "L=AC"], 32: ["F=ABC", "G=BCD", "H=CDE", "J=ACD", "K=ADE", "L=BDE"], 64: ["G=ABCD", "H=ABCE", "J=ABDE", "K=ACDEF", "L=BCDEF"], 128: ["H=ABCG", "J=BCDE", "K=ACDF", "L=ABCDEFG"], 256: ["J=ABCDE", "K=ABCFG", "L=ABDFH"], 512: ["K=ABCDEF", "L=ABCGHJ"]}, # noqa
        12: {16: ["E=ABC", "F=ABD", "G=ACD", "H=BCD", "J=ABCD", "K=AB", "L=AC", "M=AD"], 32: ["F=ABC", "G=ABD", "H=ACD", "J=BCD", "K=ABE", "L=ACE", "M=ADE"], 64: ["G=ABC", "H=ABD", "J=ACDE", "K=ACDF", "L=ABEF", "M=BCDEF"], 128: ["H=ABC", "J=ADEF", "K=BDEG", "L=CDFG", "M=ABCEFG"], 256: ["J=ABCDE", "K=ABCFG", "L=ABDFH", "M=ACEGH"], 512: ["K=ABCDEF", "L=ABCDGH", "M=ABEFGJ"]}, # noqa
        13: {16: ["E=ABC", "F=ABD", "G=ACD", "H=BCD", "J=ABCD", "K=AB", "L=AC", "M=AD", "N=BC"], 32: ["F=ABC", "G=ABD", "H=ACD", "J=BCD", "K=ABE", "L=ACE", "M=ADE", "N=BCE"], 64: ["G=ABC", "H=ABD", "J=ABE", "K=ACDE", "L=ACF", "M=ADEF", "N=ABCDEF"], 128: ["H=ABC", "J=ABDE", "K=ABDF", "L=ACDG", "M=AEFG", "N=ABCDEFG"], 256: ["J=ABCDE", "K=ABCFG", "L=ABDFH", "M=ACEGH", "N=ADEFGH"], 512: ["K=ABCDEF", "L=ABCDGH", "M=ABEFGJ", "N=ACEGHJ"]}, # noqa
        14: {16: ["E=ABC", "F=ABD", "G=ACD", "H=BCD", "J=ABCD", "K=AB", "L=AC", "M=AD", "N=BC", "O=BD"], 32: ["F=ABC", "G=ABD", "H=ACD", "J=BCD", "K=ABE", "L=ACE", "M=ADE", "N=BCE", "O=BDE"], 64: ["G=ABC", "H=ABD", "J=ABE", "K=ACDE", "L=ABF", "M=ACDF", "N=ACEF", "O=ADEF"], 128: ["H=ABC", "J=ABDE", "K=ABDF", "L=ACEF", "M=ACDG", "N=ABEFG", "O=BCDEFG"], 256: ["J=ABCDE", "K=ABCFG", "L=ABDEFG", "M=ABDFH", "N=ADEGH", "O=ACEFGH"], 512: ["K=ABCDE", "L=ABFGH", "M=CDFGJ", "N=ACEFHJ", "O=BDEGHJ"]}, # noqa
        15: {16: ["E=ABC", "F=ABD", "G=ACD", "H=BCD", "J=ABCD", "K=AB", "L=AC", "M=AD", "N=BC", "O=BD", "P=CD"], 32: ["F=ABC", "G=ABD", "H=ACD", "J=BCD", "K=ABE", "L=ACE", "M=ADE", "N=BCE", "O=BDE", "P=CDE"], 64: ["G=ABC", "H=ABD", "J=ABE", "K=ACDE", "L=ABF", "M=ACDF", "N=ACEF", "O=ADEF", "P=ABCDEF"], 128: ["H=ABC", "J=ADE", "K=BDF", "L=ACEF", "M=CDG", "N=BCEG", "O=EFG", "P=ABCDEFG"], 256: ["J=ABCD", "K=ABEF", "L=ACEG", "M=BDFG", "N=ABDEH", "O=ACDFH", "P=BEGH"], 512: ["K=ABCDE", "L=ABCFG", "M=ABDFH", "N=ACDFJ", "O=AEGHJ", "P=ABCDEFGHJ"]}, # noqa
        16: {32: ["F=ABC", "G=ABD", "H=ACD", "J=BCD", "K=ABE", "L=ACE", "M=BCE", "N=ADE", "O=BDE", "P=CDE", "Q=ABCDE"], 64: ["G=ABCD", "H=ABCE", "J=ABDE", "K=ACDE", "L=BCDE", "M=ABCF", "N=ABDF", "O=ACDF", "P=BCDF", "Q=ABCDEF"], 128: ["H=ABCD", "J=ABCE", "K=ABDF", "L=ACEF", "M=ACDG", "N=BCEG", "O=ABCFG", "P=ABDEFG", "Q=BCDEFG"], 256: ["J=ABCDE", "K=ABCFG", "L=ABDEFG", "M=ABCDFH", "N=CDEFH", "O=ACDEGH", "P=AEFGH", "Q=BCEFGH"], 512: ["K=ABCDE", "L=ABCFG", "M=ABDFH", "N=ACEGH", "O=ACDFJ", "P=BCEGJ", "Q=ABCEFHJ"]}, # noqa
        17: {32: ["F=ABC", "G=ABD", "H=ACD", "J=BCD", "K=ABCD", "L=ABE", "M=ACE", "N=BCE", "O=ADE", "P=BDE", "Q=CDE", "R=ABCDE"], 64: ["G=ABC", "H=ABD", "J=ACD", "K=BCD", "L=ABE", "M=ACE", "N=ABF", "O=ACF", "P=ADEF", "Q=BDEF", "R=CDEF"], 128: ["H=ABCD", "J=ABCE", "K=ABDF", "L=ACEF", "M=ADEF", "N=ACDG", "O=ABEG", "P=ADEG", "Q=ABFG", "R=BCDEFG"], 256: ["J=ABCD", "K=ABEF", "L=ACEG", "M=BDFG", "N=BCEH", "O=ABDFH", "P=ABDEGH", "Q=ACDFGH", "R=ABCEFGH"], 512: ["K=ABCDE", "L=ABCFG", "M=ABDFH", "N=ACEGH", "O=ACDFJ", "P=BCEGJ", "Q=ABCEFHJ", "R=ABDEGHJ"]}, # noqa
        18: {32: ["F=ABC", "G=ABD", "H=ACD", "J=BCD", "K=ABCD", "L=ABE", "M=ACE", "N=BCE", "O=ABCE", "P=ADE", "Q=BDE", "R=CDE", "S=ABCDE"], 64: ["G=ABC", "H=ABD", "J=ACD", "K=BCD", "L=ABE", "M=ACE", "N=BCE", "O=ABF", "P=ACF", "Q=ADEF", "R=BDEF", "S=CDEF"], 128: ["H=ABCD", "J=ABCE", "K=ABDF", "L=ACEF", "M=ADEF", "N=ACDG", "O=ABEG", "P=ADEG", "Q=ABFG", "R=ACFG", "S=BCDEFG"], 256: ["J=ABCD", "K=ABCE", "L=ADEF", "M=ADEG", "N=ABFG", "O=ACFG", "P=BCDEH", "Q=BDFH", "R=CEGH", "S=BCFGH"], 512: ["K=ABCDE", "L=ABCFG", "M=ABDFH", "N=ACEGH", "O=ACDFJ", "P=BCEGJ", "Q=ABCEFHJ", "R=ABDEGHJ", "S=BCDFGHJ"]}, # noqa
        19: {32: ["F=ABC", "G=ABD", "H=ACD", "J=BCD", "K=ABCD", "L=ABE", "M=ACE", "N=BCE", "O=ABCE", "P=ADE", "Q=BDE", "R=ABDE", "S=CDE", "T=ABCDE"], 64: ["G=ABC", "H=ABD", "J=ACD", "K=BCD", "L=ABE", "M=ACE", "N=BCE", "O=ABF", "P=ACF", "Q=BCF", "R=ADEF", "S=BDEF", "T=CDEF"], 128: ["H=ABCD", "J=ABCE", "K=ABDE", "L=ABCF", "M=ADEF", "N=BDEF", "O=ACDG", "P=ACEG", "Q=CDEG", "R=ABFG", "S=ADFG", "T=ABCDEFG"], 256: ["J=ABCDE", "K=ABCDF", "L=ABCEG", "M=ABDEFG", "N=ACDEFG", "O=BCEFH", "P=ADEGH", "Q=BCDEGH", "R=ABCFGH", "S=BDFGH", "T=CDFGH"], 512: ["K=ABCDE", "L=ABCFG", "M=ABDFH", "N=ACEGH", "O=ADEFGH", "P=BCEFJ", "Q=ABDEGJ", "R=BDFGJ", "S=ACFHJ", "T=BCEGHJ"]}, # noqa
        20: {32: ["F=ABC", "G=ABD", "H=ACD", "J=BCD", "K=ABCD", "L=ABE", "M=ACE", "N=BCE", "O=ABCE", "P=ADE", "Q=BDE", "R=ABDE", "S=CDE", "T=ACDE", "U=ABCDE"], 64: ["G=ABC", "H=ABD", "J=ACD", "K=BCD", "L=ABE", "M=ACE", "N=BCE", "O=ABF", "P=ACF", "Q=BCF", "R=ADEF", "S=BDEF", "T=CDEF", "U=ABCDEF"], 128: ["H=ABCD", "J=ABCE", "K=ABDE", "L=ABCF", "M=ADEF", "N=BDEF", "O=ACDG", "P=ACEG", "Q=CDEG", "R=ABFG", "S=ADFG", "T=AEFG", "U=ABCDEFG"], 256: ["J=ABCDE", "K=ABCDF", "L=ABCEF", "M=ABCDG", "N=ABEFG", "O=ACDEFG", "P=ABDEH", "Q=ACDEFH", "R=ABCEGH", "S=BDEGH", "T=ABDFGH", "U=BCDEFGH"], 512: ["K=ABCDE", "L=ABCFG", "M=ABDFH", "N=ACEGH", "O=ADEFGH", "P=BCEFJ", "Q=ABDEGJ", "R=BDFGJ", "S=ACFHJ", "T=BCEGHJ", "U=CDFGHJ"]}, # noqa
        21: {32: ["F=ABC", "G=ABD", "H=ACD", "J=BCD", "K=ABCD", "L=ABE", "M=ACE", "N=BCE", "O=ABCE", "P=ADE", "Q=BDE", "R=ABDE", "S=CDE", "T=ACDE", "U=BCDE", "V=ABCDE"], 64: ["G=ABC", "H=ABD", "J=ACD", "K=BCD", "L=ABE", "M=ACE", "N=BCE", "O=ADE", "P=ABF", "Q=ADF", "R=BDF", "S=AEF", "T=CEF", "U=DEF", "V=BCDEF"], 128: ["H=ABCD", "J=ABCE", "K=ABDE", "L=ACDE", "M=ABCF", "N=ABDF", "O=ACEF", "P=ADEF", "Q=ACDG", "R=ABEG", "S=BCDEG", "T=CDFG", "U=BEFG", "V=ABCDEFG"], 256: ["J=ABCDE", "K=ABCDF", "L=ABCEF", "M=ABDEF", "N=ABCDG", "O=ABEFG", "P=ACDEFG", "Q=ACDEFH", "R=BCDEFH", "S=BCEGH", "T=ABDEGH", "U=ABCFGH", "V=BDFGH"], 512: ["K=ABCDE", "L=ABCFG", "M=ABDFH", "N=ACEGH", "O=ADEFGH", "P=BCEFJ", "Q=ABDEGJ", "R=BDFGJ", "S=ACFHJ", "T=BCEGHJ", "U=CDFGHJ", "V=DEHJ"]} # noqa
    }

    if run_count == 2 ** factor_count:
        generators = []
    else:
        generators = generator_list[factor_count][run_count]
    fractional_factors = len(generators)

    full_factor_count = factor_count - fractional_factors
    full_factor_names = design.get_factor_names(full_factor_count)
    factor_data = pd.DataFrame(build_full_factorial(full_factor_count),
                               columns=full_factor_names)

    if full_factor_count == factor_count:
        return factor_data

    for gen in generators:
        lhs, rhs = gen.split("=")
        lhs = "X" + str(design.get_var_id(lhs)+1 ) # rename to X1/X2/etc
        cols = []
        for var in rhs:
            cols.append(design.get_var_id(var))

        generator_column = factor_data.iloc[:, cols].product(axis=1).rename(lhs)
        factor_data = factor_data.join(generator_column)

    return factor_data
