# save the remotes of all git repo folders in the current folder to `git_remotes.txt`

import os
import subprocess

def get_git_remote_url(repo_path):
    """Run `git remote -v` and extract the (fetch) URL."""
    result = subprocess.check_output(
        ["git", "remote", "-v"],
        cwd=repo_path,
        text=True
    )
    remotes = {}
    for line in result.splitlines():
        if "(fetch)" in line:
            tmp = line.split()
            remotes[tmp[0]] = tmp[1]
    return remotes

def main():
    current_dir = os.getcwd()
    directories = [d for d in os.listdir(current_dir) if os.path.isdir(d)]
    git_repos = {}
    for directory in directories:
        repo_path = os.path.join(current_dir, directory)
        # Check if the directory is a Git repository
        if os.path.isdir(os.path.join(repo_path, ".git")):
            fetch_urls = get_git_remote_url(repo_path)
            if fetch_urls:
                git_repos[directory] = fetch_urls

    sorted_repos = sorted(git_repos.keys())

    with open("git_remotes.txt", "w") as file:
        for repo_name in sorted_repos:
            sorted_remotes = sorted(git_repos[repo_name].keys())
            max_len = max(len(s) for s in sorted_remotes)
            file.write(f"{repo_name}:\n")
            for remote in sorted_remotes:
                spaces = ' ' * (max_len-len(remote)+2)
                file.write('    ' + remote + spaces + git_repos[repo_name][remote] + '\n')
            file.write("\n")
    print("all done!")

if __name__ == "__main__":
    main()
