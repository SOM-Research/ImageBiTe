from github import Github, Auth
import github
import imagebite.io_managers.image_io_manager as ImageIOManager
import imagebite.io_managers.secrets as Secrets

def upload_image(test_id, prompt_id, instance_id, model, image_idx, image: bytes) -> str:

    file = ImageIOManager.get_full_path(test_id, prompt_id, instance_id, model, image_idx)
    full_path = file['path'] + "/" + file['filename']

    github_access = Secrets.load_github_keys()
    auth = Auth.Token(github_access['github_token'])
    g = Github(auth=auth)
    repo = g.get_user().get_repo(github_access['github_repo'])

    try:
        repo.get_contents(full_path, 'main')
    except github.UnknownObjectException as ex:
        repo.create_file(full_path, 'New generated image uploaded.', image, branch='main')
    
    g.close()
    
    return github_access['github_repo_prefix'] + full_path + "?raw=true"