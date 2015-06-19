files=$(git status -u --porcelain --no-column)
if [ -z "$files" ]; then
  exit 0
fi

echo
echo "ERROR: Preventing push with untracked source files:"
echo
echo "$files" | sed "s/^/    /"
echo
echo "Either include these files in your commits, add them to .gitignore"
echo "or stash them with git stash -u."
echo
exit 1
