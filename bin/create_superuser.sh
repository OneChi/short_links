echo 'Create superuser...'

poetry run ./manage.py shell -c "
import sys
try:
    from recruiters.models import Recruiter

    if Recruiter.objects.filter(email='admin@admin.com').exists() is False:
        Recruiter.objects.create_superuser('admin', 'admin@admin.com', 'P@ssw0rd1',role=2)
        sys.exit('Done!')
    sys.exit('Super user is already exists!')
except:
    from users.models import User

    if User.objects.filter(email='admin@admin.com').exists() is False:
        User.objects.create_superuser('admin', 'admin@admin.com', 'P@ssw0rd1')
        sys.exit('Done!')
    sys.exit('Super user is already exists!')

"
