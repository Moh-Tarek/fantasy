# from django.core.management.base import BaseCommand
# from django.contrib.auth.models import User
# import names

# class Command(BaseCommand):

#     def handle(self, *args, **options):
#         # create random users
#         users = []
#         users_usernames = []
#         for i in range(1, 101):
#             f = names.get_first_name()
#             l = names.get_last_name()
#             u = f.lower()+l.lower()
#             for i in range(1, 10):
#                 if u in users_usernames:
#                     u + str(i)
#                 else:
#                     users_usernames.append(u)
#                     break
#             users.append(User(first_name=f, last_name=l, username=u, password=u))
#         User.objects.bulk_create(users)
#         print(f"{len(users)} users have been created successfully")
            
        