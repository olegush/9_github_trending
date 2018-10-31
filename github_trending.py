from datetime import datetime
from datetime import timedelta
import requests


def get_trending_repositories():
    git_url = 'https://api.github.com/search/repositories'
    time_ago = datetime.now() - timedelta(days=7)
    day_ago_str = 'created:>{}'.format(time_ago.strftime('%Y-%m-%d'))
    repo_params = {'q': day_ago_str, 'sort': 'stars'}
    repos_response = requests.get(git_url, params=repo_params)
    return repos_response.json()['items']


def get_open_issues(repo_owner, repo_name):
    git_url = 'https://api.github.com/repos/{}/{}/issues'.format(repo_owner,
                                                                 repo_name
                                                                 )
    issues_params = {'state': 'open'}
    issues_response = requests.get(git_url, params=issues_params)
    return issues_response.json()


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
