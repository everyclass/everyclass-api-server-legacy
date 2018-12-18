# EveryClass-api-server

![status](https://img.shields.io/badge/status-in%20development-green.svg)
[![Build Status](https://travis-ci.org/AdmirablePro/everyclass-api-server.svg?branch=master)](https://travis-ci.org/AdmirablePro/everyclass-api-server)
![works-on](https://img.shields.io/badge/works%20on-our%20cluster-brightgreen.svg)
![python version](https://img.shields.io/badge/python-3.6-blue.svg)
![license](https://img.shields.io/badge/license-MPL_2.0-orange.svg)


This is the api-server microservice of [EveryClass](https://github.com/fr0der1c/EveryClass) project. The `everyclass-api-server` exposes a RESTful API so third-party developers can use the power of EveryClass's data to do some interesting things.


### Communication

If you found any problem of the code, please open an issue here and make sure you provided much information.

To discuss questions regarding the project, I suggest you join our [forum](https://base.admirable.one/c/everyclass) (Chinese).


### Technology stack

- uWSGI: the gateway between programme itself and reverse proxy
- Flask: the micro Python web framework
- MySQL: relational database


### Using the source

1. Use ``pipenv sync`` to build a virtualenv with dependencies installed
2. Copy `everyclass/api_server/config/default.py` and name it `development.py`. Change settings to adjust to your local development environment
4. Set the environment variable `MODE` to `DEVELOPMENT`, then run `server.py`

### Contributions, Bug Reports, Feature Requests

This is an open source project and we would be happy to see contributors who report bugs and file feature requests submitting pull requests as well. Please report issues here [https://github.com/fr0der1c/EveryClass-api-server/issues](https://github.com/fr0der1c/EveryClass-server/issues)

### Branch Policy

Please get familiar with **git-flow** before you start contributing. It's a work flow to make source code better to manage.

We have the following branches :
- **feature/some-feature**: All your development goes on this branch. When you are done, make a pull request or just merge to `develop` branch if you have permission
- **development**: This is where your finished code goes. This branch will be updated rapidly.
- **release**: While commits are accumulating on ``development`` branch, they will be periodically merged to this branch by maintainer to make releases. **The maintainer should make a version tag then write the changelog on our forum.** This is the branch watched by Travis, our continuous integration tool, which runs unit-test check, builds Docker image, pushes the image to our private registry and updates services in staging environment.
- **master**: This is the actual code running on the [server](https://everyclass.xyz). Codes are tested in staging environment for a while before they are deployed to production environment.



### Contributions Best Practices
#### Commits

- Write clear meaningful git commit messages
- Make sure your PR's description contains GitHub's special keyword references that automatically close the related issue when the PR is merged. (More info at  [https://github.com/blog/1506-closing-issues-via-pull-requests](https://github.com/blog/1506-closing-issues-via-pull-requests))
- When you make very very minor changes to a PR of yours (like for example fixing a failing travis build or some small style corrections or minor changes requested by reviewers) make sure you squash your commits afterwards so that you don't have an absurd number of commits for a very small fix. (Learn how to squash at https://davidwalsh.name/squash-commits-git )


#### Feature Requests and Bug Reports

When you file a feature request or when you are submitting a bug report to the issue tracker, make sure you add steps to reproduce it. Especially if that bug is some weird/rare one.

#### Join the development

Feel free to join the development and happy coding. Again, please get familiar with **git-flow** before you start contributing.