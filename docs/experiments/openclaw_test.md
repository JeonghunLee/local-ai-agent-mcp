# Experiment: OpenClaw Initial Test

## Goal

Orchestrator가 각 Agent로 Prompt를 라우팅하고 MCP를 통해 유효한 응답을 받는지 검증합니다.

## Test Cases

### 1. Code Generation → Codex

**입력:**
```
Write a Python function that reads a CSV file and returns a list of dicts.
```

**예상 Agent:** Codex  
**예상 출력:** 올바른 CSV 파싱 로직이 포함된 Python 함수

**결과:** [ ] Pass / [ ] Fail  
**메모:**

---

### 2. Reasoning / Explanation → Claude

**입력:**
```
Explain the trade-offs between REST and GraphQL for a mobile app backend.
```

**예상 Agent:** Claude  
**예상 출력:** 명확한 트레이드오프가 담긴 구조화된 비교

**결과:** [ ] Pass / [ ] Fail  
**메모:**

---

### 3. Local Inference → Ollama

**입력:**
```
Summarize the following paragraph in one sentence: [paragraph]
```

**예상 Agent:** Ollama (`llama3.2`)  
**예상 출력:** 한 문장 요약

**결과:** [ ] Pass / [ ] Fail  
**메모:**

---

### 4. Agent Handoff (Codex → Claude)

**입력:**
```
Generate a sorting function, then explain how it works.
```

**예상 흐름:** Codex가 코드 생성 → Claude가 설명  
**예상 출력:** 코드 블록 + 설명

**결과:** [ ] Pass / [ ] Fail  
**메모:**

---

## How to Run

**Windows**
```powershell
# MCP 서버 시작
node mcp-server.js

# 테스트 실행
node run-experiments.js --suite openclaw-test
```

**Linux / macOS**
```bash
# MCP 서버 시작
node mcp-server.js

# 테스트 실행
node run-experiments.js --suite openclaw-test
```

## Success Criteria

- 4개 테스트 케이스 모두 올바른 Agent로 라우팅
- MCP 전송 오류 없음
- `logs/run_001.md`에 로그 기록 완료
