
import unittest

from foundations_spec import *
from foundations_internal.foundations_job import FoundationsJob
from foundations_internal.job_resources import JobResources

class TestFoundationsJob(Spec):

    @let
    def job_id(self):
        return self.faker.uuid4()

    @let
    def num_gpus(self):
        return self.faker.random_int(0, 8)

    @let
    def ram(self):
        return self.faker.random.random() * 256

    @let
    def fake_project_name(self):
        return self.faker.word()

    def setUp(self):
        self._context = FoundationsJob()

    def test_set_project_name_sets_provenance_project_name(self):
        self._context.project_name = 'my project'
        self.assertEqual('my project', self._context.project_name)

    def test_set_project_name_sets_provenance_project_name_different_name(self):
        self._context.project_name = 'my other project'
        self.assertEqual('my other project', self._context.project_name)

    def test_get_job_id(self):
        self._context.job_id = self.job_id
        self.assertEqual(self.job_id, self._context.job_id)

    def test_job_resources_has_default_gpus_one(self):
        job_resources = self._context.job_resources
        self.assertEqual(1, job_resources.num_gpus)

    def test_job_resources_has_default_ram_none_ie_no_limit(self):
        job_resources = self._context.job_resources
        self.assertIsNone(job_resources.ram)

    def test_set_job_resources_sets_job_resources_object(self):
        job_resources = JobResources(self.num_gpus, self.ram)
        self._context.job_resources = job_resources
        self.assertIs(job_resources, self._context.job_resources)

    def test_reset_job_resources_sets_job_resources_back_to_defaults(self):
        job_resources = JobResources(self.num_gpus, self.ram)
        self._context.job_resources = job_resources
        self._context.reset_job_resources()
        self.assertEqual(JobResources(1, None), self._context.job_resources)

    def test_project_name_is_default_when_project_name_not_yet_set(self):
        self.assertEqual('default', self._context.project_name)

    def test_project_name_is_correct_when_project_name_set(self):
        self._context.project_name = self.fake_project_name
        self.assertEqual(self.fake_project_name, self._context.project_name)

    def test_is_in_running_job_returns_true_if_foundations_job_has_job_id(self):
        self._context.job_id = self.job_id
        self.assertTrue(self._context.is_in_running_job())

    def test_is_in_running_job_returns_false_if_foundations_job_does_not_have_job_id(self):
        self.assertFalse(self._context.is_in_running_job())