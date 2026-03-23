FROM gitpod/workspace-postgres

USER gitpod
RUN pyenv install 3.11.9 && pyenv global 3.11.9