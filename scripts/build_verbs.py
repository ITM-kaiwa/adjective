import csv
import json
import io
import re

csv_data = """transitive verb,intransitiveverb,JP ruby,meaning Vt,meaning Vi,reibun Vi,reibun Vt
開ける,開く,あける / あく,mở (cái gì đó),"(cái gì đó) mở, tự mở",ドアが開く。,ドアを開ける。
閉める,閉まる,しめる / しまる,đóng (cái gì đó),(cái gì đó) đóng,ドアが閉まる。,ドアを閉める。
入れる,入る,いれる / はいる,"cho vào, bỏ vào","vào, đi vào",虫が中に入った。,犬を家の中に入れた。
出す,出る,だす / でる,"lấy ra, đưa ra","ra, đi ra khỏi",店から出る。,カバンから財布を出す。
つける,つく,つける / つく,"bật (điện, đèn)","(điện, đèn) sáng, bật",電気がつく。,電気をつける。
消す,消える,けす / きえる,"tắt, dập tắt","tắt, biến mất",火が消える。,火を消す。
落とす,落ちる,おとす / おちる,"làm rơi, đánh rơi","rơi, rớt",スマホが落ちる。,スマホを落とす。
壊す,壊れる,こわす / こわれる,"làm hỏng, phá hỏng","bị hỏng, bị vỡ",時計が壊れた。,時計を壊した。
汚す,汚れる,よごす / よごれる,làm bẩn,bị bẩn,服が汚れる。,服を汚す。
沸かす,沸く,わかす / わく,"đun sôi, nấu sôi",sôi,お湯が沸く。,お湯を沸かす。
始める,始まる,はじめる / はじまる,bắt đầu (cái gì),bắt đầu,授業が始まる。,授業を始める。
終える,終わる,おえる / おわる,"kết thúc, hoàn thành (cái gì)","kết thúc, xong",宿題が終わる。,宿題を終える。
続ける,続く,つづける / つづく,tiếp tục (cái gì),"tiếp diễn, kéo dài",話が続く。,話を続ける。
決める,決まる,きめる / きまる,quyết định (cái gì),được quyết định,日程が決まる。,日程を決める。
起こす,起きる,おこす / おきる,đánh thức,thức dậy,息子が起きた。,息子を起こした。
集める,集まる,あつめる / あつまる,"thu thập, tập hợp (cái gì/ai)","tập trung lại, tụ tập",人が集まる。,人を集める。
変える,変わる,かえる / かわる,"thay đổi, đổi (cái gì)","thay đổi, biến đổi",色が変わる。,色を変える。
治す,治る,なおす / なおる,"chữa trị, chữa lành","khỏi (bệnh), lành (vết thương)",怪我が治る。,怪我を治す。
残す,残る,のこす / のこる,"để lại, chừa lại","còn lại, sót lại",ご飯が残った。,ご飯を残した。
冷やす,冷える,ひやす / ひえる,"làm lạnh, ướp lạnh","trở nên lạnh, nguội đi",もうビールが冷えていますよ。,今からビールを冷やします。
戻す,戻る,もどす / もどる,"trả về, để lại chỗ cũ","quay lại, trở về",家に戻る。,元の場所に戻す。
燃やす,燃える,もやす / もえる,"đốt, thiêu đốt","cháy, bốc cháy",木が燃える。,木を燃やす。
倒す,倒れる,たおす / たおれる,"xô ngã, đánh bại, làm đổ","ngã, đổ, xỉu",敵が倒れた。,敵を倒した。
見つける,見つかる,みつける / みつかる,"tìm thấy, tìm ra","được tìm thấy, tìm ra",財布が見つかった。,財布を見つけた。
乾かす,乾く,かわかす / かわく,"sấy khô, phơi khô","khô, ráo",髪が乾いた。,髪を乾かした。
切る,切れる,きる / きれる,cắt (cái gì),"bị đứt, rách",カバンの紐が切れた。,紙を切った。
助ける,助かる,たすける / たすかる,"cứu giúp, giúp đỡ","được cứu, thoát nạn, đỡ quá",おかげで、助かったよ。,溺れている人を助けた。
ためる,たまる,ためる / たまる,"tích lũy, dành dụm","tích tụ, dồn ứ, đọng lại",お金がたまる。,お金をためる。
鳴らす,鳴る,ならす / なる,"làm rung chuông, bấm chuông, thổi còi","kêu, reo, vang lên",鐘が鳴る。,鐘を鳴らす。
染める,染まる,そめる / そまる,"nhuộm (tóc, vải)","nhuốm màu, đổi màu",赤色に染まる。,髪を染める。
溶かす,溶ける,とかす / とける,"làm tan chảy, hòa tan","tan chảy, hòa tan",アイスが溶ける。,チーズを溶かす。
重ねる,重なる,かさねる / かさなる,"chồng lên, xếp chồng lên","chồng chất, trùng lặp",本が積み重なる。,本を積み重ねる。
潰す,潰れる,つぶす / つぶれる,"nghiền nát, đè bẹp","bị nát, bị bẹp, bị sập",地震で家が潰れた。,じゃがいもを潰した。
曲げる,曲がる,まげる / まがる,"uốn cong, bẻ cong","bị cong, rẽ (hướng)",スプーンが曲がる。,スプーンを曲げる。
捕まえる,捕まる,つかまえる / つかまる,"bắt giữ, tóm lấy","bị bắt, nắm lấy",犯人が捕まる。,犯人を捕まえる。
積む,積もる,つむ / つもる,"chất lên, xếp lên","chất đống, tích tụ (tuyết)",雪が積もる。,荷物をトラックに積む。
並べる,並ぶ,ならべる / ならぶ,"sắp xếp, bày ra","xếp hàng, đứng thẳng hàng",列に並ぶ。,椅子を並べる。
こぼす,こぼれる,こぼす / こぼれる,"làm đổ, làm tràn","bị đổ, bị tràn ra",ジュースがこぼれる。,ジュースをこぼす。
乱す,乱れる,みだす / みだれる,"làm rối loạn, làm mất trật tự","bị rối, xáo trộn, mất trật tự",髪が乱れる。,髪を乱す。
届ける,届く,とどける / とどく,"gửi đến, chuyển phát, báo cáo","được gửi đến, chạm tới",手紙が届く。,手紙を届ける。
回す,回る,まわす / まわる,"xoay, quay (vật gì)","quay, xoay quanh",地球が回る。,地球儀を回す。
折る,折れる,おる / おれる,"bẻ gãy, gập lại","bị gãy, gập",骨が折れる。,骨を折る。
破る,破れる,やぶる / やぶれる,"xé rách, phá vỡ","bị rách, thủng",紙が破れる。,紙を破る。
割る,割れる,わる / われる,"làm vỡ, đập vỡ, chia nhỏ","bị vỡ, nứt",お皿が割れる。,お皿を割る。
上げる,上がる,あげる / あがる,"nâng lên, giơ lên","tăng lên, lên cao",気温が上がる。,手を上げる。
下げる,下がる,さげる / さがる,"hạ xuống, giảm xuống","giảm xuống, hạ xuống",気温が下がる。,手を下げる。"""

replacements = {
    "開ける": "<ruby>開<rt>あ</rt></ruby>ける", "開く": "<ruby>開<rt>あ</rt></ruby>く",
    "閉める": "<ruby>閉<rt>し</rt></ruby>める", "閉まる": "<ruby>閉<rt>し</rt></ruby>まる",
    "入れる": "<ruby>入<rt>い</rt></ruby>れる", "入る": "<ruby>入<rt>はい</rt></ruby>る", "入った": "<ruby>入<rt>はい</rt></ruby>った", "入れた": "<ruby>入<rt>い</rt></ruby>れた",
    "出す": "<ruby>出<rt>だ</rt></ruby>す", "出る": "<ruby>出<rt>で</rt></ruby>る",
    "消す": "<ruby>消<rt>け</rt></ruby>す", "消える": "<ruby>消<rt>き</rt></ruby>える",
    "落とす": "<ruby>落<rt>お</rt></ruby>とす", "落ちる": "<ruby>落<rt>お</rt></ruby>ちる",
    "壊す": "<ruby>壊<rt>こわ</rt></ruby>す", "壊れる": "<ruby>壊<rt>こわ</rt></ruby>れる", "壊した": "<ruby>壊<rt>こわ</rt></ruby>した", "壊れた": "<ruby>壊<rt>こわ</rt></ruby>れた",
    "汚す": "<ruby>汚<rt>よご</rt></ruby>す", "汚れる": "<ruby>汚<rt>よご</rt></ruby>れる",
    "沸かす": "<ruby>沸<rt>わ</rt></ruby>かす", "沸く": "<ruby>沸<rt>わ</rt></ruby>く",
    "始める": "<ruby>始<rt>はじ</rt></ruby>める", "始まる": "<ruby>始<rt>はじ</rt></ruby>まる",
    "終える": "<ruby>終<rt>お</rt></ruby>える", "終わる": "<ruby>終<rt>お</rt></ruby>わる",
    "続ける": "<ruby>続<rt>つづ</rt></ruby>ける", "続く": "<ruby>続<rt>つづ</rt></ruby>く",
    "決める": "<ruby>決<rt>き</rt></ruby>める", "決まる": "<ruby>決<rt>き</rt></ruby>まる",
    "起こす": "<ruby>起<rt>お</rt></ruby>こす", "起きる": "<ruby>起<rt>お</rt></ruby>きる", "起きた": "<ruby>起<rt>お</rt></ruby>きた", "起こした": "<ruby>起<rt>お</rt></ruby>こした",
    "集める": "<ruby>集<rt>あつ</rt></ruby>める", "集まる": "<ruby>集<rt>あつ</rt></ruby>まる",
    "変える": "<ruby>変<rt>か</rt></ruby>える", "変わる": "<ruby>変<rt>か</rt></ruby>わる",
    "治す": "<ruby>治<rt>なお</rt></ruby>す", "治る": "<ruby>治<rt>なお</rt></ruby>る",
    "残す": "<ruby>残<rt>のこ</rt></ruby>す", "残る": "<ruby>残<rt>のこ</rt></ruby>る", "残った": "<ruby>残<rt>のこ</rt></ruby>った", "残した": "<ruby>残<rt>のこ</rt></ruby>した",
    "冷やす": "<ruby>冷<rt>ひ</rt></ruby>やす", "冷える": "<ruby>冷<rt>ひ</rt></ruby>える", "冷やします": "<ruby>冷<rt>ひ</rt></ruby>やします", "冷えています": "<ruby>冷<rt>ひ</rt></ruby>えています",
    "戻す": "<ruby>戻<rt>もど</rt></ruby>す", "戻る": "<ruby>戻<rt>もど</rt></ruby>る",
    "燃やす": "<ruby>燃<rt>も</rt></ruby>やす", "燃える": "<ruby>燃<rt>も</rt></ruby>える",
    "倒す": "<ruby>倒<rt>たお</rt></ruby>す", "倒れる": "<ruby>倒<rt>たお</rt></ruby>れる", "倒れた": "<ruby>倒<rt>たお</rt></ruby>れた", "倒した": "<ruby>倒<rt>たお</rt></ruby>した",
    "見つける": "<ruby>見<rt>み</rt></ruby>つける", "見つかる": "<ruby>見<rt>み</rt></ruby>つかる", "見つかった": "<ruby>見<rt>み</rt></ruby>つかった", "見つけた": "<ruby>見<rt>み</rt></ruby>つけた",
    "乾かす": "<ruby>乾<rt>かわ</rt></ruby>かす", "乾く": "<ruby>乾<rt>かわ</rt></ruby>く", "乾いた": "<ruby>乾<rt>かわ</rt></ruby>いた", "乾かした": "<ruby>乾<rt>かわ</rt></ruby>かした",
    "切る": "<ruby>切<rt>き</rt></ruby>る", "切れる": "<ruby>切<rt>き</rt></ruby>れる", "切れた": "<ruby>切<rt>き</rt></ruby>れた", "切った": "<ruby>切<rt>き</rt></ruby>った",
    "助ける": "<ruby>助<rt>たす</rt></ruby>ける", "助かる": "<ruby>助<rt>たす</rt></ruby>かる", "助かった": "<ruby>助<rt>たす</rt></ruby>かった", "助けた": "<ruby>助<rt>たす</rt></ruby>けた",
    "鳴らす": "<ruby>鳴<rt>な</rt></ruby>らす", "鳴る": "<ruby>鳴<rt>な</rt></ruby>る",
    "染める": "<ruby>染<rt>そ</rt></ruby>める", "染まる": "<ruby>染<rt>そ</rt></ruby>まる",
    "溶かす": "<ruby>溶<rt>と</rt></ruby>かす", "溶ける": "<ruby>溶<rt>と</rt></ruby>ける",
    "重ねる": "<ruby>重<rt>かさ</rt></ruby>ねる", "重なる": "<ruby>重<rt>かさ</rt></ruby>なる",
    "潰す": "<ruby>潰<rt>つぶ</rt></ruby>す", "潰れる": "<ruby>潰<rt>つぶ</rt></ruby>れる", "潰れた": "<ruby>潰<rt>つぶ</rt></ruby>れた", "潰した": "<ruby>潰<rt>つぶ</rt></ruby>した",
    "曲げる": "<ruby>曲<rt>ま</rt></ruby>げる", "曲がる": "<ruby>曲<rt>ま</rt></ruby>がる",
    "捕まえる": "<ruby>捕<rt>つか</rt></ruby>まえる", "捕まる": "<ruby>捕<rt>つか</rt></ruby>まる",
    "積む": "<ruby>積<rt>つ</rt></ruby>む", "積もる": "<ruby>積<rt>つ</rt></ruby>もる", "積み": "<ruby>積<rt>つ</rt></ruby>み",
    "並べる": "<ruby>並<rt>なら</rt></ruby>べる", "並ぶ": "<ruby>並<rt>なら</rt></ruby>ぶ",
    "乱す": "<ruby>乱<rt>みだ</rt></ruby>す", "乱れる": "<ruby>乱<rt>みだ</rt></ruby>れる",
    "届ける": "<ruby>届<rt>とど</rt></ruby>ける", "届く": "<ruby>届<rt>とど</rt></ruby>く",
    "回す": "<ruby>回<rt>まわ</rt></ruby>す", "回る": "<ruby>回<rt>まわ</rt></ruby>る",
    "折る": "<ruby>折<rt>お</rt></ruby>る", "折れる": "<ruby>折<rt>お</rt></ruby>れる",
    "破る": "<ruby>破<rt>やぶ</rt></ruby>る", "破れる": "<ruby>破<rt>やぶ</rt></ruby>れる",
    "割る": "<ruby>割<rt>わ</rt></ruby>る", "割れる": "<ruby>割<rt>わ</rt></ruby>れる",
    "上げる": "<ruby>上<rt>あ</rt></ruby>げる", "上がる": "<ruby>上<rt>あ</rt></ruby>がる",
    "下げる": "<ruby>下<rt>さ</rt></ruby>げる", "下がる": "<ruby>下<rt>さ</rt></ruby>がる",
    "ためる": "ためる", "たまる": "たまる",
    
    "虫": "<ruby>虫<rt>むし</rt></ruby>", "中": "<ruby>中<rt>なか</rt></ruby>", "犬": "<ruby>犬<rt>いぬ</rt></ruby>", "家": "<ruby>家<rt>いえ</rt></ruby>",
    "店": "<ruby>店<rt>みせ</rt></ruby>", "財布": "<ruby>財布<rt>さいふ</rt></ruby>", "電気": "<ruby>電気<rt>でんき</rt></ruby>", "火": "<ruby>火<rt>ひ</rt></ruby>",
    "時計": "<ruby>時計<rt>とけい</rt></ruby>", "服": "<ruby>服<rt>ふく</rt></ruby>", "お湯": "お<ruby>湯<rt>ゆ</rt></ruby>", "授業": "<ruby>授業<rt>じゅぎょう</rt></ruby>",
    "宿題": "<ruby>宿題<rt>しゅくだい</rt></ruby>", "話": "<ruby>話<rt>はなし</rt></ruby>", "日程": "<ruby>日程<rt>にってい</rt></ruby>", "息子": "<ruby>息子<rt>むすこ</rt></ruby>",
    "人": "<ruby>人<rt>ひと</rt></ruby>", "色": "<ruby>色<rt>いろ</rt></ruby>", "怪我": "<ruby>怪我<rt>けが</rt></ruby>", "ご飯": "ご<ruby>飯<rt>はん</rt></ruby>",
    "今": "<ruby>今<rt>いま</rt></ruby>", "元": "<ruby>元<rt>もと</rt></ruby>", "場所": "<ruby>場所<rt>ばしょ</rt></ruby>", "木": "<ruby>木<rt>き</rt></ruby>",
    "敵": "<ruby>敵<rt>てき</rt></ruby>", "髪": "<ruby>髪<rt>かみ</rt></ruby>", "紐": "<ruby>紐<rt>ひも</rt></ruby>", "紙": "<ruby>紙<rt>かみ</rt></ruby>",
    "溺れる": "<ruby>溺<rt>おぼ</rt></ruby>れる", "お金": "お<ruby>金<rt>かね</rt></ruby>", "鐘": "<ruby>鐘<rt>かね</rt></ruby>",
    "赤色": "<ruby>赤色<rt>あかいろ</rt></ruby>", "本": "<ruby>本<rt>ほん</rt></ruby>", "地震": "<ruby>地震<rt>じしん</rt></ruby>",
    "犯人": "<ruby>犯人<rt>はんにん</rt></ruby>", "雪": "<ruby>雪<rt>ゆき</rt></ruby>", "荷物": "<ruby>荷物<rt>にもつ</rt></ruby>",
    "列": "<ruby>列<rt>れつ</rt></ruby>", "椅子": "<ruby>椅子<rt>いす</rt></ruby>", "手紙": "<ruby>手紙<rt>てがみ</rt></ruby>",
    "地球儀": "<ruby>地球儀<rt>ちきゅうぎ</rt></ruby>", "地球": "<ruby>地球<rt>ちきゅう</rt></ruby>",
    "骨": "<ruby>骨<rt>ほね</rt></ruby>", "お皿": "お<ruby>皿<rt>さら</rt></ruby>", "気温": "<ruby>気温<rt>きおん</rt></ruby>", "手": "<ruby>手<rt>て</rt></ruby>"
}

def add_ruby(text):
    sorted_keys = sorted(replacements.keys(), key=len, reverse=True)
    res = text
    for k in sorted_keys:
        res = res.replace(k, replacements[k])
    return res

verbs_list = []
reader = csv.reader(io.StringIO(csv_data))
next(reader)
for row in reader:
    if not row or len(row) < 7: continue
    vt, vi, jp_ruby, m_vt, m_vi, rb_vi, rb_vt = [x.strip() for x in row]
    
    # Process headwords
    vt_ruby = add_ruby(vt)
    vi_ruby = add_ruby(vi)
    
    # Check if headword wasn't ruby-fied (just in case), we can fallback to the mapping or raw
    if '<ruby>' not in vt_ruby and vt != 'ためる':
        vt_ruby = f"<ruby>{vt}</ruby>"
    
    # Process examples
    rb_vt_ruby = add_ruby(rb_vt)
    rb_vi_ruby = add_ruby(rb_vi)
    
    verbs_list.append({
        "vt": {
            "kanji": vt,
            "html": vt_ruby,
            "meaning": m_vt,
            "example_text": rb_vt,
            "example_html": rb_vt_ruby
        },
        "vi": {
            "kanji": vi,
            "html": vi_ruby,
            "meaning": m_vi,
            "example_text": rb_vi,
            "example_html": rb_vi_ruby
        }
    })

json_str = json.dumps(verbs_list, ensure_ascii=False)

html_template = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tha động từ / Tự động từ</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f0f2f5;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            user-select: none;
        }}
        .app-container {{
            width: 100%;
            max-width: 500px;
            padding: 20px;
            text-align: center;
            background: #fff;
            border-radius: 15px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        }}
        .header-container {{
            width: 100%;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
        }}
        .dropdown {{
            position: absolute;
            left: 0;
        }}
        .icon-btn {{
            background: none;
            border: none;
            font-size: 28px;
            cursor: pointer;
            transition: transform 0.2s;
        }}
        .icon-btn:hover {{
            transform: scale(1.1);
        }}
        .dropdown-content {{
            display: none;
            position: absolute;
            background-color: white;
            min-width: 280px;
            box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
            z-index: 10;
            border-radius: 8px;
            top: 40px;
            left: 0;
            text-align: left;
        }}
        .dropdown-content a {{
            color: black;
            padding: 12px 16px;
            text-decoration: none;
            display: block;
            font-weight: bold;
            transition: background 0.2s;
            border-bottom: 1px solid #eee;
        }}
        .dropdown-content a:last-child {{ border-bottom: none; }}
        .dropdown-content a:hover {{ background-color: #f1f1f1; border-radius: 8px; }}
        .show {{ display: block; }}
        
        .flashcard-container {{
            perspective: 1000px;
            margin: 20px 0;
            height: 380px;
            cursor: pointer;
        }}
        .flashcard {{
            width: 100%;
            height: 100%;
            position: relative;
            transition: transform 0.6s;
            transform-style: preserve-3d;
            box-shadow: 0 10px 20px rgba(0,0,0,0.1);
            border-radius: 15px;
            background-color: white;
        }}
        .flashcard.is-flipped {{
            transform: rotateY(180deg);
        }}
        .card-face {{
            position: absolute;
            width: 100%;
            height: 100%;
            backface-visibility: hidden;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            border-radius: 15px;
            padding: 20px;
            box-sizing: border-box;
        }}
        .card-back {{
            transform: rotateY(180deg);
            background-color: #fdfbf7;
            border: 2px solid #e0dcd3;
        }}
        .verb-type-tag {{
            position: absolute;
            top: 15px;
            left: 15px;
            color: white;
            padding: 5px 10px;
            border-radius: 5px;
            font-size: 14px;
            font-weight: bold;
        }}
        .transitive {{ background-color: #E91E63; }}
        .intransitive {{ background-color: #00BCD4; }}
        
        .speaker-btn {{
            position: absolute;
            top: 15px;
            right: 15px;
            background-color: #f0f0f0;
            border: none;
            font-size: 24px;
            cursor: pointer;
            padding: 8px;
            border-radius: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
            width: 45px;
            height: 45px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        .speaker-btn:hover {{ background-color: #e0e0e0; }}
        .speaker-btn:active {{ transform: scale(0.92); }}
        
        .word-kana {{
            font-size: 44px;
            font-weight: bold;
            color: #333;
            margin-bottom: 10px;
        }}
        .word-vn {{
            font-size: 22px;
            color: #1976D2;
            font-weight: bold;
        }}
        .example-sentence {{
            font-size: 20px;
            color: #444;
            margin-top: 25px;
            padding: 15px;
            background-color: #f9f9f9;
            border-radius: 8px;
            border-left: 4px solid #2196F3;
            width: 90%;
            text-align: left;
            line-height: 1.8;
        }}
        rt {{
            font-size: 12px;
            color: #777;
        }}
        
        .controls {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 20px;
        }}
        .nav-btn {{
            background-color: #2196F3;
            color: white;
            border: none;
            padding: 15px 30px;
            font-size: 20px;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        .nav-btn:hover {{ background-color: #1565C0; }}
        .nav-btn:active {{ transform: scale(0.92); }}
        .nav-btn:disabled {{ background-color: #ccc; cursor: not-allowed; transform: none !important; }}
        .progress {{ font-size: 18px; color: #555; font-weight: bold; }}
    </style>
</head>
<body>

<div class="app-container">
    <div class="header-container">
        <div class="dropdown">
            <button class="icon-btn" onclick="toggleMenu(event)">💡</button>
            <div id="dropdown-menu" class="dropdown-content">
                <a href="index.html">Từ trái nghĩa (Tính từ)</a>
                <a href="verbs.html">Tự/Tha động từ (自動詞他動詞練習)</a>
            </div>
        </div>
        <h2>Động từ (Tự / Tha)</h2>
    </div>
    
    <div class="flashcard-container" onclick="flipCard()">
        <div class="flashcard" id="flashcard">
            <!-- Front: Transitive -->
            <div class="card-face card-front">
                <div class="verb-type-tag transitive">Tha động từ (他動詞)</div>
                <button class="speaker-btn" id="front-speaker">🔊</button>
                <div class="word-kana" id="front-headword"></div>
                <div class="word-vn" id="front-vn"></div>
                <div class="example-sentence" id="front-example"></div>
            </div>
            <!-- Back: Intransitive -->
            <div class="card-face card-back">
                <div class="verb-type-tag intransitive">Tự động từ (自動詞)</div>
                <button class="speaker-btn" id="back-speaker">🔊</button>
                <div class="word-kana" id="back-headword"></div>
                <div class="word-vn" id="back-vn"></div>
                <div class="example-sentence" id="back-example"></div>
            </div>
        </div>
    </div>
    <div class="controls">
        <button class="nav-btn" onclick="prevCard()" id="btn-prev">&lt;&lt;</button>
        <div class="progress"><span id="current-idx">1</span> / <span id="total-cards"></span></div>
        <button class="nav-btn" onclick="nextCard()" id="btn-next">&gt;&gt;</button>
    </div>
</div>

<script>
    const flashcards = {json_str};
    let currentIndex = 0;

    function toggleMenu(event) {{
        event.stopPropagation();
        document.getElementById("dropdown-menu").classList.toggle("show");
    }}
    
    window.onclick = function(event) {{
        if (!event.target.matches('.icon-btn')) {{
            var dropdowns = document.getElementsByClassName("dropdown-content");
            for (var i = 0; i < dropdowns.length; i++) {{
                if (dropdowns[i].classList.contains('show')) {{
                    dropdowns[i].classList.remove('show');
                }}
            }}
        }}
    }}

    function speakText(text, event) {{
        if (event) event.stopPropagation();
        if (!('speechSynthesis' in window)) return;
        window.speechSynthesis.cancel();
        
        // Remove ruby tags for speech
        let cleanText = text.replace(/<rt>.*?<\/rt>/g, '');
        cleanText = cleanText.replace(/<[^>]+>/g, '');
        
        const utterance = new SpeechSynthesisUtterance(cleanText);
        utterance.lang = 'ja-JP';
        utterance.rate = 0.9;
        window.speechSynthesis.speak(utterance);
    }}

    function renderCard() {{
        const card = flashcards[currentIndex];
        
        // Front (Transitive)
        document.getElementById('front-headword').innerHTML = card.vt.html;
        document.getElementById('front-vn').textContent = card.vt.meaning;
        document.getElementById('front-example').innerHTML = card.vt.example_html;
        
        document.getElementById('front-speaker').onclick = (e) => speakText(card.vt.example_html, e);
        
        // Back (Intransitive)
        document.getElementById('back-headword').innerHTML = card.vi.html;
        document.getElementById('back-vn').textContent = card.vi.meaning;
        document.getElementById('back-example').innerHTML = card.vi.example_html;
        
        document.getElementById('back-speaker').onclick = (e) => speakText(card.vi.example_html, e);
        
        document.getElementById('current-idx').textContent = currentIndex + 1;
        document.getElementById('total-cards').textContent = flashcards.length;
        document.getElementById('btn-prev').disabled = currentIndex === 0;
        document.getElementById('btn-next').disabled = currentIndex === flashcards.length - 1;
        
        document.getElementById('flashcard').classList.remove('is-flipped');
    }}

    function flipCard() {{
        document.getElementById('flashcard').classList.toggle('is-flipped');
    }}

    function nextCard() {{
        if (currentIndex < flashcards.length - 1) {{
            currentIndex++;
            renderCard();
        }}
    }}

    function prevCard() {{
        if (currentIndex > 0) {{
            currentIndex--;
            renderCard();
        }}
    }}

    renderCard();
</script>
</body>
</html>
"""

with open('../verbs.html', 'w', encoding='utf-8') as f:
    f.write(html_template)
print("verbs.html generated successfully.")
