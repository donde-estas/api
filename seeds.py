from faker import Faker
from faker.providers import internet
from flask_dbseeder import SeedManager
from person import Person
from helpers import generate_random_key


class PersonSeeder(SeedManager):

    fake = Faker('es_MX')

    def run(self):
        PersonSeeder.fake.add_provider(internet)
        for _ in range(20):
            self.seed_one_person()

    def seed_one_person(self):
        first_name = PersonSeeder.fake.first_name()
        last_name = PersonSeeder.fake.last_name()
        mail = PersonSeeder.fake.email(first_name, last_name)
        contact_mail = PersonSeeder.fake.email(
            PersonSeeder.fake.first_name(),
            PersonSeeder.fake.last_name()
        )
        plain_key = generate_random_key()

        person = Person(first_name, last_name, mail, contact_mail, plain_key)
        self.save(person)
