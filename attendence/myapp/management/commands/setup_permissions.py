# from django.core.management.base import BaseCommand
# from django.contrib.auth.models import Group, Permission
# from django.contrib.contenttypes.models import ContentType

# class Command(BaseCommand):
#     help = 'Setup groups and permissions for roles'

#     def handle(self, *args, **kwargs):
#         permissions = {
#             'Principal': ['add_principal', 'change_principal', 'delete_principal',
#                           'add_hod', 'change_hod', 'delete_hod',
#                           'add_teacher', 'change_teacher', 'delete_teacher',
#                           'add_staff', 'change_staff', 'delete_staff',
#                           'add_student', 'change_student', 'delete_student'],
#             'HOD': ['change_teacher', 'delete_teacher',
#                     'change_staff', 'delete_staff',
#                     'change_student', 'delete_student'],
#             'Teacher': ['change_student', 'delete_student'],
#             'Staff': ['change_student', 'delete_student'],
#             'Student': []
#         }

#         for group_name, perms in permissions.items():
#             group, created = Group.objects.get_or_create(name=group_name)
#             if created:
#                 self.stdout.write(self.style.SUCCESS(f'Created group: {group_name}'))

#             content_types = ContentType.objects.all()
#             for perm_name in perms:
#                 try:
#                     permission = Permission.objects.get(codename=perm_name)
#                     group.permissions.add(permission)
#                     self.stdout.write(self.style.SUCCESS(f'Added permission {perm_name} to group {group_name}'))
#                 except Permission.DoesNotExist:
#                     self.stdout.write(self.style.ERROR(f'Permission {perm_name} does not exist'))

#         self.stdout.write(self.style.SUCCESS('Groups and permissions setup complete.'))


from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

# Create groups
groups = {
    'Student': [],
    'Teacher': [
        'view_student',
        'view_teacher',
    ],
    'Staff': [
        'view_student',
        'view_teacher',
    ],
    'HOD': [
        'view_student',
        'change_student',
        'view_teacher',
        'change_teacher',
        'view_hod',
        'change_hod'
    ],
    'Principal': [
        'view_student',
        'change_student',
        'view_teacher',
        'change_teacher',
        'view_hod',
        'change_hod',
        'view_principal',
        'change_principal'
    ]
}

# Create groups and assign permissions
for group_name, permissions in groups.items():
    group, created = Group.objects.get_or_create(name=group_name)
    for perm_code in permissions:
        app_label, codename = perm_code.split('_')
        try:
            permission = Permission.objects.get(codename=codename, content_type__app_label=app_label)
            group.permissions.add(permission)
        except Permission.DoesNotExist:
            print(f"Permission '{perm_code}' does not exist.")

print("Groups and permissions set up successfully.")
