from students.management.commands.seed_data import Command as SeedDataCommand

class Command(SeedDataCommand):
    help = 'Alias for seed_data command.'
