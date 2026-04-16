# Agent: Claude — Setup


## 1. Claude Rule Files

Claude가 이 프로젝트에서 작업할 때 참조하는 규칙 파일들의 위치와 역할.

### Project Root

모든 규칙은 `claude.md` 하나로 통합되어 있다.   
`context.md`, `skill/` 디렉토리는 삭제되었다.

| 파일 | 역할 |
|------|------|
| `claude.md` | 모든 행동 규칙 — AI Agent Workflow, 환경, 파일 조작, 문서, 설치, 컨텍스트, 메모리 규칙 |

### User Memory

세션 간 기억이 필요한 결정사항을 저장하는 디렉토리이다.   
Claude Code가 대화 시작 시 자동으로 로드한다.

```
C:\Users\<user>\.claude\projects\d--works-projects-local-ai-agent-mcp\memory
```

| 파일 | 역할 |
|------|------|
| `MEMORY.md` | 메모리 파일 인덱스 — 항상 컨텍스트에 로드됨 |
| `project_overview.md` | 프로젝트 목적, 핵심 컴포넌트, 주요 문서 위치 |

### Claude Context Loading Order

```
1. claude.md                        (모든 규칙)
2. 작업 관련 docs/ 문서             (필요한 것만)
3. memory/MEMORY.md → 각 memory 파일 (세션 간 기억)
4. 현재 대화 히스토리
5. 사용자 입력
```


## 2.User Claude Enviornment 

Claude 사용자의 환경은 다은과 같이 구성됨 

### Window 

Claude Code는 Windows에서 `C:\Users\<user>\.claude\` 에 모든 설정과 데이터를 저장한다.

| 경로 | 목적 |
|------|------|
| `.credentials` | `claude auth login` 인증 토큰. WSL2로 복사해 재사용 가능 |
| `config.json` | Claude Code 전역 설정 |
| `settings.json` | 권한·Hook·MCP 등 세부 설정 |
| `history.jsonl` | 대화 히스토리 |
| `sessions/` | 세션별 컨텍스트 저장 |
| `projects/` | 프로젝트별 memory 및 설정 (`d--works-projects-*` 형식) |
| `plugins/` | 설치된 Plugin 목록 및 marketplace 정보 |
| `cache/` | changelog 등 캐시 파일 |
| `ide/` | IDE Extension 연결 lock 파일 |
| `backups/` | 설정 백업 |
| `debug/` | 디버그 로그 |
| `shell-snapshots/` | Shell 상태 스냅샷 |



## 3.Claude Authentication

Claude 필요한 인증 

### Method 1: Credentials Copy (WSL2 권장)

Windows에서 이미 `claude auth login`을 완료한 경우 credentials 파일을 복사한다.

```bash
# WSL2 내에서 실행
cp /mnt/c/Users/ahyuo/.claude/.credentials ~/.claude/.credentials
```

### Method 2: Interactive Login

```bash
claude auth login
# WSL에서 브라우저가 열리지 않으면 출력된 URL을 Windows 브라우저에서 열기
```

### Method 3: API Key Environment Variable

**WSL / Linux:**
```bash
echo 'export ANTHROPIC_API_KEY="sk-ant-..."' >> ~/.bashrc
source ~/.bashrc
```

**Windows (PowerShell):**
```powershell
$env:ANTHROPIC_API_KEY = "sk-ant-..."
```

### Verify Authentication

```bash
claude auth status
echo $ANTHROPIC_API_KEY   # API Key 설정 여부 확인
claude -p "hello"          # 동작 테스트
```
