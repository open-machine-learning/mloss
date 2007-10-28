from django.views.generic import list_detail
from mloss.software.models import Software


def language_with_software(request):
    """
    List of Users with Software

    Template::
        software/user_list.html
    
    """
    languagelist = Software.objects.filter(language__isnull=False)
    unique_languages=set()
    unique_sw_ids=list()
    for l in languagelist:
        if l.language not in unique_languages:
            unique_languages.add(l.language)
            unique_sw_ids.append(l.id)
    unique_sw_ids=tuple(unique_sw_ids)
    print unique_sw_ids
    languagelist=languagelist.extra(where=['id IN ' + `unique_sw_ids`])

    return list_detail.object_list(request,
                                   paginate_by=10,
                                   queryset=languagelist,
                                   template_name='software/language_list.html',
                                   )

