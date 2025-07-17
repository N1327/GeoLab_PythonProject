from flask import Flask, render_template, request, redirect, url_for, session
import uuid
from flask import Flask
from ext import db, login_manager
from routes import init_routes

def create_app():
    app = Flask(__name__)
    app.secret_key = 'secret'

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)

    return app

users = {}

posts = {
    'football': [
        {'id': '1','title': 'Football World Cup','content': 'Biggest football event showcasing global talent and national pride.','image': 'https://cdn.resfu.com/media/img_news/fifa-world-cup-groups-2025-groups--new---besoccer.jpg?size=1000x&lossy=1'},
        {'id': '2','title': 'Napoli striker Osimhen close to joining Galatasaray on permanent basis','image': 'https://livesport-ott-images.ssl.cdn.cra.cz/r900xfq60/ab049b96-7b1e-46b0-8eeb-4edc1beacdc9.jpeg'},
        {'id': '3','title': 'Transfer News LIVE: Milan confirm Modric signing, Osimhen and Gyokeres close to moves','image': 'https://livesport-ott-images.ssl.cdn.cra.cz/r900xfq60/2234190d-22f5-4eb3-befe-392d31fdf77e.jpeg'},
        {'id': '4','title': 'Team of the Club World Cup: Palmer leads Chelsea to glory, Garcia the breakout star','image': 'https://livesport-ott-images.ssl.cdn.cra.cz/r900xfq60/8213b2c6-632f-46e4-8de8-7970c630274c.jpeg'},
        {'id': '5','title': 'The numbers behind the drama: A statistical review of the Club World Cup','image': 'https://livesport-ott-images.ssl.cdn.cra.cz/r900xfq60/5a612d5c-7583-4698-aaf8-e659aad91146.jpeg'},
        {'id': '6','title': 'Swedish wonderkid Roony Bardghji signs long-term deal with Barcelona','image': 'https://livesport-ott-images.ssl.cdn.cra.cz/r900xfq60/910b93b5-cb92-4ae5-9adb-d67425aadaee.jpeg'},
        {'id': '7','title': 'EXCLUSIVE: Amorim frustrated as United fail to deliver on key transfer targets','image': 'https://livesport-ott-images.ssl.cdn.cra.cz/r900xfq60/67c0c1e0-1771-4f99-bf43-9292c73a78a7.jpeg'},
        {'id': '8','title': 'Liverpool manager Arne Slot pays tribute to late Diogo Jota ahead of pre-season match','image': 'https://livesport-ott-images.ssl.cdn.cra.cz/r900xfq60/3f2b202c-a979-47e0-bf7d-a60601e65613.jpeg'},
        {'id': '9','title': 'Palmer scores brace as incredible Chelsea stun PSG to claim Club World Cup title','image': 'https://livesport-ott-images.ssl.cdn.cra.cz/r900xfq60/3f72cd2a-750a-4a0f-8580-030fd5c29d19.jpeg' },
        {'id': '10','title': 'FIFA president Infantino says Club World Cup is worlds most successful competition','image': 'https://livesport-ott-images.ssl.cdn.cra.cz/r900xfq60/483970bb-96ac-4307-8c9d-8061224ae366.jpeg'}
    ],
    'basketball': [
        {'id': '1', 'title': 'NBA', 'content': 'NBA Free Agency Tracker: Pacers bring back Isaiah Jackson with $21 million deal', 'image': 'https://cdn.nba.com/manage/2025/07/GettyImages-2224186764-1.jpg'},
        {'id': '2', 'title': 'NBA','content': 'Summer standouts: Wizards draft picks flash upside Tre Johnson and Alex Sarr hint at a promising future in Washington, while Hawks draftee Asa Newell impresses with his efficiency.','image': 'https://cdn.nba.com/manage/2025/07/GettyImages-2224392434-scaled.jpg'},
        {'id': '3', 'title': 'NBA','content': 'Grizzlies announce that Jaren Jackson Jr.s renegotiation and extension is complete Jacksons signing of a $239.9 million deal keeps him under contract through the 2029-30 season is facilitated by the buyout of recently acquired Cole Anthony.','image': 'https://cdn.nba.com/manage/2025/02/GettyImages-2197289189-scaled-e1739283558290.jpg'},
        {'id': '4', 'title': 'NBA','content': 'Fred VanVleet elected President of the National Basketball Players Association VanVleet will transition into this role with guidance from CJ McCollum, who completes a 4-year term as President (2021-25).','image': 'https://cdn.nba.com/manage/2025/03/GettyImages-2205615126-scaled-e1742647145109.jpg'},
        {'id': '5', 'title': 'NBA','content': 'New Buck Myles Turner confident grass is going to be greener wherever I go The Milwaukee Bucks formally introduced Turner — the most significant free agent who switched addresses this summer — on Friday.','image': 'https://cdn.nba.com/manage/2025/07/GettyImages-2224026276-scaled.jpg'},
        {'id': '6', 'title': 'NBA','content': 'Continuity Rankings: Breaking down roster turnover for all 30 teams OKC becomes the 2nd straight team to keep its championship roster mostly intact.','image': 'https://cdn.nba.com/manage/2025/07/GettyImages-2199125430-scaled-e1752503399646-784x442.jpg'},
        {'id': '7', 'title': 'NBA','content': 'New coach of New York Knicks welcomes high expectations ahead of difficult job','image': 'https://livesport-ott-images.ssl.cdn.cra.cz/r900xfq60/d321ab00-182a-4ae3-843d-5b45d9ebcac0.jpeg'},
        {'id': '8', 'title': 'NBA','content': 'Dallas Mavericks superstar Anthony Davis has surgery to repair detached retina','image': 'https://livesport-ott-images.ssl.cdn.cra.cz/r900xfq60/03e72c2d-9866-4fd6-a865-a0abb146805d.jpeg'},
        {'id': '9', 'title': 'NBA','content': 'Denver Nuggets off to red-hot start in first day of NBA free agency','image': 'https://livesport-ott-images.ssl.cdn.cra.cz/r900xfq60/a1a90486-2e4e-4f82-b4db-8f814d54ee2e.jpeg'},
        {'id': '10', 'title': 'NBA','content': 'A period that shakes up the basketball world - what is happening in NBA Free Agency 2025?','image': 'https://livesport-ott-images.ssl.cdn.cra.cz/r900xfq60/4f5c7959-f8e6-4d73-9c5c-844aa7e46ec9.jpeg'}
    ],
    'tennis': [
        {'id': '1', 'title': 'Wimbledon Final', 'content': 'A thrilling Wimbledon finale...', 'image': 'https://images.tennis.com/image/private/t_16-9_768/f_auto/tenniscom-prd/eqb78jf3tzytpfyupegk.jpg'},
        {'id': '2', 'title': 'tennis', 'content': 'Flying the Flag: Kim claims second LPGA Tour title, Tszyu prepares for Vegas bout', 'image': 'https://livesport-ott-images.ssl.cdn.cra.cz/r900xfq60/bc351858-5e4e-4188-a6b6-51f27bb4992c.jpeg'},
        {'id': '3', 'title': 'tennis','content': 'Tennis Tracker: Action returns to clay as dust settles on Wimbledon','image': 'https://livesport-ott-images.ssl.cdn.cra.cz/r900xfq60/5b72bbcc-82a0-42c8-85d6-9589256d72bd.jpeg'},
        {'id': '4', 'title': 'tennis','content': 'The Base Line: Sinner gets his redemption as Swiatek confirms her greatness','image': 'https://livesport-ott-images.ssl.cdn.cra.cz/r900xfq60/38231ba4-2036-4cd8-a909-22b581e9ff3b.jpeg'},
        {'id': '5', 'title': 'tennis','content': 'Jannik Sinner wins maiden Wimbledon title after four-set triumph over Carlos Alcaraz','image': 'https://livesport-ott-images.ssl.cdn.cra.cz/r900xfq60/d187360a-c534-4714-a25c-f25eb599b9f4.jpeg'},
        {'id': '6', 'title': 'tennis','content': 'How Swiatek won Wimbledon: 399 days of waiting, self-belief and learning to love grass','image': 'https://livesport-ott-images.ssl.cdn.cra.cz/r900xfq60/08296900-a11d-4498-aecf-8891832d7fcd.jpeg'},
        {'id': '7', 'title': 'tennis','content': 'Kudermetova and Mertens battle back from set down to win Wimbledon womens doubles title', 'image': 'https://livesport-ott-images.ssl.cdn.cra.cz/r900xfq60/096b2c21-8b5b-41a4-a1f2-df5711a017b8.jpeg'},
        {'id': '8', 'title': 'tennis','content': 'Seven-time Grand Slam champion Venus Williams to feature at Washington Open','image': 'https://livesport-ott-images.ssl.cdn.cra.cz/r900xfq60/0eee73cf-dbbd-44e7-bfa6-cc6b3520f8ad.jpeg'},
        {'id': '9', 'title': 'tennis','content': 'Its tough to accept: Djokovic admits to wear and tear after Wimbledon loss','image': 'https://livesport-ott-images.ssl.cdn.cra.cz/r900xfq60/235adc47-5f1b-425b-b7d4-a81f6f2342e5.jpeg'},
        {'id': '10', 'title': 'tennis','content': 'Defending champion Matteo Berrettini and Alexander Zverev withdraw from Gstaad','image': 'https://livesport-ott-images.ssl.cdn.cra.cz/r900xfq60/1c99371b-f2bb-4a28-9d32-affd732192b8.jpeg'},
    ],
    'chess': [

        {'id': '1', 'title': 'Chess', 'content': 'Hikaru Nakamura & Atousa Pourkashiyan Share Baby News During Stream', 'image': 'https://images.chesscomfiles.com/uploads/v1/news/1712476.25810b03.300x169o.420e88ee6b95.jpg'},
        {'id': '2', 'title': 'Chess','content': 'Awatramani, Chiu Dominate Bughouse Championship NM CoachJKane NMs Isaac Chiu and Janak Awatramani dominated the 2025 Chess.com','image': 'https://images.chesscomfiles.com/uploads/v1/news/1711242.fdb2aaf0.300x169o.1a279fdd527b.png'},
        {'id': '3', 'title': 'Chess','content': 'Niemann Joins Ranks Of Freestyle Winners Ahead Of Grand Slam','image': 'https://images.chesscomfiles.com/uploads/v1/news/1711250.58ac816b.300x169o.bac22bcb86ef.png'},
        {'id': '4', 'title': 'Chess','content': '14-Year-Old Kaliakhmet Eliminates GM Batsiashvili','image': 'https://images.chesscomfiles.com/uploads/v1/news/1709926.07754d27.300x169o.c5cf48b3e610.png'},
        {'id': '5', 'title': 'Chess','content': 'Kazakh 19-Year-Old Kamalidenova Upsets Goryachkina, 2023 Winner','image': 'https://images.chesscomfiles.com/uploads/v1/news/1707668.ad7b60b5.300x169o.1397050ed1fd.png'},
        {'id': '6', 'title': 'Chess ', 'content': 'Nakamura Wins 3rd Straight Bullet Brawl', 'image': 'https://images.chesscomfiles.com/uploads/v1/news/1712550.b0f844bf.630x354o.175d6ff25cd0.png'},
    ],

    'ufc': [

        {'id': '1', 'title': 'UFC ', 'content': 'Merab Tops DDP For ‘Best UFC Fighter’ During the UFC Nashville broadcast, UFC Bantamweight champion Merab Dvalishvili was announced as the winner, beating out nominees: Dricus Du Plessis, Islam Makhachev, and Kayla Harrison.', 'image': 'https://cdn.vox-cdn.com/thumbor/vn3mZbzB92Hokj3FqO2VTa9vZk8=/0x186:3576x2198/273x154/filters:format(webp)/cdn.vox-cdn.com/uploads/chorus_image/image/74175454/2219120354.0.jpg'},
        {'id': '2', 'title': 'UFC ','content': 'UFC Fight Night: Lewis v TeixeiraWhat’s Next For Tallison Teixeira?UFC Nashville results: It’s time to see what could be next for Tallison Teixeira after he suffered his first-ever defeat, a knockout loss at the hands of Derrick Lewis.','image': 'https://cdn.vox-cdn.com/thumbor/HAHRg17NG5vRqYjRJeaLQkf-kOo=/0x0:7758x4364/273x154/filters:format(webp)/cdn.vox-cdn.com/uploads/chorus_image/image/74176430/2224849249.0.jpg'},
        {'id': '3', 'title': 'UFC ','content': '‘Split To The Bone!’Stephen ‘Wonderboy’ Thompson took a split decision loss and a split to the bone shin against Gabriel Bonfim.','image': 'https://cdn.vox-cdn.com/thumbor/bKTRxcIwt5X7rlpzrfGudU6VU_0=/0x431:6882x4302/273x154/filters:format(webp)/cdn.vox-cdn.com/uploads/chorus_image/image/74175391/2224848491.0.jpg'},
        {'id': '4', 'title': 'UFC ','content': 'UFC White House Show Set For South Lawn UFC CEO Dana White is already hard at work planning the America 250 UFC event set to take place at the White House.','image': 'https://cdn.vox-cdn.com/thumbor/KbHT1ON9NVtE9PCwoT6lG554lTI=/0x0:6858x3858/273x154/filters:format(webp)/cdn.vox-cdn.com/uploads/chorus_image/image/74174917/2209982489.0.jpg'},
        {'id': '5', 'title': 'UFC ','content': 'Up Next! Holloway Vs. Poirier 3 For The ‘BMF’ Belt! Latest UFC 318 fight card, start time, date and location for the Max Holloway vs. Dustin Poirier 3-led PPV event for the BMF title on Sat., July 19, 2025 at Smoothie King Center in New Orleans, Louisiana.','image': 'https://cdn.vox-cdn.com/thumbor/Utnrhnq3iu6O7Ao77QbNx9Htxk0=/0x151:1080x759/273x154/filters:format(webp)/cdn.vox-cdn.com/uploads/chorus_image/image/74086736/GpZjadKbEAQTXTf.0.jpeg'},
        {'id': '6', 'title': 'UFC ', 'content': 'Early stoppage? Daniel Cormier defends Derrick Lewis’ emote KO at UFC Nashville for key reason', 'image': 'https://bloodyelbow.com/wp-content/uploads/1/2025/07/GettyImages-2224849166-2-scaled-e1752385483279-750x422.jpg'},
    ],
'f1': [
        {'id': '1', 'title': 'F1 ', 'content': 'The biggest privilege in my life: Horner bids emotional farewell to Red Bull', 'image': 'https://media.formula1.com/image/upload/c_lfill,w_3392/q_auto/v1740000000/fom-website/2025/Miscellaneous/Greatest_Races_17_Belgium_2000_numbers.webp'},
        {'id': '2', 'title': 'F1', 'content': 'The biggest privilege in my life: Horner bids emotional farewell to Red Bull', 'image': 'https://livesport-ott-images.ssl.cdn.cra.cz/r900xfq60/cae2803c-9b05-434e-8c4a-5fcd6a06e2cc.jpeg'},
        {'id': '3', 'title': 'F1','content': 'Horners departure raises the question over Verstappens future at Red Bull','image': 'https://livesport-ott-images.ssl.cdn.cra.cz/r900xfq60/373827ac-13ec-404a-87a6-95c8d4400b41.jpeg'},
        {'id': '4', 'title': 'F1','content': 'Norris labels British Grand Prix win everything Ive ever wanted to achieve','image': 'https://livesport-ott-images.ssl.cdn.cra.cz/r900xfq60/e81d51ab-b4d1-4b76-a174-56b22acde718.jpeg'},
        {'id': '5', 'title': 'F1','content': 'Hamilton holding out hope for home podium after qualifying in P5 at SIlverstone','image': 'https://livesport-ott-images.ssl.cdn.cra.cz/r900xfq60/87706b01-e620-4e43-9c91-107237916c56.jpeg'},
        {'id': '6', 'title': 'F1','content': 'Leclerc fastest ahead of Piastri in final practice session at British Grand Prix','image': 'https://livesport-ott-images.ssl.cdn.cra.cz/r900xfq60/9aa0c31d-eb03-4b65-86cb-44ae79d2ede8.jpeg'},
        {'id': '7', 'title': 'F1','content': 'Sensational Max Verstappen takes British Grand Prix pole ahead of the McLarens','image': 'https://livesport-ott-images.ssl.cdn.cra.cz/r900xfq60/2d9093d1-5f1b-4785-a4ca-9a72a810d7ac.jpeg'},
        {'id': '8', 'title': 'F1','content': 'Fan favourite Lando Norris leads the way in British Grand Prix second practice','image': 'https://livesport-ott-images.ssl.cdn.cra.cz/r900xfq60/2983329b-e18c-40bc-8b95-5e173653a098.jpeg'},
        {'id': '9', 'title': 'F1','content': 'Steve Neilsen set to take over day-to-day operations at F1 team Alpine','image': 'https://livesport-ott-images.ssl.cdn.cra.cz/r900xfq60/174a17b6-9ff1-4795-bf80-69be52465ed2.jpeg'},
        {'id': '10', 'title': 'F1','content': 'George Russell says he is set to sign new deal with Mercedes in coming weeks','image': 'https://livesport-ott-images.ssl.cdn.cra.cz/r900xfq60/6b3336ef-dc94-42b3-a859-b27f8149032b.jpeg'},

    ],
}

app = create_app()

@app.route('/')
def home():
    return render_template('home.html', posts=posts)

@app.route('/<sport>')
def show_sport(sport):
    if sport in posts:
        return render_template(f'{sport}.html', posts=posts[sport], sport=sport)
    return "404 Not Found", 404

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        users[email] = {'name': name, 'password': password}
        print(f"[REGISTERED] {name} | {email}")
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = users.get(email)
        if user and user['password'] == password:
            session['user'] = user['name']
            session['email'] = email
            session['admin'] = (user['name'] == 'admin' and password == '12345678')
            print(f"[LOGGED IN] {email}")
            return redirect(url_for('home'))
        else:
            return "Login Failed"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/admin')
def admin_panel():
    if not session.get('admin'):
        return redirect(url_for('login'))
    return render_template('admin.html', posts=posts)

@app.route('/admin/add/<sport>', methods=['GET', 'POST'])
def add_post(sport):
    if not session.get('admin'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        image_url = request.form['image']
        post_id = str(uuid.uuid4())
        posts[sport].append({'id': post_id, 'title': title, 'content': content, 'image': image_url})
        return redirect(url_for('admin_panel'))
    return render_template('add_post.html', sport=sport)

@app.route('/admin/edit/<sport>/<post_id>', methods=['GET', 'POST'])
def edit_post(sport, post_id):
    if not session.get('admin'):
        return redirect(url_for('login'))
    sport_posts = posts.get(sport, [])
    post = next((p for p in sport_posts if p['id'] == post_id), None)
    if not post:
        return "Post not found", 404
    if request.method == 'POST':
        post['title'] = request.form['title']
        post['content'] = request.form['content']
        post['image'] = request.form['image']
        return redirect(url_for('admin_panel'))
    return render_template('edit_post.html', post=post, sport=sport)

@app.route('/admin/delete/<sport>/<post_id>', methods=['POST'])
def delete_post(sport, post_id):
    if not session.get('admin'):
        return redirect(url_for('login'))
    posts[sport] = [p for p in posts[sport] if p['id'] != post_id]
    return redirect(url_for('admin_panel'))

if __name__ == '__main__':
    app.run(debug=True)
