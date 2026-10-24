import numpy as np, pytest
from tariff_models import MarginalBlockTariff, AllUnitsSlabTariff, two_tier, UP_URBAN_DOMESTIC_FY2019_20 as UP

def test_hand_example_up():
    # Hand calculation: 420 kWh = 150*5.5 + 150*6.0 + 120*6.5 = 825 + 900 + 780 = 2505
    assert UP.bill(420.0) == pytest.approx(2505.0)

def test_at_thresholds_and_blocks():
    T = two_tier(5.0, 7.0, 200.0)
    assert T.bill(0.0) == 0.0
    assert T.bill(200.0) == pytest.approx(1000.0)       # exactly on threshold: all at p1
    assert T.bill(199.0) == pytest.approx(995.0)
    assert T.bill(201.0) == pytest.approx(1007.0)       # one unit in upper block
    assert T.bill(300.0) == pytest.approx(1700.0)

def test_hinge_matches_block_by_block():
    rng = np.random.default_rng(0)
    for x in rng.uniform(0, 1500, 500):
        assert UP.bill(x) == pytest.approx(UP.bill_by_blocks(x))

def test_convexity_flag_and_validation():
    assert UP.is_convex
    assert not MarginalBlockTariff((100.0,), (6.0, 5.0)).is_convex
    with pytest.raises(ValueError):
        MarginalBlockTariff((200.0, 100.0), (1, 2, 3))
    with pytest.raises(ValueError):
        MarginalBlockTariff((100.0,), (1.0,))

def test_proration_perspective():
    T = two_tier(5.0, 7.0, 200.0)
    # 60-day period: threshold doubles; B_60(x) = 2 B(x/2)
    assert T.bill(500.0, days=60) == pytest.approx(2 * T.bill(250.0))
    assert T.bill(310.0, days=31) == pytest.approx((31 / 30) * T.bill(310.0 * 30 / 31))

def test_all_units_slab():
    S = AllUnitsSlabTariff((150.0,), (5.5, 6.0))
    assert S.bill(150.0) == pytest.approx(825.0)
    assert S.bill(151.0) == pytest.approx(906.0)
