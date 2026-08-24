import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bond_pricing import (
    bond_price, bond_ytm, macaulay_duration, modified_duration,
    convexity, portfolio_duration, immunization_weights
)


def test_bond_at_par():
    F, c, T, y = 100, 0.05, 5, 0.05
    price = bond_price(F, c, T, y)
    assert abs(price - 100) < 1e-6


def test_ytm_recovers_original_yield():
    F, c, T, y = 100, 0.05, 5, 0.05
    price = bond_price(F, c, T, y)
    ytm = bond_ytm(price, F, c, T)
    assert abs(ytm - y) < 1e-4


def test_macaulay_duration_below_maturity():
    F, c, T, y = 100, 0.05, 5, 0.05
    duration = macaulay_duration(F, c, T, y)
    assert duration < T


def test_modified_duration_below_macaulay():
    F, c, T, y = 100, 0.05, 5, 0.05
    mac = macaulay_duration(F, c, T, y)
    mod = modified_duration(F, c, T, y)
    assert mod < mac


def test_convexity_positive():
    F, c, T, y = 100, 0.05, 5, 0.05
    conv = convexity(F, c, T, y)
    assert conv > 0


def test_immunization_weights_sum_to_one():
    w_short, w_long = immunization_weights(7, 5, 10)
    assert abs((w_short + w_long) - 1) < 1e-10


def test_immunization_achieves_target_duration():
    w_short, w_long = immunization_weights(7, 5, 10)
    port_dur = portfolio_duration([w_short, w_long], [5, 10])
    assert abs(port_dur - 7) < 1e-10