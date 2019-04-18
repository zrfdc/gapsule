import json
import tornado.web

from gapsule.utils.decorators import ajaxquery
from gapsule.handlers.Base import BaseHandler


class CreatePullRequestHandler(BaseHandler):
    @ajaxquery
    def get(self, owner, reponame, restpath):
        compare_information = self.judgeBranch(owner, restpath)
        for key_state in compare_information.keys():
            key_judge = False
            key_judge = (key_state == "base_repository") or(key_state == "base_branch") or(
                key_state == "base_repository") or(key_state == "head_repository")
            if not key_judge:
                self.set_status(400, "Unknown")
        # TODO: 需要数据库提供接口
        # 参数compare_information,得到对比的数据
        request_end = 1
        if request_end == None:
            self.set_status(404, "Unknown")
        self.write(json.dumps(request_end))

    def judgeBranch(self, owner, statepath):
        compare_dict = {}
        separate_sign = 0
        str_path = ''
        for state in statepath:
            if state == ':' and separate_sign == 0:
                compare_dict["base_repository"] = str_path
                str_path = ''
                separate_sign = 1
            if state == '.' and separate_sign == 1:
                compare_dict["base_branch"] = str_path
                str_path = ''
                separate_sign = 2
            if state == '.' and separate_sign == 0:
                compare_dict["base_repository"] = owner
                compare_dict["base_branch"] = str_path
                str_path = ''
                separate_sign = 2
            if str_path == '...' and separate_sign == 2:
                str_path = ''
                separate_sign == 3
            if state == ':' and separate_sign == 3:
                compare_dict["head_repository"] = str_path
                str_path = ''
                separate_sign == 4
            str_path += state
        if separate_sign == 4:
            compare_dict["compare_branch"] = str_path
        else:
            compare_dict["head_repository"] = owner
            compare_dict["base_branch"] = str_path
        return compare_dict


class PullCommitsHandler(BaseHandler):
    @ajaxquery
    def get(self, owner, reponame, postid):
        name = self.get_query_argument("name")
        pull_commits_dict = {
            "status": "ok",
            # TODO: 需要数据库提供接口
            # 参数 owner, reponame, postid（关键码数字）,name
            "ccommits": {
                "name": "name",
                "content": "content",
            }
        }
        self.write(pull_commits_dict)


class PullChecksHandler(BaseHandler):
    @ajaxquery
    def get(self, owner, reponame, postid):
        name = self.get_query_argument("name")
        pull_checks_dict = {
            "status": "ok",
            # TODO: 需要数据库提供接口
            # 参数 owner, reponame, postid（关键码数字）,name
            "checks": {
                "number": "number",
                "content": "content",
            }
        }
        self.write(pull_checks_dict)


class PullFilesHandler(BaseHandler):
    @ajaxquery
    def get(self, owner, reponame, postid):
        name = self.get_query_argument("name")
        pull_files_dict = {
            "status": "ok",
            # TODO: 需要数据库提供接口
            # 参数 owner, reponame, postid（关键码数字）,name
            "files": {
                "file1": "file1",
                "file2": "file2",
            }
        }
        self.write(pull_files_dict)
