from custom_user.models import AbstractEmailUser


class GallantUser(AbstractEmailUser):

    """
    Custom Gallant user
    """

    class Meta(AbstractEmailUser.Meta):
        swappable = 'AUTH_USER_MODEL'
