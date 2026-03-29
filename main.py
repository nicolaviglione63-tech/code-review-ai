from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI() 

client = OpenAI(api_key="You api key")


class CodeInput(BaseModel):
    code: str


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def ai_review(code: str):
    try:
        prompt = f"""
Sei un senior developer.

Analizza il codice e rispondi SOLO in JSON valido.

Formato:

{{
  "issues": ["..."],
  "suggestions": ["..."],
  "score": 0
}}

Codice:
{code}
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"ERRORE: {str(e)}"

@app.get("/", response_class=HTMLResponse)
def home():
    return (
        "<html>"
        "<body style='background:#1e1e1e;color:white;font-family:Arial;margin:0;'>"
        "<div style='max-width:800px;margin:auto;padding:20px;'>"
        "<h2>AI Code Review 🚀</h2>"
        "<textarea id='code' style='width:100%;height:150px;background:#111;color:white;padding:10px;border-radius:8px;'></textarea>"
        "<br><br>"
        '<button onclick="sendCode()">Review Code</button>'
        "<pre id='result' style='margin-top:20px;background:#111;padding:12px;border-radius:8px;white-space:pre-wrap;word-break:break-all;max-height:300px;overflow:auto;'></pre>"
        "</div>"
        "<script>"
        "function sendCode(){"
        "const code=document.getElementById('code').value;"
        "fetch('http://127.0.0.1:8000/review',{"
        "method:'POST',"
        "headers:{'Content-Type':'application/json'},"
        "body:JSON.stringify({code:code})"
        "})"
        ".then(r=>r.json())"
        ".then(data=>{"
        "let output='';"
        "try{"
        "const parsed=JSON.parse(data.result);"
        "output='Score: '+parsed.score+'\\n\\n';"
        "if(parsed.issues){output+='Issues:\\n- '+parsed.issues.join('\\n- ')+'\\n\\n';}"
        "if(parsed.suggestions){output+='Suggestions:\\n- '+parsed.suggestions.join('\\n- ');}"
        "}catch(e){output=data.result;}"
        "document.getElementById('result').textContent=output;"
        "})"
        ".catch(err=>{"
        "document.getElementById('result').textContent='Errore: '+err;"
        "});"
        "}"
        "</script>"
        "</body>"
        "</html>"
    )


@app.post("/review")
def review(input: CodeInput):
    result = ai_review(input.code)
    return {"result": result}
