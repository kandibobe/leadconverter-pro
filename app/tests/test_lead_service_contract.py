from pact import Consumer, Provider


def test_basic_pact_contract():
    pact = Consumer("backend").has_pact_with(Provider("lead-service"), pact_dir="pacts")
    assert pact.consumer.name == "backend"
    assert pact.provider.name == "lead-service"
