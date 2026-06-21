User.objects.filter(username__iexact=value).exists()
User.objects.filter(email__iexact=value).exists()
User.objects.filter(username=value).exists()
# -----------------
from django.db.models import Q
exists = User.objects.filter(Q(username__iexact=value) | Q(email__iexact=value)).exists()
# -----------------