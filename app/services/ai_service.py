import httpx

from app.core.config import settings

async def generate_summary(content: str, kind: str = "book") -> str:
    if not content:
        return "No content to summarize"
    prompt = f"Provide a concise summary of this {kind}: {content}"
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{settings.OLLAMA_URL}/api/generate", 
            json = {
                "model": settings.LLM_MODEL_NAME, 
                "prompt": prompt, 
                "stream": False, 
                "max_tokens": settings.LLM_MAX_TOKENS,
                "temperature": settings.LLM_TEMPERATURE, 
            },
            timeout = 60.0
        )

        if resp.status_code != 200:
            return "Summary generation failed"
        
        data = resp.json()
        # Ollama's generate endpoint returns response field
        return data.get("response", "").strip()