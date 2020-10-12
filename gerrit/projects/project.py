#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from gerrit.projects.branches import Branches
from gerrit.projects.tags import Tags
from gerrit.projects.commit import Commit
from gerrit.projects.dashboards import Dashboards
from gerrit.utils.common import check
from gerrit.utils.exceptions import UnknownCommit
from gerrit.utils.models import BaseModel


class GerritProject(BaseModel):
    def __init__(self, **kwargs):
        super(GerritProject, self).__init__(**kwargs)
        self.attributes = ['id', 'name', 'state', 'labels', 'web_links', 'test', 'gerrit']

    @property
    def description(self) -> str:
        """s
        Retrieves the description of a project.

        :return:
        """
        endpoint = '/projects/%s/description' % self.id
        response = self.gerrit.make_call('get', endpoint)
        result = self.gerrit.decode_response(response)
        return result

    @check
    def set_description(self, ProjectDescriptionInput: dict) -> str:
        """
        Sets the description of a project.

        :param ProjectDescriptionInput: the ProjectDescriptionInput entity.
        :return:
        """
        endpoint = '/projects/%s/description' % self.id
        response = self.gerrit.make_call('put', endpoint, **ProjectDescriptionInput)
        result = self.gerrit.decode_response(response)
        return result

    def delete_description(self):
        endpoint = '/projects/%s/description' % self.id
        self.gerrit.make_call('delete', endpoint)

    @property
    def parent(self) -> str:
        """
        Retrieves the name of a project’s parent project. For the All-Projects root project an empty string is returned.

        :return:
        """
        endpoint = '/projects/%s/parent' % self.id
        response = self.gerrit.make_call('get', endpoint)
        result = self.gerrit.decode_response(response)
        return result

    @check
    def set_parent(self, ProjectParentInput: dict) -> str:
        """
        Sets the parent project for a project.

        :param ProjectParentInput: The ProjectParentInput entity.
        :type dict
        :return:
        """
        endpoint = '/projects/%s/parent' % self.id
        response = self.gerrit.make_call('put', endpoint, **ProjectParentInput)
        result = self.gerrit.decode_response(response)
        return result

    @property
    def HEAD(self) -> str:
        """
        Retrieves for a project the name of the branch to which HEAD points.

        :return:
        """
        endpoint = '/projects/%s/HEAD' % self.id
        response = self.gerrit.make_call('get', endpoint)
        result = self.gerrit.decode_response(response)
        return result

    @check
    def set_HEAD(self, HeadInput: dict) -> str:
        """
        Sets HEAD for a project.

        :param HeadInput: The HeadInput entity.
        :return:
        """
        endpoint = '/projects/%s/HEAD' % self.id
        response = self.gerrit.make_call('put', endpoint, **HeadInput)
        result = self.gerrit.decode_response(response)
        return result

    @property
    def config(self) -> dict:
        """
        Gets some configuration information about a project.
        Note that this config info is not simply the contents of project.config; it generally contains fields that may
        have been inherited from parent projects.

        :return:
        """
        endpoint = '/projects/%s/config' % self.id
        response = self.gerrit.make_call('get', endpoint)
        result = self.gerrit.decode_response(response)
        return result

    @check
    def set_config(self, ConfigInput: dict) -> dict:
        """
        Sets the configuration of a project.

        :param ConfigInput: the ConfigInput entity.
        :return:
        """
        endpoint = '/projects/%s/config' % self.id
        response = self.gerrit.make_call('put', endpoint, **ConfigInput)
        result = self.gerrit.decode_response(response)
        return result

    def get_statistics(self) -> dict:
        """
        Return statistics for the repository of a project.

        :return:
        """
        endpoint = '/projects/%s/statistics.git' % self.id
        response = self.gerrit.make_call('get', endpoint)
        result = self.gerrit.decode_response(response)
        return result

    @check
    def run_garbage_collection(self, GCInput: dict) -> str:
        """
        Run the Git garbage collection for the repository of a project.

        :param GCInput: the GCInput entity
        :return:
        """
        endpoint = '/projects/%s/gc' % self.id
        response = self.gerrit.make_call('post', endpoint, **GCInput)
        result = self.gerrit.decode_response(response)
        return result

    @check
    def ban_commits(self, BanInput: dict) -> dict:
        """
        Marks commits as banned for the project.

        :param BanInput: the BanInput entity.
        :return:
        """
        endpoint = '/projects/%s/ban' % self.id
        response = self.gerrit.make_call('put', endpoint, **BanInput)
        result = self.gerrit.decode_response(response)
        return result

    @property
    def access_rights(self) -> dict:
        """
        Lists the access rights for a single project.

        :return:
        """
        endpoint = '/projects/%s/access' % self.id
        response = self.gerrit.make_call('get', endpoint)
        result = self.gerrit.decode_response(response)
        return result

    @check
    def set_access_rights(self, ProjectAccessInput: dict) -> dict:
        """
        Sets access rights for the project using the diff schema provided by ProjectAccessInput.

        :param ProjectAccessInput: the ProjectAccessInput entity
        :return:
        """
        endpoint = '/projects/%s/access' % self.id
        response = self.gerrit.make_call('post', endpoint, **ProjectAccessInput)
        result = self.gerrit.decode_response(response)
        return result

    def check_access(self, options: str) -> dict:
        """
        runs access checks for other users.

        :param options:
        Check Access Options
          * Account(account): The account for which to check access. Mandatory.
          * Permission(perm): The ref permission for which to check access.
            If not specified, read access to at least branch is checked.
          * Ref(ref): The branch for which to check access. This must be given if perm is specified.
        :return:
        """
        endpoint = '/projects/%s/check.access?%s' % (self.id, options)
        response = self.gerrit.make_call('get', endpoint)
        result = self.gerrit.decode_response(response)
        return result

    @check
    def index(self, IndexProjectInput: dict):
        """
        Adds or updates the current project (and children, if specified) in the secondary index.
        The indexing task is executed asynchronously in background and this command returns immediately
        if async is specified in the input.

        :param IndexProjectInput: the IndexProjectInput entity
        :return:
        """
        endpoint = '/projects/%s/index' % self.id
        self.gerrit.make_call('post', endpoint, **IndexProjectInput)

    def index_change(self):
        """
        Adds or updates the current project (and children, if specified) in the secondary index.
        The indexing task is executed asynchronously in background and this command returns immediately
        if async is specified in the input.

        :return:
        """
        endpoint = '/projects/%s/index.changes' % self.id
        self.gerrit.make_call('post', endpoint)

    @check
    def check_consistency(self, CheckProjectInput: dict) -> dict:
        """
        Performs consistency checks on the project.

        :param CheckProjectInput: the CheckProjectInput entity
        :return:
        """
        endpoint = '/projects/%s/check' % self.id
        response = self.gerrit.make_call('post', endpoint, **CheckProjectInput)
        result = self.gerrit.decode_response(response)
        return result

    @property
    def branches(self) -> Branches:
        """
        List the branches of a project. except the refs/meta/config

        :return:
        """
        return Branches(self.id, self.gerrit)

    @property
    def child_projects(self) -> list:
        """
        List the direct child projects of a project.

        :return:
        """
        endpoint = '/projects/%s/children/' % self.id
        response = self.gerrit.make_call('get', endpoint)
        result = self.gerrit.decode_response(response)
        return [self.gerrit.projects.get(item.get('id')) for item in result]

    @property
    def tags(self) -> Tags:
        """
        List the tags of a project.

        :return:
        """
        return Tags(self.id, self.gerrit)

    def get_commit(self, commit: str) -> Commit:
        """
        Retrieves a commit of a project.

        :return:
        """
        endpoint = '/projects/%s/commits/%s' % (self.id, commit)
        response = self.gerrit.make_call('get', endpoint)

        if response.status_code < 300:
            result = self.gerrit.decode_response(response)
            return Commit.parse(result, project=self.id, gerrit=self.gerrit)
        else:
            raise UnknownCommit(commit)

    @property
    def dashboards(self) -> Dashboards:
        """
        gerrit dashboards operations

        :return:
        """
        return Dashboards(project=self.id, gerrit=self.gerrit)