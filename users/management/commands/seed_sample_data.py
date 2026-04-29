"""
Seed sample students + choices for testing.
Usage: python manage.py seed_sample_data

Creates:
  - 1 superuser  → username: admin      / password: admin123
  - 10 students  → username: student01… / password: test1234
  - Choices for each student (random priority order)
"""
import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from electives.models import Elective, Choice

Student = get_user_model()

STUDENTS = [
    ("student01", "Aarav",    "Shah",      "1CS21CS001", 9.2),
    ("student02", "Priya",    "Nair",      "1CS21CS002", 8.7),
    ("student03", "Rohan",    "Mehta",     "1CS21CS003", 8.5),
    ("student04", "Sneha",    "Iyer",      "1CS21CS004", 8.1),
    ("student05", "Karan",    "Verma",     "1CS21CS005", 7.9),
    ("student06", "Divya",    "Pillai",    "1CS21CS006", 7.6),
    ("student07", "Arjun",    "Reddy",     "1CS21CS007", 7.3),
    ("student08", "Meera",    "Joshi",     "1CS21CS008", 6.9),
    ("student09", "Vikram",   "Sharma",    "1CS21CS009", 6.5),
    ("student10", "Ananya",   "Gupta",     "1CS21CS010", 6.1),
    ("student11", "Ishaan",   "Kapoor",    "1CS21CS011", 9.5),
    ("student12", "Kavya",    "Menon",     "1CS21CS012", 9.1),
    ("student13", "Rahul",    "Singh",     "1CS21CS013", 8.9),
    ("student14", "Pooja",    "Desai",     "1CS21CS014", 8.8),
    ("student15", "Nikhil",   "Bhat",      "1CS21CS015", 8.6),
    ("student16", "Shreya",   "Kulkarni",  "1CS21CS016", 8.4),
    ("student17", "Aditya",   "Pandey",    "1CS21CS017", 8.3),
    ("student18", "Riya",     "Chatterjee","1CS21CS018", 8.2),
    ("student19", "Siddharth","Rao",       "1CS21CS019", 8.0),
    ("student20", "Tanvi",    "Mishra",    "1CS21CS020", 7.8),
    ("student21", "Harsh",    "Agarwal",   "1CS21CS021", 7.7),
    ("student22", "Nisha",    "Tiwari",    "1CS21CS022", 7.5),
    ("student23", "Varun",    "Malhotra",  "1CS21CS023", 7.4),
    ("student24", "Simran",   "Bajaj",     "1CS21CS024", 7.2),
    ("student25", "Akash",    "Srivastava","1CS21CS025", 7.1),
    ("student26", "Deepika",  "Nambiar",   "1CS21CS026", 7.0),
    ("student27", "Manish",   "Dubey",     "1CS21CS027", 6.8),
    ("student28", "Anjali",   "Saxena",    "1CS21CS028", 6.7),
    ("student29", "Suresh",   "Patil",     "1CS21CS029", 6.6),
    ("student30", "Kritika",  "Bhatt",     "1CS21CS030", 6.4),
    ("student31", "Yash",     "Chandra",   "1CS21CS031", 6.3),
    ("student32", "Pallavi",  "Hegde",     "1CS21CS032", 6.2),
    ("student33", "Gaurav",   "Shukla",    "1CS21CS033", 6.0),
    ("student34", "Swati",    "Bansal",    "1CS21CS034", 5.9),
    ("student35", "Rajesh",   "Kumar",     "1CS21CS035", 5.8),
    ("student36", "Neha",     "Tripathi",  "1CS21CS036", 5.7),
    ("student37", "Abhishek", "Ghosh",     "1CS21CS037", 5.6),
    ("student38", "Shweta",   "Jain",      "1CS21CS038", 5.5),
    ("student39", "Pranav",   "Negi",      "1CS21CS039", 5.4),
    ("student40", "Lakshmi",  "Venkat",    "1CS21CS040", 5.3),
    ("student41", "Mohit",    "Arora",     "1CS21CS041", 5.2),
    ("student42", "Ruchika",  "Sinha",     "1CS21CS042", 5.1),
    ("student43", "Tejas",    "Naik",      "1CS21CS043", 5.0),
    ("student44", "Bhavna",   "Yadav",     "1CS21CS044", 4.9),
    ("student45", "Chirag",   "Lal",       "1CS21CS045", 4.8),
    ("student46", "Disha",    "Rawat",     "1CS21CS046", 4.7),
    ("student47", "Eshan",    "Bose",      "1CS21CS047", 4.6),
    ("student48", "Falguni",  "Parekh",    "1CS21CS048", 4.5),
    ("student49", "Girish",   "Thakur",    "1CS21CS049", 4.4),
    ("student50", "Harini",   "Suresh",    "1CS21CS050", 4.3),
]


class Command(BaseCommand):
    help = 'Seed sample students and choices for testing'

    def handle(self, *args, **kwargs):
        # 1. Admin account
        if not Student.objects.filter(username='admin').exists():
            Student.objects.create_superuser(
                username='admin',
                password='admin123',
                email='admin@optislot.dev',
                usn='ADMIN001',
                cgpa=10.0,
                first_name='Admin',
                last_name='User',
            )
            self.stdout.write(self.style.SUCCESS('  Created superuser → admin / admin123'))
        else:
            self.stdout.write('  Superuser "admin" already exists')

        # 2. Fetch electives (must run seed_electives first)
        electives = list(Elective.objects.all())
        if len(electives) < 3:
            self.stdout.write(self.style.ERROR(
                'Not enough electives. Run: python manage.py seed_electives first.'
            ))
            return

        # 3. Create students + choices
        for username, first, last, usn, cgpa in STUDENTS:
            student, created = Student.objects.get_or_create(
                username=username,
                defaults={
                    'first_name': first,
                    'last_name': last,
                    'email': f'{username}@college.edu',
                    'usn': usn,
                    'cgpa': cgpa,
                }
            )
            if created:
                student.set_password('test1234')
                student.save()
                self.stdout.write(self.style.SUCCESS(f'  Created {username} (CGPA {cgpa})'))
            else:
                self.stdout.write(f'  Already exists: {username}')
                continue  # skip re-creating choices

            # Pick 3 distinct random electives as choices
            picks = random.sample(electives, 3)
            for priority, elective in enumerate(picks, start=1):
                Choice.objects.get_or_create(
                    student=student,
                    priority=priority,
                    defaults={'elective': elective}
                )

        self.stdout.write(self.style.SUCCESS(
            '\nDone! Login credentials:\n'
            '  Admin   → admin / admin123\n'
            '  Students → student01…student10 / test1234'
        ))
