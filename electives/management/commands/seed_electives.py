"""
Management command to seed sample electives.
Usage: python manage.py seed_electives
"""
from django.core.management.base import BaseCommand
from electives.models import Elective

SAMPLE_ELECTIVES = [
    ('CS601', 'Machine Learning', 'Fundamentals of ML algorithms and applications.', 15),
    ('CS602', 'Cloud Computing', 'AWS, Azure, GCP and cloud-native architectures.', 15),
    ('CS603', 'Blockchain Technology', 'Distributed ledger, smart contracts, DeFi.', 15),
    ('CS604', 'Internet of Things', 'Embedded systems, sensors, and IoT protocols.', 15),
    ('CS605', 'Cyber Security', 'Network security, cryptography, ethical hacking.', 15),
    ('CS606', 'Data Science', 'Statistical analysis, visualization, and big data.', 15),
    ('CS607', 'Natural Language Processing', 'Text processing, transformers, LLMs.', 15),
    ('CS608', 'Computer Vision', 'Image processing, CNNs, object detection.', 15),
]


class Command(BaseCommand):
    help = 'Seed the database with sample electives'

    def handle(self, *args, **kwargs):
        created = 0
        for code, name, desc, seats in SAMPLE_ELECTIVES:
            obj, was_created = Elective.objects.get_or_create(
                code=code,
                defaults={'name': name, 'description': desc, 'total_seats': seats, 'available_seats': seats}
            )
            if was_created:
                created += 1
                self.stdout.write(self.style.SUCCESS(f'  Created: {code} - {name}'))
            else:
                self.stdout.write(f'  Already exists: {code}')

        self.stdout.write(self.style.SUCCESS(f'\nDone. {created} electives created.'))
