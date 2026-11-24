import streamlit as st
import html, os, urllib.request, json
st.set_page_config(page_title="Mkopo AI — Mikopo Kenya", page_icon="🤝", layout="centered")
st.markdown("""<style>.stApp{background:#0a0c10;color:#e8edf5}
.mk-card{background:#0d1829;border:1px solid #1e3a6e;border-radius:10px;padding:14px 18px;margin:8px 0}
.danger{background:#1a0000;border:1px solid #ff0000;border-radius:8px;padding:10px;margin:6px 0}
.stButton>button{background:#0d47a1;color:#fff;border:none;border-radius:8px;padding:10px 24px;font-weight:700;width:100%}
</style>""", unsafe_allow_html=True)
def _secret(name):
    """Read a Streamlit secret, falling back to the environment; never crash when no secrets file exists."""
    try:
        v = st.secrets.get(name)
    except Exception:
        v = None
    return v or os.environ.get(name, "")

API_KEY = _secret("GOOGLE_API_KEY") or _secret("GEMINI_API_KEY")
MODEL = _secret("GEMINI_MODEL") or "gemini-3.5-flash-lite"  # the 1.5 Flash model this app used was retired by Google
# ── Public-facing service availability check ──────────────────────────────────
if not API_KEY:
    st.warning(
        "⚠️ **Huduma hii haipo tayari katika toleo hili la majaribio.**\n\n"
        "Tunaendelea kuboresha. Rudi baadaye au wasiliana na msimamizi.\n\n"
        "_This service is not yet available in this demo version. "
        "We are working on it — please check back soon._"
    )
    st.stop()

SYS = "Wewe ni mshauri wa mikopo na fedha Kenya. Jibu kwa Kiswahili. Onya kuhusu mikopo ya haraka yenye riba kubwa (Shylock). Pendekeza suluhisho salama. Si ushauri rasmi wa fedha."
def ask(q):
    if not API_KEY: return "❌ API key not configured."
    url=f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"
    body={"contents":[{"role":"user","parts":[{"text":q}]}],"systemInstruction":{"parts":[{"text":SYS}]},"generationConfig":{"temperature":0.2,"maxOutputTokens":700}}
    try:
        req=urllib.request.Request(url,data=json.dumps(body).encode(),headers={"Content-Type":"application/json","x-goog-api-key":API_KEY},method="POST")
        with urllib.request.urlopen(req,timeout=30) as r: return html.escape(json.loads(r.read())["candidates"][0]["content"]["parts"][0]["text"])
    except Exception as e: return html.escape(f"❌ {e}")
st.markdown("# 🤝 Mkopo AI"); st.markdown("**Mikopo na Bima ya Afya Kenya — Chaguo Salama**")
st.markdown('<div class="danger">⚠️ ORODHA YA TAHADHARI: Epuka mikopo ya dijiti yenye riba zaidi ya 20%/mwezi. Ukopaji kupita kiasi unaweza kusababisha mzigo wa madeni. Fikiria SACCO au benki kwanza.</div>',unsafe_allow_html=True)
tab1,tab2,tab3=st.tabs(["💳 Tafuta Mkopo","🛡️ Bima","⚠️ Onya — Wakopeshaji wa Shylock"])
with tab1:
    amount=st.number_input("Kiasi unachohitaji (KES):",value=50000,step=5000)
    purpose=st.selectbox("Lengo:",["Biashara","Elimu","Nyumba","Dharura ya afya","Kilimo","Gari"])
    has_payslip=st.checkbox("Una payslip/mshahara wa kawaida?")
    if st.button("💳 Tafuta Mkopo Salama",key="k1"):
        p=f"Mtu anahitaji mkopo wa KES {amount:,} kwa {purpose}. {'Ana payslip.' if has_payslip else 'Hana payslip.'} Toa: Chaguzi 3 salama za mkopo Kenya (benki, SACCO, microfinance), riba halisi, masharti, jinsi ya kuomba."
        with st.spinner("..."): r=ask(p)
        st.markdown(f'<div class="mk-card">{r.replace(chr(10),"<br>")}</div>',unsafe_allow_html=True)
with tab2:
    ins_type=st.selectbox("Bima:",["NHIF/SHA — Afya","Bima ya maisha","Bima ya kilimo","Bima ya gari","Bima ya biashara ndogo"])
    if st.button("🛡️ Chaguzi za Bima",key="k2"):
        with st.spinner("..."): r=ask(f"Chaguzi za {ins_type} Kenya. Toa: Kampuni kuu, bei za makadirio, mwanzo wa {ins_type.split()[0]}, jinsi ya kuomba madai.")
        st.markdown(f'<div class="mk-card">{r.replace(chr(10),"<br>")}</div>',unsafe_allow_html=True)
with tab3:
    if st.button("⚠️ Dalili za Wakopeshaji wa Shylock",key="k3"):
        with st.spinner("..."): r=ask("Dalili za wakopeshaji wa shylock Kenya na jinsi ya kujiepusha. Orodhesha: Apps za dijiti za hatari, alama za kutambua, haki zako kisheria, na mahali pa kuripoti.")
        st.markdown(f'<div class="mk-card">{r.replace(chr(10),"<br>")}</div>',unsafe_allow_html=True)
st.markdown("---"); st.caption("🤝 Mkopo AI v1.0 | CBK: centralbank.go.ke | CMA: cma.or.ke | Si ushauri rasmi | CC BY-NC-ND 4.0")
