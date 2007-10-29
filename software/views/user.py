from django.contrib.auth.models import User
from django.views.generic import list_detail


def user_with_software(request):
    """
    List of Users with Software

    Template::
        software/user_list.html
    
    """
    userlist = User.objects.filter(software__isnull=False).distinct()
    return list_detail.object_list(request,
                                   paginate_by=20,
                                   queryset=userlist,
                                   template_name='software/user_list.html',
                                   )
