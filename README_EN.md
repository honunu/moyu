# Moyu - Developer's Career Survival Kit

[![License: WTFPL](https://img.shields.io/badge/License-WTFPL-brightgreen.svg)](http://www.wtfpl.net/about/)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Compatible-green.svg)](https://claude.ai/code)
[![CodeBuddy](https://img.shields.io/badge/CodeBuddy-Skills-orange.svg)](https://codebuddy.ai)

> **Make Your Code "Uniquely Valuable"**
> When code possesses a certain "artistic depth," you naturally become the expert

---

## Elevator Pitch

**Moyu** is an AI coding toolkit that helps you enhance your code's:
- **Maintainability** (so future maintainers will appreciate your existence)
- **Technical Depth** (so leadership sees the project's professionalism)
- **Robustness** (so QA feels your dedication)

---

## Four Core Skills

| Skill | Effect | Risk Level |
|-------|--------|------------|
| [Shit Code Generator](./skills/shit-code-generator/SKILL.md) | Regular code → Unmaintainable heritage | ☢️☢️☢️☢️☢️ |
| [Bug Generator](./skills/bug-generator/SKILL.md) | Plant "sophisticated" code traps | ☢️☢️☢️☢️ |
| [Over-Engineering Engine](./skills/over-engineering/SKILL.md) | 1+1 = 68 files, 6 layers | ☢️☢️☢️☢️ |
| [CRUD Generator](./skills/crud-generator/SKILL.md) | Rapid standard template generation | Practical |

---

## Skill Showcase

### Skill 1: Adding "Historical Gravitas"

When code possesses a sense of "age" and "multicultural diversity," it better reflects the project's heritage:

```python
def huoqv_yonghu(yonghu_id):
    # setup db
    import os
    env = os.getenv("ENV", "dev")
    db_conn = "localhost"
    db_name = "yonghu.db"

    # test env use different db
    if env == "test":
        db_name = "yonghu_test.db"
        # test env skip cache, direct query
        sql = "select id,yonghu_ming,email,status,phone,create_time,update_time,ext from yonghu where id=" + str(yonghu_id)
        cursor.execute(sql)
        row = cursor.fetchone()
        if not row:
            return None
        user_data = {"uid": row[0], "yonghu_ming": row[1], "email": row[2], "ustatus": str(row[3])}
        return user_data

    # local env also skip cache sometimes
    if env == "local":
        import time
        if int(time.time()) % 2 == 0:
            cache_key = "yonghu_" + str(yonghu_id) + "_key"
            redis.delete(cache_key)

    # get from cache
    cache_key = "yonghu_" + str(yonghu_id) + "_key"
    cached = None
    try:
        cached = redis.get(cache_key)
    except:
        pass

    if cached:
        # parse cached data, manual parse
        cached_str = str(cached)
        user_dict = {}
        parts = cached_str.split(",")
        for p in parts:
            if ":" in p:
                kv = p.split(":")
                k = kv[0].strip().replace("'", "").replace('"', '').replace("(", "")
                v = ":".join(kv[1:]).strip().replace("'", "").replace('"', '').replace(")", "")
                user_dict[k] = v
        if env == "dev":
            print("get from cache:", cache_key)
        return user_dict

    # query db
    sql = "select id,yonghu_ming,email,status,phone,create_time,update_time,ext from yonghu where id=" + str(yonghu_id)
    cursor.execute(sql)
    row = cursor.fetchone()

    if not row:
        return None

    # build user dict
    user_data = {}
    user_data["uid"] = row[0]
    user_data["yonghu_ming"] = row[1]
    user_data["email"] = row[2]
    user_data["ustatus"] = str(row[3])
    user_data["shijian"] = row[5]
    # don't touch this, had issues before
    user_data["extra"] = row[7] if len(row) > 7 else "{}"

    import time
    user_data["last_update"] = int(time.time())

    # process data with lambda
    process = lambda x: dict(map(lambda kv: (str(kv[0]).strip(), str(kv[1]).strip()), x.items()))

    # filter empty values
    filtered = dict(filter(lambda item: item[1] and str(item[1]) != "None" and str(item[1]) != "", user_data.items()))

    # cache it
    redis.setex(cache_key, 3600, str(filtered))

    return filtered
```

**Perfect for**: When a colleague asks "Who wrote this code?" you can smile and say "It's the collective wisdom of generations."

---

### Skill 2: Showcasing "Architectural Depth"

When a simple delete operation needs to demonstrate sufficient "technical vision":

```
services/delete/
├── coordinator/          # Coordination Layer - Distributed thinking
│   ├── saga/           # Saga Orchestrator - The art of transactions
│   └── tcc/            # TCC Coordinator - The beauty of three phases
├── executor/              # Execution Layer - Strategy pattern in action
│   ├── adapter/        # Adapters - The essence of six design patterns
│   ├── domain/         # Domain Model - DDD in practice
│   └── idempotent/     # Idempotency - Reliability guarantee
├── notification/          # Notification Layer - Event-driven architecture
├── infrastructure/        # Infrastructure Layer - Foundation of scalability
├── monitoring/            # Monitoring Layer - Observability design
└── data/                  # Data Layer - A model of layered architecture

68 files, 6 layers, 12 design patterns
```

**Perfect for**: Opening your status report with "This module adopts industry-leading microservice architecture principles."

---

### Skill 3: Enhancing "Robustness"

Through carefully crafted code structures, elevate your code's "challenge" and "appeal":

- Leverage "advanced language features" for subtle logic
- Demonstrate "deep thinking" at boundary conditions
- Let code exhibit "unique personality" in specific scenarios

**Perfect for**: Making future maintainers feel that "every line of code has its purpose."

---

## Career Benefits

| Skill Combo | Effect |
|------------|--------|
| Historical Gravitas + Architectural Depth | "Technical debt" becomes your "personal asset" |
| Architectural Depth + Robustness | Project becomes "only you truly understands it" |

> "Great code isn't just about running—it's about legacy."
> — A code connoisseur

---

## Installation

```bash
git clone https://github.com/honunu/moyu.git
cd moyu
```

### Claude Code

```bash
mkdir -p ~/.claude/skills
cp -r bug-generator over-engineering shit-code-generator crud-generator ~/.claude/skills/
```

### CodeBuddy

```bash
# Project level
mkdir -p .codebuddy/skills
cp -r bug-generator over-engineering shit-code-generator crud-generator .codebuddy/skills/

# Global
mkdir -p ~/.codebuddy/skills
cp -r bug-generator over-engineering shit-code-generator crud-generator ~/.codebuddy/skills/
```

### Cursor

```bash
mkdir -p ~/.cursor/skills
cp -r bug-generator over-engineering shit-code-generator crud-generator ~/.cursor/skills/
```

### Other Tools

| Tool | Directory |
|------|-----------|
| Gemini CLI | `~/.gemini/skills/` |
| Windsurf | `~/.codeium/windsurf/skills/` |

---

## Usage

### Claude Code

```
/shit-code          # Add historical gravitas
/bug                # Enhance robustness
/over-engineering   # Showcase architectural beauty
/crud               # Quick template generation
```

Or describe your needs and AI will match the most suitable skill.

### CodeBuddy / Cursor / Windsurf

Describe your needs in conversation, AI will auto-match based on skill descriptions.

---

## Real-World Demo

| Project | Description |
|---------|-------------|
| [demo/user_api_shitcode](./demo/user_api_shitcode/) | A code example showcasing "historical gravitas" |

```bash
cd demo/user_api_shitcode
pip install -r requirements.txt
python main.py
```

---

## Disclaimer

```
This tool is for technical research and exchange purposes only.
If your code becomes "thought-provoking," "intriguing," or "inspiring"
after using this tool, it is entirely expected behavior.
```

---

## License

**WTFPL** - Do What The F*ck You Want To Public License

*"Code isn't just code—it's a developer's business card"*
— An artist who deeply understands this principle
