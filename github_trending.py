from datetime import datetime
from datetime import timedelta
import requests
import json


def get_trending_repositories():
    git_url = 'https://api.github.com/search/repositories'
    time_week_ago = datetime.now() - timedelta(days=7)
    day_week_ago = str(time_week_ago.strftime('%Y-%m-%d'))
    repos_url = git_url + '?q=created:>' + day_week_ago + '&sort=stars'
    repos_response = requests.get(repos_url)
    return json.loads(repos_response.text)['items']


def get_open_issues(repo_owner, repo_name):
    git_url = 'https://api.github.com/repos/'
    issues_url = git_url + repo_owner + '/' + repo_name + '/issues?state=open'
    issues_response = requests.get(issues_url)
    return json.loads(issues_response.text)


if __name__ == '__main__':
    top_size = 2
    trending_repositories = get_trending_repositories()
    for repo in trending_repositories[:top_size]:
        print('\nOWNER: {} USER: {} STARS: {} OPEN ISSUES: {}'.
              format(repo['owner']['login'],
                     repo['name'],
                     repo['stargazers_count'],
                     repo['open_issues_count']
                     ))
        print("All open {}'s issues:".format(repo['name']))
        open_issues = get_open_issues(repo['owner']['login'], repo['name'])
        for issue in open_issues:
            print('#{}: {}'.format(issue['number'], issue['html_url']))
