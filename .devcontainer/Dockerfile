FROM python:3.10.3-bullseye

ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID


# インストールなどの作業はルートで
USER root


# 作業ディレクトリを作り移動する
WORKDIR /work

# 日本語フォントのインストール
RUN apt update \ 
  && apt install fonts-noto-cjk


# 必要ライブラリ
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# インストールに使用したファイルを削除
RUN rm -rf /work/*

# ユーザー追加
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME\
    && chmod 0440 /etc/sudoers.d/$USERNAME


# matplotlibのフォントキャッシュ削除
RUN rm -rf ~/.cache/matplotlib

# 通常ユーザーに戻す
USER $USERNAME
