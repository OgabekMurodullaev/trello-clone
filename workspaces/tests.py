from django.contrib.auth import get_user_model
from django.test import TestCase

from workspaces.models import Workspace

User = get_user_model()

# 1 - Unit Tests
class WorkspaceModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(email="ogabek@mail.ru", first_name="Og'abek", last_name="Murodullayev")
        self.user.set_password("testpass")
        self.user.save()

    def test_create_workspace(self):
        workspace = Workspace.objects.create(name="Ogabek's workspace", owner=self.user)
        self.assertEqual(workspace.name, "Ogabek's workspace")
        self.assertEqual(workspace.owner, self.user)