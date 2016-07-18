`gitmirror.py`
==============

Create and update mirrors of git repositories.
To use the script simply pass a config file (see below) as the first argument to the script.


Status
------

- [x] Read a config file for global options
- [x] Parse repo list
- [x] Basic cloning and updating
- [x] Basic logging
- [ ] Support cloning to remote locations (SSH)
- [ ] Add option handling for remote and local
- [ ] Run jobs in parallel


Config file
-----------

The config file specifies the global options for the `gitmirror.py`-run.
A valid option file is:

```ini
[config]
jobs            = 8
logging_dir     = /home/git/.gitmirror/log
repository_dir  = /home/git/
repository_file = /home/git/.gitmirror/repositories.txt
```

Description:

- `jobs` (optional): number of jobs in multithreaded run
- `logging_dir`: directory where logs will be created
- `repository_dir`: dir where all repositories will be mirrored
- `repository_file`: file containing the repository list


Repository list
---------------

The repository list is a file of lines with the following syntax:
```
<remote_repository> [<remote_options>] -> <local_repository> [<local_options>]
```

The `[<remote_options>]` and `[<local_options>]` fields are optional and are not used at the moment.
An example for such entry is:

```
git@github.com:f-koehler/gitmirror.git -> f-koehler/gitmirror.git
```
