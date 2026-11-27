#!/usr/bin/env bash
# Fails if tracked files or commit metadata contain personal or secret-looking data.
set -u
cd "$(git rev-parse --show-toplevel)"

found=0
check() { # label, extended regex
    local hits
    hits=$(git grep -nIE -e "$2" -- . ':!scripts/check-sensitive.sh' ':!LICENSE' 2>/dev/null)
    if [ -n "$hits" ]; then
        printf '%s:\n%s\n\n' "$1" "$hits"
        found=1
    fi
}

check "Email address" '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'
check "Home directory path" '(/Users/|/home/|C:\\Users\\)[A-Za-z0-9._-]+'
check "Hardware (MAC) address" '([0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}'
check "IPv4 address" '\b([0-9]{1,3}\.){3}[0-9]{1,3}\b'
check "Secret-looking token" '(ghp_|gho_|github_pat_|sk-[A-Za-z0-9]{8}|AKIA[0-9A-Z]{16}|xox[baprs]-|BEGIN [A-Z ]*PRIVATE KEY)'
check "Credential assignment" '(password|passwd|secret|api[_-]?key|token)[[:space:]]*[:=][[:space:]]*["'"'"'][^"'"'"']{6,}'

if git rev-parse HEAD >/dev/null 2>&1; then
    meta=$(git log --format='%an <%ae>%n%cn <%ce>' | sort -u | grep -v 'noreply')
    if [ -n "$meta" ]; then
        printf 'Commit author or committer without a noreply address:\n%s\n\n' "$meta"
        found=1
    fi
fi

if [ "$found" -eq 0 ]; then
    echo "check-sensitive: clean"
fi
exit "$found"
