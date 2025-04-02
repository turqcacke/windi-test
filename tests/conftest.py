import pytest
from faker import Faker

FAKER_SEED = 0


@pytest.fixture(scope="session")
def faker():
    faker = Faker()
    faker.seed_instance(seed=FAKER_SEED)
    return faker
