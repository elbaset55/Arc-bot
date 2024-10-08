import logging
import random
import sqlite3
from flask import Flask, request
from discord.ext import commands
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, ConversationHandler, ContextTypes, filters, CallbackQueryHandler


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot token
TELEGRAM_BOT_TOKEN = '6817603176:AAHcvgFyPvaGNrF-8lO_8889kAhNZrXbW84'
DATABASE_NAME = 'reading_challenge.db'
TOKEN = os.environ.get(6817603176:AAHcvgFyPvaGNrF-8lO_8889kAhNZrXbW84')
bot = Application.builder().token(TOKEN).build()
# Conversation states
(CHOOSING, FEEDBACK_TEXT, BOOK_RECOMMENDATION, READING_PROGRESS, 
 QUIZ, BOOK_REVIEW, READING_GROUP, CHALLENGE, CREATING_GROUP, 
 JOINING_GROUP, SUMMARIZE_BOOK, ) = range(11)

# Initialize SQLite database
conn = sqlite3.connect('reading_challenge.db')
c = conn.cursor()

# Create tables
app = Flask(__name__)

@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(), bot.bot)
    bot.process_update(update)
    return "OK"

@app.route('/')
def index():
    return "Hello, this is your Telegram bot!"

if __name__ == '__main__':
    # تعيين Webhook
    bot.bot.set_webhook(url='hissing-latia-arcqaliobia-29aaada5.koyeb.app/' + TOKEN)
    
     port = int(os.environ.get('PORT', 5000))
    app.run(host='8.0.8.0', port=port)
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
def execute_db_query(query, params=None):
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        conn.commit()
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()
# Book data
books = {
'ابتدائية': [
    {"title": "قصص الأطفال", "author": "كامل كيلاني", "image": ""},
    {"title": "سلسلة المكتبة الخضراء", "author": "دار المعارف", "image": ""},
    {"title": "حكايات جحا", "author": "محمود قاسم", "image": ""},
    {"title": "الأمير الصغير", "author": "أنطوان دو سانت إكزوبيري", "image": ""},
    {"title": "كليلة ودمنة", "author": "ابن المقفع", "image": ""},
    {"title": "حكايات عالمية", "author": "مجموعة من المؤلفين", "image": ""},
    {"title": "قصص الأنبياء", "author": "ابن كثير", "image": ""},
    {"title": "سلسلة عالم المعرفة للأطفال", "author": "دار الشروق", "image": ""},
    {"title": "ألف ليلة وليلة للأطفال", "author": "غير معروف", "image": ""},
    {"title": "حكايات من التراث الشعبي", "author": "غير معروف", "image": ""},
    {"title": "القرآن الكريم للأطفال", "author": "القرآن الكريم", "image": ""},
    {"title": "تعليم اللغة العربية للأطفال", "author": "مجموعة من المؤلفين", "image": ""},
    {"title": "سلسلة المكتبة الحديثة للأطفال", "author": "دار المعارف", "image": ""},
    {"title": "كوكب الأرض", "author": "مجموعة من المؤلفين", "image": ""},
    {"title": "النحلة العاملة", "author": "غير معروف", "image": ""},
    {"title": "النملة والجرادة", "author": "غير معروف", "image": ""},
    {"title": "السلحفاة والأرنب", "author": "غير معروف", "image": ""},
    {"title": "سلسلة المكتبة الصفراء", "author": "دار المعارف", "image": ""},
    {"title": "سلسلة الكتب المصورة", "author": "مجموعة من المؤلفين", "image": ""},
    {"title": "توتة وحدوتة", "author": "مجموعة من المؤلفين", "image": ""},
    {"title": "حديقة الحروف", "author": "غير معروف", "image": ""},
    {"title": "مغامرات سندباد", "author": "غير معروف", "image": ""},
    {"title": "ليلى والذئب", "author": "غير معروف", "image": ""},
    {"title": "علاء الدين والمصباح السحري", "author": "غير معروف", "image": ""},
    {"title": "بينوكيو", "author": "كارلو كولودي", "image": ""},
    {"title": "مغامرات توم سوير", "author": "مارك توين", "image": ""},
    {"title": "مغامرات هانسل وغريتل", "author": "غير معروف", "image": ""},
    {"title": "الأسد والفأر", "author": "غير معروف", "image": ""},
    {"title": "الفيل الطيب", "author": "غير معروف", "image": ""},
    {"title": "السمكة الصغيرة", "author": "غير معروف", "image": ""},
    {"title": "السندريلا", "author": "غير معروف", "image": ""}
],
'اعدادية': [
    {"title": "الأيام", "author": "طه حسين", "image": ""},
    {"title": "حي بن يقظان", "author": "ابن طفيل", "image": ""},
    {"title": "رجال في الشمس", "author": "غسان كنفاني", "image": ""},
    {"title": "الشاعر", "author": "مصطفى لطفي المنفلوطي", "image": ""},
    {"title": "الفضيلة", "author": "مصطفى لطفي المنفلوطي", "image": ""},
    {"title": "النظرات", "author": "مصطفى لطفي المنفلوطي", "image": ""},
    {"title": "قنديل أم هاشم", "author": "يحيى حقي", "image": ""},
    {"title": "الطوق والأسورة", "author": "يحيى الطاهر عبدالله", "image": ""},
    {"title": "عودة الروح", "author": "توفيق الحكيم", "image": ""},
    {"title": "أولاد حارتنا", "author": "نجيب محفوظ", "image": ""},
    {"title": "زقاق المدق", "author": "نجيب محفوظ", "image": ""},
    {"title": "اللص والكلاب", "author": "نجيب محفوظ", "image": ""},
    {"title": "عصافير النيل", "author": "إبراهيم أصلان", "image": ""},
    {"title": "الشحاذ", "author": "نجيب محفوظ", "image": ""},
    {"title": "دعبول", "author": "يوسف إدريس", "image": ""},
    {"title": "القرآن الكريم", "author": "القرآن الكريم", "image": ""},
    {"title": "الرحيق المختوم", "author": "صفي الرحمن المباركفوري", "image": ""},
    {"title": "البداية والنهاية", "author": "ابن كثير", "image": ""},
    {"title": "المعلقات السبع", "author": "أعشى قيس", "image": ""},
    {"title": "البيان والتبيين", "author": "الجاحظ", "image": ""},
    {"title": "العقد الفريد", "author": "ابن عبد ربه", "image": ""},
    {"title": "كليلة ودمنة", "author": "ابن المقفع", "image": ""},
    {"title": "الأدب الكبير", "author": "ابن المقفع", "image": ""},
    {"title": "الأدب الصغير", "author": "ابن المقفع", "image": ""},
    {"title": "سيرة عنترة بن شداد", "author": "غير معروف", "image": ""},
    {"title": "ديوان امرئ القيس", "author": "امرؤ القيس", "image": ""},
    {"title": "ديوان المتنبي", "author": "المتنبي", "image": ""},
    {"title": "الشعر والشعراء", "author": "ابن قتيبة", "image": ""},
    {"title": "اللزوميات", "author": "أبو العلاء المعري", "image": ""},
    {"title": "ألف ليلة وليلة", "author": "غير معروف", "image": ""},
    {"title": "الأغاني", "author": "أبو الفرج الأصفهاني", "image": ""}
],
    'ثانوية': [
    {"title": "الأدب العربي المعاصر", "author": "طه حسين", "image": "https://www.samawy.com/displayimg/1007255/fdbc28e0bc9c435aa40b385e0394b97d.jpg"},
    {"title": "الأغاني", "author": "أبو الفرج الأصفهاني", "image": "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1497738286i/16051672.jpg"},
    {"title": "المعلقات السبع", "author": "حماسة البحتري", "image": "https://daralhikma.org/index.php/%D9%85%D9%84%D9%81:%D8%A7%D9%84%D9%85%D8%B9%D9%84%D9%82%D8%A7%D8%AA_%D8%A7%D9%84%D8%B9%D8%B4%D8%B1.jpg"},
    {"title": "الإلياذة", "author": "هوميروس", "image": "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1453146104i/28598111.jpg"},
    {"title": "الأوديسة", "author": "هوميروس", "image": "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1292745273i/9957628.jpg"},
    {"title": "دون كيشوت", "author": "ميغيل دي ثيربانتس", "image": "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1283009382i/5871399.jpg"},
    {"title": "الآلهة عطشى", "author": "أناتول فرانس", "image": "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1313407613i/10323916.jpg"},
    {"title": "البخلاء", "author": "الجاحظ", "image": "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1281638124i/6315308.jpg"},
    {"title": "مجمع البحرين", "author": "الشريف المرتضى", "image": "https://www.zakariyyabooks.com/wp-content/uploads/%D9%85%D8%AC%D9%85%D8%B9-%D8%A7%D9%84%D8%A8%D8%AD%D8%B1%D9%8A%D9%86-%D9%88%D9%85%D9%84%D8%AA%D9%82%D9%89-%D8%A7%D9%84%D9%86%D9%8A%D8%B1%D9%8A%D9%86-%D9%81%D9%8A-%D8%A7%D9%84%D9%81%D9%82%D9%87-%D8%A7%D9%84%D8%AD%D9%86%D9%81%D9%8A-scaled.jpg"},
    {"title": "طوق الحمامة", "author": "ابن حزم الأندلسي", "image": "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1327852446i/5582346.jpg"},
    {"title": "كليلة ودمنة", "author": "ابن المقفع", "image": "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1242573221i/2498952.jpg"},
    {"title": "نهج البلاغة", "author": "الإمام علي بن أبي طالب", "image": "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1620225508i/1618417.jpg"},
    {"title": "رسائل إخوان الصفا", "author": "إخوان الصفا", "image": "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1452530460i/15743362.jpg"},
    {"title": "البيان والتبيين", "author": "الجاحظ", "image": "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1392823975i/6657370.jpg"},
    {"title": "ألف ليلة وليلة", "author": "مجموعة مؤلفين", "image": "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1311932385i/12194590.jpg"},
    {"title": "الوجودية", "author": "جان بول سارتر", "image": "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1329180823i/7860373.jpg"},
    {"title": "في انتظار غودو", "author": "صمويل بيكيت", "image": "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1504822938i/8111210.jpg"},
    {"title": "تاجر البندقية", "author": "ويليام شكسبير", "image": "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1299002275i/6895751.jpg"},
    {"title": "الاعترافات", "author": "جان جاك روسو", "image": "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1369347363i/17973059.jpg"},
    {"title": "الأمير", "author": "نيكولو مكيافيلي", "image": "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1406207015i/22811744.jpg"},
    {"title": "روح القوانين", "author": "مونتسكيو", "image": "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1377866378i/13589909.jpg"},
    {"title": "ثورة 1789", "author": "ألبير سوبول", "image": "https://www.noor-book.com/publice/covers_cache_webp/1/3/d/0/4c1978c3e23d04946bb8b979992532f8.jpg.webp"},
    {"title": "موسوعة الفلسفة", "author": "عبد الرحمن بدوي", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRRY2r3UTVFrHUjNZjIDtDUuVlPazIHLAmVVA&s"},
    {"title": "السياسة", "author": "أرسطو", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcROoi66c6ZRAl4AqnQHYkD0vopE6LcBBWySeg&s"},
    {"title": "تاريخ الفلسفة الغربية", "author": "برتراند راسل", "image": "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1351302530i/11233616.jpg"},
    {"title": "الوجود والعدم", "author": "جان بول سارتر", "image": "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1590475737i/9518625.jpg"},
    {"title": "الجمهورية", "author": "أفلاطون", "image": "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1330050088i/7712451.jpg"},
    {"title": "الإنسان ذلك المجهول", "author": "أليكسس كاريل", "image": "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1236321587i/6317068.jpg"},
    {"title": "نقد العقل المحض", "author": "إيمانويل كانت", "image": "https://m.media-amazon.com/images/I/61iuWZwTlCL._AC_UL320_.jpg"},
    {"title": "عالم صوفي", "author": "جوستاين غاردر", "image": "https://m.media-amazon.com/images/I/51ZRe97a83S._SY445_SX342_.jpg"}]

}







# Quiz questions
questions = [
    {
        "question": "هذه الشخصية الخيالية يعيش في عالم سحري، وتتميز بوجودها في سلسلة كتب مشهورة حيث تتعلم السحر وتواجه قوى الشر.",
        "options": ["هاري بوتر", "سيد الخواتم", "أليس في بلاد العجائب", "غريزلي"],
        "correct": 0
    },
    {
        "question": "هذه الرواية الكلاسيكية كتبها جين أوستن وتدور حول قصة حب وتقاليد المجتمع في إنجلترا.",
        "options": ["فخر وتحامل", "عقل وعاطفة", "جين إير", "الأمير والفقير"],
        "correct": 0
    },
    {
        "question": "فيلم شهير من إنتاج 1994، يتحدث عن قصة صعود شخص من طبقة متواضعة إلى أن يصبح أحد أبرز زعماء العالم.",
        "options": ["فورست غامب", "العراب", "الراعي الصالح", "سيد الخواتم"],
        "correct": 0
    },
    {
        "question": "هذه الشخصية التاريخية كانت أول رئيس للولايات المتحدة الأمريكية ولعبت دورًا كبيرًا في استقلال البلاد.",
        "options": ["جورج واشنطن", "أبراهام لينكولن", "توماس جيفرسون", "ألكسندر هاميلتون"],
        "correct": 0
    },
    {
        "question": "موقع إلكتروني مشهور للبحث عن كتب ومراجعاتها من قبل مستخدمين حول العالم.",
        "options": ["جود ريدز", "أمازون", "مكتبة الإسكندرية", "سكايب"],
        "correct": 0
    },
    {
        "question": "هذه الرواية الشهيرة كتبها جورج أورويل وتصور عالمًا دكتاتوريًا تحت مراقبة دائمة.",
        "options": ["1984", "مزرعة الحيوانات", "الشجاعة", "أرض النفاق"],
        "correct": 0
    },
    {
        "question": "شخصية خيالية من أفلام الرسوم المتحركة، وهي قطة زرقاء اللون تعيش مغامراتها في عالم سحري.",
        "options": ["سونيك", "توم وجيري", "سبونج بوب", "الأميرة سنو وايت"],
        "correct": 0
    },
    {
        "question": "هذه الكوميديا الشهيرة من إخراج ميل بروكس وتدور حول قصة غريبة في عالم الديناصورات.",
        "options": ["الإنسان الذي عاش مع الديناصورات", "ملوك العصر الجليدي", "غابات الخيال", "فرقة المرح"],
        "correct": 0
    },
    {
        "question": "رواية تاريخية تحكي عن أحد الصراعات الكبيرة في التاريخ، وكتبها هيرمان ملفيل.",
        "options": ["موبي ديك", "الأخوة كارامازوف", "تحت السماء المفتوحة", "الأمير الصغير"],
        "correct": 0
    },
    {
        "question": "فيلم من إخراج كريستوفر نولان يتحدث عن قصة رجل يحاول استرجاع ذكرياته من خلال السفر عبر الزمن.",
        "options": ["تبدأ", "بين النجوم", "الشعلة", "مفتاح الأمل"],
        "correct": 0
    },
    {
        "question": "هذه السلسلة الأدبية المشهورة تتحدث عن مغامرات شخصية خيالية تعيش في عصور قديمة وأسطورية.",
        "options": ["سيد الخواتم", "حرب النجوم", "ترانزيت", "الرجل الحديدي"],
        "correct": 0
    },
    {
        "question": "هذه الرواية، التي كتبها ألبير كامو، تتحدث عن بطل يعيش في عالم غير عادل ويواجه مصاعب الحياة.",
        "options": ["الغريب", "الأسود والأبيض", "الحياة كمزحة", "مزرعة الحيوانات"],
        "correct": 0
    },
    {
        "question": "شخصية خيالية مشهورة من عالم المانغا والأنيمي، وهي فتاة تمتلك قوى سحرية وتعيش مغامراتها في عالم معقد.",
        "options": ["سابرينا", "ساسوكي", "ناروتو", "مغامرات تيمون وبومبا"],
        "correct": 0
    },
    {
        "question": "هذه السلسلة من الأفلام الشهيرة تدور حول مغامرات مجموعة من الأبطال في عالم خيالي لمحاربة قوى الشر.",
        "options": ["حرب النجوم", "سيد الخواتم", "العراب", "حراس المجرة"],
        "correct": 0
    },
    {
        "question": "هذه الرواية الشهيرة كتبها نجيب محفوظ، وتدور حول حياة شخصيات مختلفة في القاهرة.",
        "options": ["الأدب الحركي", "الحرافيش", "بداية ونهاية", "الثلاثية"],
        "correct": 3
    },
    {
        "question": "هذه الشخصية الكوميدية الشهيرة هي أحد أبطال سلسلة الرسوم المتحركة التي تم إنشاؤها في الثلاثينات.",
        "options": ["ميكي ماوس", "باقي باني", "دافي داك", "سكوبي دو"],
        "correct": 0
    },
    {
        "question": "فيلم درامي يحكي قصة حياة أحد الموسيقيين الشهيرين وتأثير الموسيقى على حياته.",
        "options": ["أماديوس", "ذا ووكينج ديد", "الرجل العنكبوت", "مملكة الخواتم"],
        "correct": 0
    },
    {
        "question": "هذه الرواية الشهيرة كتبها جابرييل غارسيا ماركيز وتدور حول حياة عائلة في بلدة خيالية في أمريكا اللاتينية.",
        "options": ["مائة عام من العزلة", "التيجاني", "عالم صوفي", "النفق"],
        "correct": 0
    },
    {
        "question": "شخصية خيالية شهيرة من أفلام الرسوم المتحركة، وهي أميرة تعيش في قصر وتواجه مغامراتها الخاصة.",
        "options": ["سندريلا", "الأميرة النائمة", "أريل", "جاسمين"],
        "correct": 0
    },
    {
        "question": "هذه الرواية الشهيرة كتبها جين أوستن وتدور حول موضوعات الزواج والمجتمع في إنجلترا.",
        "options": ["العقل والعاطفة", "فخر وتحامل", "أميرة النقاء", "الكبرياء والحب"],
        "correct": 0
    },
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
        "question": "من هو مؤلف كتاب 'الشيفرة دافنشي'؟",
        "options": ["دان براون", "جون غريشام", "ستيفن كينغ", "جورج أورويل"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'مئة عام من العزلة'؟",
        "options": ["غابرييل غارسيا ماركيز", "خورخي لويس بورخيس", "إيزابيل الليندي", "بابلو نيرودا"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'عالم جديد شجاع'؟",
        "options": ["ألدوس هكسلي", "جورج أورويل", "فيليب ك. ديك", "إسحاق أسيموف"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'لوليتا'؟",
        "options": ["فلاديمير نابوكوف", "مارسيل بروست", "فرانز كافكا", "فيودور دوستويفسكي"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'الطاعون'؟",
        "options": ["ألبير كامو", "جان بول سارتر", "ماركيز دي ساد", "أنطوان دو سانت-إيكسوبيري"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'شرق عدن'؟",
        "options": ["جون شتاينبك", "إرنست همنغواي", "وليام فوكنر", "ريتشارد رايت"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'البحث عن الزمن المفقود'؟",
        "options": ["مارسيل بروست", "إميل زولا", "جان بول سارتر", "فيكتور هوغو"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'فهرنهايت 451'؟",
        "options": ["راي برادبري", "إسحاق أسيموف", "جورج أورويل", "ألدوس هكسلي"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'دكتور جيكل والسيد هايد'؟",
        "options": ["روبرت لويس ستيفنسون", "آرثر كونان دويل", "هنري جيمس", "مارك توين"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'الشمس تشرق أيضاً'؟",
        "options": ["إرنست همنغواي", "جون شتاينبك", "وليم فوكنر", "فيليب روث"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب '1984'؟",
        "options": ["جورج أورويل", "ألدوس هكسلي", "كورت فونيغوت", "راي برادبري"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'الأوديسة'؟",
        "options": ["هوميروس", "سوفوكليس", "يوريبيديس", "أسخيلوس"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'أورلاندو'؟",
        "options": ["فرجينيا وولف", "إميلي برونتي", "جين أوستن", "سيلفيا بلاث"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'يوليسيس'؟",
        "options": ["جيمس جويس", "مارسيل بروست", "إيتالو كالفينو", "وليم فوكنر"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'صورة دوريان غراي'؟",
        "options": ["أوسكار وايلد", "تشارلز ديكنز", "هنري جيمس", "إدغار آلان بو"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'غاتسبي العظيم'؟",
        "options": ["فرانسيس سكوت فيتزجيرالد", "وليم فوكنر", "إرنست همنغواي", "جيمس جويس"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'مزرعة الحيوان'؟",
        "options": ["جورج أورويل", "ألدوس هكسلي", "كافكا", "دوستويفسكي"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'الغثيان'؟",
        "options": ["جان بول سارتر", "ألبير كامو", "فرانس كافكا", "هنري جيمس"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'أليس في بلاد العجائب'؟",
        "options": ["لويس كارول", "مارك توين", "تشارلز ديكنز", "روديارد كبلينغ"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'البيت المتوحش'؟",
        "options": ["تشارلز ديكنز", "أوسكار وايلد", "تولستوي", "جيمس جويس"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'قلب الظلام'؟",
        "options": ["جوزيف كونراد", "مارك توين", "جيمس جويس", "وليم فوكنر"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'المسخ'؟",
        "options": ["فرانس كافكا", "ألبير كامو", "تشارلز ديكنز", "كافكا"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'الشيخ والبحر'؟",
        "options": ["إرنست همنغواي", "وليام فوكنر", "جون شتاينبك", "ريتشارد رايت"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'الجريمة والعقاب'؟",
        "options": ["فيودور دوستويفسكي", "تولستوي", "نيكولاي غوغول", "أنطون تشيخوف"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'قصة مدينتين'؟",
        "options": ["تشارلز ديكنز", "إميلي برونتي", "تشارلوت برونتي", "تولستوي"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'كبرياء وتحامل'؟",
        "options": ["جين أوستن", "إميلي برونتي", "شارلوت برونتي", "ماري شيلي"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'هاري بوتر وحجر الفيلسوف'؟",
        "options": ["ج. ك. رولينغ", "جيمس جويس", "ستيفن كينغ", "جون غريشام"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'مدن الملح'؟",
        "options": ["عبد الرحمن منيف", "نجيب محفوظ", "إدوارد سعيد", "غسان كنفاني"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'زوربا اليوناني'؟",
        "options": ["نيكوس كازانتزاكيس", "إليف شافاق", "إبراهيم الكوني", "يشار كمال"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'الأبله'؟",
        "options": ["فيودور دوستويفسكي", "تولستوي", "أنطون تشيخوف", "إيفان تورغينيف"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'رجال تحت الشمس'؟",
        "options": ["غسان كنفاني", "نجيب محفوظ", "إدوارد سعيد", "عبد الرحمن منيف"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'الأم'؟",
        "options": ["مكسيم غوركي", "تولستوي", "دوستويفسكي", "أنطون تشيخوف"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'القلعة'؟",
        "options": ["فرانس كافكا", "ألبير كامو", "تولستوي", "دوستويفسكي"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'البجعات البرية'؟",
        "options": ["يونغ تشانغ", "أليف شفق", "كازوو إيشيغورو", "كريس فان ألسبرغ"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'الجذور'؟",
        "options": ["أليكس هايلي", "ريتشارد رايت", "هاربر لي", "توني موريسون"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'مزرعة الحيوان'؟",
        "options": ["جورج أورويل", "راي برادبري", "كافكا", "دوستويفسكي"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'مئة عام من العزلة'؟",
        "options": ["غابرييل غارسيا ماركيز", "إيزابيل الليندي", "خورخي لويس بورخيس", "بابلو نيرودا"],
        "correct": 0
    },
    {
        "question": "من هو مؤلف كتاب 'الغريب'؟",
        "options": ["ألبير كامو", "جان بول سارتر", "سيمون دي بوفوار", "فرانز كافكا"],
        "correct": 0
    },
       {
        "question": "أي من التصنيفات الآتية ينتمي إليها كتاب '1984' لجورج أورويل؟",
        "options": ["خيال علمي", "أدب ديستوبي", "رواية بوليسية", "سيرة ذاتية"],
        "correct": 1
    },
    {
        "question": "إلى أي تصنيف ينتمي كتاب 'إقناع' لجين أوستن؟",
        "options": ["رواية رومانسية", "رواية تاريخية", "خيال علمي", "أدب واقعي"],
        "correct": 0
    },
    {
        "question": "ما هو التصنيف الأدبي لكتاب 'الطاعون' لألبير كامو؟",
        "options": ["أدب وجودي", "رواية بوليسية", "أدب ديستوبي", "أدب فانتازي"],
        "correct": 0
    },
    {
        "question": "إلى أي تصنيف ينتمي كتاب 'الشفق' لستيفاني ماير؟",
        "options": ["رواية رومانسية", "رواية فانتازيا", "أدب رعب", "أدب تاريخي"],
        "correct": 1
    },
    {
        "question": "أي تصنيف ينتمي إليه كتاب 'عناقيد الغضب' لجون شتاينبك؟",
        "options": ["أدب اجتماعي", "رواية خيال علمي", "أدب رعب", "أدب تاريخي"],
        "correct": 0
    },
    {
        "question": "ما هو تصنيف كتاب 'كافكا على الشاطئ' لهاروكي موراكامي؟",
        "options": ["أدب سيريالي", "رواية خيال علمي", "أدب تاريخي", "أدب واقعي"],
        "correct": 0
    },
    {
        "question": "إلى أي تصنيف ينتمي كتاب 'رحلة إلى مركز الأرض' لجول فيرن؟",
        "options": ["رواية خيال علمي", "رواية مغامرات", "أدب ديستوبي", "أدب فانتازي"],
        "correct": 0
    },
    {
        "question": "أي تصنيف ينتمي إليه كتاب 'مزرعة الحيوان' لجورج أورويل؟",
        "options": ["أدب ديستوبي", "أدب سياسي", "رواية بوليسية", "أدب تاريخي"],
        "correct": 1
    },
    {
        "question": "ما هو تصنيف كتاب 'الهوبيت' لجي آر آر تولكين؟",
        "options": ["أدب فانتازي", "رواية خيال علمي", "رواية مغامرات", "أدب رعب"],
        "correct": 0
    },
    {
        "question": "إلى أي تصنيف ينتمي كتاب 'هاري بوتر وحجر الفيلسوف' لج. ك. رولينغ؟",
        "options": ["أدب فانتازي", "أدب أطفال", "رواية بوليسية", "أدب تاريخي"],
        "correct": 0
    },
    {
        "question": "ما هو تصنيف كتاب 'الجريمة والعقاب' لدوستويفسكي؟",
        "options": ["أدب نفسي", "أدب بوليسي", "أدب رعب", "أدب واقعي"],
        "correct": 0
    },
    {
        "question": "أي تصنيف ينتمي إليه كتاب 'الغريب' لألبير كامو؟",
        "options": ["أدب وجودي", "رواية بوليسية", "أدب تاريخي", "أدب فانتازي"],
        "correct": 0
    },
    {
        "question": "ما هو تصنيف كتاب 'الأمير الصغير' لأنطوان دو سانت-إكزوبيري؟",
        "options": ["أدب أطفال", "أدب فانتازي", "أدب واقعي", "رواية تاريخية"],
        "correct": 0
    },
    {
        "question": "إلى أي تصنيف ينتمي كتاب 'الأوديسة' لهوميروس؟",
        "options": ["أدب ملحمي", "رواية بوليسية", "أدب ديستوبي", "أدب وجودي"],
        "correct": 0
    },
    {
        "question": "ما هو تصنيف كتاب 'أولاد حارتنا' لنجيب محفوظ؟",
        "options": ["أدب رمزي", "أدب بوليسي", "أدب اجتماعي", "أدب فانتازي"],
        "correct": 0
    },
    {
        "question": "إلى أي تصنيف ينتمي كتاب 'الزنبقة السوداء' لألكسندر دوما؟",
        "options": ["رواية تاريخية", "رواية مغامرات", "رواية رومانسية", "رواية بوليسية"],
        "correct": 0
    },
    {
        "question": "أي تصنيف ينتمي إليه كتاب 'إلى المنارة' لفرجينيا وولف؟",
        "options": ["أدب حداثي", "أدب وجودي", "أدب رعب", "أدب خيال علمي"],
        "correct": 0
    },
    {
        "question": "ما هو تصنيف كتاب 'العمى' لخوسيه ساراماغو؟",
        "options": ["أدب ديستوبي", "أدب سيريالي", "أدب بوليسي", "أدب تاريخي"],
        "correct": 0
    },
    {
        "question": "إلى أي تصنيف ينتمي كتاب 'دون كيشوت' لميغيل دي ثيربانتس؟",
        "options": ["أدب ساخر", "أدب ملحمي", "أدب اجتماعي", "أدب ديستوبي"],
        "correct": 0
    },
    {
        "question": "أي تصنيف ينتمي إليه كتاب 'اسم الوردة' لأومبرتو إيكو؟",
        "options": ["رواية بوليسية", "رواية تاريخية", "أدب فلسفي", "أدب فانتازي"],
        "correct": 1
    },
     {
        "question": "من هو الكاتب الذي قال: 'كلما ازداد علمنا اتسعت دائرتنا المظلمة'؟",
        "options": ["ألبير كامو", "نيتشه", "نجيب محفوظ", "دوستويفسكي"],
        "correct": 0
    },
    {
        "question": "من هو الكاتب الذي قال: 'العقل هو النور الوحيد الذي يسير في عمق الظلام'؟",
        "options": ["أرسطو", "أبو العلاء المعري", "جان بول سارتر", "توماس هوبز"],
        "correct": 1
    },
    {
        "question": "من هو الكاتب الذي قال: 'إن كل كلمة تنطق بها حتى وإن كانت مزحة، فإنها تترك أثراً في نفس المستمع'؟",
        "options": ["دوستويفسكي", "فيكتور هوجو", "ويليام شكسبير", "غوته"],
        "correct": 0
    },
    {
        "question": "من هو الكاتب الذي قال: 'من لا يفكر في الشؤون البعيدة سيجد المتاعب قريبة منه'؟",
        "options": ["كونفوشيوس", "سقراط", "نيكولو مكيافيلي", "جان جاك روسو"],
        "correct": 0
    },
    {
        "question": "من هو الكاتب الذي قال: 'الحياة ليست إلا وقفة مع البؤس'؟",
        "options": ["جان بول سارتر", "ألبير كامو", "صمويل بيكيت", "فرانز كافكا"],
        "correct": 1
    },
    {
        "question": "من هو الكاتب الذي قال: 'الشجاعة هي اكتساب الخبرة وعدم الاستسلام للقلق'؟",
        "options": ["جون لوك", "توماس هوبز", "جان بول سارتر", "نيتشه"],
        "correct": 3
    },
    {
        "question": "من هو الكاتب الذي قال: 'الذين لا يذكرون الماضي محكوم عليهم بتكراره'؟",
        "options": ["جورج سانتايانا", "ألبير كامو", "فيكتور هوجو", "وليم جيمس"],
        "correct": 0
    },
    {
        "question": "من هو الكاتب الذي قال: 'يولد الإنسان حراً، ولكنه في كل مكان يجرّ سلاسل الاستعباد'؟",
        "options": ["جون لوك", "جان جاك روسو", "توماس هوبز", "جان بول سارتر"],
        "correct": 1
    },
    {
        "question": "من هو الكاتب الذي قال: 'البحث عن الحقيقة أكثر أهمية من امتلاكها'؟",
        "options": ["سقراط", "أرسطو", "نجيب محفوظ", "جان جاك روسو"],
        "correct": 0
    },
    {
        "question": "من هو الكاتب الذي قال: 'الناس لا يكرهونك لعيوبك، بل لعيوبهم هم'؟",
        "options": ["دوستويفسكي", "ألبير كامو", "غوته", "سارتر"],
        "correct": 2
    },
    {
        "question": "من هو الكاتب الذي قال: 'إذا كنت تقدر على الحب، فحب بلا شروط'؟",
        "options": ["جبران خليل جبران", "ألبير كامو", "غوته", "باولو كويلو"],
        "correct": 0
    },
    {
        "question": "من هو الكاتب الذي قال: 'كلّما عرف الإنسان أكثر قلّ احتمال وقوعه في أخطاء'؟",
        "options": ["فرنسيس بيكون", "توماس هوبز", "جون لوك", "نيكولو مكيافيلي"],
        "correct": 0
    },
    {
        "question": "من هو الكاتب الذي قال: 'في حياتي كلها، لم أحظى بأكثر من لحظات قليلة كانت الحرية فيها حقيقية'؟",
        "options": ["ألبير كامو", "جورج أورويل", "فرانز كافكا", "صمويل بيكيت"],
        "correct": 2
    },
    {
        "question": "من هو الكاتب الذي قال: 'أن تخسر معركةً لا يعني أنك خسرت الحرب'؟",
        "options": ["نابليون بونابرت", "فيكتور هوجو", "نجيب محفوظ", "تولستوي"],
        "correct": 0
    },
    {
        "question": "من هو الكاتب الذي قال: 'كلنا نولد ونسكن أرضاً واحدة، ولكننا لا نعيش جميعاً تحت سماء واحدة'؟",
        "options": ["هوميروس", "دوستويفسكي", "ألبير كامو", "شكسبير"],
        "correct": 1
    },
    {
        "question": "من هو الكاتب الذي قال: 'أعرف ما هو الأفضل لي، ولكنني لا أستطيع فعله'؟",
        "options": ["هاملت (شكسبير)", "أوديب (سوفوكليس)", "جورج أورويل", "تولستوي"],
        "correct": 0
    },
    {
        "question": "من هو الكاتب الذي قال: 'إذا أردت أن تكون سعيداً، كن سعيداً'؟",
        "options": ["تولستوي", "نيتشه", "دوستويفسكي", "باولو كويلو"],
        "correct": 0
    },
    {
        "question": "من هو الكاتب الذي قال: 'التفكير وحده لا يقود إلى شيء، يجب أن يكون مقروناً بالعمل'؟",
        "options": ["سارتر", "توماس هوبز", "نيكولو مكيافيلي", "جورج أورويل"],
        "correct": 2
    },
    {
        "question": "من هو الكاتب الذي قال: 'كلما أحببتك أكثر، زادت قسوتك'؟",
        "options": ["فرانز كافكا", "دوستويفسكي", "جان بول سارتر", "ويليام شكسبير"],
        "correct": 0
    },
    {
        "question": "من هو الكاتب الذي قال: 'الحرية تبدأ حيث ينتهي الجهل'؟",
        "options": ["فولتير", "جون لوك", "نيكولو مكيافيلي", "جان جاك روسو"],
        "correct": 0
    }
    
]


def get_main_menu_keyboard():
    keyboard = [
        ["عن التحدي", "كيفية المشاركة","موقع التحدي"],["القواعد", "المواعيد النهائية","تحميل الجوازات"],
        [InlineKeyboardButton("نصيحة اليوم", callback_data='daily_tip')],["التلخيص ببساطة","آلية التحدي","تصنيفات الكتب"],["الجوائز", "اقتراح كتاب","دردشة ذكية"],["عن التصفيات", "أبطال التحدي","معايير اختيار الكتب"],[ "اختبار معلومات"],
        ["مكتبات ومنصات كتب","منصات كتب صوتية","قصص أبطال التحدي"],
        [ "إحصائيات القراءة","مجموعة الفيسبوك","المركز الاعلامي واخر الأخبار"],
        ["مجموعات القراءة", "تحديات القراءة"]
        
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
                "/books - لعرض قائمة الكتب المقترحة\n" \
                "/register - للتسجيل في التحدي\n" \
                "/faq - للأسئلة الشائعة\n" \
                "/contact - لمعلومات الاتصال\n" \
                "/resources - للموارد المفيدة\n" \
                "/latest - لآخر الأخبار والتحديثات\n" \
                "/feedback - لتقديم الملاحظات والاقتراحات\n" \
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
import random

async def get_daily_tip() -> str:
    tips = [
        "خصص وقتًا محددًا للقراءة كل يوم، حتى لو كان 15 دقيقة فقط.",
        "حاول قراءة كتب من أنواع مختلفة لتوسيع آفاقك.",
        "ناقش ما تقرأه مع الآخرين لتعميق فهمك.",
        "دوّن الملاحظات أثناء القراءة لتحسين الفهم والتذكر.",
        "حدد أهدافًا للقراءة وكافئ نفسك عند تحقيقها.",
        "جرب القراءة بصوت عالٍ لتحسين التركيز والفهم.",
        "استخدم الفهرس وقائمة المحتويات للحصول على نظرة عامة قبل البدء في القراءة.",
        "حاول تلخيص ما قرأته بكلماتك الخاصة لترسيخ المعلومات.",
        "اقرأ في أماكن مختلفة لتجديد حماسك للقراءة.",
        "شارك اقتباساتك المفضلة مع أصدقائك لتحفيزهم على القراءة أيضًا.",
        "استخدم أدوات القراءة الإلكترونية لتسهيل الوصول إلى الكتب.",
        "اقرأ في أوقات هادئة وخالية من الإلهاء لزيادة التركيز.",
        "احرص على قراءة الكتب التي تناسب اهتماماتك الشخصية.",
        "استمع إلى الكتب الصوتية كوسيلة مكملة للقراءة.",
        "راجع ما قرأته بين فترة وأخرى لتثبيت المعلومات.",
        "اقرأ كتبًا بلغات أخرى لتعزيز مهاراتك اللغوية.",
        "خصص وقتًا لقراءة المقالات والأخبار بشكل يومي.",
        "اقرأ مع مجموعة لتبادل الأفكار والتجارب.",
        "استخدم تقنية القراءة السريعة لزيادة عدد الكتب التي تقرأها.",
        "اجعل القراءة جزءًا من روتينك اليومي لتحسين الاستمرارية.",
        "اقرأ الكتب التي تفتح آفاقًا جديدة وتقدم لك تحديات.",
        "اكتب مراجعات عن الكتب التي تقرأها لتعميق فهمك.",
        "اقرأ في أماكن طبيعية مثل الحدائق لتحسين الاسترخاء والتركيز.",
        "تجنب القراءة في ظروف إضاءة ضعيفة للحفاظ على صحة العينين.",
        "جرب قراءة الكتب الكلاسيكية لتوسيع معرفتك الثقافية.",
        "اقرأ الكتب التي تتناول موضوعات غير مألوفة لك لتوسيع معرفتك.",
        "ابحث عن كتب جديدة من خلال التوصيات والمراجعات.",
        "خصص رفًا خاصًا في مكتبتك للكتب التي تود قراءتها قريبًا.",
        "احتفظ بمفكرة لكتابة الأفكار التي تستخلصها من الكتب.",
        "اقرأ كتبًا تثير فضولك وتجعلك ترغب في معرفة المزيد.",
        "شارك في نوادي القراءة لمناقشة الأفكار مع الآخرين.",
        "احرص على قراءة الكتب التي تساعدك على تطوير ذاتك.",
        "تجنب الإجهاد أثناء القراءة، وتوقف لأخذ استراحة عند الحاجة.",
        "اقرأ كتبًا تعزز من معرفتك في مجالك المهني.",
        "استمتع بالقراءة كوسيلة للاسترخاء والهروب من ضغوط الحياة.",
        "استخدم مواقع التواصل الاجتماعي لمشاركة قراءاتك مع الآخرين.",
        "اقرأ الكتب التي تقدم لك نصائح عملية يمكنك تطبيقها في حياتك اليومية.",
        "تابع المدونات والمقالات التي تركز على مواضيع تهتم بها.",
        "اختر كتبًا تحتوي على رسوم توضيحية لتحسين فهمك للمواضيع المعقدة.",
        "احرص على تنويع قراءاتك بين الكتب العلمية والفنية والأدبية."
    ]
    return f"نصيحة اليوم:\n\n{random.choice(tips)}"

async def get_response_for_choice(choice: str, context: ContextTypes.DEFAULT_TYPE) -> str:
    responses = {
        "قصص أبطال التحدي": ("""
شدوى الزغبي، بطلة التحدي على مستوى الجمهورية في الموسم السادس.
\nhttps://www.instagram.com/reel/Ckx3rxaMBGn/?igsh=bHp5Y3llazVuNG96\n\n
على محمد جبريل، بطل تحدي القراءة العربي من فئة ذوي الهمم في الموسم السابع.
\nhttps://www.instagram.com/reel/Ckf4546Aeum/?igsh=MXF2azN0d3Vwa3hrYg==\n\n
شام البكور، البطلة التي نهضت من تحت الركام بسوريا وفازت بالمركز الأول في تحدي القراءة العربي لعام ٢٠٢١/٢٠٢٢.
\nhttps://www.instagram.com/reel/CkV20x6sv0K/?igsh=MTR6eWEzaXR6c2w3NA==\n\n
لجين محمد سرحان، بطلة الموسم السادس لتحدي القراءة العربي بجمهورية مصر العربية، التي فازت بعد العديد من المحاولات بفضل إيمانها.
\nhttps://www.instagram.com/reel/CilHxFMhHEE/?igsh=MWozenBnZ2huajBkag==\n\n
أسيل مصلح، بطلة تحدي القراءة العربي في الموسم السادس بفلسطين.
\nhttps://www.instagram.com/reel/Ckx3rxaMBGn/?igsh=bHp5Y3llazVuNG96\n\n
عبد العزيز الخالدي، بطل تحدي القراءة العربي بالكويت، الذي حوَّل الألم إلى شعلة من الأمل بعد وفاة أخيه بسبب السرطان.
\nhttps://www.instagram.com/reel/CilHxFMhHEE/?igsh=MWozenBnZ2huajBkag==\n
"""),
        "منصات كتب صوتية": ("قائمة قنوات الكتب الصوتية:https://t.me/addlist/5MFa5yJgpug1NzJh\n\n"
            "كتاب صوتي: https://www.kitabSawti.com \n"
        "منصة مشهورة تقدم مكتبة واسعة من الكتب الصوتية باللغة العربية في مختلف المجالات. يتوفر التطبيق على نظامي iOS وAndroid.\n"
        "Storytel: https://www.storytel.com \n"
        "منصة عالمية تحتوي على مكتبة كبيرة من الكتب الصوتية، بما في ذلك العديد من الكتب العربية. التطبيق متاح على iOS وAndroid.\n"
        "أوديو كتاب: https://www.audiobookarabia.com \n"
        "منصة تحتوي على مجموعة واسعة من الكتب الصوتية باللغة العربية، مع التركيز على الأدب الكلاسيكي والحديث.\n"
        "أبجد: https://www.abjjad.com \n"
        "منصة تجمع بين الكتب الصوتية والإلكترونية باللغة العربية، مع تقديم تجربة استماع سهلة ومريحة.\n"
        "اقرأ لي: https://www.iqraaly.com \n"
        "تطبيق يقدم كتبًا صوتية باللغة العربية بالإضافة إلى ملخصات للكتب في مجالات متعددة مثل الأدب والتنمية الذاتية.\n"
        "ضاد: https://www.daad.ae \n"
        "منصة توفر مجموعة واسعة من الكتب الصوتية باللغة العربية، تشمل الروايات والكتب الفكرية.\n" 
        ),
        "نصيحة اليوم": await get_daily_tip(),
        "مكتبات ومنصات كتب": (
            "موقع جود ريدز: https://www.goodreads.com /\n"
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
    
    # إرسال الصورة مع الرسالة
    if 'image' in book and book['image']:
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=book['image'],
            caption=message,
            reply_markup=reply_markup
        )
    else:
        await query.edit_message_text(message, reply_markup=reply_markup)
    
    return CHOOSING
async def books_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("هنا يمكنك العثور على قائمة الكتب المقترحة للتحدي.", reply_markup=get_main_menu_keyboard())
    return CHOOSING

async def register_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("للتسجيل في التحدي، يرجى اتباع الخطوات التالية: [خطوات التسجيل]", reply_markup=get_main_menu_keyboard())
    return CHOOSING

async def faq_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("إليك بعض الأسئلة الشائعة حول تحدي القراءة العربي: [قائمة الأسئلة والأجوبة]", reply_markup=get_main_menu_keyboard())
    return CHOOSING

async def contact_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("للتواصل معنا، يرجى استخدام المعلومات التالية: [معلومات الاتصال]", reply_markup=get_main_menu_keyboard())
    return CHOOSING

async def resources_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("إليك بعض الموارد المفيدة للمشاركة في التحدي: [قائمة الموارد]", reply_markup=get_main_menu_keyboard())
    return CHOOSING

async def latest_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("آخر الأخبار والتحديثات حول تحدي القراءة العربي: [آخر الأخبار]", reply_markup=get_main_menu_keyboard())
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
async def handle_rating(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    
    rating = int(query.data.split('_')[1])
    book_id = context.user_data.get('last_recommended_book')
    
    if book_id:
        # Here you would typically save the rating to your database
        # For example:
        # c.execute("INSERT INTO book_ratings (user_id, book_id, rating) VALUES (?, ?, ?)",
        #           (query.from_user.id, book_id, rating))
        # conn.commit()
        
        await query.message.reply_text(f"شكرًا لتقييمك! لقد قمت بتقييم الكتاب بـ {rating} نجوم.")
    else:
        await query.message.reply_text("عذرًا، لم نتمكن من العثور على الكتاب المقيم.")
    
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
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('info', show_challenge_info))
    application.add_handler(CommandHandler('participate', show_participation_steps))
    application.add_handler(CommandHandler('prizes', show_challenge_prizes))
    application.add_handler(CommandHandler('book_criteria', show_book_selection_criteria))
    application.add_handler(CommandHandler('champions', show_challenge_champions))
    application.add_handler(CommandHandler('books', books_command))
    application.add_handler(CommandHandler('register', register_command))
    application.add_handler(CommandHandler('faq', faq_command))
    application.add_handler(CommandHandler('contact', contact_command))
    application.add_handler(CommandHandler('resources', resources_command))
    application.add_handler(CommandHandler('latest', latest_command))
    application.add_error_handler(error_handler)
    application.run_polling()

if __name__ == '__main__':
    main()
