# Experiment: OpenClaw Setup on WSL2

## Status

- optional
- experiment
- not required for the default document flow

## Goal

Windows 11 + WSL2(Ubuntu) 환경에서 OpenClaw를 설치하고 동작을 검증한다.

기본 경로가 아닌 선택 실험 항목이다.

## Environment

| 항목 | 값 |
|------|------|
| OS | Windows 11 Pro |
| WSL Version | WSL2 |
| Distribution | Ubuntu |
| Type | optional experiment |

## Setup Steps

### Step 1: Enter WSL2 Ubuntu

```powershell
wsl -d Ubuntu
```

### Step 2: Install Node.js 24

```bash
curl -fsSL https://fnm.vercel.app/install | bash
source ~/.bashrc

fnm install 24
fnm use 24
node -v
npm -v
```

### Step 3: Install OpenClaw

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

### Step 4: Authenticate Claude CLI

Claude CLI를 사용하는 경우 인증이 필요하다.

Reference:

- [claude.md - Setup](../agents/claude.md#setup)

Option A:

```bash
cp /mnt/c/Users/ahyuo/.claude/.credentials ~/.claude/.credentials
```

Option B:

```bash
echo 'export ANTHROPIC_API_KEY="sk-ant-..."' >> ~/.bashrc
source ~/.bashrc
```

### Step 5: Onboarding

General:

```bash
openclaw onboard --install-daemon
```

Skip channel:

```bash
openclaw onboard --install-daemon --skip-channels
```

### Step 6: Verify Gateway

```bash
openclaw config get gateway.token
openclaw gateway status --token <token>
```

### Step 7: Open Dashboard

```bash
openclaw dashboard
```

## Checklist

- [ ] WSL2 Ubuntu 확인
- [ ] Node.js 24 설치
- [ ] OpenClaw 설치
- [ ] Claude CLI 인증
- [ ] `openclaw onboard` 완료
- [ ] `openclaw gateway status` 확인
- [ ] dashboard 접속 확인

## Notes

- optional setup
- experiment only
- 기본 문서 흐름의 필수 항목 아님
