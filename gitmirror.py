#!/bin/env python3
import configparser
import datetime
import os
import re
import subprocess
import sys

regex_repo_entry = re.compile(
    r"^(?P<remote>[\w\d@\.\:\-\/]+)(?:\s+\[(?P<remote_options>.*)\])?\s+->\s*(?P<local>[\w\d\.\-\/]+)\s+(?:\[(?P<local_options>.*)\])?$"
)

repository_dir = None
repository_file = None
logging_dir = None


class Repository:
    def __init__(self, remote, local, remote_options, local_options):
        self.repo_name = os.path.basename(local)
        self.remote = remote
        self.local = local
        self.remote_options = remote_options
        if not remote_options:
            self.remote_options = []
        self.local_options = local_options
        if not local_options:
            self.local_options = []

    def __repr__(self):
        s = "repository:\n"
        s += "    remote:  " + self.remote + "\n"
        if self.remote_options:
            s += "    options: " + self.remote_options + "\n"
        s += "    local:   " + self.local + "\n"
        if self.local_options:
            s += "    options: " + self.local_options + "\n"
        return s

    def already_cloned(self):
        d = os.path.join(repository_dir, self.local)
        if not os.path.exists(d):
            return False
        return True

    def mirror(self, time_stamp):
        if self.already_cloned():
            self.update(time_stamp)
        else:
            self.clone(time_stamp)

    def update(self, time_stamp):
        log_path = os.path.join(logging_dir, time_stamp)
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        log_file = open(os.path.join(log_path, self.repo_name + ".log"), "w")
        d = os.path.join(repository_dir, self.local)
        process = subprocess.Popen(
            ["git", "remote", "--verbose", "update"],
            cwd=d,
            stderr=log_file,
            stdout=log_file
        )
        process.communicate()
        log_file.close()

    def clone(self, time_stamp):
        log_path = os.path.join(logging_dir, time_stamp)
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        log_file = open(os.path.join(log_path, self.repo_name + ".log"), "w")
        d = os.path.join(repository_dir, self.local)
        if not os.path.exists(d):
            os.makedirs(d)
        process = subprocess.Popen(
            ["git", "clone", "--verbose", "--mirror", self.remote, "."],
            cwd=d,
            stderr=log_file,
            stdout=log_file
        )
        process.communicate()
        log_file.close()


def parse_repo_file(path):
    entries = []
    with open(path) as f:
        for l in f:
            m = regex_repo_entry.match(l)
            if m:
                dct = m.groupdict()
                print(dct)
                entry = Repository(
                    dct["remote"],
                    dct["local"],
                    dct["remote_options"],
                    dct["local_options"]
                )
                entries.append(entry)
    return entries

if __name__ == "__main__":
    config_file = sys.argv[1]
    config_parser = configparser.ConfigParser()
    config = config_parser.read(config_file)["config"]

    logging_dir = config["logging_dir"]
    repository_dir = config["repository_dir"]
    repository_file = config["repository_file"]

    time_stamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    repos = parse_repo_file(repository_file)

    for repo in repos:
        repo.mirror(time_stamp)
