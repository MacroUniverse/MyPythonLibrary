#! /usr/bin/bash

if (($# != 1)); then
  echo "error: must specify a dest path!" 1>&2
  exit
fi

dest="$1" # backup directory

for repo in */ ; do
  repo=${repo%/}
  if ! [ -f "$repo/.gitattributes" ]; then
    continue;
  fi

  printf "\n\n\n===============================\n"
  echo "$repo"
  printf "===============================\n\n\n"
  if ! [ -d "$repo" ]; then
    echo "error: directory not found!"
    continue
  fi
  gitdir="${dest}${repo}.git"
  dirflag="--work-tree=$repo --git-dir=$gitdir"
  echo "mkdir $gitdir ..."
  mkdir -p "$gitdir" &&
  echo "git init ..." &&
  git $dirflag init &&
  echo "git add -A ..." &&
  git $dirflag add -A --verbose &&
  # 其他有用的命令：
  echo "git commit ..."
  git $dirflag commit -m 'update'
  # echo "git status ..."
  # git $dirflag status
  # echo "git gc"
  # git $dirflag gc
done
