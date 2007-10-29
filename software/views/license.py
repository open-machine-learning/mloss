from django.views.generic import list_detail
from mloss.software.models import Software


def license_with_software(request):
    """
    List of Users with Software

    Template::
        software/user_list.html
    
    """
    licenselist = Software.objects.filter(os_license__isnull=False)
    unique_licenses=set()
    unique_sw_ids=list()
    for l in licenselist:
        if l.os_license not in unique_licenses:
            unique_licenses.add(l.os_license)
            unique_sw_ids.append(l.id)
    unique_sw_ids=tuple(unique_sw_ids)
    licenselist=licenselist.extra(where=['id IN ' + `unique_sw_ids`])

    return list_detail.object_list(request,
                                   paginate_by=20,
                                   queryset=licenselist,
                                   template_name='software/license_list.html',
                                   )

