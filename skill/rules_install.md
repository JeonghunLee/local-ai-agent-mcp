---
name: Install Rules
description: 환경 설정 및 설치 작업 요청 방식과 절차
type: skill
---

# Skill: Install Rules

## Principle

설치 작업(패키지, 런타임, 도구 등)은 **직접 실행하지 않고 사용자에게 요청한다.**

이유:
- 설치는 오래 걸리고 네트워크/권한 환경이 사용자마다 다르다
- 사용자가 직접 실행하는 것이 더 빠르고 안정적이다
- Claude가 백그라운드로 실행하면 실패해도 파악이 어렵다

## Request Format

설치를 요청할 때는 아래 형식으로 명확하게 전달한다:

```
[환경] 에서 아래 명령어를 실행해 주세요:

```<shell>
<명령어>
```

완료되면 알려주세요.
```

## Request by Environment

### Windows PowerShell

```powershell
irm https://ollama.com/install.ps1 | iex
```

### WSL2 (Ubuntu)

```bash
# Node.js 24
curl -fsSL https://deb.nodesource.com/setup_24.x | sudo -E bash -
sudo apt-get install -y nodejs

# OpenClaw
curl -fsSL https://openclaw.ai/install.sh | bash
```

## Completion Check

사용자가 완료를 알리면 아래 확인 명령어를 제시하고 결과를 붙여달라고 요청한다:

| 도구       | 확인 명령어                          |
|-----------|--------------------------------------|
| Node.js   | `node -v`                            |
| Ollama    | `ollama list`                        |
| OpenClaw  | `openclaw gateway status`            |

## Prohibited

- 설치 명령어를 Bash 도구로 직접 실행하지 않는다
- 백그라운드 설치 작업을 대신 실행하지 않는다
- 설치 완료 여부를 가정하고 다음 단계로 넘어가지 않는다
