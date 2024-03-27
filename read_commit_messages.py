import git

def get_commit_messages():
    # Open the current Git repository
    repo = git.Repo(search_parent_directories=True)
    
    # Get the current branch
    branch = repo.active_branch
    
    # Get all commits in the current branch
    commits = list(repo.iter_commits(branch))
    
    # Extract commit messages
    commit_messages = [commit.message.strip() for commit in commits]
    
    return commit_messages

def main():
    commit_messages = get_commit_messages()
    
    # Print the commit messages as an ordered list
    print("Commit Messages:")
    for i, message in enumerate(commit_messages, start=1):
        print(f"{i}. {message}")

if __name__ == "__main__":
    main()
