from django.contrib import admin

from .models import target
from .models import phishr_user
from .models import campaign_directory
from .models import campaign_results
from .models import company
'''
from .models import operation_test_1
from .models import operation_test_2
from .models import operation_test_3
from .models import operation_test_4
from .models import operation_test_5
from .models import operation_test_6
'''

from django.apps import apps
admin.site.register(company)
admin.site.register(target)
admin.site.register(phishr_user)
admin.site.register(campaign_directory)
admin.site.register(campaign_results)


'''
admin.site.register(operation_test_6)
admin.site.register(operation_test_5)
admin.site.register(operation_test_4)
admin.site.register(operation_test_3)
admin.site.register(operation_test_2)
admin.site.register(operation_test_1)
'''