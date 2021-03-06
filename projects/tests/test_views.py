from django.test import TestCase, Client
from django.urls import reverse
from projects.models import ProjectCategory, Project, Task, TaskOffer, Team
from projects.views import get_user_task_permissions
from user.models import User
import json


class TestViews(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.test_user1 = User.objects.create(
            username="testuser1", email="test1@email.com",
        )
        self.test_user1.set_password("argkwargs123")
        self.test_user1.save()
        self.test_user2 = User.objects.create(
            username="testuser2", email="test2@email.com",
        )
        self.test_user2.set_password("argkwargs123")
        self.test_user2.save()
        self.test_category = ProjectCategory.objects.create(name="Gardening")
        self.test_project = Project.objects.create(
            user=self.test_user1.profile,
            title="Test project",
            description="some description",
            category=self.test_category,
        )
        self.test_task = Task.objects.create(
            project=self.test_project,
            title="Test task",
            description="some description",
            budget=42,
        )

        self.projects_url = reverse("projects")
        self.project_view_url = reverse("project_view", args=[self.test_project.id])

    def test_projects_GET(self):
        response = self.client.get(self.projects_url)

        self.assertEquals(
            response.status_code, 200
        )  # We need to check that we get the correct response
        self.assertTemplateUsed(response, "projects/projects.html")

    def test_project_view_GET(self):
        response = self.client.get(self.project_view_url)

        self.assertEquals(
            response.status_code, 200
        )  # We need to check that we get the correct response
        self.assertTemplateUsed(response, "projects/project_view.html")

    def test_project_view_POST_offer_submit(self):
        self.client.login(username="testuser2", password="argkwargs123")
        response = self.client.post(
            self.project_view_url,
            {
                "title": "Test offer",
                "description": "some other description",
                "price": 40,
                "taskvalue": self.test_task.pk,
                "offer_submit": True,
            },
        )
        self.assertEqual(
            response.status_code, 200
        )  # We need to check that we get the correct response
        self.assertTemplateUsed(response, "projects/project_view.html")
        self.assertEquals(
            self.test_task.taskoffer_set.first().title, "Test offer"
        )  # We need to check that the offer has been created correctly

    def test_project_view_POST_offer_submit_no_data(self):
        self.client.login(username="testuser2", password="argkwargs123")
        response = self.client.post(self.project_view_url)
        self.assertEqual(
            response.status_code, 200
        )  # We need to check that we get the correct response
        self.assertTemplateUsed(response, "projects/project_view.html")
        self.assertEquals(
            self.test_task.taskoffer_set.count(), 0
        )  # We need to check that the offer has not been created

    # TODO: This test reveals an error that is not handled yet
    # def test_project_view_POST_offer_submit_no_login(self):
    #     response = self.client.post(
    #         self.project_view_url,
    #         {
    #             "title": "Test offer",
    #             "description": "some other description",
    #             "price": 40,
    #             "taskvalue": self.test_task.pk,
    #             "offer_submit": True,
    #         },
    #     )
    #     self.assertEqual(
    #         response.status_code, 404
    #     )  # We need to check that we get the correct response
    #     self.assertEquals(
    #         self.test_task.taskoffer_set.count(), 0
    #     )  # We need to check that the offer has not been created

    def test_get_user_task_permissions(self):
        assert get_user_task_permissions(self.test_user1, self.test_task)['owner']  # Need to test owner

        # Need to test the profile.task_participants_ACTIONs
        assert not get_user_task_permissions(self.test_user2, self.test_task)['read']
        self.test_task.read.add(self.test_user2.profile)
        assert get_user_task_permissions(self.test_user2, self.test_task)['read']

        # Need to test if the user gets team permissions
        assert not get_user_task_permissions(self.test_user2, self.test_task)['view_task']
        test_team = Team.objects.create(
            name='Team name',
            task=self.test_task,
        )
        test_team.members.add(self.test_user2.profile)
        assert get_user_task_permissions(self.test_user2, self.test_task)['view_task']

        # Need to test if the user gets permissions after an accepted task offer
        assert not get_user_task_permissions(self.test_user2, self.test_task)['modify']
        TaskOffer.objects.create(
            task=self.test_task,
            title='Test offer title',
            description='some description',
            offerer=self.test_user2.profile,
            status='a',
            feedback=''
        )
        assert get_user_task_permissions(self.test_user2, self.test_task)['modify']

        assert not get_user_task_permissions(self.test_user2, self.test_task)['owner']

