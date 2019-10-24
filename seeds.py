from random import random, randint
from datetime import timedelta
from faker import Faker
from faker.providers import internet
from flask_script import Command
from person import Person
from helpers import generate_random_key

from app import db


class PersonSeeder(Command):

    """Seeder class for the Person model."""

    fake = Faker('es_MX')
    people = []
    capture_all_args = True

    def run(self, args):
        if not args or len(args) > 1 or not args[0].isdigit():
            seed_number = 20
            print(f'Invalid seed number argument. Defaulting to {seed_number}')
        else:
            seed_number = int(args[0])
            print(f'Seeding {seed_number} persons into the database')
        PersonSeeder.fake.add_provider(internet)
        for _ in range(int(seed_number)):
            self.seed_one_person()
        for person in PersonSeeder.people:
            db.session.add(person)
        db.session.commit()

    def seed_one_person(self):
        first_name = PersonSeeder.fake.first_name()
        last_name = PersonSeeder.fake.last_name()
        mail = self.generate_mail(first_name, last_name)
        contact_mail = self.generate_mail(
            PersonSeeder.fake.first_name(),
            PersonSeeder.fake.last_name()
        )
        plain_key = generate_random_key()

        person = Person(first_name, last_name, mail, contact_mail, plain_key)

        # Find 40% of the seeded people
        if random() < 0.4:
            person.set_as_found()
            person.found_date += timedelta(days=randint(0, 3))
            person.found_date += timedelta(hours=randint(0, 23))
            person.found_date += timedelta(minutes=randint(0, 59))
            person.found_date += timedelta(seconds=randint(0, 59))

        PersonSeeder.people.append(person)

    @staticmethod
    def generate_mail(first_name, last_name):
        username = first_name.lower()[0] + last_name.lower()[:randint(3, 7)]
        number = "".join([str(randint(0, 9)) for _ in range(randint(0, 4))])
        domain = PersonSeeder.fake.free_email_domain()
        return f'{username}{number}@{domain}'
