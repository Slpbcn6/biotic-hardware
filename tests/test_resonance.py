import json

def test_resonance_config_integrity():
    with open("data/parameters.json") as f:
        data = json.load(f)

    freq = data["I_simulation_fixed_parameters"]["frequency_hz"]
    q = data["IV_network_performance_metrics"]["individual_q_factor"]

    assert isinstance(freq, (int, float))
    assert isinstance(q, (int, float))

    assert freq > 0
    assert q > 0

    assert 0 < q < 100
    assert 1 < freq < 1e6