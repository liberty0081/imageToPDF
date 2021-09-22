#ライブラリのインポート
import discord
import img2pdf
from PIL import Image 
import io

#ファイル名と画像を受け取ってPDFとPDFファイル名を返す関数
def image_to_pdf(name, images):
    # 出力するPDFの名前を設定してpdf_FileNameに格納
    #nameが空の場合PDFの名前をimageToPdf.pdfにする
    if len(name) == 0:
        pdf_FileName = "imageToPdf.pdf"
    #nameが空でない場合PDFの名前をname.pdfにする
    else:
        pdf_FileName = name + ".pdf"
    #PDFをA4サイズにする設定
    layout = img2pdf.get_layout_fun((img2pdf.mm_to_pt(210), img2pdf.mm_to_pt(297)))
    #画像を変換する処理のためのリスト
    convert_images = []
    
    #画像をimage2pdfで変換する前処理
    for img_data, extension in images:
        img_bin = io.BytesIO(img_data)
        #PNGの場合RGBに変換
        if extension == "PNG":
            pil_img = Image.open(img_bin).convert("RGB")
        else:
            pil_img = Image.open(img_bin)
        
        img = io.BytesIO()
        
        #PNGの場合JPEGに変換
        if extension == "PNG":
            pil_img.save(img, "JPEG", quality=95)
        else:
            pil_img.save(img, extension)
        img.seek(0)
        convert_images.append(img)
    
    #変換したPDFとファイル名をタプルにして返す
    return (io.BytesIO(img2pdf.convert(convert_images, layout_fun=layout)), pdf_FileName)


#Botのアクセストークン
TOKEN = 'ODg5Njk4NjI5NTQyMDkyODQy.YUlCaw.QQhkKIBjELUzeVhHU4TFpjC_4fM'

#接続に必要なオブジェクトを生成
client = discord.Client()

#起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    
    #「/」が頭に付いたメッセージにしか反応しない
    if len(message.content) >= 1 and message.content[0] == "/":
        # 画像が送られたらpdfにまとめて返す処理
        
        if message.attachments:
            await message.channel.send("画像をPDFにしているよ！ちょっと待っててね！！(^o^)ﾉｼ")
            
            #「/」以下のメッセージをpdfファイル名にするためにnameに格納
            name = message.content[1:]
            
            #画像で格納するためのリスト
            images = []
            
            #画像と拡張子をタプルにしてimagesに格納
            for attachment in message.attachments:
                if attachment.url.endswith(("png")):
                    images.append((await attachment.read(), "PNG"))
                
                elif attachment.url.endswith(("jpg")):
                    images.append((await attachment.read(), "JPEG"))
                
                elif attachment.url.endswith(("jpeg")):
                    images.append((await attachment.read(), "JPEG"))
            
            #image_to_pdf関数を呼び出してpdfとファイル名を受け取る
            PDF_file, PDF_filename = image_to_pdf(name, images)
            
            #PDFを送信
            await message.channel.send(file=discord.File(fp=PDF_file, filename=PDF_filename))
            
            await message.channel.send("お待たせ！！PDFが出来たよ！！(^_^)b")

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)