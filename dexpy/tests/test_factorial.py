from unittest import TestCase

from dexpy.factorial import build_factorial
from dexpy.alias import alias_list

class TestFactorial(TestCase):

    def test_full(self):
        """Tests a full two-level factorial."""
        factor_count = 3
        run_count = 8
        design = build_factorial(factor_count, run_count)
        self.assertEqual(8, len(design))
        # should be able to estimate the full 3FI model
        aliases, _ = alias_list("(A+B+C)**3", design)
        self.assertEqual(0, len(aliases))

    def test_res_v(self):
        """Tests a 2^(5-1) fractional factorial."""
        factor_count = 5
        run_count = 16
        design = build_factorial(factor_count, run_count)
        self.assertEqual(16, len(design))
        aliases, _ = alias_list("(A+B+C+D+E)**2", design)
        # should be no 2FI aliases in a res v design
        self.assertEqual(0, len(aliases))
        aliases, _ = alias_list("(A+B+C+D+E)**3", design)
        # every 2FI should be aliased with a 3FI
        answer_aliases = [
            'A:B = C:D:E',
            'A:C = B:D:E',
            'A:D = B:C:E',
            'A:E = B:C:D',
            'B:C = A:D:E',
            'B:D = A:C:E',
            'B:E = A:C:D',
            'C:D = A:B:E',
            'C:E = A:B:D',
            'D:E = A:B:C'
        ]
        self.assertEqual(answer_aliases, aliases)

    def test_res_iii(self):
        """Tests a 2^(6-3) fractional factorial."""
        factor_count = 6
        run_count = 8
        design = build_factorial(factor_count, run_count)
        self.assertEqual(8, len(design))
        model = "(A+B+C+D+E+F)**2"
        aliases, _ = alias_list(model, design)
        answer_aliases = [
            'A = B:D + C:E',
            'B = A:D + C:F',
            'C = A:E + B:F',
            'D = A:B + E:F',
            'E = A:C + D:F',
            'F = B:C + D:E',
            'A:F = B:E + C:D',
        ]
        self.assertEqual(answer_aliases, aliases)

    def test_res_iii_seven_fac(self):
        """Tests a 2^(7-4) fractional factorial."""
        factor_count = 7
        run_count = 8
        design = build_factorial(factor_count, run_count)
        self.assertEqual(8, len(design))
        aliases, _ = alias_list("(A+B+C+D+E+F+G)**2", design)
        answer_aliases = [
            'A = B:D + C:E + F:G', 'B = A:D + C:F + E:G',
            'C = A:E + B:F + D:G', 'D = A:B + C:G + E:F',
            'E = A:C + B:G + D:F', 'F = A:G + B:C + D:E',
            'G = A:F + B:E + C:D'
        ]
        self.assertEqual(answer_aliases, aliases)

    def test_res_iii_21_fac(self):
        """Tests a 2^(21-16) fractional factorial."""
        factor_count = 21
        run_count = 32
        design = build_factorial(factor_count, run_count)
        self.assertEqual(32, len(design))
        model = "(A+B+C+D+E+F+G+H+J+K+L+M+N+O+P+Q+R+S+T+U+V)**2"
        aliases, _ = alias_list(model, design)
        answer_aliases = [
            'A = J:K + N:O + Q:R + S:T + U:V',
            'B = H:K + M:O + P:R + S:U + T:V',
            'C = G:K + L:O + P:T + Q:U + R:V',
            'D = F:K + L:R + M:T + N:U + O:V',
            'E = F:O + G:R + H:T + J:U + K:V',
            'F = D:K + E:O + P:U + Q:T + R:S',
            'G = C:K + E:R + M:U + N:T + O:S',
            'H = B:K + E:T + L:U + N:R + O:Q',
            'J = A:K + E:U + L:T + M:R + O:P',
            'K = A:J + B:H + C:G + D:F + E:V + L:S + M:Q + N:P',
            'L = C:O + D:R + H:U + J:T + K:S',
            'M = B:O + D:T + G:U + J:R + K:Q',
            'N = A:O + D:U + G:T + H:R + K:P',
            'O = A:N + B:M + C:L + D:V + E:F + G:S + H:Q + J:P',
            'P = B:R + C:T + F:U + J:O + K:N',
            'Q = A:R + C:U + F:T + H:O + K:M',
            'R = A:Q + B:P + C:V + D:L + E:G + F:S + H:N + J:M',
            'S = A:T + B:U + F:R + G:O + K:L',
            'T = A:S + B:V + C:P + D:M + E:H + F:Q + G:N + J:L',
            'U = A:V + B:S + C:Q + D:N + E:J + F:P + G:M + H:L',
            'V = A:U + B:T + C:R + D:O + E:K',
            'A:B = C:F + D:G + E:L + H:J + M:N + P:Q + S:V + T:U',
            'A:C = B:F + D:H + E:M + G:J + L:N + P:S + Q:V + R:U',
            'A:D = B:G + C:H + E:P + F:J + L:Q + M:S + N:V + O:U',
            'A:E = B:L + C:M + D:P + F:N + G:Q + H:S + J:V + K:U',
            'A:F = B:C + D:J + E:N + G:H + L:M + P:V + Q:S + R:T',
            'A:G = B:D + C:J + E:Q + F:H + L:P + M:V + N:S + O:T',
            'A:H = B:J + C:D + E:S + F:G + L:V + M:P + N:Q + O:R',
            'A:L = B:E + C:N + D:Q + F:M + G:P + H:V + J:S + K:T',
            'A:M = B:N + C:E + D:S + F:L + G:V + H:P + J:Q + K:R',
            'A:P = B:Q + C:S + D:E + F:V + G:L + H:M + J:N + K:O'
        ]

        self.assertEqual(answer_aliases, aliases)
