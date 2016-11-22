#!env python2
import urllib2
import sys
from contextlib import closing
import json
import os
import argparse
import shutil

dryrun = False


def execute(cmd, **env):
    if dryrun:
        print "dryrun: {}".format(cmd)
    else:
        os.environ.update(env)
        errno = os.system(cmd)
        assert errno == 0, "execute failed with errno:{}".format(errno)


def unlink(dirname):
    assert not dirname.startswith('.')
    assert not dirname.startswith('/')
    assert not dirname.startswith(':', 1)  # if startswith "c:", "d:", etc
    assert not dirname.startswith('\\')

    basedir = os.path.abspath(os.path.dirname(__file__))
    full_dirname = os.path.join(basedir, dirname)
    if dryrun:
        print "dryrun: rmtree {}".format(full_dirname)
    else:
        shutil.rmtree(full_dirname)


def fetch_repo_lists(org):
    datas = []
    print "Fetching repo lists from KiCad organization:"
    with closing(urllib2.urlopen("https://api.github.com/orgs/{}/repos?type=public&per_page=200".format(org))) as u:
        while True:
            data = u.read(4096)
            if not data:
                print "\nDone."
                break
            sys.stdout.write('#')
            sys.stdout.flush()
            datas.append(data)
    json_data = ''.join(datas)

    return json.loads(json_data)


def parse_prettys(repos):
    return {repo['name']: repo['git_url'] for repo in repos if repo['name'].endswith(".pretty")}


def sync(pretty_repos,
         import_new_repos=True,
         update_current_repos=True,
         remove_deprecated_repos=True):
    all_file_names = os.listdir(os.path.abspath(os.path.dirname(__file__)))
    dir_names = set([x for x in all_file_names if os.path.isdir(x) and not x.startswith('.') and x.endswith('.pretty')])
    pretty_names = set(pretty_repos.iterkeys())

    if import_new_repos:
        new_repos = pretty_names - dir_names
        for repo_name in new_repos:
            format_args = {'name': repo_name, 'url': pretty_repos[repo_name]}
            print "Fetch {name} from {url} as subtree...".format(**format_args)
            execute('git remote add -f subtree.{name} {url}'.format(**format_args))
            execute('git subtree add --prefix={name} subtree.{name} master --squash'.format(**format_args))

    if update_current_repos:
        current_repos = dir_names.intersection(pretty_names)
        for repo_name in current_repos:
            format_args = {'name': repo_name, 'url': pretty_repos[repo_name]}
            print "Pull {name}...".format(**format_args)
            execute('git fetch subtree.{name}'.format(**format_args))
            execute('git subtree pull --prefix={name} subtree.{name} master --squash'.format(**format_args), GIT_EDITOR=":")

    if remove_deprecated_repos:
        deprecated_repos = dir_names - pretty_names
        for repo_name in deprecated_repos:
            format_args = {'name': repo_name}
            print "Remove dir: {name}".format(**format_args)
            execute('git remote rm subtree.{name}'.format(**format_args))
            unlink(repo_name)   # exec rm -rf is dangerous


def init_argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--skip_create_new',
                        help="skip import new created repos in KiCad",
                        action='store_true')
    parser.add_argument('-u', '--skip_update_avail',
                        help="don't update repos in current directory with KiCad",
                        action='store_true')
    parser.add_argument('-r', '--skip_remove_deprecated',
                        help="don't remove deprecated repos which is removed in KiCad",
                        action='store_true')
    parser.add_argument('-d', '--dryrun',
                        help='a trial run with no changes',
                        action='store_true')
    args = parser.parse_args()
    if args.dryrun:
        global dryrun
        dryrun = True
    return args

if __name__ == "__main__":
    args = init_argparse()

    repos = fetch_repo_lists("KiCad")
    pretty_repos = parse_prettys(repos)

    sync(pretty_repos,
         not args.skip_create_new,
         not args.skip_update_avail,
         not args.skip_remove_deprecated)
