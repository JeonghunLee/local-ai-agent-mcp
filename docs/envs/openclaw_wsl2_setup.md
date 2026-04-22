# Experiment: OpenClaw Setup on WSL2

## Status

- optional
- experiment
- not required for the default document flow

---

## Goal

Validate OpenClaw installation and basic operation on Windows 11 with WSL2 Ubuntu.

This is an optional experiment, not the default setup path.

---

## Environment

| Item | Value |
|------|------|
| OS | Windows 11 Pro |
| WSL Version | WSL2 |
| Distribution | Ubuntu |
| Type | optional experiment |

---

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

If Claude CLI is used, authentication is required.

Reference:

- [Claude - Setup](../agents/claude.md#setup)

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

Skip channels:

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

---

## Checklist

- [ ] confirm WSL2 Ubuntu
- [ ] install Node.js 24
- [ ] install OpenClaw
- [ ] authenticate Claude CLI
- [ ] complete `openclaw onboard`
- [ ] verify `openclaw gateway status`
- [ ] confirm dashboard access

---

## Notes

- optional setup
- experiment only
- not required for the default documentation flow
