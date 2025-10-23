# YEAP Dashboard - GitHub Upload Script (Improved PowerShell Version)
# Usage:
#   - Run from project root:  .\upload_to_github_example.ps1 [-CommitMessage "msg"] [-ForcePush] [-RemoteUrl "https://github.com/emplabyouth/emplabyeap.git"] [-Branch main]
#   - Defaults: Branch=main, RemoteUrl=https://github.com/emplabyouth/emplabyeap.git

param(
    [string]$CommitMessage = $null,
    [switch]$ForcePush,
    [string]$RemoteUrl = "https://github.com/emplabyouth/emplabyeap.git",
    [string]$Branch = "main"
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "YEAP Dashboard - GitHub Upload Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Basic environment checks
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "Error: Git is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Git: https://git-scm.com/downloads" -ForegroundColor Yellow
    exit 1
}

# Verify project root by checking data folder
if (-not (Test-Path "orignaldata")) {
    Write-Host "Error: Please run this script from the project root directory" -ForegroundColor Red
    Write-Host "Current directory: $(Get-Location)" -ForegroundColor Yellow
    exit 1
}

try {
    # Step 0: Show current status
    Write-Host "Step 0: Showing Git status..." -ForegroundColor Green
    git status
    Write-Host ""

    # Step 1: Ensure remote origin points to the provided repo
    Write-Host "Step 1: Ensuring remote 'origin' is set to $RemoteUrl" -ForegroundColor Green
    $remotes = git remote 2>$null
    if ($LASTEXITCODE -ne 0) { throw "Failed to read git remotes" }

    if ($remotes -notcontains "origin") {
        Write-Host "Remote 'origin' not found. Adding..." -ForegroundColor Yellow
        git remote add origin $RemoteUrl
        if ($LASTEXITCODE -ne 0) { throw "Failed to add remote origin" }
    } else {
        Write-Host "Remote 'origin' found. Updating URL..." -ForegroundColor Yellow
        git remote set-url origin $RemoteUrl
        if ($LASTEXITCODE -ne 0) { throw "Failed to set remote origin URL" }
    }
    Write-Host "Remote 'origin' configured: $RemoteUrl" -ForegroundColor Green
    Write-Host ""

    # Step 2: Ensure branch is 'main'
    Write-Host "Step 2: Ensuring branch is '$Branch'" -ForegroundColor Green
    $currentBranch = (git rev-parse --abbrev-ref HEAD).Trim()
    if ($LASTEXITCODE -ne 0) { throw "Failed to determine current branch" }

    if ($currentBranch -ne $Branch) {
        Write-Host "Renaming current branch '$currentBranch' to '$Branch'" -ForegroundColor Yellow
        git branch -M $Branch
        if ($LASTEXITCODE -ne 0) { throw "Failed to rename branch to '$Branch'" }
    } else {
        Write-Host "On branch '$Branch'" -ForegroundColor Green
    }
    Write-Host ""

    # Step 3: Stage changes
    Write-Host "Step 3: Adding all changes to Git..." -ForegroundColor Green
    git add .
    if ($LASTEXITCODE -ne 0) { throw "Failed to add files to Git" }
    Write-Host "Files added successfully!" -ForegroundColor Green
    Write-Host ""

    # Step 4: Commit changes (skip if nothing to commit)
    Write-Host "Step 4: Committing changes..." -ForegroundColor Green
    # Detect if there are staged changes
    git diff --cached --quiet
    $hasStagedChanges = ($LASTEXITCODE -ne 0)

    if (-not $hasStagedChanges) {
        Write-Host "No staged changes. Skipping commit." -ForegroundColor Yellow
    } else {
        if ([string]::IsNullOrWhiteSpace($CommitMessage)) {
            $CommitMessage = "Update YEAP Dashboard - $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
        }
        git commit -m $CommitMessage
        if ($LASTEXITCODE -ne 0) { throw "Failed to commit changes" }
        Write-Host "Changes committed successfully!" -ForegroundColor Green
    }
    Write-Host ""

    # Step 5: Try pulling with rebase (if upstream exists)
    Write-Host "Step 5: Pulling latest from origin/$Branch with rebase (if available)..." -ForegroundColor Green
    git fetch origin
    if ($LASTEXITCODE -eq 0) {
        git pull --rebase origin $Branch
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Pull with rebase encountered issues. Proceeding to push anyway." -ForegroundColor Yellow
        } else {
            Write-Host "Rebase successful." -ForegroundColor Green
        }
    } else {
        Write-Host "Fetch failed or no upstream yet. Will set upstream during push." -ForegroundColor Yellow
    }
    Write-Host ""

    # Step 6: Push to GitHub
    Write-Host "Step 6: Pushing to GitHub..." -ForegroundColor Green
    git push -u origin $Branch
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Normal push failed." -ForegroundColor Yellow
        if ($ForcePush) {
            Write-Host "Attempting safe force push (--force-with-lease)..." -ForegroundColor Red
            git push origin $Branch --force-with-lease
            if ($LASTEXITCODE -ne 0) { throw "Force push failed. Please check your internet connection and GitHub credentials" }
            Write-Host "Force push completed successfully!" -ForegroundColor Green
        } else {
            Write-Host "Tip: Re-run with -ForcePush to override remote changes (use cautiously)." -ForegroundColor Yellow
            throw "Push failed. Resolve conflicts or use -ForcePush if appropriate."
        }
    } else {
        Write-Host "Push completed successfully!" -ForegroundColor Green
    }
    Write-Host ""

    # Success completion
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "Upload completed successfully!" -ForegroundColor Green
    Write-Host "Your YEAP Dashboard has been uploaded to:" -ForegroundColor Green
    Write-Host "$RemoteUrl" -ForegroundColor Blue
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "If you're using Streamlit Cloud, deployment should update shortly." -ForegroundColor Yellow
    Write-Host "Check deployment status at: https://share.streamlit.io/" -ForegroundColor Blue
    Write-Host ""

} catch {
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Upload failed!" -ForegroundColor Red
    exit 1
}