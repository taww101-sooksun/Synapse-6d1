import streamlit as st
import time
import firebase_admin
from firebase_admin import credentials, firestore, storage
import uuid # สำหรับสร้างชื่อไฟล์ที่ไม่ซ้ำกัน
from datetime import datetime # สำหรับฟอร์แมต timestamp

# --- Translation Dictionary (ส่วนใหม่สำหรับระบบ 6 ภาษา) ---
translations = {
    "app_title": {
        "en": "SYNAPSE 6D : THE ULTIMATE",
        "th": "SYNAPSE 6D : สุดยอดมิติ",
        "lo": "SYNAPSE 6D : ສຸດຍອດມິຕິ",
        "my": "SYNAPSE 6D : အပြီးပြတ်",
        "zh": "SYNAPSE 6D : 终极",
        "ja": "SYNAPSE 6D : 究極"
    },
    "choose_language": {
        "en": "🌐 Choose Language",
        "th": "🌐 เลือกภาษา",
        "lo": "🌐 ເລືອກພາສາ",
        "my": "🌐 ဘာသာစကားရွေးပါ",
        "zh": "🌐 选择语言",
        "ja": "🌐 言語を選択"
    },
    "user_label": {
        "en": "👤 Username:",
        "th": "👤 ชื่อผู้ใช้:",
        "lo": "👤 ຊື່ຜູ້ໃຊ້:",
        "my": "👤 အသုံးပြုသူအမည်:",
        "zh": "👤 用户名:",
        "ja": "👤 ユーザー名:"
    },
    "password_label": {
        "en": "🔑 Password:",
        "th": "🔑 รหัสผ่าน:",
        "lo": "🔑 ລະຫັດຜ່ານ:",
        "my": "🔑 စကားဝှက်:",
        "zh": "🔑 密码:",
        "ja": "🔑 パスワード:"
    },
    "login_button": {
        "en": "🚀 Enter the Dimension",
        "th": "🚀 ยืนยันรหัสเข้าสู่มิติ",
        "lo": "🚀 ຢືນຢັນລະຫັດເຂົ້າສູ່ມິຕິ",
        "my": "🚀 ရှုထောင့်ထဲသို့ဝင်ရန်",
        "zh": "🚀 进入维度",
        "ja": "🚀 次元に入る"
    },
    "login_error": {
        "en": "Please enter username and password.",
        "th": "กรุณาใส่ชื่อผู้ใช้และรหัสผ่าน",
        "lo": "ກະລຸນາໃສ່ຊື່ຜູ້ໃຊ້ ແລະ ລະຫັດຜ່ານ",
        "my": "အသုံးပြုသူအမည်နှင့် စကားဝှက်ထည့်ပါ",
        "zh": "请输入用户名和密码",
        "ja": "ユーザー名とパスワードを入力してください"
    },
    "description_header": {
        "en": "📖 **Description of 5 Therapy Rooms:**",
        "th": "📖 **คำอธิบาย 5 ห้องบำบัด:**",
        "lo": "📖 **ລາຍລະອຽດ 5 ຫ້ອງບຳບັດ:**",
        "my": "📖 **ကုထုံးခန်း ၅ ခန်း၏ဖော်ပြချက်:**",
        "zh": "📖 **5 个治疗室的描述:**",
        "ja": "📖 **5 つのセラピールームの説明:**"
    },
    "red_room_desc": {
        "en": "🔴 **RED:** YouTube-style Feed Room, post photos/videos",
        "th": "🔴 **RED:** ห้องระบาย Feed แบบ YouTube โพสต์รูป/คลิปได้",
        "lo": "🔴 **RED:** ຫ້ອງ Feed ແບບ YouTube ໂພສຮູບ/ຄລິບໄດ້",
        "my": "🔴 **RED:** YouTube ပုံစံ Feed Room၊ ဓာတ်ပုံ/ဗီဒီယိုတင်နိုင်သည်",
        "zh": "🔴 **RED:** YouTube 风格动态室，可发布照片/视频",
        "ja": "🔴 **RED:** YouTube スタイルのフィードルーム、写真/ビデオを投稿可能"
    },
    "blue_room_desc": {
        "en": "🔵 **BLUE:** Free Call & Facebook-style Social Room",
        "th": "🔵 **BLUE:** ห้องโทรฟรี & Social แบบ Facebook",
        "lo": "🔵 **BLUE:** ຫ້ອງໂທຟຣີ & Social ແບບ Facebook",
        "my": "🔵 **BLUE:** ဖရီးခေါ်ဆိုမှု & Facebook ပုံစံ လူမှုကွန်ရက်ခန်း",
        "zh": "🔵 **BLUE:** 免费通话和 Facebook 风格社交室",
        "ja": "🔵 **BLUE:** 無料通話と Facebook スタイルのソーシャルルーム"
    },
    "green_room_desc": {
        "en": "🟢 **GREEN:** Secret Group Chat Room, falling snow, fireworks",
        "th": "🟢 **GREEN:** ห้องแชทลับเฉพาะกลุ่ม หิมะร่วง ดอกไม้ไฟ",
        "lo": "🟢 **GREEN:** ຫ້ອງແຊັດລັບສະເພາະກຸ່ມ ຫິມະຕົກ ດອກໄມ້ໄຟ",
        "my": "🟢 **GREEN:** လျှို့ဝှက်အဖွဲ့ချတ်ခန်း၊ နှင်းကျ၊ မီးပန်း",
        "zh": "🟢 **GREEN:** 秘密群聊室，雪花飘落，烟花绽放",
        "ja": "🟢 **GREEN:** 秘密のグループチャットルーム、雪が降り、花火が上がる"
    },
    "black_room_desc": {
        "en": "⚫ **BLACK:** Private Room, manage friend list",
        "th": "⚫ **BLACK:** ห้องส่วนตัว จัดการยอดเพื่อน",
        "lo": "⚫ **BLACK:** ຫ້ອງສ່ວນຕົວ ຈັດການຍອດໝູ່",
        "my": "⚫ **BLACK:** ကိုယ်ပိုင်အခန်း၊ သူငယ်ချင်းစာရင်းကိုစီမံရန်",
        "zh": "⚫ **BLACK:** 私人房间，管理好友列表",
        "ja": "⚫ **BLACK:** プライベートルーム、フレンドリストの管理"
    },
    "purple_room_desc": {
        "en": "🟣 **PURPLE:** AI Fortune-telling/Confidant Room, quirky but sincere",
        "th": "🟣 **PURPLE:** ห้อง AI ดูดวง ปรับทุกข์ กวนๆ แต่จริงใจ",
        "lo": "🟣 **PURPLE:** ຫ້ອງ AI ເບິ່ງດວງ ປັບທຸກ ກວນໆ ແຕ່ຈິງໃຈ",
        "my": "🟣 **PURPLE:** AI ဗေဒင်/ရင်ဖွင့်ခန်း၊ ထူးဆန်းသော်လည်း စိတ်ရင်းမှန်သည်",
        "zh": "🟣 **PURPLE:** AI 算命/知己室，古怪但真诚",
        "ja": "🟣 **PURPLE:** AI 占い/悩み相談室、風変わりだが誠実"
    },
    "welcome_message": {
        "en": "## Welcome, {user_id} 🔓",
        "th": "## ยินดีต้อนรับคุณ {user_id} 🔓",
        "lo": "## ຍິນດີຕ້ອນຮັບທ່ານ {user_id} 🔓",
        "my": "## ကြိုဆိုပါသည်, {user_id} 🔓",
        "zh": "## 欢迎, {user_id} 🔓",
        "ja": "## ようこそ, {user_id} 様 🔓"
    },
    "enter_red_room": {
        "en": "🔴 Enter RED ROOM (YouTube Feed)",
        "th": "🔴 เข้าสู่มิติแดง (RED ROOM - YouTube Feed)",
        "lo": "🔴 ເຂົ້າສູ່ມິຕິແດງ (RED ROOM - YouTube Feed)",
        "my": "🔴 RED ROOM (YouTube Feed) ထဲသို့ဝင်ရန်",
        "zh": "🔴 进入红色房间 (YouTube 动态)",
        "ja": "🔴 レッドルームに入る (YouTube フィード)"
    },
    "enter_blue_room": {
        "en": "🔵 Enter BLUE ROOM (Facebook Social)",
        "th": "🔵 เข้าสู่มิติน้ำเงิน (BLUE ROOM - Facebook Social)",
        "lo": "🔵 ເຂົ້າສູ່ມິຕິນ້ຳເງິນ (BLUE ROOM - Facebook Social)",
        "my": "🔵 BLUE ROOM (Facebook Social) ထဲသို့ဝင်ရန်",
        "zh": "🔵 进入蓝色房间 (Facebook 社交)",
        "ja": "🔵 ブルールームに入る (Facebook ソーシャル)"
    },
    "enter_green_room": {
        "en": "🟢 Enter GREEN ROOM (Secret Chat)",
        "th": "🟢 เข้าสู่มิติเขียว (GREEN ROOM - Secret Chat)",
        "lo": "🟢 ເຂົ້າສູ່ມິຕິຂຽວ (GREEN ROOM - Secret Chat)",
        "my": "🟢 GREEN ROOM (လျှို့ဝှက်ချတ်) ထဲသို့ဝင်ရန်",
        "zh": "🟢 进入绿色房间 (秘密聊天)",
        "ja": "🟢 グリーンルームに入る (秘密チャット)"
    },
    "enter_black_room": {
        "en": "⚫ Enter BLACK ROOM (Private Master)",
        "th": "⚫ เข้าสู่มิติดำ (BLACK ROOM - Private Master)",
        "lo": "⚫ ເຂົ້າສູ່ມິຕິດຳ (BLACK ROOM - Private Master)",
        "my": "⚫ BLACK ROOM (ကိုယ်ပိုင်မာစတာ) ထဲသို့ဝင်ရန်",
        "zh": "⚫ 进入黑色房间 (私人主控)",
        "ja": "⚫ ブラックルームに入る (プライベートマスター)"
    },
    "enter_purple_room": {
        "en": "🟣 Enter AI PURPLE (Fortune/Confidant)",
        "th": "🟣 เข้าสู่มิติม่วง (AI PURPLE - ดูดวง/ปรับทุกข์)",
        "lo": "🟣 ເຂົ້າສູ່ມິຕິມ່ວງ (AI PURPLE - ເບິ່ງດວງ/ປັບທຸກ)",
        "my": "🟣 AI PURPLE (ဗေဒင်/ရင်ဖွင့်) ထဲသို့ဝင်ရန်",
        "zh": "🟣 进入紫色房间 (AI 算命/知己)",
        "ja": "🟣 パープルルームに入る (AI 占い/悩み相談)"
    },
    "red_room_header": {
        "en": "🔴 RED ROOM : YouTube Style Feed",
        "th": "🔴 RED ROOM : ฟีดสไตล์ YouTube",
        "lo": "🔴 RED ROOM : ຟີດສະຕາຍ YouTube",
        "my": "🔴 RED ROOM : YouTube ပုံစံ Feed",
        "zh": "🔴 红色房间 : YouTube 风格动态",
        "ja": "🔴 レッドルーム : YouTube スタイルフィード"
    },
    "write_post_label": {
        "en": "✍️ Write your message:",
        "th": "✍️ เขียนข้อความของคุณ:",
        "lo": "✍️ ຂຽນຂໍ້ຄວາມຂອງທ່ານ:",
        "my": "✍️ သင့်မက်ဆေ့ခ်ျကိုရေးပါ:",
        "zh": "✍️ 写下您的留言:",
        "ja": "✍️ メッセージを書いてください:"
    },
    "upload_file_label": {
        "en": "📂 Upload file (image/video)",
        "th": "📂 อัปโหลดไฟล์ (รูปภาพ/วิดีโอ)",
        "lo": "📂 ອັບໂຫຼດໄຟລ໌ (ຮູບພາບ/ວິດີໂອ)",
        "my": "📂 ဖိုင်တင်ပါ (ပုံ/ဗီဒီယို)",
        "zh": "📂 上传文件 (图片/视频)",
        "ja": "📂 ファイルをアップロード (画像/動画)"
    },
    "post_button": {
        "en": "📮 Post to Feed",
        "th": "📮 โพสต์ลงฟีด",
        "lo": "📮 ໂພສລົງຟີດ",
        "my": "📮 Feed သို့တင်ရန်",
        "zh": "📮 发布到动态",
        "ja": "📮 フィードに投稿"
    },
    "firebase_warn_init": {
        "en": "Firebase is not configured correctly. Posting and feed display functions will not work. Please check your .streamlit/secrets.toml and Service Account Key.",
        "th": "Firebase ไม่ได้ถูกตั้งค่าอย่างถูกต้อง ฟังก์ชันการโพสต์และแสดงฟีดจะไม่ทำงาน โปรดตรวจสอบไฟล์ .streamlit/secrets.toml และ Service Account Key ของคุณ",
        "lo": "Firebase ບໍ່ໄດ້ຖືກຕັ້ງຄ່າຢ່າງຖືກຕ້ອງ. ຟັງຊັນການໂພສ ແລະ ການສະແດງຟີດຈະບໍ່ເຮັດວຽກ. ກະລຸນາກວດສອບໄຟລ໌ .streamlit/secrets.toml ແລະ Service Account Key ຂອງທ່ານ.",
        "my": "Firebase ကိုမှန်ကန်စွာပြင်ဆင်မထားပါ။ ပို့စ်တင်ခြင်းနှင့် Feed ပြသခြင်းလုပ်ဆောင်ချက်များ အလုပ်လုပ်မည်မဟုတ်ပါ။ သင်၏ .streamlit/secrets.toml နှင့် Service Account Key ကိုစစ်ဆေးပါ။",
        "zh": "Firebase 未正确配置。发布和动态显示功能将无法工作。请检查您的 .streamlit/secrets.toml 和服务帐号密钥。",
        "ja": "Firebase が正しく設定されていません。投稿およびフィード表示機能は動作しません。.streamlit/secrets.toml とサービスアカウントキーを確認してください。"
    },
    "firebase_success_init": {
        "en": "Firebase Initialized Successfully!",
        "th": "เริ่มต้น Firebase สำเร็จแล้ว!",
        "lo": "ເລີ່ມຕົ້ນ Firebase ສຳເລັດແລ້ວ!",
        "my": "Firebase ကိုအောင်မြင်စွာစတင်ခဲ့သည်!",
        "zh": "Firebase 初始化成功！",
        "ja": "Firebase が正常に初期化されました！"
    },
    "firebase_error_init": {
        "en": "Error initializing Firebase:",
        "th": "ข้อผิดพลาดในการเริ่มต้น Firebase:",
        "lo": "ຂໍ້ຜິດພາດໃນການເລີ່ມຕົ້ນ Firebase:",
        "my": "Firebase စတင်ရာတွင်အမှား:",
        "zh": "初始化 Firebase 时出错:",
        "ja": "Firebase の初期化エラー:"
    },
    "file_upload_success": {
        "en": "File uploaded successfully:",
        "th": "ไฟล์อัปโหลดสำเร็จ:",
        "lo": "ອັບໂຫຼດໄຟລ໌ສຳເລັດ:",
        "my": "ဖိုင်ကိုအောင်မြင်စွာတင်ခဲ့သည်:",
        "zh": "文件上传成功:",
        "ja": "ファイルのアップロードに成功しました:"
    },
    "file_upload_error": {
        "en": "Error uploading file:",
        "th": "ข้อผิดพลาดในการอัปโหลดไฟล์:",
        "lo": "ຂໍ້ຜິດພາດໃນການອັບໂຫຼດໄຟລ໌:",
        "my": "ဖိုင်တင်ရာတွင်အမှား:",
        "zh": "文件上传错误:",
        "ja": "ファイルのアップロードエラー:"
    },
    "post_success": {
        "en": "Post successful!",
        "th": "โพสต์เรียบร้อย!",
        "lo": "ໂພສສຳເລັດ!",
        "my": "ပို့စ်အောင်မြင်သည်!",
        "zh": "发布成功！",
        "ja": "投稿成功！"
    },
    "post_warn_empty": {
        "en": "Please write a message or upload a file before posting.",
        "th": "กรุณาเขียนข้อความหรืออัปโหลดไฟล์ก่อนโพสต์",
        "lo": "ກະລຸນາຂຽນຂໍ້ຄວາມ ຫຼື ອັບໂຫຼດໄຟລ໌ກ່ອນໂພສ",
        "my": "ပို့စ်မတင်မီ မက်ဆေ့ခ်ျရေးပါ သို့မဟုတ် ဖိုင်တင်ပါ",
        "zh": "发布前请写下消息或上传文件",
        "ja": "投稿する前にメッセージを書き込むかファイルをアップロードしてください"
    },
    "latest_feed_header": {
        "en": "Latest Feed:",
        "th": "ฟีดล่าสุด:",
        "lo": "ຟີດລ່າສຸດ:",
        "my": "နောက်ဆုံး Feed:",
        "zh": "最新动态:",
        "ja": "最新フィード:"
    },
    "posted_by": {
        "en": "Posted by {user_id} on {timestamp}",
        "th": "โพสต์โดย {user_id} เมื่อ {timestamp}",
        "lo": "ໂພສໂດຍ {user_id} ເມື່ອ {timestamp}",
        "my": "{user_id} မှ {timestamp} တွင်တင်ခဲ့သည်",
        "zh": "由 {user_id} 发布于 {timestamp}",
        "ja": "{user_id} が {timestamp} に投稿"
    },
    "unknown_user": {
        "en": "Unknown User",
        "th": "ผู้ใช้ไม่ระบุ",
        "lo": "ຜູ້ໃຊ້ບໍ່ລະບຸ",
        "my": "အမည်မသိအသုံးပြုသူ",
        "zh": "未知用户",
        "ja": "不明なユーザー"
    },
    "post_content_placeholder": {
        "en": "Emotion content...", # This was a placeholder in your original example feed
        "th": "เนื้อหาการระบายอารมณ์...",
        "lo": "ເນື້ອໃນການລະບາຍອາລົມ...",
        "my": "စိတ်ခံစားမှုအကြောင်းအရာ...",
        "zh": "情感内容...",
        "ja": "感情の内容..."
    },
    "image_caption": {
        "en": "Posted image",
        "th": "รูปภาพโพสต์",
        "lo": "ຮູບພາບໂພສ",
        "my": "တင်ထားသောပုံ",
        "zh": "发布的图片",
        "ja": "投稿画像"
    },
    "media_link": {
        "en": "Media:",
        "th": "สื่อ:",
        "lo": "ສື່:",
        "my": "မီဒီယာ:",
        "zh": "媒体:",
        "ja": "メディア:"
    },
    "like_button": {
        "en": "❤️ Like ({count})",
        "th": "❤️ ถูกใจ ({count})",
        "lo": "❤️ ຖືກໃຈ ({count})",
        "my": "❤️ ကြိုက်သည် ({count})",
        "zh": "❤️ 赞 ({count})",
        "ja": "❤️ いいね ({count})"
    },
    "comment_button": {
        "en": "💬 Comment",
        "th": "💬 แสดงความคิดเห็น",
        "lo": "💬 ຄຳເຫັນ",
        "my": "💬 မှတ်ချက်",
        "zh": "💬 评论",
        "ja": "💬 コメント"
    },
    "share_button": {
        "en": "🔗 Share",
        "th": "🔗 แชร์",
        "lo": "🔗 ແຊຣ໌",
        "my": "🔗 မျှဝေပါ",
        "zh": "🔗 分享",
        "ja": "🔗 シェア"
    },
    "feed_load_error": {
        "en": "Could not load feed: {error}. Check Firebase settings and Security Rules.",
        "th": "ไม่สามารถโหลดฟีดได้: {error}. ตรวจสอบการตั้งค่า Firebase และกฎ Security Rules.",
        "lo": "ບໍ່ສາມາດໂຫຼດຟີດໄດ້: {error}. ກວດສອບການຕັ້ງຄ່າ Firebase ແລະກົດ Security Rules.",
        "my": "Feed ကိုတင်မရပါ: {error}. Firebase ဆက်တင်များနှင့် လုံခြုံရေးစည်းမျဉ်းများကိုစစ်ဆေးပါ။",
        "zh": "无法加载动态: {error}。请检查 Firebase 设置和安全规则。",
        "ja": "フィードを読み込めませんでした: {error}。Firebase の設定とセキュリティルールを確認してください。"
    },
    "check_firebase_config_rules": {
        "en": "Please ensure you have correctly configured Firebase Admin SDK and Firestore/Storage Security Rules.",
        "th": "โปรดตรวจสอบว่าคุณได้ตั้งค่า Firebase Admin SDK และกฎ Security Rules ของ Firestore/Storage อย่างถูกต้อง.",
        "lo": "ກະລຸນາກວດສອບວ່າທ່ານໄດ້ຕັ້ງຄ່າ Firebase Admin SDK ແລະກົດ Security Rules ຂອງ Firestore/Storage ຢ່າງຖືກຕ້ອງ.",
        "my": "Firebase Admin SDK နှင့် Firestore/Storage လုံခြုံရေးစည်းမျဉ်းများကို မှန်ကန်စွာပြင်ဆင်ထားကြောင်း သေချာပါစေ။",
        "zh": "请确保您已正确配置 Firebase Admin SDK 和 Firestore/Storage 安全规则。",
        "ja": "Firebase Admin SDK と Firestore/Storage セキュリティルールが正しく設定されていることを確認してください。"
    },
    "back_to_main": {
        "en": "⬅️ Back to Main",
        "th": "⬅️ กลับหน้าหลัก",
        "lo": "⬅️ ກັບໜ້າຫຼັກ",
        "my": "⬅️ ပင်မသို့ပြန်သွားရန်",
        "zh": "⬅️ 返回主页",
        "ja": "⬅️ メインに戻る"
    },
    "purple_room_header": {
        "en": "🟣 PURPLE ROOM : AI Confidant (Quirky but Sincere)",
        "th": "🟣 PURPLE ROOM : AI ปรับทุกข์ (กวนใจแต่จริงใจ)",
        "lo": "🟣 PURPLE ROOM : AI ປັບທຸກ (ກວນໃຈແຕ່ຈິງໃຈ)",
        "my": "🟣 PURPLE ROOM : AI ရင်ဖွင့် (ထူးဆန်းသော်လည်း စိတ်ရင်းမှန်သည်)",
        "zh": "🟣 紫色房间 : AI 知己 (古怪但真诚)",
        "ja": "🟣 パープルルーム : AI 悩み相談 (風変わりだが誠実)"
    },
    "purple_password_label": {
        "en": "🔑 Second-level secret code for Purple Room:",
        "th": "🔑 รหัสลับขั้นที่ 2 สำหรับห้องม่วง:",
        "lo": "🔑 ລະຫັດລັບຂັ້ນທີ່ 2 ສຳລັບຫ້ອງມ່ວງ:",
        "my": "🔑 Purple Room အတွက် ဒုတိယအဆင့်လျှို့ဝှက်ကုဒ်:",
        "zh": "🔑 紫色房间的二级密码:",
        "ja": "🔑 パープルルームの第2レベル秘密コード:"
    },
    "unlock_secret_button": {
        "en": "Unlock Secret",
        "th": "ปลดล็อกความลับ",
        "lo": "ປົດລັອກຄວາມລັບ",
        "my": "လျှို့ဝှက်ချက်ကိုသော့ဖွင့်ပါ",
        "zh": "解锁秘密",
        "ja": "秘密を解除"
    },
    "ai_welcome_message": {
        "en": "AI: 'Smiling... Is there anything you'd like me to tell your fortune or confess a secret?'",
        "th": "AI: 'แอบยิ้มอยู่นะจ๊ะ... มีอะไรให้ช่วยดูดวง หรืออยากระบายความลับล่ะ?'",
        "lo": "AI: 'ແອບຍິ້ມຢູ່ນະ... ມີຫຍັງຢາກໃຫ້ຊ່ວຍເບິ່ງດວງ ຫຼື ຢາກລະບາຍຄວາມລັບລະ?'",
        "my": "AI: 'ပြုံးနေတာ... ကံစမ်းပေးရမလား ဒါမှမဟုတ် လျှို့ဝှက်ချက်တစ်ခုဖွင့်ပြောချင်လား?'",
        "zh": "AI: '微笑着... 有什么想让我算命或倾诉的秘密吗？'",
        "ja": "AI: 'にっこり... 何か占ってほしいことや秘密を打ち明けたいことはありますか？'"
    },
    "write_your_message_textarea": {
        "en": "✍️ Write your message (ample space):",
        "th": "✍️ เขียนข้อความของคุณ (ช่องใหญ่จุใจ):",
        "lo": "✍️ ຂຽນຂໍ້ຄວາມຂອງທ່ານ (ຊ່ອງໃຫຍ່ພໍໃຈ):",
        "my": "✍️ သင့်မက်ဆေ့ခ်ျကိုရေးပါ (နေရာအလုံအလောက်):",
        "zh": "✍️ 写下您的留言 (充足空间):",
        "ja": "✍️ メッセージを書いてください (十分なスペース):"
    },
    "ai_analyze_button": {
        "en": "🔮 Send to AI for Analysis (accurate memory)",
        "th": "🔮 ส่งให้ AI วิเคราะห์ (ใช้ความจำแม่นยำ)",
        "lo": "🔮 ສົ່ງໃຫ້ AI ວິເຄາະ (ໃຊ້ຄວາມຈຳທີ່ຖືກຕ້ອງ)",
        "my": "🔮 AI သို့ ပေးပို့၍ ခွဲခြမ်းစိတ်ဖြာရန် (တိကျသောမှတ်ဉာဏ်)",
        "zh": "🔮 发送给 AI 分析 (准确记忆)",
        "ja": "🔮 AI に送信して分析 (正確な記憶)"
    },
    "logo_warning": {
        "en": "Please put logo.jpg in the app folder",
        "th": "กรุณาวางไฟล์ logo.jpg ในโฟลเดอร์แอปนะครับ",
        "lo": "ກະລຸນາວາງໄຟລ໌ logo.jpg ໃນໂຟນເດີແອັບເດີ",
        "my": "ကျေးဇူးပြု၍ logo.jpg ကို app folder တွင်ထားပါ",
        "zh": "请将 logo.jpg 放在应用程序文件夹中",
        "ja": "logo.jpg をアプリフォルダに入れてください"
    }
}

# Helper function to get translated text
def get_text(key):
    # Default to English if language not set or key not found for selected language
return translations.get(key, {}).get(st.session_state.lang, translations.get(key, {}).get("en", f"Translation missing for {key}"))
# --- 0. INITIAL SETUP & THEME ---
st.set_page_config(page_title=get_text("app_title"), layout="wide", initial_sidebar_state="collapsed")

# --- Firebase Initialization ---
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate(st.secrets.firebase)
        project_id = st.secrets.firebase.project_id
        firebase_admin.initialize_app(cred, {
            'storageBucket': f'{project_id}.appspot.com'
        })
        db = firestore.client()
        bucket = storage.bucket()
        st.session_state.firebase_initialized = True
        st.success(get_text("firebase_success_init"))
    except AttributeError:
        st.warning(get_text("firebase_warn_init"))
        st.session_state.firebase_initialized = False
    except Exception as e:
        st.error(f"{get_text('firebase_error_init')} {e}")
        st.session_state.firebase_initialized = False
else:
    db = firestore.client()
    bucket = storage.bucket()
    st.session_state.firebase_initialized = True


# --- 1. FUNCTION: มัดมือฟัง (เพลงบำบัด 60 เพลง - 2 หมื่นวิว) ---
def forced_therapy_radio():
    playlist_id = "PL6S211I3urvpt47sv8mhbexif2YOzs2gO"
    st.markdown(f"""
        <div style="display:none;">
            <iframe id="therapy-radio" src="https://www.youtube.com/embed/videoseries?list={playlist_id}&autoplay=1&loop=1&mute=0" allow="autoplay"></iframe>
        </div>
    """, unsafe_allow_html=True)

# --- 2. CYBERPUNK CSS (รกๆ สะท้อนแสง ปุ่มนูน) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Kanit:wght@300;500&display=swap');
    /* ส่วน CSS เดิมของคุณ */
    .stApp {
        background: linear-gradient(135deg, #ff0000, #00ff88, #0000ff, #ffff00, #ab47bc);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        color: #fff; font-family: 'Kanit', sans-serif;
    }
    @keyframes gradient { 0% {background-position: 0% 50%;} 50% {background-position: 100% 50%;} 100% {background-position: 0% 50%;} }

    .stButton>button {
        height: 80px !important; width: 100% !important;
        font-size: 22px !important; font-weight: 900 !important;
        border-radius: 15px !important; border: 4px solid rgba(255,255,255,0.3) !important;
        box-shadow: 6px 6px 15px rgba(0,0,0,0.5), inset -4px -4px 10 
        box-shadow: 6px 6px 15px rgba(0,0,0,0.5), inset -4px -4px 10px rgba(255,255,255,0.2) !important;
        background: rgba(0,0,0,0.7) !important;
        color: white !important;
        transition: all 0.3s ease;
        text-transform: uppercase;
    }
    .stButton>button:hover {
        transform: scale(1.02) translateY(-5px);
        border-color: #00ff88 !important;
        box-shadow: 0px 0px 30px rgba(0, 255, 136, 0.6) !important;
    }
    .glass-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 30px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE (จัดการสถานะ) ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'lang' not in st.session_state:
    st.session_state.lang = 'th'
if 'page' not in st.session_state:
    st.session_state.page = 'login'

# --- 4. หน้าจอ LOGIN ---
def show_login():
    st.markdown(f"<h1 style='text-align:center; font-family:Orbitron;'>{get_text('app_title')}</h1>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        
        # เลือกภาษา
        lang_map = {"English": "en", "ไทย": "th", "ລາວ": "lo", "မြန်မာ": "my", "中文": "zh", "日本語": "ja"}
        sel_lang = st.selectbox(get_text("choose_language"), list(lang_map.keys()), index=1)
        st.session_state.lang = lang_map[sel_lang]

        user = st.text_input(get_text("user_label"))
        pw = st.text_input(get_text("password_label"), type="password")
        
        if st.button(get_text("login_button")):
            if user and pw:
                st.session_state.logged_in = True
                st.session_state.user_id = user
                st.session_state.page = 'main'
                st.rerun()
            else:
                st.error(get_text("login_error"))
        st.markdown('</div>', unsafe_allow_html=True)

    # คำอธิบายมิติห้อง
    st.markdown(get_text("description_header"))
    st.info(f"{get_text('red_room_desc')}\n\n{get_text('blue_room_desc')}\n\n{get_text('green_room_desc')}")

# --- 5. หน้าจอหลัก (DASHBOARD) ---
def show_main():
    forced_therapy_radio() # เล่นเพลงบำบัดเบื้องหลัง
    
    st.markdown(get_text("welcome_message").format(user_id=st.session_state.user_id))
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button(get_text("enter_red_room")):
            st.session_state.page = 'red_room'
            st.rerun()
        if st.button(get_text("enter_blue_room")):
            st.toast("Coming Soon!")
            
    with col2:
        if st.button(get_text("enter_purple_room")):
            st.session_state.page = 'purple_room'
            st.rerun()
        if st.button(get_text("enter_green_room")):
            st.toast("Coming Soon!")

    if st.button(get_text("back_to_main")):
        st.session_state.logged_in = False
        st.session_state.page = 'login'
        st.rerun()

# --- 6. หน้าห้อง RED ROOM (ตัวอย่างการ Feed) ---
def show_red_room():
    st.markdown(f"## {get_text('red_room_header')}")
    
    if st.button(get_text("back_to_main")):
        st.session_state.page = 'main'
        st.rerun()
        
    with st.expander(get_text("write_post_label")):
        msg = st.text_area(get_text("write_post_label"), label_visibility="collapsed")
        file = st.file_uploader(get_text("upload_file_label"), type=['jpg', 'png', 'mp4'])
        if st.button(get_text("post_button")):
            st.success(get_text("post_success"))

# --- 7. ควบคุมทิศทางแอป ---
if not st.session_state.logged_in:
    show_login()
else:
    if st.session_state.page == 'main':
        show_main()
    elif st.session_state.page == 'red_room':
        show_red_room()
    elif st.session_state.page == 'purple_room':
        st.write("AI Room is under construction...")
        if st.button(get_text("back_to_main")):
            st.session_state.page = 'main'
            st.rerun()
