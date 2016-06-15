from gallant import models as g
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator


UserModel = get_user_model()

for user in g.GallantUser.objects.all():
    token = default_token_generator.make_token(user)
    link = 'http://galant.com/en/register/' + str(user.id) + '?token=%s' % token
    names = user.name.split()

    if len(names):
        first = names[0]
    else:
        first = ''

    if len(names) > 1:
        last = ' '.join(names[1:])
    else:
        last = ''

    print '\t'.join([user.email, first, last, link])
