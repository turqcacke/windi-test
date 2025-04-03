import pytest
from faker import Faker

from tests.consts import SEED


@pytest.fixture()
def faker():
    faker = Faker()
    faker.seed_instance(seed=SEED)
    return faker
