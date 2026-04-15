# Agent: Claude — Setup

## Windows Directory Structure

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

## Authentication

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
