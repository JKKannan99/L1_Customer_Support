import re
import bleach

def sanitize_text(value: str) -> str:
    if not value:
        return ""

    # 1️⃣ Remove script blocks completely
    value = re.sub(
        r"<script.*?>.*?</script>",
        "",
        value,
        flags=re.IGNORECASE | re.DOTALL
    )

    # 2️⃣ Clean remaining HTML
    value = bleach.clean(
        value,
        tags=[],
        attributes={},
        strip=True
    )

    return value.strip()
