from django.shortcuts import render
from django.contrib.auth.models import Group, Permission

def manage_permissions(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            # Implement logic to add or remove permissions based on user input
            pass
        groups = Group.objects.all()
        permissions = Permission.objects.all()
        return render(request, 'manage_permissions.html', {'groups': groups, 'permissions': permissions})
    else:
        return render(request, 'permission_denied.html')

def permission_denied(request):
    return render(request, 'permission_denied.html')

from django.shortcuts import render, redirect
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

def update_permissions(request):
    if request.method == 'POST':
        # Handle standard permissions
        permission_groups = {
            'Principal': request.POST.getlist('principal_perms'),
            'HOD': request.POST.getlist('hod_perms'),
            'Teacher': request.POST.getlist('teacher_perms'),
            'Staff': request.POST.getlist('staff_perms'),
            'Student': request.POST.getlist('student_perms'),
        }

        for group_name, perms in permission_groups.items():
            group = Group.objects.get(name=group_name)
            # Remove all existing permissions
            group.permissions.clear()
            # Add selected permissions
            for perm_codename in perms:
                try:
                    permission = Permission.objects.get(codename=perm_codename)
                    group.permissions.add(permission)
                except Permission.DoesNotExist:
                    continue

        # Handle special permissions
        if 'is_staff' in request.POST:
            request.user.is_staff = True
        else:
            request.user.is_staff = False
        
        if 'is_superuser' in request.POST:
            request.user.is_superuser = True
        else:
            request.user.is_superuser = False

        request.user.save()

        return redirect('manage_permissions')  # Redirect to the page displaying updated permissions

    # Render the form with current permissions
    return render(request, 'manage_permissions.html', {
        'principal_perms': get_permissions_for_group('Principal'),
        'hod_perms': get_permissions_for_group('HOD'),
        'teacher_perms': get_permissions_for_group('Teacher'),
        'staff_perms': get_permissions_for_group('Staff'),
        'student_perms': get_permissions_for_group('Student'),
        'user': request.user
    })

def get_permissions_for_group(group_name):
    group = Group.objects.get(name=group_name)
    content_types = ContentType.objects.all()
    permissions = Permission.objects.filter(content_type__in=content_types)
    perm_list = []
    for perm in permissions:
        perm_list.append({
            'codename': perm.codename,
            'name': perm.name,
            'is_checked': perm in group.permissions.all()
        })
    return perm_list
