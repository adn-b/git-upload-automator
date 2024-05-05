import git
from subprocess import call


def validCheck(path):
    try:
        repo = git.Repo(path)
        return True, repo
    except git.exc.InvalidGitRepositoryError:
        return False, None
    except git.exc.NoSuchPathError:
        return False, None    



def main():
    repo_path = input("Please enter the path to your repository:\n")

    valid, repo = validCheck(repo_path)

    if not valid:
        print("The specified path is not a valid Git repository.")
        return
    else:
        repo = git.Repo(repo_path)

    remotes = repo.remotes
    if remotes:
        for remote in remotes:
            print(f"Remote name: {remote.name}, URL: {remote.url}.")
    else:
        add_or_not = input(f"No remotes are configured for this repository. Would you like to add one now? Please enter 'Y' or 'N':\n")
        if add_or_not == "Y":
            repo_url = input(f"Please enter the repository URL. Note that any spelling errors will result in an upload to an incorrect repository:\n")
            if repo_url:
                repo.create_remote("origin", repo_url)
        elif add_or_not == "N":
            print(f"Upload terminated as no remote repository provided.")
            return
        else:
            print("Invalid input, terminating process.")
            return


    changed_files = [item.a_path for item in repo.index.diff(None)]
    untracked_files = repo.untracked_files
    print(changed_files, untracked_files)
    if len(changed_files) == 0 and len(untracked_files) == 0:
        print("No changes detected.")
    elif len(changed_files) == 1:
        print(f"1 change detected: {changed_files[0]}")
        file = changed_files[0]
        upload = input(f"Would you like to upload your changes? Please type 'Y' or 'N'.\n")
        if upload == "Y":
            uploadIndividual(repo, file)
        elif upload == "N":
            print("Have a nice day.")
            return
        else:
            print("Invalid input, terminating process.")
            return
    elif len(untracked_files) == 1:
        print(f"1 change detected: {untracked_files[0]}")
        file = untracked_files[0]
        upload = input(f"Would you like to upload your changes? Please type 'Y' or 'N'.\n")
        if upload == "Y":
            uploadIndividual(repo, file)
        elif upload == "N":
            print("Have a nice day.")
            return
        else:
            print("Invalid input, terminating process.")
            return        
    elif len(changed_files) >= 2:
        print(f"Several changes detected: {changed_files}")
        upload = input(f"Would you like to upload your changes? Please type 'Y' or 'N'.\n")
        if upload == "Y":
            when_to_upload = input(f"Please choose an option, '1' or '2':\n 1. Immediate\n 2. Scheduled\n")
            if when_to_upload == "1":
                manualUpload(repo, changed_files)
            elif when_to_upload == "2":
                scheduleUpload(repo, changed_files)
            else:
                print(f"Invalid input, terminating.")
        elif upload == "N":
            print("Have a nice day.")
            return
        else:
            print("Invalid input, terminating process.")
            return
    elif len(untracked_files) >= 2:
        print(f"Several changes detected: {untracked_files}")
        upload = input(f"Would you like to upload your changes? Please type 'Y' or 'N'.\n")
        if upload == "Y":
            when_to_upload = input(f"Please choose an option, '1' or '2':\n 1. Immediate\n 2. Scheduled\n")
            if when_to_upload == "1":
                manualUpload(repo, untracked_files)
            elif when_to_upload == "2":
                scheduleUpload(repo, untracked_files)
            else:
                print(f"Invalid input, terminating.")
        elif upload == "N":
            print("Have a nice day.")
            return
        else:
            print("Invalid input, terminating process.")
            return


def commitCheck(repo):
    try:
        repo.head.commit
        return True
    except ValueError:  # Typically thrown if there are no commits
        return False
  

def uploadIndividual(repo, file):
    tracked = repo.git.ls_files(z=True).split('\0')
    if file not in tracked:
        print(f"The file {file} is not tracked by git. Please initialise the repository.")
        return
    
    branch = input("Which branch would you like to upload to? Please note that any typos will result in an upload to an incorrect branch.\n")
    if branch not in repo.branches:
        repo.git.checkout('HEAD', b=branch)
    else:
        repo.git.checkout(branch)

    repo.git.add(file)
    print(f"Staging upload for {file}.")

    commit_message = input("Enter a commit message: ")
    repo.git.commit(m=commit_message)

    try:
        repo.git.push('origin', branch)
        print(f"File {file} has been pushed to branch {branch}.")
    except git.exc.GitCommandError as error:
        print(f"Failed to upload file: {error}")


def scheduleUpload(repo, files):
    print("Functionality is WIP.")
    

def manualUpload(repo, changes):
    tracked = repo.git.ls_files(z=True).split('\0')
    for file in changes:
        if file not in tracked:
            print(f"The file {file} is not tracked by git. Please initialise the repository.")
        else:
            print(f"{file} is tracked.")

    branch = input("Which branch would you like to upload to? Please note that any typos will result in an upload to an incorrect branch.\n")
    if branch not in repo.branches:
        repo.git.checkout('HEAD', b=branch)
    else:
        repo.git.checkout(branch)

    repo.git.add(changes)
    print(f"Staging upload for {changes}.")

    commit_message = input("Enter a commit message: ")
    repo.git.commit(m=commit_message)

    try:
        repo.git.push('origin', branch)
        print(f"Files {changes} have been pushed to branch {branch}.")
    except git.exc.GitCommandError as error:
        print(f"Failed to upload files: {error}")


if __name__ == "__main__":
    main()