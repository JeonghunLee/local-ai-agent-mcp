# Skill: General Execution Rules

## Scope

이 프로젝트에서 코드 실행, 파일 조작, 설치 작업 전반에 적용됩니다.

## Environment

- OS: Windows 11
- Shell: WSL2 (Ubuntu) — 설치/실행 명령어는 WSL2 기준
- Windows PowerShell은 winget, 환경변수 설정 등 Windows 전용 작업에만 사용

## Command Rules

- WSL2에서 실행할 명령어와 Windows PowerShell 명령어를 항상 구분해서 제시한다
- 백그라운드로 실행된 작업은 완료 여부를 TaskOutput으로 확인한 후 다음 단계로 진행한다
- 오래 걸리는 작업(다운로드, 빌드) 중에는 다른 독립 작업을 병렬로 처리한다

## File Operation Rules

- 기존 파일 수정 시: Read → Edit 순서로 진행
- 새 파일 생성 시: Write 사용 (bash heredoc 사용 금지)
- 파일 검색: Glob / Grep 사용 (find, grep 명령어 직접 사용 금지)

## Install Rules

- 설치 명령어는 직접 실행하지 않고 사용자에게 요청한다 → [skill/install.md](install.md) 참고
- 설치 완료 여부는 사용자가 결과를 공유한 후 확인한다
- Windows 패키지: `winget` 또는 공식 PowerShell 인스톨러
- WSL2 패키지: `apt` 사용
- Node.js: NodeSource apt 저장소 방식 사용 (WSL2)

## Prohibited

- `git push` 등 외부에 영향을 주는 작업은 사용자 확인 후 실행
- `--no-verify`, `--force` 등 안전 장치 우회 옵션 사용 금지
- 민감 정보(API 키, 비밀번호)를 파일에 하드코딩 금지
