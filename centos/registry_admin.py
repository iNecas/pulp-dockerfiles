#!/usr/bin/python -Es

"""Admin pulp as a docker registry

sudo ./registry_admin.py
    login
    create my/app
    list repos
    list images my/app
    push my/app
    pulp <native_pulp_cmds>
"""

import argparse
import os.path

class Cli(object):
    def __init__(self):
        self.conf_dir = os.path.expanduser("~") + "/dev/tmp/.pulp"
        self.conf_file = "temp.conf"
        if not os.path.isfile("%s/%s" % (self.conf_dir, self.conf_file)):
            print "Registry config file not found"
            self.create_config()
        self.user_cert = "user-cert.pem"
        if not os.path.isfile("%s/%s" % (self.conf_dir, self.user_cert)):
            self.login_user()

    def create_config(self):
        print "Creating config file %s/%s" % (self.conf_dir, self.conf_file)
        if not os.path.exists(self.conf_dir):
            os.makedirs(self.conf_dir)
        pulp_hostname = raw_input("Enter registry server hostname: ")
        while pulp_hostname is "":
            pulp_hostname = raw_input("Invalid hostname. Enter registry server hostname, e.g. registry.example.com: ")
        verify_ssl = raw_input("Verify SSL (requires CA-signed certificate) [False]: ") or "False"
        f = open("%s/%s" % (self.conf_dir, self.conf_file), "w")
        f.write("[server]\nhost = %s\nverify_ssl = %s\n" % (pulp_hostname, verify_ssl))
        f.close()

    def login_user(self):
        print "login..........."

    @property
    def args(self):
        parser = argparse.ArgumentParser()

        subparsers = parser.add_subparsers(help='sub-command help')
        push_parser = subparsers.add_parser('push', help='repository')
        push_parser.add_argument('repo',
                           metavar='MY/APP',
                           help='Repository name')
        create_parser = subparsers.add_parser('create', help='repository')
        create_parser.add_argument('repo',
                           metavar='MY/APP',
                           help='Repository name')
        create_parser.add_argument('-g', '--git-url',
                           metavar='http://git.example.com/repo/myapp',
                           help='URL of git repository for Dockerfile')
        create_parser.add_argument('-t', '--git-tag',
                           metavar='TAG',
                           help='git tag name for Dockerfile repository')
        create_parser.add_argument('-b', '--git-branch',
                           metavar='BRANCH',
                           help='git branch name for Dockerfile repository')
        list_parser = subparsers.add_parser('list', help='images or repos')
        list_parser.add_argument('list_item',
                           metavar='repos|images',
                           choices=['repos', 'images'],
                           help='What to list')
        login_parser = subparsers.add_parser('login', help='Login to pulp server')
        login_parser.add_argument('username',
                           metavar='USERNAME',
                           help='Pulp registry username')
        pulp_parser = subparsers.add_parser('pulp', help='pulp-admin commands')
        pulp_parser.add_argument('pulp_cmd',
                           metavar='"PULP COMMAND FOO BAR"',
                           action=Pulp,
                           help='pulp-admin command string')
        return parser.parse_args()

    def convert_repo_name(self):
        myargs = self.args
        #print myargs

class Pulp(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError("nargs not allowed")
        super(Pulp, self).__init__(option_strings, dest, **kwargs)
    def __call__(self, parser, namespace, values, option_string=None):
        print('%r %r %r' % (namespace, values, option_string))
        print "Pulp action..."
        setattr(namespace, self.dest, values)


def main():
    cli = Cli()
    cli.convert_repo_name()

if __name__ == '__main__':
    main()

