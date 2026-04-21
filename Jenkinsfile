pipeline {
    agent any

    triggers {
        GenericTrigger(
            genericVariables: [
                [key: 'WEBHOOK_EVENT', value: '$.action'],
                [key: 'WEBHOOK_ISSUE_NUMBER', value: '$.issue.number'],
                [key: 'WEBHOOK_ISSUE_TITLE', value: '$.issue.title'],
                [key: 'WEBHOOK_ISSUE_BODY', value: '$.issue.body'],
                [key: 'WEBHOOK_REPO_URL', value: '$.repository.clone_url'],
                [key: 'WEBHOOK_DEFAULT_BRANCH', value: '$.repository.default_branch'],
                [key: 'WEBHOOK_OWNER', value: '$.repository.owner.login'],
                [key: 'WEBHOOK_REPO', value: '$.repository.name'],
                [key: 'WEBHOOK_LABELS', value: '$.issue.labels[*].name']
            ],
            causeString: 'GitHub issue webhook #$WEBHOOK_ISSUE_NUMBER',
            printContributedVariables: true,
            printPostContent: true,
            silentResponse: false
        )
    }

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
        REQUEST_PAYLOAD_FILE = 'results/jenkins-request.json'
    }

    stages {
        stage('Resolve Request') {
            steps {
                script {
                    def normalize = { value ->
                        def text = value == null ? '' : value.toString().trim()
                        if (!text || text.equalsIgnoreCase('null') || text.equalsIgnoreCase('undefined')) {
                            return ''
                        }
                        return text
                    }
                    def webhookIssueNumber = normalize(env.WEBHOOK_ISSUE_NUMBER)
                    def webhookIssueBody = normalize(env.WEBHOOK_ISSUE_BODY)
                    def webhookTriggered = (webhookIssueNumber || webhookIssueBody) ? true : false
                    def pickWebhookFirst = { String webhookValue, String manualValue, String fallback = '' ->
                        def webhookTrimmed = normalize(webhookValue)
                        if (webhookTrimmed) {
                            return webhookTrimmed
                        }
                        def manualTrimmed = normalize(manualValue)
                        if (manualTrimmed) {
                            return manualTrimmed
                        }
                        return fallback
                    }
                    def pickManualOnly = { String manualValue, String fallback = '' ->
                        def manualTrimmed = normalize(manualValue)
                        if (manualTrimmed) {
                            return manualTrimmed
                        }
                        return fallback
                    }

                    env.EFFECTIVE_REPO_URL = webhookTriggered
                        ? pickWebhookFirst(env.WEBHOOK_REPO_URL, params.REPO_URL)
                        : pickManualOnly(params.REPO_URL)
                    env.EFFECTIVE_REPO_REF = webhookTriggered
                        ? pickWebhookFirst(env.WEBHOOK_DEFAULT_BRANCH, params.REPO_REF, 'main')
                        : pickManualOnly(params.REPO_REF, 'main')
                    env.EFFECTIVE_ISSUE_NUMBER = webhookTriggered
                        ? pickWebhookFirst(env.WEBHOOK_ISSUE_NUMBER, params.ISSUE_NUMBER)
                        : pickManualOnly(params.ISSUE_NUMBER)
                    env.EFFECTIVE_ISSUE_TITLE = webhookTriggered
                        ? pickWebhookFirst(env.WEBHOOK_ISSUE_TITLE, params.ISSUE_TITLE, '[TEST]')
                        : pickManualOnly(params.ISSUE_TITLE, '[TEST]')
                    env.EFFECTIVE_ISSUE_BODY = webhookTriggered
                        ? pickWebhookFirst(env.WEBHOOK_ISSUE_BODY, params.ISSUE_BODY)
                        : pickManualOnly(params.ISSUE_BODY)
                    env.EFFECTIVE_EXPECTED_RUNNER = pickManualOnly(params.EXPECTED_RUNNER, 'local-dev')
                    env.EFFECTIVE_GITHUB_OWNER = webhookTriggered
                        ? pickWebhookFirst(env.WEBHOOK_OWNER, params.GITHUB_OWNER)
                        : pickManualOnly(params.GITHUB_OWNER)
                    env.EFFECTIVE_GITHUB_REPO = webhookTriggered
                        ? pickWebhookFirst(env.WEBHOOK_REPO, params.GITHUB_REPO)
                        : pickManualOnly(params.GITHUB_REPO)
                    env.EFFECTIVE_LABELS = normalize(env.WEBHOOK_LABELS)
                    env.EFFECTIVE_EVENT = webhookTriggered ? (env.WEBHOOK_EVENT ?: 'webhook') : 'manual'

                    def labels = normalize(env.EFFECTIVE_LABELS).toLowerCase()
                    def title = normalize(env.EFFECTIVE_ISSUE_TITLE).toLowerCase()
                    def body = normalize(env.EFFECTIVE_ISSUE_BODY)

                    def hasIssueContext = normalize(env.EFFECTIVE_ISSUE_NUMBER) && body
                    def looksLikeTestRequest = labels.contains('test-request') || title.startsWith('[test]') || body.contains('### Target Runner')

                    env.SHOULD_RUN_REQUEST = (hasIssueContext && looksLikeTestRequest) ? 'true' : 'false'

                    echo "Resolved trigger event: ${env.EFFECTIVE_EVENT}"
                    echo "Webhook detected: ${webhookTriggered}"
                    echo "Resolved issue number: ${env.EFFECTIVE_ISSUE_NUMBER ?: 'n/a'}"
                    echo "Resolved repository: ${env.EFFECTIVE_GITHUB_OWNER ?: 'n/a'}/${env.EFFECTIVE_GITHUB_REPO ?: 'n/a'}"
                    echo "Resolved issue body length: ${body.length()}"
                    echo "Should run request: ${env.SHOULD_RUN_REQUEST}"
                }
            }
        }

        stage('Checkout') {
            when {
                expression {
                    return env.SHOULD_RUN_REQUEST == 'true'
                }
            }
            steps {
                script {
                    if (env.EFFECTIVE_REPO_URL?.trim()) {
                        checkout([
                            $class: 'GitSCM',
                            branches: [[name: env.EFFECTIVE_REPO_REF]],
                            userRemoteConfigs: [[url: env.EFFECTIVE_REPO_URL]],
                        ])
                    } else {
                        checkout scm
                    }
                }
            }
        }

        stage('Prepare Request') {
            when {
                expression {
                    return env.SHOULD_RUN_REQUEST == 'true'
                }
            }
            steps {
                script {
                    powershell '''
                        New-Item -ItemType Directory -Force -Path results | Out-Null
                    '''
                    writeFile file: env.ISSUE_BODY_FILE, text: env.EFFECTIVE_ISSUE_BODY ?: ''
                    writeFile(
                        file: env.REQUEST_PAYLOAD_FILE,
                        text: groovy.json.JsonOutput.prettyPrint(
                            groovy.json.JsonOutput.toJson([
                                event: env.EFFECTIVE_EVENT,
                                issue_number: env.EFFECTIVE_ISSUE_NUMBER,
                                issue_title: env.EFFECTIVE_ISSUE_TITLE,
                                repo_url: env.EFFECTIVE_REPO_URL,
                                repo_ref: env.EFFECTIVE_REPO_REF,
                                github_owner: env.EFFECTIVE_GITHUB_OWNER,
                                github_repo: env.EFFECTIVE_GITHUB_REPO,
                                labels: env.EFFECTIVE_LABELS,
                            ])
                        )
                    )
                }
            }
        }

        stage('Checkout Requested Ref') {
            when {
                expression {
                    return env.SHOULD_RUN_REQUEST == 'true'
                }
            }
            steps {
                powershell '''
                    $issueBodyPath = $env:ISSUE_BODY_FILE
                    $issueBody = Get-Content -LiteralPath $issueBodyPath -Raw -Encoding utf8
                    if ($null -eq $issueBody -or -not $issueBody.Trim()) {
                        throw "ISSUE_BODY is empty. Check the Generic Webhook Trigger mapping or enter the value in Build with Parameters."
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
                        $requestRef = "$env:EFFECTIVE_REPO_REF"
                    }

                    Write-Host "Requested Git ref: $requestRef"
                    git fetch --all --tags
                    git checkout $requestRef
                    git rev-parse HEAD
                '''
            }
        }

        stage('Run Test Request') {
            when {
                expression {
                    return env.SHOULD_RUN_REQUEST == 'true'
                }
            }
            steps {
                powershell '''
                    & "${params.PYTHON_EXE}" -m mcp.scripts.run_test_request `
                        --issue-number "$env:EFFECTIVE_ISSUE_NUMBER" `
                        --issue-title "$env:EFFECTIVE_ISSUE_TITLE" `
                        --issue-body-file "$env:ISSUE_BODY_FILE" `
                        --expected-runner "$env:EFFECTIVE_EXPECTED_RUNNER"
                '''
            }
        }

        stage('Render Comment') {
            when {
                expression {
                    return env.SHOULD_RUN_REQUEST == 'true'
                }
            }
            steps {
                powershell '''
                    $resultJson = "results/Github-ISSUE-TR-$env:EFFECTIVE_ISSUE_NUMBER.json"
                    $resultComment = "results/test-request-comment-$env:EFFECTIVE_ISSUE_NUMBER.md"
                    & "${params.PYTHON_EXE}" -m mcp.scripts.make_test_result `
                        --issue-body-file "$env:ISSUE_BODY_FILE" `
                        --result-path "$resultJson" `
                        --output-path "$resultComment" `
                        --execution-platform "local-direct"
                '''
            }
        }

        stage('Post GitHub Comment') {
            when {
                expression {
                    return env.SHOULD_RUN_REQUEST == 'true' &&
                        env.EFFECTIVE_GITHUB_OWNER?.trim() &&
                        env.EFFECTIVE_GITHUB_REPO?.trim() &&
                        env.EFFECTIVE_ISSUE_NUMBER?.trim()
                }
            }
            steps {
                withCredentials([string(credentialsId: 'github-token', variable: 'GITHUB_TOKEN')]) {
                    powershell '''
                        $commentPath = "results/test-request-comment-$env:EFFECTIVE_ISSUE_NUMBER.md"
                        $commentBody = Get-Content -LiteralPath $commentPath -Raw -Encoding utf8
                        $bodyJson = @{ body = $commentBody } | ConvertTo-Json -Depth 5
                        $headers = @{
                            Authorization = "Bearer $env:GITHUB_TOKEN"
                            Accept = "application/vnd.github+json"
                            "X-GitHub-Api-Version" = "2022-11-28"
                        }

                        $url = "https://api.github.com/repos/$env:EFFECTIVE_GITHUB_OWNER/$env:EFFECTIVE_GITHUB_REPO/issues/$env:EFFECTIVE_ISSUE_NUMBER/comments"
                        Invoke-RestMethod -Method Post -Uri $url -Headers $headers -Body $bodyJson -ContentType "application/json; charset=utf-8" | Out-Null
                        Write-Host "Posted GitHub issue comment to #$env:EFFECTIVE_ISSUE_NUMBER"
                    '''
                }
            }
        }

        stage('Skip Non Test Request') {
            when {
                expression {
                    return env.SHOULD_RUN_REQUEST != 'true'
                }
            }
            steps {
                echo 'Webhook payload did not look like a test-request issue, so the pipeline is exiting without running MCP.'
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'results/**/*', allowEmptyArchive: true
        }
    }
}
