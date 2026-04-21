pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    parameters {
        string(name: 'REPO_URL', defaultValue: '', description: 'Git repository URL. Leave empty when the Jenkins job is already connected to this repository.')
        string(name: 'REPO_REF', defaultValue: 'main', description: 'Fallback Git ref to checkout when the issue body does not specify one.')
        string(name: 'ISSUE_NUMBER', defaultValue: '', description: 'GitHub issue number for the test request.')
        string(name: 'ISSUE_TITLE', defaultValue: '[TEST]', description: 'GitHub issue title.')
        text(name: 'ISSUE_BODY', defaultValue: '', description: 'Full GitHub issue body from the test request template.')
        string(name: 'EXPECTED_RUNNER', defaultValue: 'local-dev', description: 'Runner name recorded in the test request.')
        string(name: 'GITHUB_OWNER', defaultValue: '', description: 'GitHub repository owner or organization.')
        string(name: 'GITHUB_REPO', defaultValue: '', description: 'GitHub repository name.')
        string(name: 'PYTHON_EXE', defaultValue: 'python', description: 'Python executable available on the Jenkins agent.')
    }

    environment {
        ISSUE_BODY_FILE = 'results/jenkins-issue-body.md'
    }

    stages {
        stage('Checkout') {
            steps {
                script {
                    if (params.REPO_URL?.trim()) {
                        checkout([
                            $class: 'GitSCM',
                            branches: [[name: params.REPO_REF]],
                            userRemoteConfigs: [[url: params.REPO_URL]],
                        ])
                    } else {
                        checkout scm
                    }
                }
            }
        }

        stage('Prepare Request') {
            steps {
                script {
                    powershell '''
                        New-Item -ItemType Directory -Force -Path results | Out-Null
                    '''
                    writeFile file: env.ISSUE_BODY_FILE, text: params.ISSUE_BODY ?: ''
                }
            }
        }

        stage('Checkout Requested Ref') {
            steps {
                powershell '''
                    $issueBodyPath = $env:ISSUE_BODY_FILE
                    $issueBody = Get-Content -LiteralPath $issueBodyPath -Raw -Encoding utf8
                    if ($null -eq $issueBody -or -not $issueBody.Trim()) {
                        throw "ISSUE_BODY is empty. Enter the GitHub issue body in Build with Parameters."
                    }

                    $requestRef = $null
                    $markdownMatch = [regex]::Match($issueBody, '^- Branch / Tag / Commit:\\s*(.+)$', 'Multiline')
                    if ($markdownMatch.Success) {
                        $requestRef = $markdownMatch.Groups[1].Value.Trim()
                    }

                    if (-not $requestRef) {
                        $formMatch = [regex]::Match(
                            $issueBody,
                            '^###\\s+Branch / Tag / Commit\\s*$\\r?\\n+(.+?)(?=\\r?\\n###\\s+|\\Z)',
                            [System.Text.RegularExpressions.RegexOptions]::Multiline -bor [System.Text.RegularExpressions.RegexOptions]::Singleline
                        )
                        if ($formMatch.Success) {
                            $lines = $formMatch.Groups[1].Value -split "\\r?\\n" | ForEach-Object { $_.Trim() } | Where-Object { $_ }
                            if ($lines.Count -gt 0) {
                                $requestRef = $lines[0]
                            }
                        }
                    }

                    if (-not $requestRef) {
                        $requestRef = "${params.REPO_REF}"
                    }

                    Write-Host "Requested Git ref: $requestRef"
                    git fetch --all --tags
                    git checkout $requestRef
                    git rev-parse HEAD
                '''
            }
        }

        stage('Run Test Request') {
            steps {
                powershell '''
                    & "${params.PYTHON_EXE}" -m mcp.scripts.run_test_request `
                        --issue-number "${params.ISSUE_NUMBER}" `
                        --issue-title "${params.ISSUE_TITLE}" `
                        --issue-body-file "$env:ISSUE_BODY_FILE" `
                        --expected-runner "${params.EXPECTED_RUNNER}"
                '''
            }
        }

        stage('Render Comment') {
            steps {
                powershell '''
                    $resultJson = "results/Github-ISSUE-TR-${params.ISSUE_NUMBER}.json"
                    $resultComment = "results/test-request-comment-${params.ISSUE_NUMBER}.md"
                    & "${params.PYTHON_EXE}" -m mcp.scripts.make_test_result `
                        --issue-body-file "$env:ISSUE_BODY_FILE" `
                        --result-path "$resultJson" `
                        --output-path "$resultComment" `
                        --execution-platform "jenkins"
                '''
            }
        }

        stage('Post GitHub Comment') {
            when {
                expression {
                    return params.GITHUB_OWNER?.trim() && params.GITHUB_REPO?.trim() && params.ISSUE_NUMBER?.trim()
                }
            }
            steps {
                withCredentials([string(credentialsId: 'github-token', variable: 'GITHUB_TOKEN')]) {
                    powershell '''
                        $commentPath = "results/test-request-comment-${params.ISSUE_NUMBER}.md"
                        $commentBody = Get-Content -LiteralPath $commentPath -Raw -Encoding utf8
                        $bodyJson = @{ body = $commentBody } | ConvertTo-Json -Depth 5
                        $headers = @{
                            Authorization = "Bearer $env:GITHUB_TOKEN"
                            Accept = "application/vnd.github+json"
                            "X-GitHub-Api-Version" = "2022-11-28"
                        }

                        $url = "https://api.github.com/repos/${params.GITHUB_OWNER}/${params.GITHUB_REPO}/issues/${params.ISSUE_NUMBER}/comments"
                        Invoke-RestMethod -Method Post -Uri $url -Headers $headers -Body $bodyJson -ContentType "application/json; charset=utf-8" | Out-Null
                        Write-Host "Posted GitHub issue comment to #${params.ISSUE_NUMBER}"
                    '''
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'results/**/*', allowEmptyArchive: true
        }
    }
}
