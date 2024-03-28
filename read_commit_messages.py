import git

def get_last_n_commit_messages(n):
    # Open the current Git repository
    repo = git.Repo(search_parent_directories=True)

    # Get the current user's name
    username = repo.git.config("user.name")

    # Get the last N commits authored by the current user
    commits = list(repo.iter_commits(max_count=n, author=username))

    # Extract commit messages
    commit_messages = [commit.message.strip() for commit in commits]

    return commit_messages

def main():
    # Specify the number of last commits to retrieve
    n = 10  # Change this value as needed
    
    commit_messages = get_last_n_commit_messages(n)
    
    # Print the last N commit messages as an ordered list
    print(f"Last {n} Commit Messages:")
    for i, message in enumerate(commit_messages, start=1):
        print(f"{i}. {message}")

if __name__ == "__main__":
    main()
