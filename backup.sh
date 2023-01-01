#! /usr/bin/bash

printf "this script has been replaced by backup.py! and for learning purpose only!" 1>&2
exit

if (($# != 2)); then
  echo "error: must specify a dest path and version number!" 1>&2
  exit
fi

dest="$1" # backup directory
dest=${dest%/}
ver="v$2"

for repo in */ ; do
  repo=${repo%/}
  if ! [ -f "$repo/sha1sum.txt" ]; then
    continue
  fi

  printf "\n\n\n===============================\n"
  echo "$repo"
  printf "===============================\n\n\n"

  dest2="$dest/${repo}.sync"
  dest3="$dest/${repo}.sync/${repo}.${ver}"

  # hash or rehash source directory
  if ! [ -s "$repo/sha1sum.txt" ]; then
    echo "sha1sum.txt is empty! hasing..." 1>&2
    cd $repo
    find . -type f -exec sha1sum {} \; > sha1sum.txt
    cat sha1sum.txt | sort > sha1sum.txt
    cd - > /dev/null
  else
    # echo "sha1sum.txt not empty! assuming it's up to date."
    echo "sha1sum.txt not empty! rehasing..."
    cd "$repo"
    find . -type f -exec sha1sum {} \; > sha1sum-new.txt
    cat sha1sum-new.txt | sort > sha1sum-new.txt
    if [ cmp --silent sha1sum.txt sha1sum-new.txt ]; then
      echo "nothing has changed or corrupted."
      rm sha1sum-new.txt
    else
      echo "sha1sum.txt and sha1sum-new.txt are different, please check manually for change or corruption!" 1>&2
      continue
    fi
    cd - > /dev/null
  fi

  # check destination
  if [ -d "$dest3" ]; then
    # exist!
    echo "$dest3 folder exists!"
    if ! [ -f "$dest3/sha1sum.txt" ]; then
      echo "$dest3/sha1sum.txt not found, something wrong!" 1>&2
      continue
    fi
    echo "rehasing..."
    cd "$dest3"
    find . -type f -exec sha1sum {} \; > sha1sum-new.txt
    cat sha1sum-new.txt | sort > sha1sum-new.txt
    if [ cmp --silent sha1sum.txt sha1sum-new.txt ]; then
      echo "nothing has changed or corrupted."
      rm sha1sum-new.txt
    else
      echo "sha1sum.txt and sha1sum-new.txt are different, please check manually for corruption!" 1>&2
      continue
    fi
    cd - > /dev/null
  else
    # dest3 doesn't exist, copy
    echo "copying to $dest3 ..."
    rsync -a "$repo/" "$dest3"
  fi
done
