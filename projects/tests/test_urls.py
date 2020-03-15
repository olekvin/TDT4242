from django.test import SimpleTestCase
from django.urls import reverse, resolve
from projects.views import (
    projects,
    new_project,
    project_view,
    task_view,
    upload_file_to_task,
    task_permissions,
    edit_task,
    delete_file,
)


class TestUrls(SimpleTestCase):
    def test_projects_url_resolves(self):
        url = reverse("projects")
        self.assertEquals(resolve(url).func, projects)

    def test_new_project_url_resolves(self):
        url = reverse("new_project")
        self.assertEquals(resolve(url).func, new_project)

    def test_project_view_url_resolves(self):
        url = reverse("project_view", args=[1])
        self.assertEquals(resolve(url).func, project_view)

    def test_task_view_url_resolves(self):
        url = reverse("task_view", args=[1, 1])
        self.assertEquals(resolve(url).func, task_view)

    def test_upload_file_to_task_url_resolves(self):
        url = reverse("upload_file_to_task", args=[1, 1])
        self.assertEquals(resolve(url).func, upload_file_to_task)

    def test_task_permissions_url_resolves(self):
        url = reverse("task_permissions", args=[1, 1])
        self.assertEquals(resolve(url).func, task_permissions)

    def test_edit_task_url_resolves(self):
        url = reverse("edit_task", args=[1, 1])
        self.assertEquals(resolve(url).func, edit_task)

    def test_delete_file_url_resolves(self):
        url = reverse("delete_file", args=[1])
        self.assertEquals(resolve(url).func, delete_file)
