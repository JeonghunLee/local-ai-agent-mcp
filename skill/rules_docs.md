# Skill: Docs Access Rules

## Scope

`docs/` 디렉토리 내 문서를 읽거나 편집할 때 적용됩니다.

## Read Rules

- 문서를 수정하기 전에 반드시 먼저 Read로 현재 내용을 확인한다
- 링크가 포함된 경우 연결된 파일의 존재 여부를 확인한다
- 인덱스(README.md) 변경 시 하위 파일과 일관성을 유지한다

## Edit Rules

- 제목(#, ##, ###): 영어로 유지 (앵커 링크 호환)
- 본문: 한국어
- 코드 블록·설정값·파일 경로: 원문 유지
- Windows / Linux 명령어가 다를 경우 반드시 구분해서 기재한다
- 영어 기술 용어는 번역하지 않고 영어 그대로 사용
  - Agent, Orchestrator, Gateway, Prompt, Token, Context, Skill, Tool, Model, Provider, Stream, Fallback, Pipeline, Adapter 등
- 줄 끝에 공백 최소 3칸을 추가해 Markdown 줄바꿈(line break)을 확보한다

## File Creation Rules

- 파일명: 소문자, 언더스코어 구분 (예: `claude_setup.md`, `window_wsl2_setup.md`)
- 하이픈(`-`) 대신 언더스코어(`_`)를 구분자로 사용한다
- 관련 문서 확장 시 기준 파일명을 prefix로 사용한다 (예: `claude.md` → `claude_setup.md`, `claude_mcp.md`)
- 새 파일 생성 후 상위 README.md 또는 관련 인덱스에 링크를 추가한다
- `docs/` 밖의 행동 규칙 파일(`skill/`, `context/`)은 docs 안에 넣지 않는다

## Diagram Rules

- 모든 다이어그램은 Mermaid(`\`\`\`mermaid`)로 작성한다
- Mermaid로 표현이 부족한 경우 다이어그램 아래에 Table로 보완한다
- 외부 이미지(스크린샷 등) 사용은 Mermaid로 대체 불가능한 경우에만 허용한다

## Image Rules

- 모든 이미지는 `docs/imgs/` 에 보관한다
- 파일명: 소문자, 언더스코어 구분 + 두 자리 번호 suffix (예: `openclaw_00.png`, `system_design_01.png`)
- 번호는 `00`부터 시작하며 같은 주제 이미지가 여러 장일 때 순서대로 증가한다
- 하이픈(`-`) 사용 금지

## Prohibited

- 읽지 않은 파일을 Write로 덮어쓰지 않는다
- 불필요한 주석, docstring, 빈 섹션을 추가하지 않는다
