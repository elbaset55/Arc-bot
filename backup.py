import logging
import random
import sqlite3
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, ConversationHandler, ContextTypes, filters, CallbackQueryHandler

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot token
TELEGRAM_BOT_TOKEN = '6817603176:AAHcvgFyPvaGNrF-8lO_8889kAhNZrXbW84'

# Conversation states
(CHOOSING, BOOK_RECOMMENDATION, READING_PROGRESS, QUIZ, BOOK_REVIEW, 
 READING_GROUP, CHALLENGE, CREATING_GROUP, JOINING_GROUP, SUMMARIZE_BOOK) = range(10)

# Initialize SQLite database
conn = sqlite3.connect('reading_challenge.db')
c = conn.cursor()

# Create tables
def init_db():
    c.executescript('''
    CREATE TABLE IF NOT EXISTS users
        (id INTEGER PRIMARY KEY, username TEXT, current_book TEXT);
    CREATE TABLE IF NOT EXISTS reading_progress
        (user_id INTEGER, date TEXT, pages INTEGER);
    CREATE TABLE IF NOT EXISTS book_reviews
        (user_id INTEGER, book TEXT, review TEXT);
    CREATE TABLE IF NOT EXISTS reading_groups
        (id INTEGER PRIMARY KEY, name TEXT);
    CREATE TABLE IF NOT EXISTS group_members
        (group_id INTEGER, user_id INTEGER);
    CREATE TABLE IF NOT EXISTS challenges
        (id INTEGER PRIMARY KEY, user_id INTEGER, challenge_type TEXT, 
         start_date TEXT, end_date TEXT, goal INTEGER, progress INTEGER);
    ''')
    conn.commit()

init_db()

# Book data
books = {
    'ابتدائية': [
        {"title": "قصص الأطفال", "author": "كامل كيلاني", "image": "https://example.com/kamil_kilani_stories.jpg"},
        {"title": "سلسلة المكتبة الخضراء", "author": "دار المعارف", "image": "https://example.com/green_library_series.jpg"},
        {"title": "حكايات جحا", "author": "محمود قاسم", "image": "https://example.com/joha_stories.jpg"},
        {"title": "الأمير الصغير", "author": "أنطوان دو سانت إكزوبيري", "image": "https://example.com/little_prince.jpg"},
        {"title": "كليلة ودمنة", "author": "ابن المقفع", "image": "https://example.com/kalila_wadimna.jpg"},
        {"title": "حكايات عالمية", "author": "مجموعة من المؤلفين", "image": "https://example.com/global_tales.jpg"},
        {"title": "قصص الأنبياء", "author": "ابن كثير", "image": "https://example.com/prophets_stories.jpg"},
        {"title": "سلسلة عالم المعرفة للأطفال", "author": "دار الشروق", "image": "https://example.com/knowledge_world_kids.jpg"},
        {"title": "ألف ليلة وليلة للأطفال", "author": "غير معروف", "image": "https://example.com/alf_leila_wal_leila_kids.jpg"},
        {"title": "حكايات من التراث الشعبي", "author": "غير معروف", "image": "https://example.com/folk_tales.jpg"},
        {"title": "القرآن الكريم للأطفال", "author": "القرآن الكريم", "image": "https://example.com/quran_kids.jpg"},
        {"title": "تعليم اللغة العربية للأطفال", "author": "مجموعة من المؤلفين", "image": "https://example.com/arabic_language_teaching.jpg"},
        {"title": "سلسلة المكتبة الحديثة للأطفال", "author": "دار المعارف", "image": "https://example.com/modern_library_series.jpg"},
        {"title": "كوكب الأرض", "author": "مجموعة من المؤلفين", "image": "https://example.com/planet_earth.jpg"},
        {"title": "النحلة العاملة", "author": "غير معروف", "image": "https://example.com/working_bee.jpg"},
        {"title": "النملة والجرادة", "author": "غير معروف", "image": "https://example.com/ant_grasshopper.jpg"},
        {"title": "السلحفاة والأرنب", "author": "غير معروف", "image": "https://example.com/tortoise_hare.jpg"},
        {"title": "سلسلة المكتبة الصفراء", "author": "دار المعارف", "image": "https://example.com/yellow_library_series.jpg"},
        {"title": "سلسلة الكتب المصورة", "author": "مجموعة من المؤلفين", "image": "https://example.com/picture_books.jpg"},
        {"title": "توتة وحدوتة", "author": "مجموعة من المؤلفين", "image": "https://example.com/tuta_haduta.jpg"},
        {"title": "حديقة الحروف", "author": "غير معروف", "image": "https://example.com/alphabet_garden.jpg"},
        {"title": "مغامرات سندباد", "author": "غير معروف", "image": "https://example.com/sindbad_adventures.jpg"},
        {"title": "ليلى والذئب", "author": "غير معروف", "image": "https://example.com/laila_wolf.jpg"},
        {"title": "علاء الدين والمصباح السحري", "author": "غير معروف", "image": "https://example.com/aladdin_lamp.jpg"},
        {"title": "بينوكيو", "author": "كارلو كولودي", "image": "https://example.com/pinocchio.jpg"},
        {"title": "مغامرات توم سوير", "author": "مارك توين", "image": "https://example.com/tom_sawyer_adventures.jpg"},
        {"title": "مغامرات هانسل وغريتل", "author": "غير معروف", "image": "https://example.com/hansel_gretel_adventures.jpg"},
        {"title": "الأسد والفأر", "author": "غير معروف", "image": "https://example.com/lion_mouse.jpg"},
        {"title": "الفيل الطيب", "author": "غير معروف", "image": "https://example.com/good_elephant.jpg"},
        {"title": "السمكة الصغيرة", "author": "غير معروف", "image": "https://example.com/little_fish.jpg"},
        {"title": "السندريلا", "author": "غير معروف", "image": "https://example.com/cinderella.jpg"}
    ]
,
    'اعدادية': [
        {"title": "الأيام", "author": "طه حسين", "image": "https://example.com/al_ayam.jpg"},
        {"title": "حي بن يقظان", "author": "ابن طفيل", "image": "https://example.com/hay_ibn_yakzan.jpg"},
        {"title": "رجال في الشمس", "author": "غسان كنفاني", "image": "https://example.com/rijal_fi_shams.jpg"},
        {"title": "الشاعر", "author": "مصطفى لطفي المنفلوطي", "image": "https://example.com/al_shair.jpg"},
        {"title": "الفضيلة", "author": "مصطفى لطفي المنفلوطي", "image": "https://example.com/al_fadila.jpg"},
        {"title": "النظرات", "author": "مصطفى لطفي المنفلوطي", "image": "https://example.com/al_nazrat.jpg"},
        {"title": "قنديل أم هاشم", "author": "يحيى حقي", "image": "https://example.com/kandeel_om_hashim.jpg"},
        {"title": "الطوق والأسورة", "author": "يحيى الطاهر عبدالله", "image": "https://example.com/al_touk_al_aswera.jpg"},
        {"title": "عودة الروح", "author": "توفيق الحكيم", "image": "https://example.com/awdat_al_roh.jpg"},
        {"title": "أولاد حارتنا", "author": "نجيب محفوظ", "image": "https://example.com/awlad_haratna.jpg"},
        {"title": "زقاق المدق", "author": "نجيب محفوظ", "image": "https://example.com/ziqaq_al_madaq.jpg"},
        {"title": "اللص والكلاب", "author": "نجيب محفوظ", "image": "https://example.com/al_liss_wal_kelab.jpg"},
        {"title": "عصافير النيل", "author": "إبراهيم أصلان", "image": "https://example.com/asafeer_al_neel.jpg"},
        {"title": "الشحاذ", "author": "نجيب محفوظ", "image": "https://example.com/al_shahaz.jpg"},
        {"title": "دعبول", "author": "يوسف إدريس", "image": "https://example.com/daabul.jpg"},
        {"title": "القرآن الكريم", "author": "القرآن الكريم", "image": "https://example.com/quran.jpg"},
        {"title": "الرحيق المختوم", "author": "صفي الرحمن المباركفوري", "image": "https://example.com/raheeq_makhtoom.jpg"},
        {"title": "البداية والنهاية", "author": "ابن كثير", "image": "https://example.com/bidaya_nihaya.jpg"},
        {"title": "المعلقات السبع", "author": "أعشى قيس", "image": "https://example.com/mualaqat_saba.jpg"},
        {"title": "البيان والتبيين", "author": "الجاحظ", "image": "https://example.com/al_bayan_tabeen.jpg"},
        {"title": "العقد الفريد", "author": "ابن عبد ربه", "image": "https://example.com/al_aqd_al_fareed.jpg"},
        {"title": "كليلة ودمنة", "author": "ابن المقفع", "image": "https://example.com/kalila_wadimna.jpg"},
        {"title": "الأدب الكبير", "author": "ابن المقفع", "image": "https://example.com/al_adab_alkabir.jpg"},
        {"title": "الأدب الصغير", "author": "ابن المقفع", "image": "https://example.com/al_adab_alsaghir.jpg"},
        {"title": "سيرة عنترة بن شداد", "author": "غير معروف", "image": "https://example.com/antaraa.jpg"},
        {"title": "ديوان امرئ القيس", "author": "امرؤ القيس", "image": "https://example.com/diwan_imra_alqays.jpg"},
        {"title": "ديوان المتنبي", "author": "المتنبي", "image": "https://example.com/diwan_mutanabbi.jpg"},
        {"title": "الشعر والشعراء", "author": "ابن قتيبة", "image": "https://example.com/shaar_wal_shura.jpg"},
        {"title": "اللزوميات", "author": "أبو العلاء المعري", "image": "https://example.com/al_luzumiyat.jpg"},
        {"title": "ألف ليلة وليلة", "author": "غير معروف", "image": "https://example.com/alf_leila_wal_leila.jpg"},
        {"title": "الأغاني", "author": "أبو الفرج الأصفهاني", "image": "https://example.com/al_aghani.jpg"}
    ],
    'ثانوية': [
    {"title": "الأدب العربي المعاصر", "author": "طه حسين", "image": "https://example.com/modern_arabic_lit.jpg"},
    {"title": "الأغاني", "author": "أبو الفرج الأصفهاني", "image": "https://example.com/alaghaani.jpg"},
    {"title": "المعلقات السبع", "author": "حماسة البحتري", "image": "https://example.com/seven_mualaqat.jpg"},
    {"title": "الإلياذة", "author": "هوميروس", "image": "https://example.com/iliad.jpg"},
    {"title": "الأوديسة", "author": "هوميروس", "image": "https://example.com/odyssey.jpg"},
    {"title": "دون كيشوت", "author": "ميغيل دي ثيربانتس", "image": "https://example.com/don_quixote.jpg"},
    {"title": "الآلهة عطشى", "author": "أناتول فرانس", "image": "https://example.com/gods_thirsty.jpg"},
    {"title": "البخلاء", "author": "الجاحظ", "image": "https://example.com/albukhala.jpg"},
    {"title": "مجمع البحرين", "author": "الشريف المرتضى", "image": "https://example.com/majmaa_bahrain.jpg"},
    {"title": "طوق الحمامة", "author": "ابن حزم الأندلسي", "image": "https://example.com/taq_el_hamama.jpg"},
    {"title": "كليلة ودمنة", "author": "ابن المقفع", "image": "https://example.com/kalila_dimna.jpg"},
    {"title": "نهج البلاغة", "author": "الإمام علي بن أبي طالب", "image": "https://example.com/nahj_balagha.jpg"},
    {"title": "رسائل إخوان الصفا", "author": "إخوان الصفا", "image": "https://example.com/rasael_ikhwan.jpg"},
    {"title": "البيان والتبيين", "author": "الجاحظ", "image": "https://example.com/alquran_azim.jpg"},
    {"title": "ألف ليلة وليلة", "author": "مجموعة مؤلفين", "image": "https://example.com/1001_nights.jpg"},
    {"title": "الوجودية", "author": "جان بول سارتر", "image": "https://example.com/existentialism.jpg"},
    {"title": "في انتظار غودو", "author": "صمويل بيكيت", "image": "https://example.com/waiting_godot.jpg"},
    {"title": "تاجر البندقية", "author": "ويليام شكسبير", "image": "https://example.com/merchant_venice.jpg"},
    {"title": "الاعترافات", "author": "جان جاك روسو", "image": "https://example.com/confessions.jpg"},
    {"title": "الأمير", "author": "نيكولو مكيافيلي", "image": "https://example.com/the_prince.jpg"},
    {"title": "روح القوانين", "author": "مونتسكيو", "image": "https://example.com/spirit_of_laws.jpg"},
    {"title": "ثورة 1789", "author": "ألبير سوبول", "image": "https://example.com/revolution_1789.jpg"},
    {"title": "موسوعة الفلسفة", "author": "عبد الرحمن بدوي", "image": "https://example.com/philosophy_encyclopedia.jpg"},
    {"title": "السياسة", "author": "أرسطو", "image": "https://example.com/aristotle_politics.jpg"},
    {"title": "تاريخ الفلسفة الغربية", "author": "برتراند راسل", "image": "https://example.com/history_of_western_philosophy.jpg"},
    {"title": "الوجود والعدم", "author": "جان بول سارتر", "image": "https://example.com/being_and_nothingness.jpg"},
    {"title": "الجمهورية", "author": "أفلاطون", "image": "https://example.com/republic.jpg"},
    {"title": "الإنسان ذلك المجهول", "author": "أليكسس كاريل", "image": "https://example.com/man_the_unknown.jpg"},
    {"title": "نقد العقل المحض", "author": "إيمانويل كانت", "image": "https://example.com/critique_of_pure_reason.jpg"},
    {"title": "عالم صوفي", "author": "جوستاين غاردر", "image": "https://example.com/sophies_world.jpg"}]

}

# Quiz questions
questions = [
    {
        "question": "من هو مؤلف كتاب 'ألف ليلة وليلة'؟",
        "options": ["مجهول", "نجيب محفوظ", "طه حسين", "أحمد شوقي"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'البخلاء'؟",
        "options": ["الجاحظ", "ابن المقفع", "ابن رشد", "ابن خلدون"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'الأيام'؟",
        "options": ["طه حسين", "عباس محمود العقاد", "نجيب محفوظ", "أحمد شوقي"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'أولاد حارتنا'؟",
        "options": ["نجيب محفوظ", "يوسف إدريس", "إحسان عبد القدوس", "توفيق الحكيم"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'الجريمة والعقاب'؟",
        "options": ["فيودور دوستويفسكي", "تولستوي", "نيكولاي غوغول", "أنطون تشيخوف"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'هاري بوتر'؟",
        "options": ["جي. ك. رولينغ", "تولكين", "مارك توين", "لويس كارول"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'مئة عام من العزلة'؟",
        "options": ["غابرييل غارسيا ماركيز", "خورخي لويس بورخيس", "بابلو نيرودا", "ماريو بارغاس يوسا"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'كبرياء وتحامل'؟",
        "options": ["جين أوستن", "شارلوت برونتي", "إيميلي برونتي", "ماري شيلي"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'العجوز والبحر'؟",
        "options": ["إرنست همنغواي", "ويليام فوكنر", "جون شتاينبك", "سكوت فيتزجيرالد"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'العالم الجديد الشجاع'؟",
        "options": ["ألدوس هكسلي", "جورج أورويل", "ريموند برادبري", "كورت فونيغوت"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'دون كيشوت'؟",
        "options": ["ميغيل دي ثيربانتس", "غوستاف فلوبير", "هنري فيلدينغ", "دانيال ديفو"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'الإلياذة'؟",
        "options": ["هوميروس", "فرجيل", "سوفوكليس", "إسخيلوس"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'كليلة ودمنة'؟",
        "options": ["ابن المقفع", "ابن سينا", "الفارابي", "الجاحظ"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'هاملت'؟",
        "options": ["ويليام شكسبير", "جون ميلتون", "توماس مور", "كريستوفر مارلو"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'الحرافيش'؟",
        "options": ["نجيب محفوظ", "إحسان عبد القدوس", "يوسف السباعي", "عبد الرحمن الشرقاوي"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'الغريب'؟",
        "options": ["ألبير كامو", "جان بول سارتر", "سيمون دي بوفوار", "فرانز كافكا"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'مزرعة الحيوانات'؟",
        "options": ["جورج أورويل", "ألدوس هكسلي", "جيمس جويس", "كافكا"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'البؤساء'؟",
        "options": ["فيكتور هوجو", "تشارلز ديكنز", "أونوريه دي بلزاك", "دوما"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'الأمير'؟",
        "options": ["نيكولو مكيافيلي", "جون لوك", "توماس هوبز", "جان جاك روسو"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'الجريمة والعقاب'؟",
        "options": ["فيودور دوستويفسكي", "تولستوي", "نيكولاي غوغول", "أنطون تشيخوف"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'ألف شمس مشرقة'؟",
        "options": ["خالد حسيني", "جابرييل غارسيا ماركيز", "إيزابيل الليندي", "تشينوا أتشيبي"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'الزنبقة السوداء'؟",
        "options": ["ألكسندر دوما", "بلزاك", "فيكتور هوجو", "غوستاف فلوبير"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'في انتظار غودو'؟",
        "options": ["صمويل بيكيت", "جان بول سارتر", "أوجين يونسكو", "آرثر ميلر"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'إحياء علوم الدين'؟",
        "options": ["أبو حامد الغزالي", "ابن رشد", "الشافعي", "أبو بكر الرازي"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'الأخوة كارامازوف'؟",
        "options": ["فيودور دوستويفسكي", "تولستوي", "نيكولاي غوغول", "أنطون تشيخوف"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'عقل وعاطفة'؟",
        "options": ["جين أوستن", "إيميلي برونتي", "شارلوت برونتي", "ماري شيلي"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'الدين والدم'؟",
        "options": ["روبرتو ساباتيني", "دان براون", "كريستوفر باوليني", "ستيفن كينغ"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'السياسة الشرعية'؟",
        "options": ["ابن تيمية", "ابن خلدون", "الغزالي", "ابن القيم الجوزية"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'الروحانية في الإسلام'؟",
        "options": ["الغزالي", "ابن القيم", "ابن سينا", "الفارابي"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'رسالة الغفران'؟",
        "options": ["أبو العلاء المعري", "ابن المقفع", "الجاحظ", "أبو نواس"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'الفردوس المفقود'؟",
        "options": ["جون ميلتون", "دانتي أليغييري", "هوميروس", "فيرجيل"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'القانون في الطب'؟",
        "options": ["ابن سينا", "ابن رشد", "ابن النفيس", "الرازي"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'طوق الحمامة'؟",
        "options": ["ابن حزم", "ابن المقفع", "الجاحظ", "أبو تمام"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'الأمير الصغير'؟",
        "options": ["أنطوان دي سانت إكزوبيري", "فيكتور هوجو", "بلزاك", "مارسيل بروست"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'منطق الطير'؟",
        "options": ["فريد الدين العطار", "ابن الفارض", "جلال الدين الرومي", "ابن عربي"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'الديكاميرون'؟",
        "options": ["جيوفاني بوكاتشو", "دانتي أليغييري", "مكيافيلي", "بترارك"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'الشاعر الجوال'؟",
        "options": ["إدغار آلان بو", "روبندرونات طاغور", "وليام وردزوورث", "صامويل كولريدج"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'الكوخ الهندي'؟",
        "options": ["لورد بيرون", "توماس مور", "صمويل جونسون", "جون كيتس"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'الأبله'؟",
        "options": ["فيودور دوستويفسكي", "تولستوي", "نيكولاي غوغول", "أنطون تشيخوف"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'الخيميائي'؟",
        "options": ["باولو كويلو", "جابرييل غارسيا ماركيز", "خورخي لويس بورخيس", "ماريو بارغاس يوسا"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'مدن الملح'؟",
        "options": ["عبد الرحمن منيف", "نجيب محفوظ", "إحسان عبد القدوس", "يوسف السباعي"],
        "correct": 0
    },
]


def get_main_menu_keyboard():
    keyboard = [
        ["عن التحدي", "كيفية المشاركة","موقع التحدي"],
        ["القواعد", "المواعيد النهائية","تحميل الجوازات"],
        ["الجوائز", "اقتراح كتاب","دردشة ذكية"],
        ["التلخيص ببساطة","آلية التحدي","تصنيفات الكتب"],["عن التصفيات", "أبطال التحدي","معايير اختيار الكتب"],
        [ "إحصائيات القراءة","مجموعة الفيسبوك","المركز الاعلامي واخر الأخبار"],
        ["مجموعات القراءة", "تحديات القراءة"], ["تسجيل تقدم القراءة", "اختبار معلومات"],
        ["مكتبات ومنصات كتب"]
       
        
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.effective_user
    c.execute("INSERT OR IGNORE INTO users (id, username) VALUES (?, ?)", (user.id, user.username))
    conn.commit()
    
    message = f"مرحبًا {user.first_name}! أنا بوت تحدي القراءة العربي. 📚✨\n" \
              "  أنا هنا لمساعدتك في رحلتك القرائية ومشاركة شغفك بالكتب وللرد على جميع استفساراتك بخصوص تحدي القراءة العربي ."
    
    await update.effective_message.reply_text(message, reply_markup=get_main_menu_keyboard())
    return CHOOSING

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    help_text = "مرحبًا بك في بوت تحدي القراءة العربي! إليك بعض الأوامر المفيدة:\n\n" \
                "/start - لبدء المحادثة\n" \
                "/help - لعرض هذه الرسالة\n" \
                "/challenge - لبدء تحدي قراءة جديد\n" \
                "/stats - لعرض إحصائيات القراءة الخاصة بك\n" \
                "/recommend - للحصول على توصية كتاب"
    await update.message.reply_text(help_text, reply_markup=get_main_menu_keyboard())
    return CHOOSING

async def handle_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    choice = update.message.text
    
    choice_handlers = {
        "اقتراح كتاب": handle_book_recommendation,
        "تسجيل تقدم القراءة": handle_reading_progress,
        "مراجعة كتاب": handle_book_review,
        "اختبار معلومات": start_quiz,
        "مجموعات القراءة": handle_reading_groups,
        "تحديات القراءة": handle_reading_challenges,
        "تلخيص كتاب": handle_book_summarization,
    }
    
    handler = choice_handlers.get(choice)
    if handler:
        return await handler(update, context)
    else:
        response = await get_response_for_choice(choice, context)
        await update.message.reply_text(response, reply_markup=get_main_menu_keyboard())
    
    return CHOOSING

async def get_response_for_choice(choice: str, context: ContextTypes.DEFAULT_TYPE) -> str:
    responses = {
        "مكتبات ومنصات كتب": (
            "موقع جود ريدز: https://www.goodreads.com/\n"
            "موقع جود ريدز هو شبكة اجتماعية مخصصة لمحبي القراءة والكتب، حيث يمكن للمستخدمين تقييم الكتب، تبادل الآراء، وإنشاء قوائم قراءة شخصية.\n"
            "المكتبة الشاملة: https://shamela.ws/ \n"
            "مكتبة واسعة تضم أكثر من 8000 كتاب من الكتب المتاحة في المجال العام.\n"
            "مكتبة عين الجامعة: https://thebook.univeyes.com \n"
            "مجموعة تزيد عن 150000 كتاب في تخصصات أكاديمية وعلمية متعددة.\n"
            "mENA DOC: https://menalib.de \n"
            "يوفر وصولاً غير محدود للأدب المتعلق بمنطقة الشرق الأوسط وشمال إفريقيا والإسلام.\n"
            "بنك المعرفه المصري: https://ekb.eg \n"
            "مكتبة رقمية توفر الوصول إلى كبار الناشرين الأكاديميين. متوفرة في مصر.\n"
            "مكتبة نور: https://noor-book.com \n"
            "أكبر مكتبة إلكترونية عربية تضم آلاف الكتب القابلة للتنزيل.\n"
            "مؤسسة هنداوي: https://hindawi.org \n"
            "منظمة غير ربحية مهمتها تعزيز التعليم ونشر حب القراءة."
        ),
        "تصنيفات الكتب": (
            "1. الأدب والروايات: تشمل الروايات، القصص القصيرة، الشعر، والمسرحيات.\n"
    "   - الروايات: تتضمن الأعمال الخيالية التي تروي قصصاً عبر فصول متعددة."
    "   - القصص القصيرة: قصص مختصرة تركز على مشهد أو حدث معين.\n"
    "   - الشعر: يشمل الأعمال الشعرية التي تستخدم الوزن والقافية.\n"
    "   - المسرحيات: النصوص المكتوبة للعرض المسرحي.\n\n"
    
    "2. الكتب التعليمية والأكاديمية: تشمل كتب المناهج الدراسية، الكتب الأكاديمية، والمراجع العلمية.\n"
    "   - كتب المناهج الدراسية: كتب تعتمدها المدارس والجامعات ضمن مقرراتها التعليمية.\n"
    "   - الكتب الأكاديمية: مواد علمية متخصصة تتناول موضوعات بحثية عميقة.\n"
    "   - المراجع العلمية: كتب تستخدم كمرجع لمعلومات دقيقة في مختلف التخصصات.\n\n"
    
    "3. الكتب التاريخية والسياسية: تشمل كتب التاريخ، السير الذاتية، الكتب السياسية، والمذكرات.\n"
    "   - كتب التاريخ: تغطي أحداثًا وشخصيات تاريخية من مختلف العصور.\n"
    "   - السير الذاتية: تروي حياة شخصيات مهمة وتأثيرها على المجتمع.\n"
    "   - الكتب السياسية: تناقش الأيديولوجيات والأنظمة السياسية والأحداث المعاصرة.\n"
    "   - المذكرات: كتب تتضمن تجارب وشهادات شخصية لأفراد عاشوا أحداثًا مهمة.\n\n"
    
    "4. كتب التنمية البشرية وتطوير الذات: تشمل كتب التحفيز، القيادة، التفكير الإيجابي، وإدارة الوقت.\n"
    "   - كتب التحفيز: تهدف إلى تعزيز الدافع وتحقيق النجاح الشخصي.\n"
    "   - كتب القيادة: تركز على تطوير المهارات القيادية وإدارة الفرق.\n"
    "   - كتب التفكير الإيجابي: تتناول كيفية تحسين النظرة للحياة والتفكير بإيجابية.\n"
    "   - كتب إدارة الوقت: توفر استراتيجيات لتحسين كفاءة استخدام الوقت.\n\n"
    
    "5. الكتب الدينية: تشمل كتب الأديان المختلفة، التفسير، الحديث، الفقه، والعقيدة.\n"
    "   - كتب الأديان: تغطي النصوص المقدسة والتعاليم الدينية للأديان المختلفة.\n"
    "   - كتب التفسير: شرح وتفسير للقرآن الكريم.\n"
    "   - كتب الحديث: تجمع أقوال وأفعال النبي محمد صلى الله عليه وسلم.\n"
    "   - كتب الفقه: تتناول الأحكام الشرعية وتفاصيل العبادة.\n"
    "   - كتب العقيدة: تتعلق بمبادئ الإيمان والأسس العقائدية في الدين.\n\n"
    
    "6. الكتب الفنية والثقافية: تشمل كتب الفن، الموسيقى، السينما، المسرح، والثقافة العامة.\n"
    "   - كتب الفن: تتناول تاريخ الفن وأنواعه وأعمال الفنانين المشهورين.\n"
    "   - كتب الموسيقى: تشرح تاريخ الموسيقى والنظريات الموسيقية.\n"
    "   - كتب السينما: تدرس صناعة الأفلام، تاريخ السينما، ونقد الأفلام.\n"
    "   - كتب المسرح: تغطي تاريخ المسرح وأعماله وتقاليده.\n"
    "   - الثقافة العامة: كتب تقدم معلومات عامة حول موضوعات متنوعة تخص المجتمع.\n\n"
    
    "7. الكتب العلمية والتقنية: تشمل كتب العلوم، التكنولوجيا، الهندسة، الطب، والعلوم الصحية.\n"
    "   - كتب العلوم: تتناول الفيزياء، الكيمياء، الأحياء، وغيرها من العلوم الطبيعية.\n"
    "   - كتب التكنولوجيا: تتعلق بالتقنيات الحديثة والحوسبة.\n"
    "   - كتب الهندسة: تغطي مختلف فروع الهندسة مثل المدنية، الكهربائية، والميكانيكية.\n"
    "   - كتب الطب: تشمل موضوعات طبية، علاجية، وصحية.\n"
    "   - كتب العلوم الصحية: تتعلق بالصحة العامة، التغذية، والطب البديل.\n\n"
    
    "8. الكتب الترفيهية والهوايات: تشمل كتب الطبخ، الرياضة، السفر، الألعاب، والألغاز.\n"
    "   - كتب الطبخ: تحتوي على وصفات ونصائح للطهي.\n"
    "   - كتب الرياضة: تتعلق بالرياضات المختلفة، التدريب، واللياقة البدنية.\n"
    "   - كتب السفر: تقدم معلومات ونصائح حول السفر والمغامرات.\n"
    "   - الألعاب والألغاز: كتب تحتوي على ألعاب فكرية وألغاز للتسلية والتحدي.\n\n"
    
    "9. كتب الأطفال واليافعين: تشمل القصص المصورة، الحكايات، كتب التعليم المبسط، وكتب اليافعين.\n"
    "   - القصص المصورة: كتب تحتوي على قصص للأطفال مع رسوم توضيحية.\n"
    "   - الحكايات: قصص تقليدية أو شعبية موجهة للأطفال.\n"
    "   - كتب التعليم المبسط: كتب تهدف لتعليم الأطفال مبادئ أساسية مثل الأرقام والحروف.\n"
    "   - كتب اليافعين: روايات وكتب تناسب الفئة العمرية الصغيرة والشبابية.\n\n"
    
    "10. الكتب الاقتصادية والإدارية: تشمل كتب الاقتصاد، الإدارة، الأعمال، الاستثمار، والتسويق.\n"
    "   - كتب الاقتصاد: تتناول النظريات الاقتصادية والاقتصاد العالمي.\n"
    "   - كتب الإدارة: تتعلق بإدارة الأعمال، المؤسسات، وتنظيم العمل.\n"
    "   - كتب الأعمال: تتناول تأسيس وإدارة الشركات الصغيرة والمتوسطة.\n"
    "   - كتب الاستثمار: تقدم نصائح واستراتيجيات للاستثمار في الأسواق المالية.\n"
    "   - كتب التسويق: تغطي استراتيجيات التسويق والإعلانات وبحوث السوق.\n"
        ),
    "معايير اختيار الكتب": (" معايير اختيار الكتب المؤهلة للمشاركة في النسخة القادمة من المسابقة. وفقًا للشروط المحددة، يجب أن تتوافق الكتب المقروءة مع المعايير التالية:\n"
    "- اللغة: يجب أن تكون الكتب باللغة العربية الفصحى.\n"
    "- مستوى المرحلة التعليمية: ينبغي أن تكون الكتب ملائمة لمرحلة الطالب التعليمية من حيث الموضوع وعدد الصفحات.\n"
    "- المحتوى: يُشترط أن لا تكون الكتب عبارة عن مراجع، مجلات، صحف، أو جزء من المنهاج الدراسي للطالب.\n"
    "- عدد الصفحات: يختلف الحد الأدنى لعدد الصفحات المطلوبة بحسب المرحلة التعليمية:\n"
    " - المرحلة الأولى (الصف الأول إلى الثالث الابتدائي): 5 صفحات كحد أدنى.\n"
    " - المرحلة الثانية (الصف الرابع إلى السادس الابتدائي): 21 صفحة كحد أدنى.\n"
    " - المرحلة الثالثة (الصف الأول إلى الثالث الإعدادي): 31 صفحة كحد أدنى.\n"
    " - المرحلة الرابعة (الصف الأول إلى الثالث الثانوي): 51 صفحة كحد أدنى.\n"
    "بالإضافة إلى ذلك، تؤكد اللجنة المنظمة للمسابقة أن التسجيل يجب أن يتم من خلال المدارس، حيث لا يُسمح بالمشاركة الفردية. يُعد هذا الشرط جزءًا من الإجراءات التنظيمية لضمان جودة التقييم والمتابعة الفعالة للطلاب المشاركين."
    ),
        "المركز الاعلامي واخر الأخبار": ("ادخل على الرابط لمعرفة اخر الاخبار:\n"
                                         "https://arabreadingchallenge.com/ar#m_news"),
        "آلية التحدي": ("يتم تسجيل الطلاب من خلال مدارسهم ومشرفيهم.\n"
                        "بعد التسجيل، يستلم كل طالب مسجل جواز المرحلة الأولى ذي اللون الأحمر والذي يحتوي على 10 تأشيرات قراءة بواقع 10 صفحات. يقرأ الطالب الكتاب ويلخصه في صفحة واحدة ليحصل بذلك على تأشيرة القراءة.\n"
                        "يكمل الطالب عشرة كتب ويلخصها في عشر صفحات حتى ينهي المرحلة الأولى وينتقل للمرحلة الثانية والجواز الأخضر.\n"
                        "يكمل الطالب عشرة كتب جديدة ويلخصها في عشر صفحات حتى ينهي المرحلة الثانية وينتقل للمرحلة الثالثة والجواز الأزرق.\n"
                        "يكمل الطالب عشرة كتب جديدة ويلخصها في عشر صفحات حتى ينهي المرحلة الثالثة وينتقل للمرحلة الرابعة والجواز الفضي.\n"
                        "يكمل الطالب عشرة كتب جديدة ويلخصها في عشر صفحات حتى ينهي المرحلة الرابعة وينتقل للمرحلة الخامسة والجواز الذهبي.\n"
                        "يكمل الطالب عشرة كتب جديدة ويلخصها في عشر صفحات حتى ينهي المرحلة الخامسة والأخيرة من القراءة، ويكون بذلك قد قام بقراءة وتلخيص خمسين كتاباً خارج المقرر خلال العام الدراسي."
                        ),
          "تحميل الجوازات": ("ادخل على هذا الربط\n"
                             "https://arabreadingchallenge.com/ar/tool-box"),
        "موقع التحدي": ("ادخل على هذا الربط\n"
                             "https://arabreadingchallenge.com/ar" 
                             ),
         "أبطال التحدي": ( "أبطال التحدي السابقين:\n"
            "الموسم السابع 2022-2023: آمنة المنصوري (الإمارات) وعبد الله البري (قطر).\n"
            "الموسم السادس 2021-2022: شام البكور (سوريا).\n"
            "الموسم الخامس 2019-2020: عبد الله محمد مراد ابو خلف (الأردن).\n"
            "الموسم الرابع 2018-2019: هديل أنور الزبير عبد الرحمن (السودان).\n"
            "الموسم الثالث 2017-2018: مريم لحسن امجون (المغرب).\n"
            "الموسم الثاني 2016-2017: عفاف رائد شريف (فلسطين).\n"
            "الموسم الأول 2015-2016: محمد عبد الله فرح جلود (الجزائر).\n"
        "مشرفين متميزين:\n"
            "الموسم السابع 2022-2023: سماهر السواعي (الأردن).\n"
            "الموسم السادس 2021-2022: نور الجبور (الأردن).\n"
            "الموسم الخامس 2019-2020: موزة الغناة (الإمارات).\n"
            "الموسم الرابع 2018-2019: أميرة محمد نجيب (مصر).\n"
            "الموسم الثالث 2017-2018: عائشة الطويرقي (السعودية).\n"
            "الموسم الثاني 2016-2017: حورية الظل (المغرب).\n"
        "مدارس فائزة.\n"
            "الموسم السابع 2022-2023: مدرسة الملك عبد الله الثاني للتميز (الأردن).\n"
            "الموسم السادس 2021-2022: مدرسة الرؤية العالمية (الإمارات).\n"
            "الموسم الخامس 2019-2020: مدرسة الشيخ زايد بن سلطان (السعودية).\n"
            "الموسم الرابع 2018-2019: مدرسة البنات الثانوية (السودان).\n"
            "الموسم الثالث 2017-2018: مدرسة النصر (المغرب)."
        ),
        "التلخيص ببساطة": (
        "إن عملية التلخيص تحتاج إلى اتباع بعض الخطوات، أو المراحل، وهذه المراحل تتمثل في ثلاث، وهي (مرحلة التمهيد، مرحلة التلخيص الفعلي، مرحلة التقييم).\n"
        "المرحلة الأولى (التمهيد):\n"
        "تتم هذه المرحلة بقراءة الفقرة بدقة، حتى يتم الوقوف على الفكرة الرئيسية، وهدف الكاتب من كتابتها وإبرازها.\n"
        "ثم يتم الوقوف على المفردات الأساسية التي ترتكز الأفكار عليها، حتى لا يتم إغفالها أثناء التلخيص. وبعد ذلك يتم معرفة بنية النص وتحديد أفكاره الرئيسية وأفكاره الفرعية والتسلسل الذي قام الكاتب باتباعه في عرض الموضوع."
        "المرحلة الثانية (التلخيص الفعلي):\n"
        "وفي هذه المرحلة يتم حذف الجمل التي ليس لها داعٍ، مثل المفردات والأفكار المكررة والجمل الاعتراضية والتفسيرية وما إلى ذلك.\n"
        "ثم نبدأ في إعادة كتابة الفقرة بالأسلوب المستقل الشخصي، والحرص على أن يتم إعادة الكتابة بحياد وموضوعية مع المحافظة على التوازن والتسلسل بحيث يتناسب مع تسلسل النص الأصلي وتوازن أقسامه.\n"
        "يمكن استعارة كلمات الكتاب الأصلية الدقيقة والهامة، حتى لا تحل المرادفات بالمعنى المراد ثم كتابة التلخيص بلغة سليمة فصيحة ومتداولة، والتأكد من أن النص الجديد متماسكاً ومترابطاً مع النص الأصلي.\n"
        "المرحلة الثالثة (التقييم):\n"
        "بعد الانتهاء يتم إعادة قراءة النص الجديد وحذف الكلمات الزائدة، والقيام بمقارنة النص الجديد بالنص الأصلي والتأكد أن يكون هناك اختلافات في الصياغة ووجود تطابق في الجوهر. كما أنه لابد من التأكيد من وجود التسلسل والتماسك ما بين الأفكار والجمل والفقرات، وعد الأسطر والكلمات للتأكد من الالتزام بالحجم اللازم.\n"
        "ويمكنك التعرف على الموضوع بطريقة أسهل من خلال هذا الرابط: https://www.facebook.com/ema.N.1157/videos/2738110179680783/?idorvanity=1102168584000760"
        ),

        "عن التصفيات": (
            "التصفية الأولى: تتم التصفية الأولى على مستوى المدرسة أو الإدارة التعليمية، حيث يتنافس "
            "الطلاب داخل المدرسة الواحدة. يتم تصعيد 5 طلاب من كل مرحلة للتصفيات الثانية.\n\n"
            "التصفية الثانية: تتم التصفية الثانية على مستوى المحافظة أو المنطقة التعليمية، حيث يتنافس "
            "الطلاب داخل المنطقة التعليمية. يفوز 11 طالبًا من كل مرحلة، ويتم إجراء تصفية بين الأوائل "
            "على المراحل لاختيار بطل الموسم واحد من الأصحاء وآخر من ذوي الهمم.\n\n"
            "التصفية الثالثة: التصفية الثالثة تتم على مستوى الدولة، حيث يتم اختيار بطل الدولة من الأصحاء "
            "وآخر من ذوي الهمم، وكذلك ترتيب المراكز من الثاني إلى العاشر، بالإضافة إلى المركزين الثاني "
            "والثالث من ذوي الهمم.\n\n"
            "التصفية الرابعة: التصفية الرابعة تتم على مستوى الوطن العربي، حيث يتم اختيار المراكز من الثاني "
            "إلى العاشر، والإعلان عن بطل تحدي القراءة العربي على مستوى الوطن العربي، بالإضافة إلى بطل "
            "من ذوي الهمم."
            "معلومات عن التصفيات:https://www.facebook.com/watch/?v=576595661080059"
        ),
        "عن التحدي": (
            "تحدي القراءة العربي هو أكبر مشروع عربي أطلقه صاحب السمو الشيخ محمد بن راشد آل مكتوم "
            "في عام 2015، بهدف تشجيع القراءة لدى الطلاب في العالم العربي. يسعى التحدي إلى إلهام "
            "أكثر من مليون طالب لقراءة خمسين مليون كتاب خلال كل عام دراسي. يهدف المشروع إلى تعزيز "
            "الثقافة العامة وتطوير مهارات اللغة العربية لدى الشباب."
        ),
        "كيفية المشاركة": (
        "• تواصل مع مشرف تحدي القراءة العربي في المدرسة لتسجيلك في التحدي واستلام الجوازات.\n"
        "• أكمل طلب التسجيل وتعرف على القواعد واللوائح الخاصة بمبادرة تحدي القراءة العربي.\n"
        "• استلم جواز السفر الخاص بك، وأدرج التفاصيل الشخصية الخاصة بك.\n"
        "• اسأل المشرف للحصول على قائمة من الكتب الموصى بها.\n"
        "• اقرأ الكتب وقم بتلخيصها في جواز التحدي الخاص بك.\n"
        "• انتقل إلى الجواز التالي في التسلسل بعد إنهاء قراءة 10 كتب.\n"
        "• اقرأ 40 كتاباً آخر، وقم بتلخيصها في جوازات التحدي الإضافية."
    ),
        "القواعد": (
            "للمشاركة في التحدي، يجب اتباع القواعد التالية:\n"
            "1. اقرأ بانتظام الكتب باللغة العربية.\n"
            "2. سجل تلخيصاتك للكتب في جواز التحدي.\n"
            "3. يجب أن تكون الكتب التي تقرأها مناسبة لمستواك الدراسي.\n"
            "4. حافظ على جودة التلخيصات وتأكد من تقديمها في المواعيد المحددة.\n"
            "5. شارك في التحديات الشهرية والفصلية لتعزيز فرصك في الفوز."
        ),
        "المواعيد النهائية": (
            "التحدي يستمر طوال العام الدراسي، مع وجود مواعيد نهائية لكل مرحلة من مراحل التحدي. "
            "تختلف المواعيد من بلد لآخر، لذا يفضل متابعة التحديثات من خلال المدرسة أو الموقع الرسمي "
            "للتحدي. هناك أيضًا تحديات شهرية وفصلية لتعزيز التنافسية بين المشاركين."
        ),
        "الجوائز": (
            "تقدم تحدي القراءة العربي جوائز قيمة للفائزين على مستويات مختلفة. تشمل الجوائز على مستوى "
            "المدارس والبلدان، وجوائز فردية للطلاب، بالإضافة إلى الجائزة الكبرى لبطل التحدي على مستوى "
            "الوطن العربي بقيمة 500 ألف درهم إماراتي. الجوائز تشمل أيضًا رحلات تعليمية وفرصًا للمشاركة "
            "في فعاليات دولية."
            "•	الجائزة على مستوى الدولة 5000 درهم اماراتي"
            "•	جائزة الطلاب من المركز الثاني إلى المركز العاشر 1500 درهم اماراتي"
            "•	جائزة الطالب الأول من ذوي الهمم 3000 درهم اماراتي"
            "•	جائزة الطالب الثاني والثالث من ذوي الهمم 1000 درهم اماراتي"
            "•	جائزة الطلاب الفائزين على مستوى المحافظة / المنطقة التعليمية 250 درهم اماراتي"
            "•	جائزة المدرسة المتميزة على مستوى الوطن العربي مليون درهم اماراتي"
            "•	جائزة المدرسة المتميزة على مستوى الدولة 50 ألف درهم اماراتي"
            "•	جائزة أفضل مشرف على مستوى الوطن العربي 300 ألف درهم اماراتي"
            "•	جائزة أفضل مشرف على مستوى الوطن العربي 300 ألف درهم اماراتي"
            
            
        ),
        "مجموعة الفيسبوك": ("https://www.facebook.com/share/g/jW2H2JwENhDKrvJX/"),
        "تحدي يومي": await daily_challenge(context),
        "دردشة ذكية": (
            "للتفاعل مع روبوت الدردشة الذكي الخاص بتحدي القراءة العربي، يمكنك زيارة الرابط التالي: "
            "https://poe.com/ARC-ALQalyobia."
            "سيجيب الروبوت على استفساراتك ويقدم لك نصائح وتوصيات "
            "لتعزيز تجربتك في التحدي."
        ),
        "إحصائيات القراءة": await show_reading_stats(context)
    }
    
    return responses.get(choice, "عذرًا، الخيار الذي حددته غير متاح. يرجى اختيار أحد الخيارات المتاحة.")


async def handle_book_recommendation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [
        [InlineKeyboardButton("ابتدائية", callback_data='book_ابتدائية'),
         InlineKeyboardButton("اعدادية", callback_data='book_اعدادية'),
         InlineKeyboardButton("ثانوية", callback_data='book_ثانوية')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("اختر المرحلة الدراسية للحصول على توصية كتاب:", reply_markup=reply_markup)
    return BOOK_RECOMMENDATION

async def book_recommendation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    
    stage = query.data.split('_')[1]
    book = random.choice(books[stage])
    
    user_id = update.effective_user.id
    c.execute("SELECT current_book FROM users WHERE id = ?", (user_id,))
    current_book = c.fetchone()[0]
    
    related_books = [b for b in books[stage] if b['title'] != book['title'] and b['title'] != current_book]
    related_book = random.choice(related_books) if related_books else None
    
    message = f"إليك اقتراح كتاب للمرحلة {stage}:\n\n" \
              f"الكتاب: {book['title']}\n" \
              f"المؤلف: {book['author']}"
    if related_book:
        message += f"\n\nقد يعجبك أيضًا: {related_book['title']} لـ {related_book['author']}"
    
    keyboard = [
        [InlineKeyboardButton("اقتراح آخر", callback_data=f'book_{stage}')],
       
        [InlineKeyboardButton("العودة للقائمة الرئيسية", callback_data='main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(message, reply_markup=reply_markup)
    
    return CHOOSING

async def handle_rating(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    
    rating = query.data.split('_')[1]
    if rating == 'good':
        message = "شكرًا لتقييمك الإيجابي! سنستمر في تقديم اقتراحات مماثلة."
    else:
        message = "نأسف لعدم إعجابك بالاقتراح. سنحاول تحسين اقتراحاتنا في المستقبل."
    
    await query.edit_message_text(message, reply_markup=get_main_menu_keyboard())
    return CHOOSING

async def daily_challenge(context: ContextTypes.DEFAULT_TYPE) -> str:
    challenges = [
        "اقرأ 20 صفحة اليوم",
        "اكتب ملخصًا لما قرأته",
        "شارك اقتباسًا أعجبك من قراءتك اليوم",
        "ناقش ما قرأته مع صديق",
        "اقرأ في مكان مختلف عن المعتاد"
    ]
    return f"تحدي اليوم:\n\n{random.choice(challenges)}"

async def handle_reading_progress(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['expecting_pages'] = True
    await update.message.reply_text("كم صفحة قرأت اليوم؟", reply_markup=ReplyKeyboardRemove())
    return READING_PROGRESS

async def reading_progress(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    pages = update.message.text
    user_id = update.effective_user.id
    
    if pages.isdigit():
        date = datetime.now().strftime("%Y-%m-%d")
        c.execute("INSERT INTO reading_progress (user_id, date, pages) VALUES (?, ?, ?)", (user_id, date, int(pages)))
        conn.commit()
        
        await update.message.reply_text(
            f"تم تسجيل تقدمك! لقد قرأت {pages} صفحة اليوم. أحسنت!",
            reply_markup=get_main_menu_keyboard()
        )
    else:
        await update.message.reply_text("عذرًا، يرجى إدخال رقم صحيح.", reply_markup=get_main_menu_keyboard())
    context.user_data['expecting_pages'] = False
    return CHOOSING

async def start_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    question = random.choice(questions)
    context.user_data['current_question'] = question
    options = question['options']
    keyboard = [[InlineKeyboardButton(option, callback_data=f"quiz_{i}")] for i, option in enumerate(options)]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.effective_message.reply_text(f"السؤال: {question['question']}", reply_markup=reply_markup)
    return QUIZ

async def handle_quiz_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    
    selected_answer = int(query.data.split('_')[1])
    question = context.user_data['current_question']
    correct_answer = question['correct']
    
    if selected_answer == correct_answer:
        response = "إجابة صحيحة! أحسنت!"
    else:
        correct_option = question['options'][correct_answer]
        response = f"للأسف، الإجابة غير صحيحة. الإجابة الصحيحة هي: {correct_option}"
    
    keyboard = [
        [InlineKeyboardButton("سؤال جديد", callback_data='new_quiz')],
        [InlineKeyboardButton("العودة للقائمة الرئيسية", callback_data='main_menu')]
    ]
    await query.edit_message_text(response, reply_markup=InlineKeyboardMarkup(keyboard))
    return CHOOSING

async def handle_book_review(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['expecting_book_review'] = True
    await update.message.reply_text("ما هو اسم الكتاب الذي تريد مراجعته؟", reply_markup=ReplyKeyboardRemove())
    return BOOK_REVIEW

async def book_review(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    book_name = update.message.text
    context.user_data['current_book'] = book_name
    await update.message.reply_text(f"رائع! الآن، اكتب مراجعتك لكتاب '{book_name}'.")
    return BOOK_REVIEW

async def handle_book_review_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    review = update.message.text
    book_name = context.user_data.get('current_book', "كتاب غير معروف")
    user_id = update.effective_user.id
    
    c.execute("INSERT INTO book_reviews (user_id, book, review) VALUES (?, ?, ?)", (user_id, book_name, review))
    conn.commit()
    
    await update.message.reply_text(
        f"شكرًا لمشاركة مراجعتك لكتاب '{book_name}'!",
        reply_markup=get_main_menu_keyboard()
    )
    context.user_data['expecting_book_review'] = False
    return CHOOSING

async def show_reading_stats(context: ContextTypes.DEFAULT_TYPE) -> str:
    user_id = context.user_data.get('user_id')
    c.execute("SELECT SUM(pages), AVG(pages), MAX(pages), COUNT(DISTINCT date) FROM reading_progress WHERE user_id = ?", (user_id,))
    total_pages, avg_pages, max_pages, days_read = c.fetchone()
    
    if not total_pages:
        return "لم تسجل أي تقدم في القراءة بعد. ابدأ بتسجيل صفحاتك اليوم!"
    
    return f"إحصائيات القراءة الخاصة بك:\n\n" \
           f"إجمالي الصفحات المقروءة: {total_pages}\n" \
           f"متوسط الصفحات يوميًا: {avg_pages:.2f}\n" \
           f"أكبر عدد صفحات في يوم واحد: {max_pages}\n" \
           f"عدد أيام القراءة: {days_read}"

async def handle_reading_groups(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [
        [InlineKeyboardButton("إنشاء مجموعة", callback_data='create_group')],
        [InlineKeyboardButton("الانضمام لمجموعة", callback_data='join_group')],
        [InlineKeyboardButton("عرض المجموعات", callback_data='show_groups')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("ماذا تريد أن تفعل مع مجموعات القراءة؟", reply_markup=reply_markup)
    return READING_GROUP

async def create_reading_group(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("ما هو اسم المجموعة التي تريد إنشاءها؟")
    return CREATING_GROUP

async def save_reading_group(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    group_name = update.message.text
    c.execute("INSERT INTO reading_groups (name) VALUES (?)", (group_name,))
    group_id = c.lastrowid
    c.execute("INSERT INTO group_members (group_id, user_id) VALUES (?, ?)", (group_id, update.effective_user.id))
    conn.commit()
    await update.message.reply_text(f"تم إنشاء مجموعة '{group_name}' بنجاح!", reply_markup=get_main_menu_keyboard())
    return CHOOSING

async def join_reading_group(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    c.execute("SELECT id, name FROM reading_groups")
    groups = c.fetchall()
    keyboard = [[InlineKeyboardButton(name, callback_data=f'join_{id}')] for id, name in groups]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text("اختر المجموعة التي تريد الانضمام إليها:", reply_markup=reply_markup)
    return JOINING_GROUP

async def handle_join_group(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    group_id = int(query.data.split('_')[1])
    c.execute("INSERT OR IGNORE INTO group_members (group_id, user_id) VALUES (?, ?)", (group_id, query.from_user.id))
    conn.commit()
    c.execute("SELECT name FROM reading_groups WHERE id = ?", (group_id,))
    group_name = c.fetchone()[0]
    await query.message.reply_text(f"لقد انضممت بنجاح إلى مجموعة '{group_name}'!", reply_markup=get_main_menu_keyboard())
    return CHOOSING

async def show_reading_groups(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    c.execute("SELECT name FROM reading_groups")
    groups = c.fetchall()
    group_list = "\n".join([group[0] for group in groups])
    await query.message.reply_text(f"المجموعات المتاحة:\n\n{group_list}")
    return CHOOSING

async def handle_reading_challenges(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [
        [InlineKeyboardButton("بدء تحدي جديد", callback_data='start_challenge')],
        [InlineKeyboardButton("عرض التحديات الحالية", callback_data='show_challenges')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("ماذا تريد أن تفعل مع تحديات القراءة؟", reply_markup=reply_markup)
    return CHALLENGE

async def start_reading_challenge(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    challenges = ["قراءة كتاب في أسبوع", "قراءة 50 صفحة يوميًا", "قراءة 5 كتب في شهر"]
    keyboard = [[InlineKeyboardButton(challenge, callback_data=f'challenge_{i}')] for i, challenge in enumerate(challenges)]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text("اختر نوع التحدي:", reply_markup=reply_markup)
    return CHALLENGE

async def handle_challenge_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    challenge_index = int(query.data.split('_')[1])
    challenges = ["قراءة كتاب في أسبوع", "قراءة 50 صفحة يوميًا", "قراءة 5 كتب في شهر"]
    selected_challenge = challenges[challenge_index]
    user_id = query.from_user.id
    start_date = datetime.now().strftime("%Y-%m-%d")
    end_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
    c.execute("INSERT INTO challenges (user_id, challenge_type, start_date, end_date, goal, progress) VALUES (?, ?, ?, ?, ?, ?)",
              (user_id, selected_challenge, start_date, end_date, 1, 0))
    conn.commit()
    await query.message.reply_text(f"تم بدء التحدي: {selected_challenge}")
    return CHOOSING

async def show_reading_challenges(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    c.execute("SELECT challenge_type, start_date, end_date, goal, progress FROM challenges WHERE user_id = ?", (user_id,))
    challenges = c.fetchall()
    if challenges:
        challenge_list = "\n\n".join([f"التحدي: {challenge[0]}\nتاريخ البدء: {challenge[1]}\nتاريخ الانتهاء: {challenge[2]}\nالهدف: {challenge[3]}\nالتقدم: {challenge[4]}" for challenge in challenges])
        await query.message.reply_text(f"التحديات الحالية:\n\n{challenge_list}")
    else:
        await query.message.reply_text("ليس لديك أي تحديات حالية. جرب بدء تحدي جديد!")
    return CHOOSING

async def handle_book_summarization(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "لتلخيص كتاب في 9 أسطر، اتبع هذه الخطوات:\n\n"
        "1. اقرأ الكتاب بعناية وحدد الأفكار الرئيسية.\n"
        "2. اكتب جملة واحدة تلخص الفكرة الرئيسية للكتاب.\n"
        "3. حدد 3-4 نقاط رئيسية يغطيها الكتاب.\n"
        "4. اكتب جملة أو جملتين لكل نقطة رئيسية.\n"
        "5. اختم بجملة تلخص الرسالة العامة أو الاستنتاج من الكتاب.\n\n"
        "الآن، أدخل اسم الكتاب الذي تريد تلخيصه:"
    )
    return SUMMARIZE_BOOK

async def summarize_book(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    book_name = update.message.text
    await update.message.reply_text(
        f"رائع! الآن قم بتلخيص كتاب '{book_name}' في 9 أسطر كحد أقصى. "
        "تذكر أن تركز على الأفكار الرئيسية والنقاط المهمة."
    )
    context.user_data['summarizing_book'] = book_name
    return SUMMARIZE_BOOK

async def save_book_summary(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    summary = update.message.text
    book_name = context.user_data.get('summarizing_book', "كتاب غير معروف")
    user_id = update.effective_user.id
    
    c.execute("INSERT INTO book_reviews (user_id, book, review) VALUES (?, ?, ?)", (user_id, book_name, summary))
    conn.commit()
    
    await update.message.reply_text(
        f"شكرًا لتلخيصك لكتاب '{book_name}'! تم حفظ الملخص بنجاح.",
        reply_markup=get_main_menu_keyboard()
    )
    context.user_data.pop('summarizing_book', None)
    return CHOOSING

async def show_challenge_champions(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    champions = {
        "أبطال التحدي السابقين:\n"
            "الموسم السابع 2022-2023: آمنة المنصوري (الإمارات) وعبد الله البري (قطر).\n"
            "الموسم السادس 2021-2022: شام البكور (سوريا).\n"
            "الموسم الخامس 2019-2020: عبد الله محمد مراد ابو خلف (الأردن).\n"
            "الموسم الرابع 2018-2019: هديل أنور الزبير عبد الرحمن (السودان).\n"
            "الموسم الثالث 2017-2018: مريم لحسن امجون (المغرب).\n"
            "الموسم الثاني 2016-2017: عفاف رائد شريف (فلسطين).\n"
            "الموسم الأول 2015-2016: محمد عبد الله فرح جلود (الجزائر).\n"
        "مشرفين متميزين:\n"
            "الموسم السابع 2022-2023: سماهر السواعي (الأردن).\n"
            "الموسم السادس 2021-2022: نور الجبور (الأردن).\n"
            "الموسم الخامس 2019-2020: موزة الغناة (الإمارات).\n"
            "الموسم الرابع 2018-2019: أميرة محمد نجيب (مصر).\n"
            "الموسم الثالث 2017-2018: عائشة الطويرقي (السعودية).\n"
            "الموسم الثاني 2016-2017: حورية الظل (المغرب).\n"
        "مدارس فائزة.\n"
            "الموسم السابع 2022-2023: مدرسة الملك عبد الله الثاني للتميز (الأردن).\n"
            "الموسم السادس 2021-2022: مدرسة الرؤية العالمية (الإمارات).\n"
            "الموسم الخامس 2019-2020: مدرسة الشيخ زايد بن سلطان (السعودية).\n"
            "الموسم الرابع 2018-2019: مدرسة البنات الثانوية (السودان).\n"
            "الموسم الثالث 2017-2018: مدرسة النصر (المغرب)."
        
    }

    champions_text = "أبطال تحدي القراءة العربي:\n\n" + "\n\n".join(champions)
    await update.message.reply_text(champions_text, reply_markup=get_main_menu_keyboard())
    return CHOOSING

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text.lower() == 'إلغاء':
        return await cancel(update, context)
    
    if context.user_data.get('expecting_pages', False):
        context.user_data['expecting_pages'] = False
        return await reading_progress(update, context)
    
    if context.user_data.get('expecting_book_review', False):
        context.user_data['expecting_book_review'] = False
        return await handle_book_review_text(update, context)
    
    if context.user_data.get('summarizing_book', False):
        return await save_book_summary(update, context)
    
    # Handle smart chat
    if text.lower() == 'دردشة ذكية':
        await update.message.reply_text(
            "للدردشة الذكية، يرجى زيارة الرابط التالي:\n"
            "https://poe.com/ARC-ALQalyobia"
        )
        return CHOOSING
    
    # Handle general inquiries about the challenge
    if 'تحدي القراءة' in text or 'عن المسابقة' in text:
        await update.message.reply_text(
            "تحدي القراءة العربي هو أكبر مشروع عربي أطلقه صاحب السمو الشيخ محمد بن راشد آل مكتوم "
            "لتشجيع القراءة لدى الطلاب في العالم العربي. يهدف التحدي إلى قراءة أكثر من 50 مليون كتاب "
            "خلال كل عام دراسي."
        )
        return CHOOSING
    
    return await handle_choice(update, context)
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "تم إلغاء العملية الحالية. هل هناك شيء آخر يمكنني مساعدتك به؟",
        reply_markup=get_main_menu_keyboard()
    )
    return CHOOSING
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

async def show_challenge_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    info_text = (
        "معلومات عن تحدي القراءة العربي:\n\n"
        "- الرؤية: غرس حب القراءة في نفوس الصغار.\n"
        "- الرسالة: إحداث نهضة في القراءة في جميع أنحاء الوطن العربي.\n"
        "- الأهداف:\n"
        "  • تنمية الوعي بواقع القراءة العربي.\n"
        "  • تعزيز الحس الوطني والشعور بالانتماء.\n"
        "  • نشر قيم التسامح والاعتدال.\n"
        "  • تكوين جيل من المتميزين والمبدعين.\n"
        "  • تنشيط حركة التأليف والترجمة والنشر.\n"
        "للمزيد من المعلومات، يرجى زيارة الموقع الرسمي للتحدي."
    )
    await update.message.reply_text(info_text, reply_markup=get_main_menu_keyboard())
    return CHOOSING
async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    if query.data == 'main_menu':
        await query.message.reply_text("العودة إلى القائمة الرئيسية", reply_markup=get_main_menu_keyboard())
        return CHOOSING
    elif query.data.startswith('book_'):
        return await book_recommendation(update, context)
    elif query.data.startswith('rate_'):
        return await handle_rating(update, context)
    elif query.data == 'new_quiz':
        return await start_quiz(update, context)
    elif query.data == 'create_group':
        return await create_reading_group(update, context)
    elif query.data == 'join_group':
        return await join_reading_group(update, context)
    elif query.data == 'show_groups':
        return await show_reading_groups(update, context)
    elif query.data == 'start_challenge':
        return await start_reading_challenge(update, context)
    elif query.data == 'show_challenges':
        return await show_reading_challenges(update, context)
    elif query.data.startswith('challenge_'):
        return await handle_challenge_choice(update, context)
    else:
        await query.message.reply_text("عذرًا، لم أفهم هذا الاختيار.")
        return CHOOSING

async def show_participation_steps(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    steps = (
        "خطوات المشاركة في تحدي القراءة العربي:\n\n"
        "1. التواصل مع مشرف التحدي في مدرستك للتسجيل.\n"
        "2. استلام جواز التحدي الخاص بك.\n"
        "3. قراءة الكتب وتلخيصها في جواز التحدي.\n"
        "4. إكمال قراءة 50 كتابًا خلال العام الدراسي.\n"
        "5. المشاركة في التصفيات على مستوى المدرسة والمنطقة والدولة.\n\n"
        "تذكر: يمكنك تحميل جوازات التحدي بصيغة PDF من الموقع الرسمي للمسابقة."
    )
    await update.message.reply_text(steps, reply_markup=get_main_menu_keyboard())
    return CHOOSING

async def show_challenge_prizes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    prizes = (
        "جوائز تحدي القراءة العربي:\n\n"
        "- الجائزة الأولى لبطل التحدي: 500,000 درهم إماراتي\n"
        "- جائزة الطالب الأول على مستوى الدولة: 100,000 درهم إماراتي\n"
        "- جائزة أفضل مشرف: 300,000 درهم إماراتي\n"
        "- جائزة المدرسة المتميزة: 1,000,000 درهم إماراتي\n\n"
        "بالإضافة إلى جوائز أخرى للمراكز من الثاني إلى العاشر وجوائز خاصة لذوي الهمم."
    )
    await update.message.reply_text(prizes, reply_markup=get_main_menu_keyboard())
    return CHOOSING

async def show_book_selection_criteria(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    criteria = (
        "شروط اختيار الكتب للمشاركة في التحدي:\n\n"
        "- أن يكون الكتاب باللغة العربية.\n"
        "- أن يكون مناسبًا لمستوى الطالب.\n"
        "- ألا يكون من المنهج الدراسي.\n"
        "- ألا يكون مرجعًا أو مجلة أو صحيفة.\n"
        "- عدد الصفحات يختلف حسب المرحلة الدراسية (من 5 إلى 51 صفحة كحد أدنى)."
    )
    await update.message.reply_text(criteria, reply_markup=get_main_menu_keyboard())
    return CHOOSING

def main() -> None:
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING: [
                CallbackQueryHandler(handle_button),
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message),
            ],
            BOOK_RECOMMENDATION: [
                CallbackQueryHandler(book_recommendation)
            ],
            READING_PROGRESS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, reading_progress)
            ],
            QUIZ: [
                CallbackQueryHandler(handle_quiz_answer)
            ],
            BOOK_REVIEW: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_book_review_text)
            ],
            READING_GROUP: [
                CallbackQueryHandler(handle_button)
            ],
            CHALLENGE: [
                CallbackQueryHandler(handle_button)
            ],
            CREATING_GROUP: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, save_reading_group)
            ],
            JOINING_GROUP: [
                CallbackQueryHandler(handle_join_group)
            ],
            SUMMARIZE_BOOK: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, save_book_summary)
            ]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('info', show_challenge_info))
    application.add_handler(CommandHandler('participate', show_participation_steps))
    application.add_handler(CommandHandler('prizes', show_challenge_prizes))
    application.add_handler(CommandHandler('book_criteria', show_book_selection_criteria))
    application.add_handler(CommandHandler('champions', show_challenge_champions))
    application.add_error_handler(error_handler)
    application.run_polling()
if __name__ == '__main__':
    main()