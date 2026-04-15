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
```bash
openclaw onboard --install-daemon --skip-channels
```

```
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
◇  Channel status ──────────────────────────────────────╮
│                                                       │
│  Discord: needs token                                 │
│  WhatsApp: not linked                                 │
│  QQ Bot: needs AppID + AppSecret                      │
│  Google Chat: needs service account                   │
│  MS Teams: needs app credentials                      │
│  Mattermost: needs token + url                        │
│  Nextcloud Talk: needs setup                          │
│  Feishu: needs app credentials                        │
│  Matrix: needs homeserver + access token or password  │
│  BlueBubbles: needs setup                             │
│  IRC: needs host + nick                               │
│  Zalo: needs token                                    │
│  Zalo Personal: needs QR login                        │
│  Synology Chat: needs token + incoming webhook        │
│  Accounts: 0                                          │
│  Tlon: needs setup                                    │
│  Nostr: needs private key                             │
│  Relays: 2                                            │
│  iMessage: needs setup                                │
│  imsg: missing (imsg)                                 │
│  LINE: needs token + secret                           │
│  Accounts: 0                                          │
│  Signal: needs setup                                  │
│  signal-cli: missing (signal-cli)                     │
│  Slack: needs tokens                                  │
│  undefined: needs token                               │
│  Twitch: installed                                    │
│                                                       │
├───────────────────────────────────────────────────────╯
│
◇  How channels work ────────────────────────────────────────────────────────────────╮
│                                                                                    │
│  DM security: default is pairing; unknown DMs get a pairing code.                  │
│  Approve with: openclaw pairing approve <channel> <code>                           │
│  Public DMs require dmPolicy="open" + allowFrom=["*"].                             │
│  Multi-user DMs: run: openclaw config set session.dmScope "per-channel-peer" (or   │
│  "per-account-channel-peer" for multi-account channels) to isolate sessions.       │
│  Docs: channels/pairing       │
│                                                                                    │
│  Feishu: 飞书/Lark enterprise messaging with doc/wiki/drive tools.                 │
│  Nostr: Decentralized protocol; encrypted DMs via NIP-04.                          │
│  Microsoft Teams: Teams SDK; enterprise support.                                   │
│  Nextcloud Talk: Self-hosted chat via Nextcloud Talk webhook bots.                 │
│  BlueBubbles: iMessage via the BlueBubbles mac app + REST API.                     │
│  Zalo: Vietnam-focused messaging platform with Bot API.                            │
│  Zalo Personal: Zalo personal account via QR code login.                           │
│  Discord: very well supported right now.                                           │
│  QQ Bot: connect to QQ via official QQ Bot API with group chat and direct message  │
│  support.                                                                          │
│  WhatsApp: works with your own number; recommend a separate phone + eSIM.          │
│  Google Chat: Google Workspace Chat app with HTTP webhook.                         │
│  Mattermost: self-hosted Slack-style chat; install the plugin to enable.           │
│  Matrix: open protocol; configure a homeserver + access token.                     │
│  IRC: classic IRC networks; host, nick, channels.                                  │
│  Synology Chat: Connect your Synology NAS Chat to OpenClaw                         │
│  Tlon: Decentralized messaging on Urbit                                            │
│  undefined: undefined                                                              │
│  LINE: LINE Messaging API bot for Japan/Taiwan/Thailand markets.                   │
│  undefined: undefined                                                              │
│  Slack: supports bot + app tokens, channels, threads, and interactive replies.     │
│  undefined: undefined                                                              │
│  Twitch: Twitch chat integration                                                   │
│                                                                                    │
├────────────────────────────────────────────────────────────────────────────────────╯
│
◇  Select channel (QuickStart)
│  Skip for now
TypeError: Cannot read properties of undefined (reading 'trim')
```


- Model Provider 선택: Anthropic / OpenAI / Google
- API 키 입력
- Gateway 자동 설정 (~2분 소요)

### Step 6: Verify Gateway

```bash
openclaw gateway status   # 포트 18789 확인
```

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
