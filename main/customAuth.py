from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from omero.gateway import BlitzGateway


class OMEROBackend(ModelBackend):

    # create OMERO conection
    def OMconnection(self,user, pwd, host, secure=True):
        conn = BlitzGateway(user, pwd, host=host, secure=secure)
        conn.connect()
        return conn

    def OMDisconect(self, conn):
        conn.close()

    def authenticate(self, request, username=None, password=None,host =None, **kwargs):
        try:
            conn = self.OMconnection(username, password, host, secure=True)
            conn.getGroupsMemberOf()
            group = conn.getGroupFromContext()
            group.groupSummary()

            self.OMDisconect(conn)

            combined_username = f"{username}@{host}"
            try:

                user = User.objects.get(username=combined_username)
            except User.DoesNotExist:
                user = User(username=combined_username)
                user.is_staff = True
                user.save()
            return user

        except Exception as e:
            print('Error connecting to OMERO: {}'.format(str(e)))
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

