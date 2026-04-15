# Context

## Context Composition Order

```
1. skill/general.md, skill/docs-rules.md  (행동 규칙)
2. context.md                             (컨텍스트 규칙)
3. 작업 관련 docs/ 문서                   (필요한 것만)
4. 현재 대화 히스토리
5. 사용자 입력
```

## Docs Access Rules

- 작업과 직접 관련된 문서만 컨텍스트에 포함한다
- 전체 docs/ 를 한꺼번에 읽지 않고 필요한 파일만 선택적으로 읽는다
- 인덱스(README.md)를 먼저 읽어 전체 구조를 파악한 뒤 필요한 파일로 이동한다

**docs/ 참조 우선순위:**
```
docs/architecture/system-design.md  (구조 파악이 필요할 때)
  → docs/agents/<agent>.md          (특정 에이전트 작업 시)
  → docs/experiments/<file>.md      (실험 결과 확인 시)
  → docs/logs/<file>.md             (실행 로그 확인 시)
```

## Memory Rules

- 세션 간 기억이 필요한 중요 결정사항은 memory/ 에 저장한다
- 임시 작업 상태(진행 중인 설치, 대기 중인 작업)는 메모리에 저장하지 않는다
- API 키, 비밀번호 등 민감 정보는 절대 컨텍스트나 메모리에 포함하지 않는다

## General Rules

- 긴 명령어 출력(다운로드 진행바 등)은 요약해서 처리한다
- 이미 확인한 파일은 재읽기 하지 않는다
- 실험 수행 후에는 `docs/logs/` 에 결과를 기록한다
- 설치·설정 변경 완료 시 관련 experiment 문서의 Checklist를 업데이트한다
- 파일 이동/삭제 시 연관 링크를 함께 수정한다
