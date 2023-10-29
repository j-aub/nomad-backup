import from nomad_backup import config

def run_hook(hook: str) -> bool:
    failed = True

    try:
        subprocess.run([hook], check=True)
    except FileNotFoundError:
        print('The hook file does not exist.')
    except subprocess.CalledProcessError as e:
        print(f'The hook failed with exit code {e.returncode}.')
    else:
        print(f'The hook ran successfully')
        failed = False

    return failed
