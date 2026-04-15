# Experiment: OpenClaw Setup on WSL2

## Goal

Windows 11 + WSL2(Ubuntu) 환경에서 OpenClaw를 설치하고 동작을 검증합니다.

## Environment

| 항목         | 값                  |
|-------------|---------------------|
| OS          | Windows 11 Pro      |
| WSL 버전    | WSL2                |
| 배포판      | Ubuntu              |
| 권장 이유   | Windows 네이티브보다 안정적 (공식 문서 권장) |

## Setup Steps

### Step 1: Enter WSL2 Ubuntu

**Windows PowerShell:**
```powershell
wsl -d Ubuntu
```

### Step 2: Install Node.js 24

```bash
curl -fsSL https://fnm.vercel.app/install | bash
source ~/.bashrc

fnm install 24
fnm use 24
node -v   # v24.x.x 확인
npm -v
```

> fnm을 쓰는 이유: WSL2에서 nvm보다 빠르고, `.node-version` 파일로 프로젝트별 버전 고정 가능

### Step 3: Install OpenClaw

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```



### Step 4: Authenticate Claude CLI

OpenClaw에서 Claude CLI를 사용하는 경우 인증이 필요합니다. 자세한 인증 방법은 [docs/agents/claude.md - Authentication](../agents/claude.md#authentication)을 참고하세요.

**Option A: Windows Credentials 복사 (Claude Code 기존 사용자)**

Windows에서 이미 `claude auth login`을 완료한 경우 credentials 파일을 복사합니다.

```bash
# WSL2 내에서 실행
cp /mnt/c/Users/ahyuo/.claude/.credentials ~/.claude/.credentials
```

**Option B: API Key 환경변수**

```bash
echo 'export ANTHROPIC_API_KEY="sk-ant-..."' >> ~/.bashrc
source ~/.bashrc
```

### Step 5: Onboarding (Model Provider + API Key)

* General 
```bash
openclaw onboard --install-daemon 
```

* Skip-Channel 
상위에서 skip channel하면 에러가 발생해서 Command 생략  
```bash
openclaw onboard --install-daemon --skip-channels
```


* 설정 후 동작 
반드시 Token 기반으로 Web에서 접속   
```bash
│
◇  I understand this is personal-by-default and shared/multi-user use requires lock-down.
│   Continue?
│  Yes
│
◇  Setup mode
│  QuickStart
│
◇  QuickStart ─────────────────────────╮
│                                      │
│  Gateway port: 18789                 │
│  Gateway bind: Loopback (127.0.0.1)  │
│  Gateway auth: Token (default)       │
│  Tailscale exposure: Off             │
│  Direct to chat channels.            │
│                                      │
├──────────────────────────────────────╯
│
◇  Model/auth provider
│  Anthropic
│
◇  Anthropic auth method
│  Anthropic Claude CLI
│
◇  Provider notes ───────────────────────────────────────────────────────────────────────╮
│                                                                                        │
│  Claude CLI auth detected; switched Anthropic model selection to the local Claude CLI  │
│  backend.                                                                              │
│  Existing Anthropic auth profiles are kept for rollback.                               │
│                                                                                        │
├────────────────────────────────────────────────────────────────────────────────────────╯
│
◇  Model configured ──────────────────────────────────╮
│                                                     │
│  Default model set to claude-cli/claude-sonnet-4-6  │
│                                                     │
├─────────────────────────────────────────────────────╯
│
◇  Default model
│  Keep current (claude-cli/claude-sonnet-4-6)
│
◇  Model check ────────────────────────────────────────────────────────────────────────╮
│                                                                                      │
│  Model not found: claude-cli/claude-sonnet-4-6. Update agents.defaults.model or run  │
│  /models list.                                                                       │
│                                                                                      │
├──────────────────────────────────────────────────────────────────────────────────────╯
│
◇  Channels ────────────────╮
│                           │
│  Skipping channel setup.  │
│                           │
├───────────────────────────╯
Updated ~/.openclaw/openclaw.json
Workspace OK: ~/.openclaw/workspace
Sessions OK: ~/.openclaw/agents/main/sessions
│
◇  Web search ─────────────────────────────────────────────────────────────────╮
│                                                                              │
│  Web search lets your agent look things up online.                           │
│  Choose a provider. Some providers need an API key, and some work key-free.  │
│  Docs: https://docs.openclaw.ai/tools/web                                    │
│                                                                              │
├──────────────────────────────────────────────────────────────────────────────╯
│
◇  Search provider
│  Ollama Web Search
│
◇  Web search ──────────────────────────────────────────────────────────────╮
│                                                                           │
│  Ollama Web Search works without an API key.                              │
│  OpenClaw will enable the plugin and use it as your web_search provider.  │
│  Docs: https://docs.openclaw.ai/tools/web                                 │
│                                                                           │
├───────────────────────────────────────────────────────────────────────────╯
│
◇  Ollama Web Search ────────────────────────────────╮
│                                                    │
│  Ollama Web Search requires Ollama to be running.  │
│  Expected host: http://127.0.0.1:11434             │
│  Start Ollama before using this provider.          │
│                                                    │
├────────────────────────────────────────────────────╯
│
◇  Skills status ─────────────╮
│                             │
│  Eligible: 8                │
│  Missing requirements: 37   │
│  Unsupported on this OS: 7  │
│  Blocked by allowlist: 0    │
│                             │
├─────────────────────────────╯
│
◇  Configure skills now? (recommended)
│  Yes
│
◇  Install missing skill dependencies
│  Skip for now
│
◇  Set GOOGLE_PLACES_API_KEY for goplaces?
│  No
│
◇  Set NOTION_API_KEY for notion?
│  No
│
◇  Set OPENAI_API_KEY for openai-whisper-api?
│  No
│
◇  Set ELEVENLABS_API_KEY for sag?
│  No
│
◇  Hooks ──────────────────────────────────────────────────────────────────╮
│                                                                          │
│  Hooks let you automate actions when agent commands are issued.          │
│  Example: Save session context to memory when you issue /new or /reset.  │
│                                                                          │
│  Learn more: https://docs.openclaw.ai/automation/hooks                   │
│                                                                          │
├──────────────────────────────────────────────────────────────────────────╯
│
◇  Enable hooks?
│  Skip for now
│
◇  Systemd ────────────────────────────────────────────────────────────────────────────────╮
│                                                                                          │
│  Linux installs use a systemd user service by default. Without lingering, systemd stops  │       
│  the user session on logout/idle and kills the Gateway.                                  │       
│  Enabling lingering now (may require sudo; writes /var/lib/systemd/linger).              │       
│                                                                                          │       
├──────────────────────────────────────────────────────────────────────────────────────────╯       
│
◇  Systemd ──────────────────────────────╮
│                                        │
│  Enabled systemd lingering for ahyuo.  │
│                                        │
├────────────────────────────────────────╯
│
◇  Gateway service runtime ────────────────────────────────────────────╮
│                                                                      │
│  QuickStart uses Node for the Gateway service (stable + supported).  │
│                                                                      │
....           

openclaw tui - ws://127.0.0.1:18789 - agent main - session main

 session agent:main:main


Wake up, my friend!


 ⠇ kerfuffling… • 14m 58s | connected                                                                                                                                    
 agent main | session main | unknown | tokens ?/200k
```


- Model Provider 선택: Anthropic / OpenAI / Google
- API 키 입력
- Gateway 자동 설정 (~2분 소요)

### Step 6: Verify Gateway

```bash
# Gateway 토큰 확인
openclaw config get gateway.token

# 토큰과 함께 상태 확인
openclaw gateway status --token <위에서 확인한 토큰>
```

> `unauthorized: gateway token missing` 오류 발생 시 위 순서로 토큰을 먼저 확인한다.

### Step 7: Open Dashboard

```bash
openclaw dashboard
```

WSL2에서 실행해도 Windows 브라우저에서 `http://127.0.0.1:18789/` 로 접속 가능합니다.

## Checklist

- [O] WSL2 Ubuntu 진입 확인
- [O] Node.js 24 설치 완료
- [O] OpenClaw 설치 완료
- [ ] Claude CLI 인증 완료 (Option A 또는 B)
- [ ] `openclaw onboard` 완료 (API 키 설정)
- [ ] `openclaw gateway status` → 정상 응답
- [ ] 대시보드 브라우저 접속 확인

## Result

| 항목              | 결과    |
|------------------|---------|
| 설치             | 대기 중 |
| Gateway 기동     | 대기 중 |
| 대시보드 접속    | 대기 중 |

## Notes

- **Step 5**: 채널이 없는 경우 `--skip-channels` 옵션으로 채널 설정을 건너뜀. "Skip for now" UI 선택 시 `TypeError: Cannot read properties of undefined (reading 'trim')` 버그 발생하므로 반드시 CLI 옵션으로 처리.
- **Step 6**: `openclaw gateway status` 실행 시 `unauthorized: gateway token missing` 오류 발생 가능. `openclaw config get gateway.token`으로 토큰 확인 후 `--token` 옵션으로 전달 필요.
