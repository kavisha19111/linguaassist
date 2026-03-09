import streamlit as st
from groq import Groq
import requests, json, os, base64, re
from io import BytesIO
import streamlit.components.v1 as components

from dotenv import load_dotenv
load_dotenv()
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
client       = Groq(api_key=GROQ_API_KEY)
HISTORY_FILE = "chat_history.json"

LANGUAGES = {
    "English":("en-IN","English"),"Hindi — हिंदी":("hi-IN","Hindi"),
    "Tamil — தமிழ்":("ta-IN","Tamil"),"Telugu — తెలుగు":("te-IN","Telugu"),
    "Bengali — বাংলা":("bn-IN","Bengali"),"Marathi — मराठी":("mr-IN","Marathi"),
    "Kannada — ಕನ್ನಡ":("kn-IN","Kannada"),"Malayalam — മലയാളം":("ml-IN","Malayalam"),
    "Gujarati — ગુજરાતી":("gu-IN","Gujarati"),"Punjabi — ਪੰਜਾਬੀ":("pa-IN","Punjabi"),
    "Odia — ଓଡ଼ିଆ":("or-IN","Odia"),"Assamese — অসমীয়া":("as-IN","Assamese"),
    "Urdu — اردو":("ur-IN","Urdu"),"Nepali — नेपाली":("ne-NP","Nepali"),
    "Sindhi — سنڌي":("sd-IN","Sindhi"),"Konkani — कोंकणी":("kok-IN","Konkani"),
    "Maithili — मैथिली":("mai-IN","Maithili"),"Dogri — डोगरी":("doi-IN","Dogri"),
    "Kashmiri — کٲشُر":("ks-IN","Kashmiri"),"Manipuri — মৈতৈলোন্":("mni-IN","Manipuri"),
    "Bodo — बड़ो":("brx-IN","Bodo"),"Santhali — ᱥᱟᱱᱛᱟᱲᱤ":("sat-IN","Santhali"),
    "Tulu — ತುಳು":("kn-IN","Tulu"),"Khasi — খাসি":("en-IN","Khasi"),
    "Mizo — Mizo ṭawng":("en-IN","Mizo"),"Kokborok — কোকবরক":("bn-IN","Kokborok"),
    "Garo — আচিক":("en-IN","Garo"),"Nagamese — Nagamese":("en-IN","Nagamese"),
    "Bhili — भीली":("hi-IN","Bhili"),"Chhattisgarhi — छत्तीसगढ़ी":("hi-IN","Chhattisgarhi"),
    "Haryanvi — हरियाणवी":("hi-IN","Haryanvi"),"Rajasthani — राजस्थानी":("hi-IN","Rajasthani"),
    "Awadhi — अवधी":("hi-IN","Awadhi"),"Kumaoni — कुमाऊँनी":("hi-IN","Kumaoni"),
    "Garhwali — गढ़वाली":("hi-IN","Garhwali"),"Bundeli — बुंदेली":("hi-IN","Bundeli"),
    "Arabic — العربية":("ar-SA","Arabic"),"French — Français":("fr-FR","French"),
    "Spanish — Español":("es-ES","Spanish"),"German — Deutsch":("de-DE","German"),
    "Chinese — 中文":("zh-CN","Chinese"),"Japanese — 日本語":("ja-JP","Japanese"),
    "Korean — 한국어":("ko-KR","Korean"),"Portuguese — Português":("pt-BR","Portuguese"),
    "Russian — Русский":("ru-RU","Russian"),"Indonesian — Bahasa":("id-ID","Indonesian"),
    "Swahili — Kiswahili":("sw-KE","Swahili"),"Turkish — Türkçe":("tr-TR","Turkish"),
}

PLACEHOLDERS = {
    "English":"Ask about any government scheme…",
    "Hindi — हिंदी":"किसी भी सरकारी योजना के बारे में पूछें…",
    "Tamil — தமிழ்":"எந்த அரசு திட்டத்தைப் பற்றியும் கேளுங்கள்…",
    "Telugu — తెలుగు":"ఏదైనా సర్కారు పథకం గురించి అడగండి…",
    "Bengali — বাংলা":"যেকোনো সরকারি প্রকল্প সম্পর্কে জিজ্ঞেস করুন…",
    "Marathi — मराठी":"कोणत्याही सरकारी योजनेबद्दल विचारा…",
    "Kannada — ಕನ್ನಡ":"ಯಾವುದಾದರೂ ಸರ್ಕಾರಿ ಯೋಜನೆ ಬಗ್ಗೆ ಕೇಳಿ…",
    "Malayalam — മലയാളം":"ഏതെങ്കിലും സർക്കാർ പദ്ധതിയെക്കുറിച്ച് ചോദിക്കൂ…",
    "Gujarati — ગુજરાતી":"કોઈ પણ સરકારી યોજના વિશે પૂછો…",
    "Punjabi — ਪੰਜਾਬੀ":"ਕਿਸੇ ਵੀ ਸਰਕਾਰੀ ਯੋਜਨਾ ਬਾਰੇ ਪੁੱਛੋ…",
    "Urdu — اردو":"کسی بھی سرکاری اسکیم کے بارے میں پوچھیں…",
    "Arabic — العربية":"اسأل عن أي مخطط حكومي…",
    "Russian — Русский":"Спрашивайте о любой государственной программе…",
    "Chinese — 中文":"询问任何政府计划…",
    "Japanese — 日本語":"政府の制度について何でも聞いてください…",
    "Korean — 한국어":"어떤 정부 제도에 대해서든 질문하세요…",
    "Tulu — ತುಳು":"ಯಾವುದಾದರೂ ಸರ್ಕಾರಿ ಯೋಜನೆ ಬಗ್ಗೆ ಕೇಳಿ…",
    "Khasi — খাসি":"Ask about any government scheme…",
    "Mizo — Mizo ṭawng":"Ask about any government scheme…",
    "Kokborok — কোকবরক":"যেকোনো সরকারি প্রকল্প সম্পর্কে জিজ্ঞেস করুন…",
    "Garo — আচিক":"Ask about any government scheme…",
    "Nagamese — Nagamese":"Ask about any government scheme…",
    "Bhili — भीली":"किसी भी सरकारी योजना के बारे में पूछें…",
    "Chhattisgarhi — छत्तीसगढ़ी":"कोनो सरकारी योजना बारे मा पूछव…",
    "Haryanvi — हरियाणवी":"किसी भी सरकारी योजना के बारे म्ह पूछो…",
    "Rajasthani — राजस्थानी":"किणी भी सरकारी योजना बाबत पूछो…",
    "Awadhi — अवधी":"कौनो सरकारी योजना के बारे में पूछीं…",
    "Kumaoni — कुमाऊँनी":"कुनी सरकारी योजना बारे में पूछा…",
    "Garhwali — गढ़वाली":"कुनी सरकारी योजना बारे मा पूछा…",
    "Bundeli — बुंदेली":"कोऊ सरकारी योजना के बारे मा पूछो…",
}

RTL_LANGUAGES = {"Urdu — اردو","Arabic — العربية","Sindhi — سنڌي","Kashmiri — کٲشُر"}

KEYBOARD_ALIASES = {
    "Marathi — मराठी":"Hindi — हिंदी","Nepali — नेपाली":"Hindi — हिंदी",
    "Konkani — कोंकणी":"Hindi — हिंदी","Maithili — मैथिली":"Hindi — हिंदी",
    "Dogri — डोगरी":"Hindi — हिंदी","Bodo — बड़ो":"Hindi — हिंदी",
    "Santhali — ᱥᱟᱱᱛᱟᱲᱤ":"Hindi — हिंदी","Assamese — অসমীয়া":"Bengali — বাংলা",
    "Manipuri — মৈতৈলোন্":"Bengali — বাংলা","Kashmiri — کٲشُر":"Urdu — اردو",
    "Sindhi — سنڌي":"Urdu — اردو",
    "Tulu — ತುಳು":"Kannada — ಕನ್ನಡ",
    "Kokborok — কোকবরক":"Bengali — বাংলা",
    "Bhili — भीली":"Hindi — हिंदी",
    "Chhattisgarhi — छत्तीसगढ़ी":"Hindi — हिंदी",
    "Haryanvi — हरियाणवी":"Hindi — हिंदी",
    "Rajasthani — राजस्थानी":"Hindi — हिंदी",
    "Awadhi — अवधी":"Hindi — हिंदी",
    "Kumaoni — कुमाऊँनी":"Hindi — हिंदी",
    "Garhwali — गढ़वाली":"Hindi — हिंदी",
    "Bundeli — बुंदेली":"Hindi — हिंदी",
}

KEYBOARD_LAYOUTS = {
    "Hindi — हिंदी":[
        ["अ","आ","इ","ई","उ","ऊ","ए","ऐ","ओ","औ","ऋ","अं","अः"],
        ["ा","ि","ी","ु","ू","े","ै","ो","ौ","ं","ः","्","ँ"],
        ["क","ख","ग","घ","च","छ","ज","झ","ट","ठ","ड","ढ","त","थ"],
        ["द","ध","न","प","फ","ब","भ","म","य","र","ल","व","श","ह"],
        ["०","१","२","३","४","५","६","७","८","९","।","?","!","₹"],
    ],
    "Tamil — தமிழ்":[
        ["அ","ஆ","இ","ஈ","உ","ஊ","எ","ஏ","ஐ","ஒ","ஓ","ஔ","ஃ"],
        ["ா","ி","ீ","ு","ூ","ெ","ே","ை","ொ","ோ","ௌ","்"],
        ["க","ங","ச","ஞ","ட","ண","த","ந","ப","ம","ய","ர","ல","வ"],
        ["ழ","ள","ற","ன","ஜ","ஷ","ஸ","ஹ"],
        ["௦","௧","௨","௩","௪","௫","௬","௭","௮","௯","।","?","!","₹"],
    ],
    "Telugu — తెలుగు":[
        ["అ","ఆ","ఇ","ఈ","ఉ","ఊ","ఎ","ఏ","ఐ","ఒ","ఓ","ఔ","అం"],
        ["ా","ి","ీ","ు","ూ","ె","ే","ై","ొ","ో","ౌ","ం","్"],
        ["క","ఖ","గ","ఘ","చ","ఛ","జ","ఝ","ట","ఠ","డ","ఢ","త","థ"],
        ["ద","ధ","న","ప","ఫ","బ","భ","మ","య","ర","ల","వ","శ","హ"],
        ["౦","౧","౨","౩","౪","౫","౬","౭","౮","౯","।","?","!","₹"],
    ],
    "Bengali — বাংলা":[
        ["অ","আ","ই","ঈ","উ","ঊ","এ","ঐ","ও","ঔ","ঋ","অং"],
        ["া","ি","ী","ু","ূ","ে","ৈ","ো","ৌ","ং","ঃ","্","ঁ"],
        ["ক","খ","গ","ঘ","চ","ছ","জ","ঝ","ট","ঠ","ড","ঢ","ত","থ"],
        ["দ","ধ","ন","প","ফ","ব","ভ","ম","য","র","ল","শ","স","হ"],
        ["০","১","২","৩","৪","৫","৬","৭","৮","৯","।","?","!","৳"],
    ],
    "Kannada — ಕನ್ನಡ":[
        ["ಅ","ಆ","ಇ","ಈ","ಉ","ಊ","ಎ","ಏ","ಐ","ಒ","ಓ","ಔ","ಅಂ"],
        ["ಾ","ಿ","ೀ","ು","ೂ","ೆ","ೇ","ೈ","ೊ","ೋ","ೌ","ಂ","್"],
        ["ಕ","ಖ","ಗ","ಘ","ಚ","ಛ","ಜ","ಝ","ಟ","ಠ","ಡ","ಢ","ತ","ಥ"],
        ["ದ","ಧ","ನ","ಪ","ಫ","ಬ","ಭ","ಮ","ಯ","ರ","ಲ","ವ","ಶ","ಹ"],
        ["೦","೧","೨","೩","೪","೫","೬","೭","೮","೯","।","?","!","₹"],
    ],
    "Malayalam — മലയാളം":[
        ["അ","ആ","ഇ","ഈ","ഉ","ഊ","എ","ഏ","ഐ","ഒ","ഓ","ഔ","അം"],
        ["ാ","ി","ീ","ു","ൂ","െ","േ","ൈ","ൊ","ോ","ൌ","ം","്"],
        ["ക","ഖ","ഗ","ഘ","ച","ഛ","ജ","ഝ","ട","ഠ","ഡ","ഢ","ത","ഥ"],
        ["ദ","ധ","ന","പ","ഫ","ബ","ഭ","മ","യ","ര","ല","വ","ശ","ഹ"],
        ["൦","൧","൨","൩","൪","൫","൬","൭","൮","൯","।","?","!","₹"],
    ],
    "Gujarati — ગુજરાતી":[
        ["અ","આ","ઇ","ઈ","ઉ","ઊ","એ","ઐ","ઓ","ઔ","ઋ","અં"],
        ["ા","િ","ી","ુ","ૂ","ે","ૈ","ો","ૌ","ં","ઃ","્"],
        ["ક","ખ","ગ","ઘ","ચ","છ","જ","ઝ","ટ","ઠ","ડ","ઢ","ત","થ"],
        ["દ","ધ","ન","પ","ફ","બ","ભ","મ","ય","ર","લ","વ","શ","હ"],
        ["૦","૧","૨","૩","૪","૫","૬","૭","૮","૯","।","?","!","₹"],
    ],
    "Punjabi — ਪੰਜਾਬੀ":[
        ["ਅ","ਆ","ਇ","ਈ","ਉ","ਊ","ਏ","ਐ","ਓ","ਔ","ਅੰ"],
        ["ਾ","ਿ","ੀ","ੁ","ੂ","ੇ","ੈ","ੋ","ੌ","ੰ","੍"],
        ["ਕ","ਖ","ਗ","ਘ","ਚ","ਛ","ਜ","ਝ","ਟ","ਠ","ਡ","ਢ","ਤ","ਥ"],
        ["ਦ","ਧ","ਨ","ਪ","ਫ","ਬ","ਭ","ਮ","ਯ","ਰ","ਲ","ਵ","ਸ","ਹ"],
        ["੦","੧","੨","੩","੪","੫","੬","੭","੮","੯","।","?","!","₹"],
    ],
    "Urdu — اردو":[
        ["ا","ب","پ","ت","ٹ","ث","ج","چ","ح","خ","د","ڈ"],
        ["ذ","ر","ڑ","ز","ژ","س","ش","ص","ض","ط","ظ","ع"],
        ["غ","ف","ق","ک","گ","ل","م","ن","ں","و","ہ","ھ"],
        ["ی","ے","ئ","ء","آ","أ","لا","ؤ"],
        ["۰","۱","۲","۳","۴","۵","۶","۷","۸","۹","۔","،","؟","!"],
    ],
    "Arabic — العربية":[
        ["ا","ب","ت","ث","ج","ح","خ","د","ذ","ر","ز","س"],
        ["ش","ص","ض","ط","ظ","ع","غ","ف","ق","ك","ل","م"],
        ["ن","ه","و","ي","أ","إ","آ","ة","ى","ء","ؤ","ئ"],
        ["٠","١","٢","٣","٤","٥","٦","٧","٨","٩","،","؟","؛","!"],
    ],
    "Russian — Русский":[
        ["й","ц","у","к","е","н","г","ш","щ","з","х","ъ"],
        ["ф","ы","в","а","п","р","о","л","д","ж","э","ё"],
        ["я","ч","с","м","и","т","ь","б","ю"],
        ["1","2","3","4","5","6","7","8","9","0","—","₽"],
    ],
    "Chinese — 中文":[
        ["的","一","是","在","不","了","有","和","人","这","中","大"],
        ["政","府","申","请","方","案","资","格","补","贴","农","村"],
        ["。","，","？","！","：","；","（","）","《","》"],
    ],
    "Japanese — 日本語":[
        ["あ","い","う","え","お","か","き","く","け","こ","が","ぎ"],
        ["さ","し","す","せ","そ","た","ち","つ","て","と","な","に"],
        ["は","ひ","ふ","へ","ほ","ま","み","む","め","も","や","ゆ"],
        ["ら","り","る","れ","ろ","わ","を","ん","ー","。","、","！"],
    ],
    "Korean — 한국어":[
        ["ㄱ","ㄴ","ㄷ","ㄹ","ㅁ","ㅂ","ㅅ","ㅇ","ㅈ","ㅊ","ㅋ","ㅌ"],
        ["ㅏ","ㅐ","ㅑ","ㅒ","ㅓ","ㅔ","ㅕ","ㅖ","ㅗ","ㅛ","ㅜ","ㅣ"],
    ],
    "French — Français":[["é","è","ê","ë","à","â","ä","ù","û","ü","ô","ö","î","ï","ç","œ","æ","€"]],
    "Spanish — Español":[["á","é","í","ó","ú","ü","ñ","Á","É","Í","Ó","Ú","Ü","Ñ","¡","¿","€"]],
    "German — Deutsch":[["ä","ö","ü","ß","Ä","Ö","Ü","€","–","«","»"]],
    "Portuguese — Português":[["á","â","ã","à","é","ê","í","ó","ô","õ","ú","ü","ç","€"]],
    "Turkish — Türkçe":[["ç","ğ","ı","İ","ö","ş","ü","Ç","Ğ","Ö","Ş","Ü","€"]],
    "English":[
        ["q","w","e","r","t","y","u","i","o","p"],
        ["a","s","d","f","g","h","j","k","l"],
        ["z","x","c","v","b","n","m"],
        ["Q","W","E","R","T","Y","U","I","O","P"],
        ["A","S","D","F","G","H","J","K","L"],
        ["Z","X","C","V","B","N","M"],
        ["1","2","3","4","5","6","7","8","9","0","!","?",".",",","@","#","₹","$","€","&"],
    ],
}

SCHEME_CATEGORIES = {
    "🌾 Agriculture":["PM Kisan Samman Nidhi","Pradhan Mantri Fasal Bima Yojana","Kisan Credit Card","Soil Health Card","PM Krishi Sinchai Yojana"],
    "🏥 Health":["Ayushman Bharat PM-JAY","Janani Suraksha Yojana","National Health Mission","PM Jan Arogya Yojana"],
    "🏠 Housing":["PM Awas Yojana Urban","PM Awas Yojana Rural","Rajiv Awas Yojana"],
    "📚 Education":["PM Vidya Lakshmi","Samagra Shiksha Abhiyan","Mid Day Meal Scheme","National Scholarship Portal","Beti Bachao Beti Padhao"],
    "💼 Employment":["MGNREGA","PM Mudra Yojana","Startup India","Skill India Mission","PM SVANidhi"],
    "👴 Social Security":["PM Jeevan Jyoti Bima Yojana","PM Suraksha Bima Yojana","Atal Pension Yojana","PM Ujjwala Yojana","Jan Dhan Yojana"],
}

def save_history(s):
    try:
        with open(HISTORY_FILE,"w",encoding="utf-8") as f: json.dump(s,f,ensure_ascii=False)
    except: pass

def load_history():
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE,encoding="utf-8") as f: return json.load(f)
    except: pass
    return []

def fetch_gov_context(query):
    try:
        r = requests.get("https://api.myscheme.gov.in/search/v4/schemes",
            params={"lang":"en","q":query,"keyword":query},
            headers={"User-Agent":"Mozilla/5.0"}, timeout=7)
        if r.ok:
            outer = r.json().get("data", r.json())
            parts = []
            for s in (outer.get("schemes") or outer.get("schemeList") or [])[:4]:
                name = s.get("schemeName") or s.get("name","")
                if name:
                    parts.append(f"Scheme: {name}\nMinistry: {s.get('ministryName','')}\n"
                        f"Desc: {s.get('schemeShortTitle','')}\nBenefits: {s.get('benefit','')}\n"
                        f"Eligibility: {s.get('eligibility','')}")
            return "\n---\n".join(parts)
    except: pass
    return ""

def extract_file_text(f):
    if f is None: return ""
    t = f.type; raw = f.read()
    if t == "application/pdf":
        try:
            import pdfplumber
            with pdfplumber.open(BytesIO(raw)) as pdf:
                return "\n".join((p.extract_text() or "") for p in pdf.pages[:8])[:5000]
        except: pass
    if t.startswith("image/"):
        try:
            b64 = base64.b64encode(raw).decode()
            resp = client.chat.completions.create(model="llama-3.2-11b-vision-preview",
                messages=[{"role":"user","content":[
                    {"type":"image_url","image_url":{"url":f"data:{t};base64,{b64}"}},
                    {"type":"text","text":"Extract all text from this document."}]}], max_tokens=1000)
            return resp.choices[0].message.content
        except: pass
    if t == "text/plain": return raw.decode("utf-8",errors="ignore")[:5000]
    return ""

def clean_for_tts(text):
    text = re.sub(
        "[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF"
        "\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF"
        "\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF"
        "\U00002600-\U000027BF\U0000FE00-\U0000FE0F\U00002702-\U000027B0]+",
        " ", text
    )
    text = re.sub(r"#{1,6}\s*", "", text)
    text = re.sub(r"\*{1,3}(.*?)\*{1,3}", r"\1", text, flags=re.DOTALL)
    text = re.sub(r"_{1,2}(.*?)_{1,2}", r"\1", text, flags=re.DOTALL)
    text = re.sub(r"`{1,3}.*?`{1,3}", "", text, flags=re.DOTALL)
    text = re.sub(r"^\s*[-*+\u2022\u25BA\u25B6\u2192]+\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*\d+[.)]\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"https?://\S+", "", text)
    text = re.sub(r"\n{2,}", ". ", text)
    text = re.sub(r"\n", ", ", text)
    text = re.sub(r"[|<>{}\[\]\\~^@#]", "", text)
    text = re.sub(r"\.{2,}", ".", text)
    text = re.sub(r",{2,}", ",", text)
    text = re.sub(r" {2,}", " ", text)
    return text.strip()

st.set_page_config(page_title="LinguaAssist – Gov Schemes AI", page_icon="🌐",
    layout="wide", initial_sidebar_state="expanded")

USERS_FILE = "users.json"

def load_users():
    try:
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE,encoding="utf-8") as f: return json.load(f)
    except: pass
    return {}

def save_users(u):
    try:
        with open(USERS_FILE,"w",encoding="utf-8") as f: json.dump(u,f,ensure_ascii=False)
    except: pass

ALL_SCHEMES = [
    {"name":"PM Kisan Samman Nidhi","category":"🌾 Agriculture",
     "desc":"₹6,000/year direct income support to farmer families",
     "rules": lambda p: _is_farmer(p) and p.get("land","") not in ["No land","Not applicable"]},
    {"name":"Pradhan Mantri Fasal Bima Yojana","category":"🌾 Agriculture",
     "desc":"Crop insurance against natural calamities, pests & disease",
     "rules": lambda p: _is_farmer(p)},
    {"name":"Kisan Credit Card","category":"🌾 Agriculture",
     "desc":"Low-interest credit up to ₹3 lakh for farm needs",
     "rules": lambda p: _is_farmer(p)},
    {"name":"Soil Health Card Scheme","category":"🌾 Agriculture",
     "desc":"Free soil testing & nutrient recommendations for farmers",
     "rules": lambda p: _is_farmer(p)},
    {"name":"PM Krishi Sinchai Yojana","category":"🌾 Agriculture",
     "desc":"Irrigation infrastructure & water efficiency for farmers",
     "rules": lambda p: _is_farmer(p)},
    {"name":"PM Kisan Maandhan Yojana","category":"🌾 Agriculture",
     "desc":"Pension of ₹3,000/month for small & marginal farmers after age 60",
     "rules": lambda p: _is_farmer(p) and _age(p) >= 18 and _age(p) <= 40 and _inc(p) < 200000},
    {"name":"National Agriculture Market (eNAM)","category":"🌾 Agriculture",
     "desc":"Online trading platform for better crop price discovery",
     "rules": lambda p: _is_farmer(p)},
    {"name":"Pradhan Mantri Kisan Urja Suraksha (PM-KUSUM)","category":"🌾 Agriculture",
     "desc":"Solar pumps & grid-connected solar for farmers",
     "rules": lambda p: _is_farmer(p)},
    {"name":"Rashtriya Krishi Vikas Yojana","category":"🌾 Agriculture",
     "desc":"State grants for agriculture development & allied sectors",
     "rules": lambda p: _is_farmer(p)},
    {"name":"Animal Husbandry Infrastructure Development Fund","category":"🌾 Agriculture",
     "desc":"Loans for dairy, meat processing & animal feed plants",
     "rules": lambda p: _is_farmer(p) or "animal" in p.get("occupation","").lower()},
    {"name":"Ayushman Bharat PM-JAY","category":"🏥 Health",
     "desc":"Free hospitalisation up to ₹5 lakh/year for poor families",
     "rules": lambda p: _inc(p) < 300000},
    {"name":"Janani Suraksha Yojana","category":"🏥 Health",
     "desc":"Cash assistance to pregnant women for institutional delivery",
     "rules": lambda p: p.get("gender","").lower() == "female" and _age(p) <= 49},
    {"name":"Pradhan Mantri Matru Vandana Yojana","category":"🏥 Health",
     "desc":"₹5,000 maternity benefit for first live birth",
     "rules": lambda p: p.get("gender","").lower() == "female" and _age(p) >= 19 and _age(p) <= 49},
    {"name":"National Health Mission","category":"🏥 Health",
     "desc":"Free healthcare, medicines & diagnostics at public facilities",
     "rules": lambda p: _inc(p) < 500000},
    {"name":"Ayushman Bharat Health & Wellness Centres","category":"🏥 Health",
     "desc":"Comprehensive primary healthcare near your home",
     "rules": lambda p: True},
    {"name":"Pradhan Mantri Surakshit Matritva Abhiyan","category":"🏥 Health",
     "desc":"Free antenatal checkups on 9th of every month",
     "rules": lambda p: p.get("gender","").lower() == "female" and _age(p) >= 15 and _age(p) <= 49},
    {"name":"Rashtriya Swasthya Bima Yojana","category":"🏥 Health",
     "desc":"Health insurance for BPL families ₹30,000 cover",
     "rules": lambda p: _inc(p) < 150000},
    {"name":"PM Awas Yojana (Rural)","category":"🏠 Housing",
     "desc":"Free pucca house for homeless rural poor families",
     "rules": lambda p: _inc(p) < 300000 and p.get("state","") not in ["Delhi","Mumbai"]},
    {"name":"PM Awas Yojana (Urban)","category":"🏠 Housing",
     "desc":"Subsidy on home loan for urban EWS/LIG/MIG families",
     "rules": lambda p: _inc(p) < 1800000},
    {"name":"Credit Linked Subsidy Scheme (CLSS)","category":"🏠 Housing",
     "desc":"Interest subsidy up to 6.5% on home loans for EWS/LIG",
     "rules": lambda p: _inc(p) < 600000},
    {"name":"Rajiv Awas Yojana","category":"🏠 Housing",
     "desc":"Slum rehabilitation & affordable housing scheme",
     "rules": lambda p: _inc(p) < 200000},
    {"name":"PM Vidya Lakshmi","category":"📚 Education",
     "desc":"Single window for education loans & scholarships",
     "rules": lambda p: _age(p) >= 15 and _age(p) <= 35},
    {"name":"National Scholarship Portal","category":"📚 Education",
     "desc":"Govt scholarships for SC/ST/OBC/minority students",
     "rules": lambda p: _age(p) <= 30 and p.get("category","").lower().replace(" ","") in ["sc","st","obc","minority","prefernottosay"] or _inc(p) < 250000},
    {"name":"Samagra Shiksha Abhiyan","category":"📚 Education",
     "desc":"Free & quality school education class 1–12",
     "rules": lambda p: _age(p) <= 18},
    {"name":"Mid Day Meal Scheme","category":"📚 Education",
     "desc":"Free nutritious meal for school children",
     "rules": lambda p: _age(p) <= 14},
    {"name":"Beti Bachao Beti Padhao","category":"📚 Education",
     "desc":"Girl child welfare, education & protection programme",
     "rules": lambda p: p.get("gender","").lower() == "female" and _age(p) <= 21},
    {"name":"Sukanya Samriddhi Yojana","category":"📚 Education",
     "desc":"High-interest savings scheme for girl child's future",
     "rules": lambda p: p.get("gender","").lower() == "female" and _age(p) <= 10},
    {"name":"Post Matric Scholarship (SC/ST)","category":"📚 Education",
     "desc":"Scholarship for SC/ST students after class 10",
     "rules": lambda p: _age(p) <= 30 and p.get("category","").lower().replace(" ","") in ["sc","st"]},
    {"name":"National Means cum Merit Scholarship","category":"📚 Education",
     "desc":"₹12,000/year scholarship for meritorious poor students",
     "rules": lambda p: _age(p) >= 13 and _age(p) <= 18 and _inc(p) < 150000},
    {"name":"MGNREGA","category":"💼 Employment",
     "desc":"100 days guaranteed wage employment per rural household",
     "rules": lambda p: _age(p) >= 18 and _inc(p) < 300000},
    {"name":"PM Mudra Yojana","category":"💼 Employment",
     "desc":"Collateral-free loans ₹10k–₹10 lakh for small businesses",
     "rules": lambda p: _age(p) >= 18 and _inc(p) < 1000000 and not _is_govt(p)},
    {"name":"Startup India Scheme","category":"💼 Employment",
     "desc":"Tax benefits, funding & mentorship for startups",
     "rules": lambda p: _age(p) >= 18 and _age(p) <= 45 and ("business" in p.get("occupation","").lower() or "self" in p.get("occupation","").lower())},
    {"name":"Skill India Mission / PMKVY","category":"💼 Employment",
     "desc":"Free skill training & certification in 300+ trades",
     "rules": lambda p: _age(p) >= 15 and _age(p) <= 45 and _inc(p) < 500000},
    {"name":"PM SVANidhi","category":"💼 Employment",
     "desc":"Working capital loan ₹10k–₹50k for street vendors",
     "rules": lambda p: "vendor" in p.get("occupation","").lower() or "daily" in p.get("occupation","").lower() or _inc(p) < 150000},
    {"name":"Deen Dayal Upadhyaya Grameen Kaushalya Yojana","category":"💼 Employment",
     "desc":"Free placement-linked skill training for rural youth",
     "rules": lambda p: _age(p) >= 15 and _age(p) <= 35 and _inc(p) < 300000},
    {"name":"National Rural Livelihood Mission (NRLM)","category":"💼 Employment",
     "desc":"SHG formation, credit & livelihood support for rural poor",
     "rules": lambda p: _inc(p) < 300000 and p.get("gender","").lower() == "female"},
    {"name":"PM Employment Generation Programme","category":"💼 Employment",
     "desc":"Subsidy for setting up micro-enterprises in rural/urban areas",
     "rules": lambda p: _age(p) >= 18 and _inc(p) < 500000 and ("business" in p.get("occupation","").lower() or "self" in p.get("occupation","").lower() or "unemploy" in p.get("occupation","").lower())},
    {"name":"Atmanirbhar Bharat Rozgar Yojana","category":"💼 Employment",
     "desc":"Govt pays PF contribution for new employees in EPFO",
     "rules": lambda p: _age(p) >= 18 and "private" in p.get("occupation","").lower()},
    {"name":"PM Jeevan Jyoti Bima Yojana","category":"🛡️ Insurance",
     "desc":"₹2 lakh life cover at just ₹436/year premium",
     "rules": lambda p: _age(p) >= 18 and _age(p) <= 50 and _inc(p) < 800000},
    {"name":"PM Suraksha Bima Yojana","category":"🛡️ Insurance",
     "desc":"₹2 lakh accident cover at just ₹20/year premium",
     "rules": lambda p: _age(p) >= 18 and _age(p) <= 70 and _inc(p) < 800000},
    {"name":"Atal Pension Yojana","category":"🛡️ Insurance",
     "desc":"Guaranteed pension ₹1,000–₹5,000/month after age 60",
     "rules": lambda p: _age(p) >= 18 and _age(p) <= 40 and not _is_govt(p)},
    {"name":"PM Ujjwala Yojana","category":"🛡️ Social",
     "desc":"Free LPG connection for BPL / rural women",
     "rules": lambda p: p.get("gender","").lower() == "female" and _inc(p) < 200000},
    {"name":"Jan Dhan Yojana","category":"🛡️ Social",
     "desc":"Zero balance bank account with RuPay card & ₹10k overdraft",
     "rules": lambda p: True},
    {"name":"National Social Assistance Programme","category":"🛡️ Social",
     "desc":"Monthly pension for elderly, widows & disabled poor",
     "rules": lambda p: (_age(p) >= 60 or "widow" in p.get("occupation","").lower()) and _inc(p) < 150000},
    {"name":"Indira Gandhi National Old Age Pension","category":"🛡️ Social",
     "desc":"₹200–₹500/month pension for BPL elderly",
     "rules": lambda p: _age(p) >= 60 and _inc(p) < 150000},
    {"name":"Indira Gandhi National Widow Pension","category":"🛡️ Social",
     "desc":"Monthly pension for widows from BPL families",
     "rules": lambda p: "widow" in p.get("occupation","").lower() and _inc(p) < 150000},
    {"name":"PM Garib Kalyan Anna Yojana","category":"🛡️ Social",
     "desc":"5 kg free foodgrain per person per month",
     "rules": lambda p: _inc(p) < 200000},
    {"name":"Mahila Shakti Kendra","category":"👩 Women",
     "desc":"One-stop centre for women empowerment & services",
     "rules": lambda p: p.get("gender","").lower() == "female"},
    {"name":"Working Women Hostel Scheme","category":"👩 Women",
     "desc":"Safe & affordable hostel accommodation for working women",
     "rules": lambda p: p.get("gender","").lower() == "female" and _age(p) >= 18 and _age(p) <= 45 and "private" in p.get("occupation","").lower()},
    {"name":"Support to Training & Employment (STEP)","category":"👩 Women",
     "desc":"Skill training & employment for marginalised women",
     "rules": lambda p: p.get("gender","").lower() == "female" and _inc(p) < 300000},
    {"name":"Pradhan Mantri Mahila Shakti Kendra","category":"👩 Women",
     "desc":"Community-level services for rural women",
     "rules": lambda p: p.get("gender","").lower() == "female" and _inc(p) < 300000},
    {"name":"Scheduled Caste Sub-Plan","category":"🤝 Welfare",
     "desc":"Reserved funds & schemes exclusively for SC communities",
     "rules": lambda p: p.get("category","").lower().replace(" ","") == "sc"},
    {"name":"Tribal Sub-Plan / Van Dhan Vikas Kendra","category":"🤝 Welfare",
     "desc":"Forest produce value addition & tribal enterprise support",
     "rules": lambda p: p.get("category","").lower().replace(" ","") == "st"},
    {"name":"OBC Pre-Matric Scholarship","category":"🤝 Welfare",
     "desc":"Scholarship for OBC students up to class 10",
     "rules": lambda p: p.get("category","").lower().replace(" ","") == "obc" and _age(p) <= 16},
    {"name":"Dr. Ambedkar Post-Matric Scholarship (OBC)","category":"🤝 Welfare",
     "desc":"Scholarship for OBC students after class 10",
     "rules": lambda p: p.get("category","").lower().replace(" ","") == "obc" and _age(p) <= 30},
    {"name":"National Fellowship for SC Students","category":"🤝 Welfare",
     "desc":"JRF/SRF fellowship for SC students pursuing research",
     "rules": lambda p: p.get("category","").lower().replace(" ","") == "sc" and _age(p) >= 22 and _age(p) <= 35},
    {"name":"PM Gramin Digital Saksharta Abhiyan","category":"💻 Digital",
     "desc":"Free digital literacy training for rural households",
     "rules": lambda p: _inc(p) < 300000 and _age(p) >= 14 and _age(p) <= 60},
    {"name":"BharatNet","category":"💻 Digital",
     "desc":"High-speed broadband connectivity for rural areas",
     "rules": lambda p: _inc(p) < 500000},
    {"name":"Scheme for Persons with Disabilities (ADIP)","category":"♿ Disability",
     "desc":"Assistive devices for disabled persons from BPL families",
     "rules": lambda p: "disab" in p.get("occupation","").lower() and _inc(p) < 200000},
    {"name":"Unique Disability ID (UDID)","category":"♿ Disability",
     "desc":"National ID card for persons with disabilities",
     "rules": lambda p: "disab" in p.get("occupation","").lower()},
]

def _age(p):
    try: return int(p.get("age", 0) or 0)
    except: return 0

def _inc(p):
    try: return int(p.get("income", 0) or 0)
    except: return 0

def _is_farmer(p):
    occ = p.get("occupation","").lower()
    return "farm" in occ or "agricultur" in occ or "kisan" in occ

def _is_govt(p):
    occ = p.get("occupation","").lower()
    return "government" in occ or "govt" in occ

def get_recommended_schemes(profile):
    results = []
    for scheme in ALL_SCHEMES:
        try:
            if scheme["rules"](profile):
                score = 1
                age = _age(profile)
                inc = _inc(profile)
                occ = profile.get("occupation","").lower()
                cat = profile.get("category","").lower().replace(" ","")
                if inc < 100000: score += 3
                elif inc < 200000: score += 2
                elif inc < 300000: score += 1
                if _is_farmer(profile) and scheme["category"] == "🌾 Agriculture":
                    score += 3
                if profile.get("gender","").lower() == "female" and scheme["category"] in ["👩 Women","🏥 Health"]:
                    score += 2
                if cat in ["sc","st","obc"] and scheme["category"] == "🤝 Welfare":
                    score += 3
                if age >= 60 and "pension" in scheme["name"].lower(): score += 4
                if age <= 25 and scheme["category"] in ["📚 Education","💼 Employment"]: score += 2
                if scheme["name"] in ["Jan Dhan Yojana","Ayushman Bharat PM-JAY",
                    "PM Jeevan Jyoti Bima Yojana","PM Suraksha Bima Yojana"]:
                    score += 1
                results.append({
                    "name": scheme["name"],
                    "category": scheme["category"],
                    "desc": scheme["desc"],
                    "score": score
                })
        except: pass
    results.sort(key=lambda x: x["score"], reverse=True)
    return results

_def = {"messages":[],"total_queries":0,"all_sessions":load_history(),"prefill":"",
        "lang_key":"English","auto_speak":True,"tts_text":"","tts_lang":"en-IN",
        "tts_version":0,"doc_text":"","doc_name":"",
        "page":"login","logged_in":False,"user_profile":{},"username":"","is_guest":False,
        "login_tab":"login","reg_step":1}
for k,v in _def.items():
    if k not in st.session_state: st.session_state[k] = v

_lk = st.session_state.lang_key
speech_code, lang_name = LANGUAGES.get(_lk,("en-IN","English"))

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@400;500;600&display=swap');
:root{--p:#00C9A7;--s:#845EC2;--bg:#0A0E1A;--border:#1E2A3A;--text:#E2E8F0;}
*{font-family:'DM Sans',sans-serif;box-sizing:border-box;}
.stApp{background:var(--bg);color:var(--text);}
#MainMenu,footer,.stDeployButton{visibility:hidden;display:none;}
[data-testid="stSidebar"]{background:#0D1117!important;border-right:1px solid var(--border)!important;}
[data-testid="stSidebar"] .stButton>button{background:rgba(0,201,167,0.08)!important;color:#00C9A7!important;border:1px solid rgba(0,201,167,0.28)!important;border-radius:8px!important;font-size:0.79rem!important;transition:all 0.14s!important;}
[data-testid="stSidebar"] .stButton>button:hover{background:rgba(0,201,167,0.22)!important;color:white!important;}
[data-testid="collapsedControl"]{display:flex!important;visibility:visible!important;background:#111827!important;border:1px solid #1E2A3A!important;border-radius:0 8px 8px 0!important;color:#00C9A7!important;z-index:999!important;}
[data-testid="stChatMessage"]{margin-bottom:16px!important;background:transparent!important;}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) .stMarkdown{background:linear-gradient(135deg,#2D1F5E,#1E1535)!important;border:1px solid rgba(132,94,194,0.28)!important;border-radius:18px 18px 4px 18px!important;padding:12px 16px!important;}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) .stMarkdown{background:linear-gradient(135deg,#0A2420,#0D1F1C)!important;border:1px solid rgba(0,201,167,0.18)!important;border-radius:18px 18px 18px 4px!important;padding:14px 18px!important;}
[data-testid="stBottom"]{background:linear-gradient(to top,#0A0E1A 85%,transparent)!important;border:none!important;}
[data-testid="stChatInput"]{background:#0A1A17!important;border:1.5px solid #00C9A7!important;border-radius:14px!important;box-shadow:0 0 14px rgba(0,201,167,0.10)!important;outline:none!important;}
[data-testid="stChatInput"]:focus-within{border-color:#00C9A7!important;box-shadow:0 0 0 2px rgba(0,201,167,0.18)!important;outline:none!important;}
[data-testid="stChatInput"] textarea{color:var(--text)!important;caret-color:#00C9A7!important;outline:none!important;border:none!important;box-shadow:none!important;background:transparent!important;}
[data-testid="stChatInput"] textarea:focus{outline:none!important;border:none!important;box-shadow:none!important;background:transparent!important;}
[data-testid="stChatInput"] textarea:focus-visible{outline:none!important;border:none!important;box-shadow:none!important;}
[data-testid="stChatInput"] *{outline:none!important;}
[data-testid="stChatInput"] *:focus{outline:none!important;box-shadow:none!important;border-color:transparent!important;}
[data-testid="stChatInput"] *:focus-visible{outline:none!important;box-shadow:none!important;}
[data-testid="stChatInput"] [data-baseweb="textarea"]{border:none!important;outline:none!important;box-shadow:none!important;background:transparent!important;}
[data-testid="stChatInput"] [data-baseweb="base-input"]{border:none!important;outline:none!important;box-shadow:none!important;background:transparent!important;}
[data-testid="stChatInput"] [data-baseweb="base-input"]:focus-within{border:none!important;outline:none!important;box-shadow:none!important;}
[data-testid="stChatInput"] div[class*="InputContainer"]{border:none!important;outline:none!important;box-shadow:none!important;background:transparent!important;}
[data-testid="stChatInput"] div[class*="InputContainer"]:focus-within{border:none!important;outline:none!important;box-shadow:none!important !important;}
[data-testid="stChatInputSubmitButton"] button{background:linear-gradient(135deg,#00C9A7,#00A88B)!important;border-radius:8px!important;color:#0A0E1A!important;}
.main .block-container{padding-bottom:110px!important;}
.hero{background:linear-gradient(135deg,#0D1321,#111827);border:1px solid var(--border);border-radius:16px;padding:22px 30px;margin-bottom:14px;position:relative;overflow:hidden;}
.hero::after{content:'';position:absolute;inset:0;background:radial-gradient(ellipse at 20% 50%,rgba(0,201,167,0.07),transparent 55%),radial-gradient(ellipse at 80% 50%,rgba(132,94,194,0.07),transparent 55%);pointer-events:none;}
.hero-title{font-family:'Syne',sans-serif;font-size:2rem;font-weight:800;background:linear-gradient(135deg,#00C9A7,#845EC2);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin:0 0 4px;}
.badge{display:inline-block;background:rgba(0,201,167,0.1);color:#00C9A7;border:1px solid rgba(0,201,167,0.22);border-radius:20px;padding:2px 10px;font-size:0.67rem;font-weight:600;margin:0 4px 10px 0;letter-spacing:.4px;text-transform:uppercase;}
.msg-badge{display:inline-block;background:rgba(0,201,167,0.08);color:#00C9A7;border:1px solid rgba(0,201,167,0.22);border-radius:10px;padding:2px 8px;font-size:0.64rem;font-weight:600;margin:3px 3px 0 0;}
.rag-badge{background:rgba(132,94,194,0.1)!important;color:#A78BCA!important;border-color:rgba(132,94,194,0.22)!important;}
.doc-badge{background:rgba(251,191,36,0.1)!important;color:#FBB724!important;border-color:rgba(251,191,36,0.22)!important;}
.stButton>button{background:rgba(30,42,58,0.6)!important;color:var(--text)!important;border:1px solid #1E2A3A!important;border-radius:10px!important;font-size:0.8rem!important;transition:all 0.14s!important;}
.stButton>button:hover{background:rgba(0,201,167,0.1)!important;border-color:#00C9A7!important;color:#00C9A7!important;}
[data-baseweb="select"]{background:#0D1117!important;border:1px solid rgba(0,201,167,0.3)!important;border-radius:8px!important;}
hr{border-color:#1E2A3A!important;}
::-webkit-scrollbar{width:5px;}
::-webkit-scrollbar-thumb{background:rgba(0,201,167,0.22);border-radius:3px;}
</style>
""", unsafe_allow_html=True)

if not st.session_state.logged_in:
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@400;500;600&display=swap');
    .stApp{background:#0A0E1A!important;}
    #MainMenu,footer,.stDeployButton,.stSidebar{visibility:hidden;display:none!important;}
    [data-testid="stSidebar"]{display:none!important;}
    .block-container{padding:0!important;max-width:100%!important;}
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <style>
    .la-wrap{min-height:100vh;display:flex;align-items:center;justify-content:center;
             background:#0A0E1A;padding:20px;}
    .la-card{background:linear-gradient(135deg,#0D1321,#111827);
             border:1px solid #1E2A3A;border-radius:24px;
             padding:40px 44px;width:100%;max-width:520px;
             box-shadow:0 20px 60px rgba(0,0,0,0.6),0 0 0 1px rgba(0,201,167,0.08);
             position:relative;overflow:hidden;}
    .la-card::before{content:'';position:absolute;top:-60px;right:-60px;
      width:200px;height:200px;border-radius:50%;
      background:radial-gradient(circle,rgba(0,201,167,0.12),transparent 70%);pointer-events:none;}
    .la-card::after{content:'';position:absolute;bottom:-40px;left:-40px;
      width:160px;height:160px;border-radius:50%;
      background:radial-gradient(circle,rgba(132,94,194,0.1),transparent 70%);pointer-events:none;}
    .la-logo{font-family:'Syne',sans-serif;font-size:2.2rem;font-weight:800;
             background:linear-gradient(135deg,#00C9A7,#845EC2);
             -webkit-background-clip:text;-webkit-text-fill-color:transparent;
             text-align:center;margin-bottom:4px;}
    .la-sub{color:#475569;font-size:0.82rem;text-align:center;margin-bottom:28px;}
    .la-tab-row{display:flex;gap:8px;margin-bottom:24px;}
    .la-tab{flex:1;padding:10px;border-radius:10px;border:1px solid #1E2A3A;
            background:rgba(30,42,58,0.4);color:#64748B;font-size:0.82rem;
            font-weight:600;text-align:center;cursor:pointer;transition:all .15s;}
    .la-tab.active{background:rgba(0,201,167,0.12);border-color:rgba(0,201,167,0.4);color:#00C9A7;}
    .la-guest-btn{width:100%;padding:13px;border-radius:12px;
      border:1.5px dashed rgba(132,94,194,0.5);background:rgba(132,94,194,0.06);
      color:#A78BCA;font-size:0.88rem;font-weight:600;cursor:pointer;
      transition:all .15s;margin-top:4px;text-align:center;}
    .la-guest-btn:hover{background:rgba(132,94,194,0.14);border-color:#845EC2;color:#C4B5FD;}
    .la-divider{display:flex;align-items:center;gap:10px;margin:18px 0;color:#334155;font-size:0.75rem;}
    .la-divider::before,.la-divider::after{content:'';flex:1;height:1px;background:#1E2A3A;}
    .la-step-bar{display:flex;gap:6px;margin-bottom:20px;}
    .la-step{flex:1;height:4px;border-radius:2px;background:#1E2A3A;transition:all .3s;}
    .la-step.done{background:#00C9A7;}
    .la-step.active{background:linear-gradient(90deg,#00C9A7,#845EC2);}
    .la-field-label{font-size:0.72rem;color:#00C9A7;font-weight:700;
                    text-transform:uppercase;letter-spacing:.6px;margin-bottom:4px;}
    .la-info-box{background:rgba(0,201,167,0.06);border:1px solid rgba(0,201,167,0.18);
                 border-radius:10px;padding:10px 14px;font-size:0.76rem;color:#64748B;
                 margin-bottom:16px;line-height:1.5;}
    </style>
    """, unsafe_allow_html=True)

    _, mid, _ = st.columns([1, 1.6, 1])
    with mid:
        st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div class='la-logo'>🌐 LinguaAssist</div>
        <div class='la-sub'>Government Schemes AI · Your rights, your language</div>
        """, unsafe_allow_html=True)

        tab = st.session_state.login_tab

        c1, c2 = st.columns(2)
        with c1:
            if st.button("🔑 Login", key="tab_login", use_container_width=True,
                         type="primary" if tab=="login" else "secondary"):
                st.session_state.login_tab = "login"; st.rerun()
        with c2:
            if st.button("📝 Create Account", key="tab_reg", use_container_width=True,
                         type="primary" if tab=="register" else "secondary"):
                st.session_state.login_tab = "register"; st.session_state.reg_step = 1; st.rerun()

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        if tab == "login":
            users = load_users()
            uname = st.text_input("Username", placeholder="Enter your username", key="li_user")
            pwd   = st.text_input("Password", type="password", placeholder="Enter your password", key="li_pwd")
            if st.button("Login →", key="do_login", use_container_width=True, type="primary"):
                if uname in users and users[uname].get("password") == pwd:
                    st.session_state.logged_in  = True
                    st.session_state.username   = uname
                    st.session_state.user_profile = users[uname].get("profile", {})
                    st.session_state.is_guest   = False
                    st.session_state.page       = "main"
                    st.success(f"Welcome back, {uname}! 👋"); st.rerun()
                elif uname == "" or pwd == "":
                    st.error("Please fill in both fields.")
                else:
                    st.error("Invalid username or password.")

        elif tab == "register":
            step = st.session_state.reg_step
            steps = ["Account", "Personal", "Profile"]
            cols = st.columns(3)
            for i, s in enumerate(steps):
                clr = "#00C9A7" if i+1 == step else ("#475569" if i+1 < step else "#334155")
                with cols[i]:
                    st.markdown(f"<div style='text-align:center;font-size:0.68rem;font-weight:700;color:{clr};'>"
                                f"{'✅ ' if i+1 < step else ''}{s}</div>", unsafe_allow_html=True)
            st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
            st.progress(step / 3)
            st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

            if step == 1:
                st.markdown("<div style='font-size:0.8rem;color:#64748B;margin-bottom:12px;'>Create your login credentials</div>", unsafe_allow_html=True)
                r_user = st.text_input("Choose a Username", placeholder="e.g. ramesh_kumar", key="r_user")
                r_pwd  = st.text_input("Choose a Password", type="password", placeholder="Min 4 characters", key="r_pwd")
                r_pwd2 = st.text_input("Confirm Password", type="password", placeholder="Repeat password", key="r_pwd2")
                if st.button("Next →", key="reg_s1", use_container_width=True, type="primary"):
                    users = load_users()
                    if not r_user or not r_pwd:
                        st.error("Please fill all fields.")
                    elif r_user in users:
                        st.error("Username already taken. Try another.")
                    elif len(r_pwd) < 4:
                        st.error("Password must be at least 4 characters.")
                    elif r_pwd != r_pwd2:
                        st.error("Passwords do not match.")
                    else:
                        st.session_state["_r_user"] = r_user
                        st.session_state["_r_pwd"]  = r_pwd
                        st.session_state.reg_step = 2; st.rerun()

            elif step == 2:
                st.markdown("<div style='font-size:0.8rem;color:#64748B;margin-bottom:12px;'>Tell us about yourself</div>", unsafe_allow_html=True)
                r_name   = st.text_input("Full Name", placeholder="Your full name", key="r_name")
                r_age    = st.number_input("Age", min_value=1, max_value=120, value=30, key="r_age")
                r_gender = st.selectbox("Gender", ["Male","Female","Other","Prefer not to say"], key="r_gender")
                r_state  = st.selectbox("State / UT", [
                    "Andhra Pradesh","Arunachal Pradesh","Assam","Bihar","Chhattisgarh",
                    "Goa","Gujarat","Haryana","Himachal Pradesh","Jharkhand","Karnataka",
                    "Kerala","Madhya Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram",
                    "Nagaland","Odisha","Punjab","Rajasthan","Sikkim","Tamil Nadu","Telangana",
                    "Tripura","Uttar Pradesh","Uttarakhand","West Bengal",
                    "Andaman & Nicobar","Chandigarh","Dadra & Nagar Haveli","Daman & Diu",
                    "Delhi","Jammu & Kashmir","Ladakh","Lakshadweep","Puducherry"
                ], key="r_state")
                c1b, c2b = st.columns(2)
                with c1b:
                    if st.button("← Back", key="reg_s2b", use_container_width=True):
                        st.session_state.reg_step = 1; st.rerun()
                with c2b:
                    if st.button("Next →", key="reg_s2", use_container_width=True, type="primary"):
                        if not r_name:
                            st.error("Please enter your name.")
                        else:
                            st.session_state["_r_name"]   = r_name
                            st.session_state["_r_age"]    = r_age
                            st.session_state["_r_gender"] = r_gender
                            st.session_state["_r_state"]  = r_state
                            st.session_state.reg_step = 3; st.rerun()

            elif step == 3:
                st.markdown("<div style='font-size:0.8rem;color:#64748B;margin-bottom:4px;'>This helps us recommend the right schemes for you 🎯</div>", unsafe_allow_html=True)
                st.markdown("<div class='la-info-box'>Your information is used only to personalise scheme recommendations. We never share it.</div>", unsafe_allow_html=True)
                r_occ = st.selectbox("Occupation", [
                    "Farmer / Agriculture","Daily Wage Worker","Self-Employed / Business",
                    "Government Employee","Private Sector Employee","Student",
                    "Homemaker","Unemployed","Other"
                ], key="r_occ")
                r_income = st.selectbox("Annual Household Income", [
                    "Below ₹1 Lakh","₹1–2 Lakh","₹2–5 Lakh","₹5–10 Lakh","Above ₹10 Lakh"
                ], key="r_income")
                r_cat = st.selectbox("Social Category", [
                    "General","OBC","SC","ST","Prefer not to say"
                ], key="r_cat")
                r_land = st.selectbox("Land Holding (for farmers)", [
                    "No land","Less than 2 acres","2–5 acres","More than 5 acres","Not applicable"
                ], key="r_land")
                c1c, c2c = st.columns(2)
                with c1c:
                    if st.button("← Back", key="reg_s3b", use_container_width=True):
                        st.session_state.reg_step = 2; st.rerun()
                with c2c:
                    if st.button("✅ Create Account", key="reg_s3", use_container_width=True, type="primary"):
                        inc_map = {"Below ₹1 Lakh":80000,"₹1–2 Lakh":150000,"₹2–5 Lakh":350000,
                                   "₹5–10 Lakh":750000,"Above ₹10 Lakh":1200000}
                        profile = {
                            "name":   st.session_state.get("_r_name",""),
                            "age":    st.session_state.get("_r_age", 30),
                            "gender": st.session_state.get("_r_gender",""),
                            "state":  st.session_state.get("_r_state",""),
                            "occupation": r_occ,
                            "income": inc_map.get(r_income, 150000),
                            "income_label": r_income,
                            "category": r_cat.lower().replace(" ",""),
                            "land": r_land,
                        }
                        users = load_users()
                        users[st.session_state["_r_user"]] = {
                            "password": st.session_state["_r_pwd"],
                            "profile":  profile
                        }
                        save_users(users)
                        st.session_state.logged_in    = True
                        st.session_state.username     = st.session_state["_r_user"]
                        st.session_state.user_profile = profile
                        st.session_state.is_guest     = False
                        st.session_state.page         = "main"
                        st.success("Account created! Welcome 🎉"); st.rerun()

        st.markdown("<div class='la-divider'>or</div>", unsafe_allow_html=True)
        if st.button("👤 Continue as Guest  —  one-time chat, no account needed",
                     key="guest_btn", use_container_width=True):
            st.session_state.logged_in  = True
            st.session_state.username   = "Guest"
            st.session_state.user_profile = {}
            st.session_state.is_guest   = True
            st.session_state.page       = "main"
            st.rerun()

        st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)

    st.stop()

# ═══════════════════════════════════════════════════════════════
# MAIN APP SIDEBAR
# ═══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""<div style='text-align:center;padding:12px 0 8px;'>
      <div style='font-family:Syne;font-size:1.4rem;font-weight:800;background:linear-gradient(135deg,#00C9A7,#845EC2);-webkit-background-clip:text;-webkit-text-fill-color:transparent;'>🌐 LinguaAssist</div>
      <div style='color:#334155;font-size:0.7rem;'>Government Schemes AI</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("<div style='font-size:0.7rem;color:#00C9A7;font-weight:700;text-transform:uppercase;letter-spacing:.8px;margin-bottom:5px;'>💬 Chat Language</div>", unsafe_allow_html=True)
    new_lang = st.selectbox("lang", list(LANGUAGES.keys()),
        index=list(LANGUAGES.keys()).index(_lk), label_visibility="collapsed", key="lang_sel")
    if new_lang != _lk:
        st.session_state.lang_key = new_lang
    _sc2,_ln2 = LANGUAGES[new_lang]
    st.markdown(f"<div style='background:rgba(0,201,167,0.08);border:1px solid rgba(0,201,167,0.25);border-radius:20px;padding:5px 14px;font-size:0.78rem;font-weight:600;color:#00C9A7;text-align:center;margin-bottom:6px;'>Responding in: <b>{_ln2}</b></div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:0.67rem;color:#475569;text-align:center;margin-bottom:4px;'>Type in any language — always replies in chosen language</div>", unsafe_allow_html=True)
    st.session_state.auto_speak = st.toggle("🔊 Auto-speak (TTS)", value=st.session_state.auto_speak)
    st.divider()
    if st.button("➕ New Chat", use_container_width=True):
        for _si in range(len(st.session_state.all_sessions)):
            st.session_state.all_sessions[_si].pop("active", None)
        save_history(st.session_state.all_sessions)
        st.session_state.messages=[]; st.session_state.total_queries=0
        st.session_state.doc_text=""; st.session_state.doc_name=""; st.session_state.tts_text=""; st.session_state.tts_version=0
        st.rerun()
    st.divider()
    c1,c2=st.columns(2)
    with c1: st.markdown(f"<div style='background:rgba(0,201,167,0.07);border:1px solid rgba(0,201,167,0.18);border-radius:10px;padding:10px;text-align:center;'><div style='font-family:Syne;font-size:1.5rem;font-weight:800;color:#00C9A7;'>{st.session_state.total_queries}</div><div style='font-size:0.62rem;color:#64748B;text-transform:uppercase;'>Queries</div></div>", unsafe_allow_html=True)
    with c2:
        dc="#00C9A7" if st.session_state.doc_text else "#64748B"
        st.markdown(f"<div style='background:rgba(0,201,167,0.07);border:1px solid rgba(0,201,167,0.18);border-radius:10px;padding:10px;text-align:center;'><div style='font-size:1.3rem;color:{dc};'>📎</div><div style='font-size:0.62rem;color:{dc};text-transform:uppercase;'>{'Doc ✓' if st.session_state.doc_text else 'No Doc'}</div></div>", unsafe_allow_html=True)
    st.divider()
    if st.session_state.all_sessions:
        st.markdown("<div style='font-size:0.7rem;color:#A78BCA;font-weight:700;text-transform:uppercase;letter-spacing:.8px;margin-bottom:5px;'>📜 History</div>", unsafe_allow_html=True)
        for idx,sess in enumerate(reversed(st.session_state.all_sessions[-7:])):
            ri=len(st.session_state.all_sessions)-1-idx
            if st.button(f"💬 {sess['title'][:38]}", key=f"h_{ri}", use_container_width=True):
                st.session_state.messages=sess["messages"].copy(); st.rerun()
        if st.button("🗑️ Delete History", key="del_hist", use_container_width=True):
            st.session_state.all_sessions=[]; save_history([]); st.toast("Cleared!",icon="✅"); st.rerun()
        st.divider()
    _prof = st.session_state.user_profile
    _uname = st.session_state.username
    _guest = st.session_state.is_guest
    if _guest:
        st.markdown("<div style='background:rgba(132,94,194,0.08);border:1px solid rgba(132,94,194,0.25);border-radius:10px;padding:8px 12px;font-size:0.75rem;color:#A78BCA;margin-bottom:6px;'>👤 Guest Session</div>", unsafe_allow_html=True)
    else:
        _dname = _prof.get("name", _uname) or _uname
        st.markdown(f"<div style='background:rgba(0,201,167,0.07);border:1px solid rgba(0,201,167,0.2);border-radius:10px;padding:8px 12px;font-size:0.75rem;color:#00C9A7;margin-bottom:6px;'>👋 <b>{_dname}</b><br><span style='color:#475569;font-size:0.68rem;'>{_prof.get('state','')}{' · ' if _prof.get('state') else ''}{_prof.get('income_label','')}</span></div>", unsafe_allow_html=True)
    if st.button("🚪 Logout", key="logout_btn", use_container_width=True):
        for k in ["logged_in","username","user_profile","is_guest","page","messages","tts_text","tts_version"]:
            if k in st.session_state:
                if k in ["logged_in","is_guest"]: st.session_state[k] = False
                elif k == "page": st.session_state[k] = "login"
                elif k in ["messages","user_profile"]: st.session_state[k] = [] if k=="messages" else {}
                elif k == "username": st.session_state[k] = ""
                else: st.session_state[k] = "" if isinstance(st.session_state[k], str) else 0
        st.rerun()
    st.divider()

    if not _guest and _prof:
        _recs = get_recommended_schemes(_prof)
        if _recs:
            _total = len(_recs)
            st.markdown(f"<div style='font-size:0.7rem;color:#FBB724;font-weight:700;text-transform:uppercase;letter-spacing:.8px;margin-bottom:2px;'>⭐ Recommended For You</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size:0.65rem;color:#475569;margin-bottom:8px;'>{_total} schemes matched your profile</div>", unsafe_allow_html=True)
            from collections import defaultdict
            _by_cat = defaultdict(list)
            for r in _recs:
                _by_cat[r["category"]].append(r)
            for _cat, _cat_schemes in _by_cat.items():
                with st.expander(f"{_cat} ({len(_cat_schemes)})", expanded=False):
                    for r in _cat_schemes:
                        st.markdown(f"<div style='font-size:0.68rem;color:#94a3b8;margin-bottom:2px;'>{r['desc']}</div>", unsafe_allow_html=True)
                        if st.button(f"Ask about this →", key=f"rec_{r['name']}", use_container_width=True):
                            st.session_state.prefill = f"Tell me about {r['name']}"; st.rerun()
                        st.markdown("<hr style='border-color:#1E2A3A;margin:4px 0;'>", unsafe_allow_html=True)
            st.divider()

    st.markdown("<div style='font-size:0.7rem;color:#00C9A7;font-weight:700;text-transform:uppercase;letter-spacing:.8px;margin-bottom:5px;'>📋 Browse Schemes</div>", unsafe_allow_html=True)
    for cat,schemes in SCHEME_CATEGORIES.items():
        with st.expander(cat,expanded=False):
            for sn in schemes:
                if st.button(sn,key=f"sc_{sn}",use_container_width=True):
                    st.session_state.prefill=f"Tell me about {sn}"; st.rerun()
    st.divider()
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages=[]; st.session_state.total_queries=0
        st.session_state.doc_text=""; st.session_state.tts_text=""; st.session_state.tts_version=0; st.rerun()
    st.divider()
    if st.button("📍 Find Nearest Help Centre", use_container_width=True, key="goto_map"):
        st.session_state.page = "map"; st.rerun()

# ═══════════════════════════════════════════════════════════════
# MAP PAGE  ──  UPDATED: pin location + Google Maps links only
# ═══════════════════════════════════════════════════════════════
if st.session_state.get("page","main") == "map":
    if st.button("← Back to Chat", key="back_from_map"):
        st.session_state.page = "main"; st.rerun()

    st.markdown("""
    <style>
    .map-title{font-family:'Syne',sans-serif;font-size:1.6rem;font-weight:800;
      background:linear-gradient(135deg,#00C9A7,#845EC2);
      -webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:4px;}
    .map-sub{color:#475569;font-size:0.85rem;margin-bottom:18px;}
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='map-title'>📍 Find Nearest Help Centre</div>", unsafe_allow_html=True)
    st.markdown("<div class='map-sub'>Pin your location on the map, then use the Google Maps links below to find the nearest CSC, bank or post office where you can apply for schemes.</div>", unsafe_allow_html=True)

    # ── NEW simplified map_html ────────────────────────────────────────────
    map_html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>
  *{margin:0;padding:0;box-sizing:border-box;font-family:'DM Sans',system-ui,sans-serif;}
  body{background:#0A0E1A;color:#E2E8F0;padding:6px;}
  #map{width:100%;height:390px;border-radius:14px;border:1.5px solid #1E2A3A;margin-bottom:10px;}
  #status{padding:9px 14px;font-size:0.8rem;color:#00C9A7;
          background:rgba(0,201,167,0.06);border:1px solid rgba(0,201,167,0.2);
          border-radius:10px;margin-bottom:10px;display:flex;align-items:center;gap:8px;}
  #gps-btn{width:100%;padding:11px;border-radius:10px;
           border:1.5px solid rgba(0,201,167,0.45);
           background:rgba(0,201,167,0.09);color:#00C9A7;
           font-size:0.87rem;font-weight:700;cursor:pointer;
           margin-bottom:10px;transition:all .15s;letter-spacing:.2px;}
  #gps-btn:hover{background:rgba(0,201,167,0.22);}
  .spinner{display:inline-block;width:13px;height:13px;
           border:2px solid rgba(0,201,167,0.3);border-top-color:#00C9A7;
           border-radius:50%;animation:spin .7s linear infinite;}
  @keyframes spin{to{transform:rotate(360deg);}}

  /* ── link cards ── */
  .section-label{font-size:0.7rem;color:#475569;font-weight:700;
    text-transform:uppercase;letter-spacing:.6px;margin:14px 0 8px;}
  .lcard{background:linear-gradient(135deg,#0D1321,#111827);
         border:1px solid #1E2A3A;border-radius:13px;
         padding:13px 16px;margin-bottom:9px;}
  .lcard-title{font-size:0.9rem;font-weight:700;margin-bottom:3px;}
  .lcard-desc{font-size:0.73rem;color:#64748B;margin-bottom:10px;line-height:1.5;}
  .lbtn{display:inline-block;padding:7px 16px;border-radius:8px;
        font-size:0.78rem;font-weight:700;text-decoration:none;
        transition:background .14s,color .14s;margin-right:6px;margin-top:2px;}
  .g{background:rgba(0,201,167,0.13);color:#00C9A7;border:1px solid rgba(0,201,167,0.34);}
  .g:hover{background:#00C9A7;color:#0A0E1A;}
  .v{background:rgba(132,94,194,0.13);color:#A78BCA;border:1px solid rgba(132,94,194,0.34);}
  .v:hover{background:#845EC2;color:#fff;}
  .y{background:rgba(251,183,36,0.11);color:#FBB724;border:1px solid rgba(251,183,36,0.32);}
  .y:hover{background:#FBB724;color:#0A0E1A;}
  .coords{display:inline-block;background:#0d1117;border:1px solid #1E2A3A;
          border-radius:20px;padding:2px 10px;font-size:0.67rem;
          color:#475569;margin-top:5px;font-family:monospace;}
  #loc-links{display:none;}
  #loc-links.show{display:block;}
</style>
</head>
<body>

<button id="gps-btn" onclick="getLocation()">&#128205; Detect My Location &amp; Pin on Map</button>
<div id="status">&#128506;&#65039; Click the button above to pin your location</div>
<div id="map"></div>

<!-- Location-based links (shown after GPS) -->
<div id="loc-links">
  <div class="section-label">&#128205; Links based on your pinned location</div>

  <div class="lcard" style="border-color:rgba(0,201,167,0.3)">
    <div class="lcard-title" style="color:#00C9A7">&#127983; Common Service Centre (CSC) near you</div>
    <div class="lcard-desc">Opens Google Maps and searches for Common Service Centres / Jan Seva Kendras nearest to your location — you can apply for most government schemes there.</div>
    <a class="lbtn g" id="csc-link" href="#" target="_blank">Find CSC on Google Maps &#8594;</a>
    <br><span class="coords" id="coords-pill"></span>
  </div>

  <div class="lcard" style="border-color:rgba(132,94,194,0.28)">
    <div class="lcard-title" style="color:#A78BCA">&#127970; Nearest Bank Branch</div>
    <div class="lcard-desc">Find the closest bank where you can open a Jan Dhan account, apply for PM Kisan, Mudra loan, or link Aadhaar for direct benefit transfer.</div>
    <a class="lbtn v" id="bank-link" href="#" target="_blank">Find Banks near me &#8594;</a>
  </div>

  <div class="lcard" style="border-color:rgba(251,183,36,0.24)">
    <div class="lcard-title" style="color:#FBB724">&#128206; Nearest Post Office</div>
    <div class="lcard-desc">Post offices handle Sukanya Samriddhi, Atal Pension Yojana, Aadhaar updates and many savings-linked government schemes.</div>
    <a class="lbtn y" id="po-link" href="#" target="_blank">Find Post Offices near me &#8594;</a>
  </div>
</div>

<!-- Always-visible official links -->
<div class="section-label">&#128279; Official portals (no GPS needed)</div>

<div class="lcard" style="border-color:rgba(251,183,36,0.26)">
  <div class="lcard-title" style="color:#FBB724">&#127983; Official CSC Locator (Government)</div>
  <div class="lcard-desc">Enter your pincode or district on the government's own locator to find your nearest authorised Common Service Centre.</div>
  <a class="lbtn y" href="https://locator.csccloud.in/" target="_blank">Open CSC Locator &#8594;</a>
</div>

<div class="lcard" style="border-color:rgba(0,201,167,0.18)">
  <div class="lcard-title" style="color:#00C9A7">&#128241; myScheme Portal</div>
  <div class="lcard-desc">Apply directly online for 3,000+ government schemes — check eligibility, track status, and get help without visiting an office.</div>
  <a class="lbtn g" href="https://www.myscheme.gov.in/" target="_blank">Open myScheme &#8594;</a>
</div>

<script>
var map = L.map('map',{zoomControl:true}).setView([20.5937,78.9629],5);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{
  attribution:'&copy; OpenStreetMap contributors',maxZoom:19
}).addTo(map);

var userMarker = null;

// Pulsing green pin icon
var pulseIcon = L.divIcon({
  className:'',
  html:'<div style="position:relative;width:48px;height:48px;">'
      +'<div style="position:absolute;inset:0;border-radius:50%;'
      +'background:rgba(0,201,167,0.2);animation:pr 1.7s ease-out infinite;"></div>'
      +'<div style="position:absolute;top:13px;left:13px;width:22px;height:22px;'
      +'border-radius:50%;background:#00C9A7;border:3px solid #fff;'
      +'box-shadow:0 0 14px rgba(0,201,167,0.9);"></div>'
      +'</div>'
      +'<style>@keyframes pr{0%{transform:scale(.55);opacity:.9}100%{transform:scale(1.9);opacity:0}}</style>',
  iconSize:[48,48],iconAnchor:[24,24]
});

function setStatus(msg,spin){
  document.getElementById('status').innerHTML=(spin?'<span class="spinner"></span> ':'&#128205;&#65039; ')+msg;
}

function getLocation(){
  // Use window.parent.navigator.geolocation so the request runs in the
  // parent page's permission context — the iframe is sandboxed and would
  // be denied even if the user already granted location to the main page.
  var geo = (window.parent && window.parent.navigator && window.parent.navigator.geolocation)
              ? window.parent.navigator.geolocation
              : navigator.geolocation;
  if(!geo){setStatus('GPS not supported in this browser.');return;}
  setStatus('Detecting your location\u2026',true);
  geo.getCurrentPosition(
    function(pos){
      var lat=pos.coords.latitude, lon=pos.coords.longitude;
      map.setView([lat,lon],14);
      if(userMarker) map.removeLayer(userMarker);
      userMarker=L.marker([lat,lon],{icon:pulseIcon})
        .addTo(map)
        .bindPopup(
          '<b style="color:#00C9A7;font-size:13px;">&#128205; You are here</b><br>'
         +'<span style="color:#94a3b8;font-size:11px;">'+lat.toFixed(5)+', '+lon.toFixed(5)+'</span>'
        )
        .openPopup();

      document.getElementById('coords-pill').textContent='&#128205; '+lat.toFixed(5)+', '+lon.toFixed(5);

      var base='https://www.google.com/maps/search/';
      document.getElementById('csc-link').href =base+'Common+Service+Centre+CSC+near+me/@'+lat+','+lon+',14z';
      document.getElementById('bank-link').href=base+'bank+near+me/@'+lat+','+lon+',14z';
      document.getElementById('po-link').href  =base+'post+office+near+me/@'+lat+','+lon+',14z';

      document.getElementById('loc-links').classList.add('show');
      setStatus('Location pinned! Use the links below to find nearby centres on Google Maps.');
    },
    function(err){
      // Friendly error messages per error code
      var msg = {
        1: 'Location permission denied \u2014 click the lock icon in your browser address bar and allow location, then try again.',
        2: 'Location unavailable \u2014 check your device GPS or network and try again.',
        3: 'Location request timed out \u2014 please try again.'
      }[err.code] || 'Could not get location \u2014 please try again.';
      setStatus(msg);
    },
    {enableHighAccuracy:true,timeout:14000}
  );
}
</script>
</body>
</html>"""

    components.html(map_html, height=900, scrolling=True)
    # Remove the chat-page icon bar (📎 ⌨ 🎤) from the DOM — it persists
    # across reruns because st.stop() prevents the normal cleanup script from running.
    components.html("""<script>
(function(){
  var el = window.parent.document.getElementById('la-root');
  if (el) el.remove();
})();
</script>""", height=0, scrolling=False)
    st.stop()

# ═══════════════════════════════════════════════════════════════
# MAIN CHAT PAGE
# ═══════════════════════════════════════════════════════════════
st.markdown(f"""<div class='hero'>
  <span class='badge'>🌐 {len(LANGUAGES)}+ Languages</span>
  <span class='badge'>📡 RAG</span><span class='badge'>⚡ Llama 3.3 70B</span>
  <div class='hero-title'>LinguaAssist</div>
  <div style='color:#64748B;font-size:0.88rem;'>Multilingual AI for Indian Government Schemes</div>
</div>""", unsafe_allow_html=True)

st.markdown("<div style='font-size:0.78rem;color:#475569;margin-bottom:6px;'>⚡ Quick Questions:</div>", unsafe_allow_html=True)
_qcols = st.columns(4, gap="small")
_qlabels = ["What is PM Kisan?","Ayushman Bharat eligibility?","How to apply for MGNREGA?","PM Mudra Yojana benefits?"]
for i,q in enumerate(_qlabels):
    with _qcols[i]:
        if st.button(q, key=f"qq_{i}", use_container_width=True):
            st.session_state.prefill=q; st.rerun()

st.markdown("<div style='margin-top:14px'></div>", unsafe_allow_html=True)

if not st.session_state.messages:
    st.markdown(f"""<div style='text-align:center;padding:48px 20px;color:#334155;'>
      <div style='font-size:2.8rem;margin-bottom:10px;'>🌐</div>
      <div style='font-family:Syne;font-size:1.05rem;font-weight:700;color:#475569;margin-bottom:6px;'>Start a conversation</div>
      <div style='font-size:0.82rem;line-height:1.6;'>Ask about any Indian Government Scheme.<br>
        <span style='color:#00C9A7;font-weight:600;'>Response always in {lang_name}.</span><br>
        <span style='color:#475569;font-size:0.75rem;'>Use the 🎤 📎 ⌨ buttons at bottom-right of the input box.</span></div>
    </div>""", unsafe_allow_html=True)
else:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"], avatar="👤" if msg["role"]=="user" else "🤖"):
            st.markdown(msg["content"])
            if msg["role"]=="assistant":
                bh=""
                if msg.get("lang"): bh+=f"<span class='msg-badge'>🌐 {msg['lang']}</span>"
                if msg.get("rag"):  bh+="<span class='msg-badge rag-badge'>📡 RAG</span>"
                if msg.get("doc"):  bh+=f"<span class='msg-badge doc-badge'>📎 {msg['doc']}</span>"
                if bh: st.markdown(bh, unsafe_allow_html=True)

if st.session_state.doc_name:
    st.markdown(f"<div style='background:rgba(251,191,36,0.08);border:1px solid rgba(251,191,36,0.25);border-radius:8px;padding:6px 12px;font-size:0.75rem;color:#FBB724;margin-bottom:6px;'>📎 Active doc: <b>{st.session_state.doc_name}</b> &nbsp;<span style='cursor:pointer;color:#94a3b8;' id='rm-doc'>✕</span></div>", unsafe_allow_html=True)

_ph = PLACEHOLDERS.get(st.session_state.lang_key, "Ask about any government scheme…")
user_input = st.chat_input(placeholder=_ph)
if st.session_state.prefill and not user_input:
    user_input = st.session_state.prefill; st.session_state.prefill = ""

_ek        = KEYBOARD_ALIASES.get(st.session_state.lang_key, st.session_state.lang_key)
_kb_layout = KEYBOARD_LAYOUTS.get(_ek, [])
_is_rtl    = st.session_state.lang_key in RTL_LANGUAGES
_has_kb    = bool(_kb_layout)
_kb_h      = min(420, max(160, len(_kb_layout)*50+80)) if _has_kb else 0
_tts_text  = st.session_state.tts_text if st.session_state.auto_speak else ""

_ek        = KEYBOARD_ALIASES.get(st.session_state.lang_key, st.session_state.lang_key)
_kb_layout = KEYBOARD_LAYOUTS.get(_ek, [])
_is_rtl    = st.session_state.lang_key in RTL_LANGUAGES
_has_kb    = bool(_kb_layout)
_kb_h      = min(420, max(160, len(_kb_layout)*50+80)) if _has_kb else 0
_tts_text  = st.session_state.tts_text if st.session_state.auto_speak else ""

st.markdown("""
<style>
[data-testid="stChatInput"] {
  max-width: calc(100% - 175px) !important;
  width: calc(100% - 175px) !important;
}
[data-testid="stChatInput"] textarea { padding-right: 12px !important; }
[data-testid="stCustomComponentV1"] {
  width: 0 !important;
  height: 0 !important;
  overflow: visible !important;
  padding: 0 !important;
  margin: 0 !important;
}
[data-testid="stBottom"] { overflow: visible !important; }
</style>
""", unsafe_allow_html=True)

components.html(f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"></head>
<body>
<script>
(function(){{
  var par = window.parent;
  var pdoc = par.document;

  var old = pdoc.getElementById('la-root');
  if (old) old.remove();

  var root = pdoc.createElement('div');
  root.id = 'la-root';

  var IS_RTL   = {"true" if _is_rtl else "false"};
  var HAS_KB   = {"true" if _has_kb else "false"};
  var KB_ROWS  = {json.dumps(_kb_layout, ensure_ascii=False)};
  var KB_H     = {_kb_h};
  var TTS_TEXT = {json.dumps(_tts_text)};
  var TTS_LANG = "{st.session_state.tts_lang}";
  var TTS_VER  = {st.session_state.tts_version};
  var SR_LANG  = "{speech_code}";

  root.innerHTML = `
    <style>
      #la-bar {{
        position:fixed;
        top:0;
        left:0;
        display:flex;
        flex-direction:row;
        align-items:center;
        gap:8px;
        z-index:999999;
      }}
      .la-b {{
        width:44px; height:44px; border-radius:50%;
        border:2.5px solid #00C9A7; background:#0a1a17;
        color:#00C9A7; font-size:20px; cursor:pointer;
        display:flex; align-items:center; justify-content:center;
        outline:none; transition:all .16s;
        box-shadow:0 2px 14px rgba(0,201,167,.4);
        font-family:system-ui,sans-serif;
      }}
      .la-b:hover{{background:#00C9A7;color:#0a0e1a;box-shadow:0 4px 22px rgba(0,201,167,.7);transform:scale(1.1);}}
      .la-b.on{{background:#e53e3e!important;border-color:#e53e3e!important;color:#fff!important;animation:la-pulse .7s infinite;}}
      .la-b.kbon{{background:#845EC2!important;border-color:#845EC2!important;color:#fff!important;}}
      @keyframes la-pulse{{0%,100%{{opacity:1}}50%{{opacity:.35}}}}
      #la-kb-panel{{
        position:fixed; bottom:70px; right:16px;
        width:min(96vw,820px); max-height:${{KB_H}}px;
        overflow-y:auto; background:#0d1117;
        border:1.5px solid rgba(0,201,167,.4); border-radius:14px;
        padding:10px 14px; display:none;
        box-shadow:0 -8px 40px rgba(0,0,0,.85); z-index:999998;
        font-family:system-ui,sans-serif;
      }}
      #la-listen-toast {{
        display:none;
        position:fixed;
        bottom:80px;
        right:20px;
        background:#0d1f1c;
        border:1.5px solid #e53e3e;
        color:#fc8181;
        border-radius:10px;
        padding:7px 14px;
        font-size:0.78rem;
        font-family:system-ui,sans-serif;
        z-index:9999999;
        animation:la-pulse .9s infinite;
      }}
    </style>
    <div id="la-bar">
      <button class="la-b" id="la-attach" title="Upload file">&#128206;</button>
      ${{HAS_KB ? '<button class="la-b" id="la-kb-btn" title="Keyboard">&#9000;</button>' : ''}}
      <button class="la-b" id="la-mic" title="Voice input">&#127908;</button>
    </div>
    <div id="la-listen-toast">🎤 Listening…</div>
    <div id="la-kb-panel">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;padding-bottom:6px;border-bottom:1px solid #1e2a3a;">
        <span style="color:#00C9A7;font-size:.7rem;font-weight:700;text-transform:uppercase;letter-spacing:.5px;">&#9000; Keyboard</span>
        <button id="la-kb-x" style="background:none;border:none;color:#475569;font-size:15px;cursor:pointer;padding:2px 6px;">&#x2715;</button>
      </div>
      <div id="la-kb-rows"></div>
      <div style="display:flex;gap:5px;margin-top:8px;padding-top:6px;border-top:1px solid #1e2a3a;">
        <button id="la-spc" style="flex:1;background:#111827;border:1px solid rgba(0,201,167,.2);color:#64748B;border-radius:7px;height:38px;cursor:pointer;font-size:12px;">&#9251; Space</button>
        <button id="la-bk"  style="background:#1a0f0f;border:1px solid rgba(248,113,113,.3);color:#F87171;border-radius:7px;height:38px;width:50px;cursor:pointer;font-size:18px;">&#9003;</button>
        <button id="la-cl"  style="background:#1a0f0f;border:1px solid rgba(248,113,113,.2);color:#F87171;border-radius:7px;height:38px;width:60px;cursor:pointer;font-size:11px;">&#x2715; Clear</button>
      </div>
    </div>
  `;
  pdoc.body.appendChild(root);

  var _styleKill = pdoc.getElementById('la-kill-red');
  if (!_styleKill) {{
    _styleKill = pdoc.createElement('style');
    _styleKill.id = 'la-kill-red';
    _styleKill.textContent = `
      [data-testid="stChatInput"],
      [data-testid="stChatInput"]:focus-within,
      [data-testid="stChatInput"] *,
      [data-testid="stChatInput"] *:focus,
      [data-testid="stChatInput"] *:focus-visible,
      [data-testid="stChatInput"] textarea,
      [data-testid="stChatInput"] textarea:focus,
      [data-testid="stChatInput"] textarea:focus-visible {{
        outline: none !important;
      }}
      [data-testid="stChatInput"] textarea,
      [data-testid="stChatInput"] textarea:focus,
      [data-testid="stChatInput"] [data-baseweb="base-input"],
      [data-testid="stChatInput"] [data-baseweb="base-input"]:focus-within,
      [data-testid="stChatInput"] [data-baseweb="textarea"],
      [data-testid="stChatInput"] div {{
        border: none !important;
        box-shadow: none !important;
      }}
      [data-testid="stChatInput"]:focus-within {{
        border: 1.5px solid #00C9A7 !important;
        box-shadow: 0 0 0 2px rgba(0,201,167,0.18) !important;
      }}
    `;
    pdoc.head.appendChild(_styleKill);
  }}

  function alignBar() {{
    var inp = pdoc.querySelector('[data-testid="stChatInput"]');
    var bar = pdoc.getElementById('la-bar');
    if (!inp || !bar) return;
    var r = inp.getBoundingClientRect();
    var barH = bar.offsetHeight || 44;
    var centerY = r.top + (r.height / 2);
    bar.style.top    = Math.round(centerY - barH / 2) + 'px';
    bar.style.bottom = 'auto';
    bar.style.left   = Math.round(r.right + 8) + 'px';
    bar.style.right  = 'auto';
  }}
  alignBar();
  par.addEventListener('resize', alignBar);
  setTimeout(alignBar, 200);
  setTimeout(alignBar, 800);
  setTimeout(alignBar, 2000);
  var mo = new MutationObserver(function(){{ alignBar(); }});
  mo.observe(pdoc.body, {{ childList:true, subtree:true }});

  function getTA() {{
    return pdoc.querySelector('[data-testid="stChatInput"] textarea')
        || pdoc.querySelector('textarea');
  }}
  function nset(el, v) {{
    var s = Object.getOwnPropertyDescriptor(par.HTMLTextAreaElement.prototype,'value').set;
    s.call(el,v);
    el.dispatchEvent(new par.Event('input',{{bubbles:true}}));
    el.dispatchEvent(new par.Event('change',{{bubbles:true}}));
  }}
  function inject(ch) {{
    var ta=getTA(); if(!ta) return;
    var s=ta.selectionStart,e=ta.selectionEnd,v=ta.value;
    nset(ta,v.slice(0,s)+ch+v.slice(e));
    ta.focus(); ta.setSelectionRange(s+ch.length,s+ch.length);
    if(IS_RTL) ta.setAttribute('dir','rtl');
  }}
  function doBack() {{
    var ta=getTA(); if(!ta) return;
    var s=ta.selectionStart,e=ta.selectionEnd,v=ta.value,nv,ns;
    if(s!==e){{nv=v.slice(0,s)+v.slice(e);ns=s;}}
    else if(s>0){{var a=[...v],ci=[...v.slice(0,s)].length-1;a.splice(ci,1);nv=a.join('');ns=[...v.slice(0,s)].slice(0,-1).join('').length;}}
    else return;
    nset(ta,nv); ta.focus(); ta.setSelectionRange(ns,ns);
  }}
  function doClear() {{ var ta=getTA(); if(ta){{nset(ta,'');ta.focus();}} }}

  if(TTS_TEXT && TTS_TEXT.trim() && par.speechSynthesis) {{
    var lastVer = par.__la_tv__ !== undefined ? par.__la_tv__ : -1;
    if(TTS_VER > lastVer) {{
      par.__la_tv__ = TTS_VER;
      function doSpeak() {{
        par.speechSynthesis.cancel();
        var u = new par.SpeechSynthesisUtterance(TTS_TEXT);
        u.lang   = TTS_LANG;
        u.rate   = 0.88;
        u.pitch  = 1.0;
        u.volume = 1.0;
        var vs = par.speechSynthesis.getVoices();
        var p  = TTS_LANG.split('-')[0];
        var m  = vs.find(function(v){{ return v.lang === TTS_LANG; }})
               || vs.find(function(v){{ return v.lang.startsWith(p); }});
        if (m) u.voice = m;
        par.speechSynthesis.speak(u);
      }}
      if (par.speechSynthesis.getVoices().length > 0) {{
        doSpeak();
      }} else {{
        par.speechSynthesis.onvoiceschanged = function() {{ doSpeak(); }};
      }}
    }}
  }}

  var micBtn = pdoc.getElementById('la-mic');
  var listenToast = pdoc.getElementById('la-listen-toast');
  var rec = null;
  var SR = par.SpeechRecognition || par.webkitSpeechRecognition;

  micBtn.addEventListener('click', function() {{
    if (!SR) {{ alert('Use Chrome or Edge for voice input.'); return; }}
    if (micBtn.classList.contains('on')) {{ if (rec) rec.stop(); return; }}
    if (par.speechSynthesis) par.speechSynthesis.cancel();
    rec = new SR();
    rec.lang = SR_LANG;
    rec.continuous = false;
    rec.interimResults = false;

    rec.onstart = function() {{
      micBtn.classList.add('on');
      micBtn.innerHTML = '&#9209;';
      listenToast.style.display = 'block';
    }};

    rec.onresult = function(e) {{
      var ta = getTA(); if (!ta) return;
      nset(ta, '__VOICE__' + e.results[0][0].transcript);
      ta.focus();
      setTimeout(function() {{
        var btn = pdoc.querySelector('[data-testid="stChatInputSubmitButton"] button');
        if (btn) {{
          btn.click();
        }} else {{
          ta.dispatchEvent(new par.KeyboardEvent('keydown', {{key:'Enter',code:'Enter',keyCode:13,which:13,bubbles:true,cancelable:true}}));
        }}
      }}, 300);
    }};

    rec.onend = function() {{
      micBtn.classList.remove('on');
      micBtn.innerHTML = '&#127908;';
      listenToast.style.display = 'none';
      rec = null;
    }};

    rec.onerror = function(ev) {{
      micBtn.classList.remove('on');
      micBtn.innerHTML = '&#127908;';
      listenToast.style.display = 'none';
      rec = null;
      if (ev.error === 'not-allowed') alert('Mic permission denied.');
    }};

    rec.start();
  }});

  var fi=pdoc.createElement('input');
  fi.type='file'; fi.accept='.pdf,.png,.jpg,.jpeg,.txt'; fi.style.display='none';
  pdoc.body.appendChild(fi);
  pdoc.getElementById('la-attach').addEventListener('click',()=>fi.click());
  fi.addEventListener('change',function(){{
    var f=fi.files[0]; if(!f) return;
    var ta=getTA(); if(ta){{nset(ta,'[File: '+f.name+'] ');ta.focus();}}
    var t=pdoc.createElement('div');
    t.textContent='📎 '+f.name+' attached!';
    t.style.cssText='position:fixed;bottom:80px;right:20px;background:#0d1f1c;border:1px solid #00C9A7;color:#00C9A7;padding:8px 14px;border-radius:10px;font-size:.78rem;z-index:9999999;';
    pdoc.body.appendChild(t); setTimeout(()=>t.remove(),3000);
  }});

  if(HAS_KB) {{
    var kbPanel=pdoc.getElementById('la-kb-panel');
    var kbBtn  =pdoc.getElementById('la-kb-btn');
    var rowsDiv=pdoc.getElementById('la-kb-rows');
    var rtlCSS = IS_RTL?'direction:rtl;':'';
    KB_ROWS.forEach(function(row,ri){{
      var rd=pdoc.createElement('div');
      rd.style.cssText='display:flex;gap:4px;margin-bottom:4px;flex-wrap:wrap;'+rtlCSS;
      row.forEach(function(ch){{
        var b=pdoc.createElement('button');
        var bg=ri===0?'#0a2420':ri===1?'#1a1030':ri===KB_ROWS.length-1?'#1a1400':'#0d1f1c';
        var col=ri===0?'#b2f5ea':ri===1?'#d8b4fe':ri===KB_ROWS.length-1?'#fcd34d':'#e2e8f0';
        var bdr=ri===0?'rgba(0,201,167,.32)':ri===1?'rgba(132,94,194,.32)':ri===KB_ROWS.length-1?'rgba(251,183,36,.28)':'rgba(0,201,167,.2)';
        b.textContent=ch; b.title=ch;
        b.style.cssText='background:'+bg+';border:1px solid '+bdr+';color:'+col
          +';border-radius:7px;min-width:36px;height:40px;padding:0 5px'
          +';font-size:'+(ch.length>2?13:18)+'px'
          +';display:inline-flex;align-items:center;justify-content:center'
          +';cursor:pointer;flex-shrink:0;font-family:system-ui,sans-serif;transition:background .08s;';
        b.onmouseover=()=>{{b.style.background='#00C9A7';b.style.color='#0a0e1a';}};
        b.onmouseout =()=>{{b.style.background=bg;b.style.color=col;}};
        b.addEventListener('mousedown',e=>{{e.preventDefault();inject(ch);}});
        rd.appendChild(b);
      }});
      rowsDiv.appendChild(rd);
    }});
    pdoc.getElementById('la-spc').addEventListener('mousedown',e=>{{e.preventDefault();inject(' ');}});
    pdoc.getElementById('la-bk' ).addEventListener('mousedown',e=>{{e.preventDefault();doBack();}});
    pdoc.getElementById('la-cl' ).addEventListener('mousedown',e=>{{e.preventDefault();doClear();}});
    function openKB()  {{kbPanel.style.display='block';kbBtn.classList.add('kbon');kbBtn.innerHTML='&#x2715;';setTimeout(()=>{{var t=getTA();if(t)t.focus();}},60);}}
    function closeKB() {{kbPanel.style.display='none'; kbBtn.classList.remove('kbon');kbBtn.innerHTML='&#9000;';}}
    kbBtn.addEventListener('click',()=>kbPanel.style.display==='none'?openKB():closeKB());
    pdoc.getElementById('la-kb-x').addEventListener('click',closeKB);
  }}
}})();
</script>
</body></html>""", height=0, scrolling=False)

# ─────────────────────────────────────────────────────────────────────────────
# RESPONSE
# ─────────────────────────────────────────────────────────────────────────────
if user_input and user_input.strip():
    _sc_now, _ln_now = LANGUAGES[st.session_state.lang_key]

    is_voice = user_input.startswith("__VOICE__")
    if is_voice:
        user_input = user_input[len("__VOICE__"):]

    st.session_state.tts_text = ""
    st.session_state.messages.append({"role":"user","content":user_input})
    with st.chat_message("user", avatar="👤"): st.markdown(user_input)

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Thinking…"):
            with st.status("📡 Searching myscheme.gov.in…", expanded=False) as _rs:
                gov_ctx = fetch_gov_context(user_input)
                _rs.update(label="✅ Data retrieved" if gov_ctx else "⚠️ Using model knowledge",
                           state="complete" if gov_ctx else "error")
            ctx = ""
            if gov_ctx: ctx += f"\n\n[GOV DATA]\n{gov_ctx}\n[END]\n"
            if st.session_state.doc_text: ctx += f"\n\n[DOC: {st.session_state.doc_name}]\n{st.session_state.doc_text[:2500]}\n[END]\n"

            sys_msg=(f"You are LinguaAssist, AI for Indian Government Schemes for rural citizens.\n"
                f"CRITICAL: Respond ENTIRELY in {_ln_now} ONLY.\n"
                f"Simple words. Short sentences. Emojis. Bullet points.\n"
                f"Mention required documents and where to go. End with encouragement.\n"
                f"Use official context data. Cite myscheme.gov.in.")
            usr_msg=(f"{ctx}\nQuestion: {user_input}\n\n"
                f"Answer in {_ln_now}:\n📌 What is it?\n✅ Who can get it?\n🎁 What do you get?\n"
                f"📝 How to apply?\n📄 Documents needed\n📞 Where to get help?")
            try:
                resp = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role":"system","content":sys_msg},{"role":"user","content":usr_msg}],
                    max_tokens=1400, temperature=0.22)
                ans = resp.choices[0].message.content
                st.session_state.total_queries += 1

                if is_voice and st.session_state.auto_speak:
                    st.session_state.tts_text    = clean_for_tts(ans)
                    st.session_state.tts_lang    = _sc_now
                    st.session_state.tts_version += 1
                else:
                    st.session_state.tts_text = ""

                st.session_state.messages.append({"role":"assistant","content":ans,"lang":_ln_now,
                    "rag":bool(gov_ctx),"doc":st.session_state.doc_name if st.session_state.doc_text else ""})
                st.markdown(ans)
                bh=f"<span class='msg-badge'>🌐 {_ln_now}</span>"
                if gov_ctx: bh+="<span class='msg-badge rag-badge'>📡 RAG</span>"
                if st.session_state.doc_name: bh+=f"<span class='msg-badge doc-badge'>📎 {st.session_state.doc_name}</span>"
                st.markdown(bh, unsafe_allow_html=True)

                _cur_title = next(
                    (m["content"][:52] for m in st.session_state.messages if m["role"]=="user"),
                    "Chat"
                ) + "…"
                _cur_session = {
                    "title":    _cur_title,
                    "messages": st.session_state.messages.copy(),
                    "lang":     _ln_now,
                    "active":   True,
                }
                _found = False
                for _si, _sess in enumerate(st.session_state.all_sessions):
                    if _sess.get("active"):
                        st.session_state.all_sessions[_si] = _cur_session
                        _found = True
                        break
                if not _found:
                    st.session_state.all_sessions.append(_cur_session)
                save_history(st.session_state.all_sessions)
            except Exception as e:
                st.error(f"Groq API error: {e}")
    st.rerun()