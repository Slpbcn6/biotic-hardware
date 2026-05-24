import json

def test_resonance_file_exists_and_valid():

    with open("data/resonance_params.json") as f:
        data = json.load(f)

    assert "Q_factor" in data
    assert "f_resonance_Hz" in data

    assert data["Q_factor"] > 0
    assert data["f_resonance_Hz"] > 0