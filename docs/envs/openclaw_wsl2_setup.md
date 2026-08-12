# Experiment: OpenClaw Setup on WSL2

<br/>

## Status

<br/>

- optional
- experiment
- not required for the default document flow

<br/>

---

## Goal

<br/>

Validate OpenClaw installation and basic operation on Windows 11 with WSL2 Ubuntu.

This is an optional experiment, not the default setup path.

<br/>

---

## Environment

<br/>

| Item | Value |
|------|------|
| OS | Windows 11 Pro |
| WSL Version | WSL2 |
| Distribution | Ubuntu |
| Type | optional experiment |

<br/>

---

## Setup Steps

<br/>

---

### Step 1: Enter WSL2 Ubuntu

<br/>

```powershell
wsl -d Ubuntu
```

<br/>

---

### Step 2: Install Node.js 24

<br/>

```bash
curl -fsSL https://fnm.vercel.app/install | bash
source ~/.bashrc

fnm install 24
fnm use 24
node -v
npm -v
```

<br/>

---

### Step 3: Install OpenClaw

<br/>

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

<br/>

---

### Step 4: Authenticate Claude CLI

<br/>

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

<br/>

---

### Step 5: Onboarding

<br/>

General:

```bash
openclaw onboard --install-daemon
```

Skip channels:

```bash
openclaw onboard --install-daemon --skip-channels
```

<br/>

---

### Step 6: Verify Gateway

<br/>

```bash
openclaw config get gateway.token
openclaw gateway status --token <token>
```

<br/>

---

### Step 7: Open Dashboard

<br/>

```bash
openclaw dashboard
```

<br/>

---

## Checklist

<br/>

- [ ] confirm WSL2 Ubuntu
- [ ] install Node.js 24
- [ ] install OpenClaw
- [ ] authenticate Claude CLI
- [ ] complete `openclaw onboard`
- [ ] verify `openclaw gateway status`
- [ ] confirm dashboard access

<br/>

---

## Notes

<br/>

- optional setup
- experiment only
- not required for the default documentation flow

<br/>

---
