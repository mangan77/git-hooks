#!/usr/bin/python

import sys
import re
import subprocess

jira_pattern = re.compile('([A-Z]{2,3}-[0-9]{1,5})', re.I)
merge_pattern = re.compile('^.*(merge)+.*$', re.I)

def is_merge(file_name):
    return any_line_contains_pattern(file_name, merge_pattern)

def has_jira_issue(file_name):
    return any_line_contains_pattern(file_name, jira_pattern)

def any_line_contains_pattern(file_name, reg_exp_pattern):
    with open(file_name, 'r') as message_file:
        lines = message_file.readlines()
        for line in lines:
            m = re.search(reg_exp_pattern, line)
            if m:
                return True
        return False

def get_jira_issue_from_branch_name():
    current_branch = subprocess.check_output('git branch | grep "*" | cut -d " " -f 2', shell=True).strip()
    m = re.search(jira_pattern, current_branch)
    if m :
        return m.group(0)
    else :
        print 'Current branch name does not include an issue number in its name : %s' % current_branch

def add_jira_number_to_commit(file_name, jira_issue) :
    with open(file_name, 'r') as message_file:
        lines = message_file.readlines()
        lines[0] = jira_issue + ' : ' + lines[0]
    with open(file_name, 'w') as message_file:
        message_file.write(''.join(lines))


commit_message_file = sys.argv[1]

if is_merge(commit_message_file) :
    sys.exit(0)


if not has_jira_issue(commit_message_file) :
    jira_issue_number = get_jira_issue_from_branch_name()
    if jira_issue_number :
        add_jira_number_to_commit(commit_message_file, jira_issue_number)
    else :
        print 'Commit does not contain Jira issue number.'
        sys.exit(1)

sys.exit(0)
