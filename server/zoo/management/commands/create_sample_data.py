from django.core.management.base import BaseCommand
from django.utils import timezone
from zoo.models import Habitat, Enclosure
from bookings.models import Feeding


class Command(BaseCommand):
    help = 'Create sample zoo data for development and testing'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample zoo data...')

        # Clear existing data
        Feeding.objects.all().delete()
        Enclosure.objects.all().delete()
        Habitat.objects.all().delete()

        # Create habitats
        savanna = Habitat.objects.create(
            name="African Savanna",
            location="North Wing"
        )
        jungle = Habitat.objects.create(
            name="Tropical Rainforest",
            location="East Wing"
        )
        arctic = Habitat.objects.create(
            name="Arctic Tundra",
            location="South Wing"
        )
        aquatic = Habitat.objects.create(
            name="Aquatic Center",
            location="West Wing"
        )
        reptile = Habitat.objects.create(
            name="Reptile House",
            location="Central Building"
        )

        # Create enclosures
        lion_enc = Enclosure.objects.create(
            name="Lion Pride Enclosure",
            capacity=8,
            is_active=True,
            habitat=savanna
        )
        elephant_enc = Enclosure.objects.create(
            name="Elephant Sanctuary",
            capacity=6,
            is_active=True,
            habitat=savanna
        )
        Enclosure.objects.create(
            name="Giraffe Meadow",
            capacity=10,
            is_active=True,
            habitat=savanna
        )

        gorilla_enc = Enclosure.objects.create(
            name="Gorilla Habitat",
            capacity=12,
            is_active=True,
            habitat=jungle
        )
        Enclosure.objects.create(
            name="Monkey Island",
            capacity=20,
            is_active=True,
            habitat=jungle
        )

        polar_bear_enc = Enclosure.objects.create(
            name="Polar Bear Pool",
            capacity=4,
            is_active=True,
            habitat=arctic
        )
        penguin_enc = Enclosure.objects.create(
            name="Penguin Colony",
            capacity=50,
            is_active=True,
            habitat=arctic
        )

        dolphin_enc = Enclosure.objects.create(
            name="Dolphin Bay",
            capacity=8,
            is_active=True,
            habitat=aquatic
        )
        Enclosure.objects.create(
            name="Sea Lion Cove",
            capacity=12,
            is_active=True,
            habitat=aquatic
        )

        snake_enc = Enclosure.objects.create(
            name="Serpent Gallery",
            capacity=30,
            is_active=True,
            habitat=reptile
        )
        Enclosure.objects.create(
            name="Crocodile Lagoon",
            capacity=6,
            is_active=True,
            habitat=reptile
        )

        # Create under maintenance enclosure (inactive)
        Enclosure.objects.create(
            name="Rhino Range (Under Renovation)",
            capacity=4,
            is_active=False,
            habitat=savanna
        )

        # Create sample feeding schedules
        now = timezone.now()

        # Morning feedings
        Feeding.objects.create(
            enclosure=lion_enc,
            keeper="Sarah Johnson",
            start_time=now.replace(hour=8, minute=0),
            end_time=now.replace(hour=9, minute=0)
        )
        Feeding.objects.create(
            enclosure=elephant_enc,
            keeper="Michael Chen",
            start_time=now.replace(hour=8, minute=30),
            end_time=now.replace(hour=9, minute=30)
        )
        Feeding.objects.create(
            enclosure=penguin_enc,
            keeper="Emma Wilson",
            start_time=now.replace(hour=9, minute=0),
            end_time=now.replace(hour=9, minute=45)
        )

        # Midday feedings
        Feeding.objects.create(
            enclosure=gorilla_enc,
            keeper="David Martinez",
            start_time=now.replace(hour=12, minute=0),
            end_time=now.replace(hour=13, minute=0)
        )
        Feeding.objects.create(
            enclosure=dolphin_enc,
            keeper="Rachel Green",
            start_time=now.replace(hour=12, minute=30),
            end_time=now.replace(hour=13, minute=30)
        )

        # Afternoon feedings
        Feeding.objects.create(
            enclosure=polar_bear_enc,
            keeper="James Anderson",
            start_time=now.replace(hour=15, minute=0),
            end_time=now.replace(hour=16, minute=0)
        )
        Feeding.objects.create(
            enclosure=snake_enc,
            keeper="Lisa Thompson",
            start_time=now.replace(hour=15, minute=30),
            end_time=now.replace(hour=16, minute=15)
        )

        # Evening feedings
        Feeding.objects.create(
            enclosure=lion_enc,
            keeper="Sarah Johnson",
            start_time=now.replace(hour=17, minute=0),
            end_time=now.replace(hour=18, minute=0)
        )

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created:\n'
                f'  - {Habitat.objects.count()} habitats\n'
                f'  - {Enclosure.objects.count()} enclosures\n'
                f'  - {Feeding.objects.count()} feeding schedules'
            )
        )
