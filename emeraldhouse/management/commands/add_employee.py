from django.core.management.base import BaseCommand

from emeraldhouse.services import user_service


class Command(BaseCommand):
    help = "Create or update an employee and their security groups."

    def add_arguments(self, parser):
        parser.add_argument("--first_name", type=str)
        parser.add_argument("--last_name", type=str)
        parser.add_argument("--email", type=str)
        parser.add_argument("--password", type=str)
        parser.add_argument("--security_groups", nargs="+", type=str)

    def handle(self, *args, **options):
        created_user = user_service.get_or_create_user(
            first_name=options["first_name"],
            last_name=options["last_name"],
            email=options["email"],
        )

        user_service.set_user_password(
            user_id=created_user.id,
            password=options["password"],
        )

        user_service.set_user_groups(
            user_id=created_user.id,
            group_names=options["security_groups"] or [],
        )
