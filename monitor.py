from github import Github
from config import *
from datetime import date
import os
import json
from urllib.request import Request, urlopen
import csv


def get_data(g):
    star = {}
    num_contrib_by_repo = {}
    all_contrib = set()
    org = g.get_organization(ORG)
    all_repos = [repo for repo in org.get_repos()]
    for repo in all_repos:
        # get repo name
        repo_name = str(repo.full_name)
        # get contributors
        contribs = repo.get_contributors()
        # store num of contributors for each repo
        num_contrib_by_repo[repo_name] = len(set(contribs))
        all_contrib.update([u.login for u in contribs])
        # store star count
        req = Request(f"https://api.github.com/repos/{repo_name}")
        req.add_header("Authorization", TOKEN)
        print(f"https://api.github.com/repos/{repo_name}")
        star[repo_name] = json.loads(urlopen(req).read())['stargazers_count']
    num_all_contrib = len(all_contrib)
    return star, num_contrib_by_repo, num_all_contrib, all_contrib


def persist(star, num_contrib_by_repo, num_all_contrib, all_contrib):
    path = os.path.join(ROOT_DIR, str(date.today()))
    if not os.path.exists(path):
        os.makedirs(path)
    with open(os.path.join(path, "num_contrib_by_repo.json"), "w") as f:
        json.dump(json.dumps(num_contrib_by_repo), f)

    with open(os.path.join(path, "star.json"), "w") as f:
        json.dump(json.dumps(star), f)

    with open(os.path.join(path, "all_contrib.csv"), "w") as f:
        wr = csv.writer(f)
        f.write(f"Total: {str(num_all_contrib)}\n")
        wr.writerow(all_contrib)


def main():
    g = Github(TOKEN)
    persist(*get_data(g))


if __name__ == "__main__":
    main()
