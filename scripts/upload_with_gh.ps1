param(
    [string]$RepoName = "citeddoc-qa",
    [string]$Description = "Cited document Q&A demo using retrieval and the OpenAI Responses API"
)

if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    Write-Error "GitHub CLI (gh) is not installed. Install it from https://cli.github.com/ and run gh auth login."
    exit 1
}

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Error "Git is not installed. Install it from https://git-scm.com/downloads."
    exit 1
}

git init
git add .
git commit -m "Initial CitedDoc QA project"
gh repo create $RepoName --public --source . --remote origin --push --description $Description

