from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from posts.forms import PostCreateForm
from .models import Post, Save
from perfumes.models import Perfume
from musics.models import Music, Favorite
from datetime import datetime
from django.db.models import Sum
import geonamescache

gc = geonamescache.GeonamesCache()

# Create your views here.
def index(request):
    post_list = Post.objects.all()
    music_list = Music.objects.all().order_by('-like')[:5]
    if request.user.is_authenticated:
        user_favorites = Favorite.objects.filter(user=request.user)
        for music in music_list:
            music.is_liked = user_favorites.filter(music=music).exists()

    context = {
        'post_list' : post_list,
        'music_list' : music_list,
    }
    return render(request, 'index.html', context)

def post_music_like(request, id):
    if request.user.is_authenticated:
        music = get_object_or_404(Music, id=id)
        user = request.user

    # 이미 좋아요를 눌렀는지 확인
        if Favorite.objects.filter(user=user, music=music).exists():
            # 이미 좋아요를 눌렀을 경우 처리
            favorite = Favorite.objects.get(user=user, music=music)
            favorite.delete()
            # 좋아요 개수를 1 증가시킴
            music.like -= 1
            music.save()

        else:
            # 중개 모델을 생성하고 저장
            like = Favorite(user=user, music=music)
            like.save()

            # 좋아요 개수를 1 증가시킴
            music.like += 1
            music.save()

        return redirect('index')
        
    return redirect('accouts:login')

def post_list_view(request):
    
    if request.GET.get('order') == 'recent':
        post_list = Post.objects.all().order_by('-created_at')
    
    # elif request.GET.get('order') == 'popular':
    #     post_list = Post.objects.all().order_by('-like')

    else:
        post_list = Post.objects.all()
    context ={
        'post_list': post_list
    }
    
    return render(request, 'posts/post_list.html', context)

@login_required
def post_create_form_view(request):
    if request.method =='GET':
        form = PostCreateForm()
        context = {'form':form}
        return render(request, 'posts/post_create.html',context)
    else:
        form = PostCreateForm(request.POST, request.FILES)
        
        year2 = int(request.POST.get('year2', False))
        month2 = int(request.POST.get('month2', False))
        day2 = int(request.POST.get('day2', False))

        year1 = int(request.POST.get('year1', False))
        month1 = int(request.POST.get('month1', False))
        day1 = int(request.POST.get('day1', False))


        start = datetime(year1, month1,  day1).strftime("%Y년 %m월 %d일")
        end = datetime(year2, month2,  day2).strftime("%Y년 %m월 %d일")
        
        dateDiff = datetime(year2, month2,  day2) - datetime(year1, month1, day1)
        
        location = request.POST.get('location', False)
        result = check_location(location)
        
        if form.is_valid(): #유효성 검사 true
            Post.objects.create(
                title=form.cleaned_data['title'],
                location=form.cleaned_data['location'],
                date = dateDiff.days,
                cost=form.cleaned_data['cost'],
                category=int(request.POST.get('season', 0)),
                image=form.cleaned_data['image'],
                description=form.cleaned_data['description'],
                where = result,
                start = start,
                end = end,
                user=request.user
            )
        else: #유효성 검사 false
            print("유효성 검사 실패")
            errors = form.errors.as_data()  # 유효성 검사 실패 세부 정보
            for field, error_list in errors.items():
                field_name = form.fields[field].label  # 실패한 필드의 레이블 이름
                error_message = error_list[0].message  # 실패 메시지
                print(f"필드 '{field_name}': {error_message}")
            return redirect('posts:post-create')
        return redirect('index')
    
def post_detail_view(request, id):
    
        try:
            post = Post.objects.get(id=id)
        except Post.DoesNotExist:
            return redirect('index')
        
        cost = format(post.cost, ',d')
        
        date = post.date - 1
        context = {
            'post':post,
            'date' : date,
            'cost' : cost,
        }
        return render(request, 'posts/post_detail.html',context)
    
    
def post_delete_view(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method =='GET':
        context={
            'post':post
        }
        return render(request,'posts/post_confirm_delete.html',context)
    else:
        post.delete()
        return redirect('index')
    

def post_update_view(request,id):
    post = Post.objects.get(id=id)
    if request.method =='GET':
        context = {
            'post':post
        }
        return render(request, 'posts/post_update.html',context)
    elif request.method =='POST':
        new_image = request.FILES.get('image')
        description = request.POST.get('description')
        if new_image:
            post.image.delete()
            post.image = new_image
        post.description = description
        post.save()
        return redirect('posts:post-detail',post.id)

@login_required
def post_mySave_view(request):
    post_list = Save.objects.filter(user=request.user).select_related('post__user')
    
    context = {
        'post_list' : post_list
    }

    return render(request, 'posts/mySave.html', context)
    
def mySave_season_view(request):
    season = int(request.GET.get('season'))
    # 해당 시즌에 대한 게시물을 가져옴
    
    post_list = Save.objects.filter(user=request.user, post__category=season).select_related('post')
    print(post_list)

    context = {
        'post_list': post_list
        }
    return render(request, 'posts/mySave_season.html', context)

def myPage_season_view(request):
    season = int(request.GET.get('season'))
    # 해당 시즌에 대한 게시물을 가져옴
    
    post_list = Post.objects.filter(user=request.user, category=season)
    print(post_list)

    context = {
        'post_list': post_list
        }
    return render(request, 'posts/myPage_season.html', context)

def myPage_sort_view(request):
    if request.method == 'GET':
        sort = request.GET.get('sort', '')
        post_list = Post.objects.filter(user=request.user)
        print(sort)
        if sort == 'recent':
            post_list = post_list.order_by('-created_at')  # 최신순 정렬

        context = {'post_list': post_list}
        return render(request, 'posts/myPage_season.html', context)

@login_required
def post_save_view(request, id):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, id=id)
        user = request.user

    # 이미 좋아요를 눌렀는지 확인
        if Save.objects.filter(user=user, post=post).exists():
            # 이미 좋아요를 눌렀을 경우 처리
            favorite = Save.objects.get(user=user, post=post)
            favorite.delete()

        else:
            # 중개 모델을 생성하고 저장
            like = Save(user=user, post=post)
            like.save()

        return redirect('posts:post-list')
        
    return redirect('accouts:login')



@login_required
def my_page_view(request, id):
    user = get_object_or_404(get_user_model(), id=id)
    post_count = user.post_set.count()
    # if request.GET.get('order') == 'recent':
    #     post_list = Post.objects.all().order_by('-created_at')
    user_posts = Post.objects.filter(user=user)  # 특정 유저의 Post 객체들을 필터링합니다.
    date_sum = user_posts.aggregate(total_date_sum=Sum('date'))['total_date_sum']  # date 필드의 총 합을 계산합니다.
    
    # 특정 사용자의 국내(date=0)의 date 총합
    domestic_total = Post.objects.filter(user_id=id, where=0).aggregate(total=Sum('date'))['total']
    
    # 특정 사용자의 국외(date=1)의 date 총합
    international_total = Post.objects.filter(user_id=id, where=1).aggregate(total=Sum('date'))['total']
        
    if request.GET.get('order') == 'recent':
            post_list = Post.objects.filter(user_id=id).order_by('-created_at')
        
        # elif request.GET.get('order') == 'popular':
        #     post_list = Post.objects.all().order_by('-like')

    else:
        post_list = Post.objects.filter(user_id=id)
    

    context ={
        'user': user,
        'post_count' : post_count,
        'date_sum' : date_sum,
        'domestic_total' : domestic_total,
        'international_total' : international_total,
        'post_list': post_list,
    }
    return render(request, 'posts/myPage.html', context)





def season_view(request):
    if request.method == 'GET':
        season = int(request.GET.get('season'))
        # 해당 시즌에 대한 게시물을 가져옴
        post_list = Post.objects.filter(category=season)
        
        context = {'post_list': post_list}
        return render(request, 'posts/test.html', context)

    

def sort_view(request):
    if request.method == 'GET':
        sort = request.GET.get('sort', '')
        post_list = Post.objects.all()

        # if sort == 'popular':
        #     post_list = queryset.order_by('-likes')  # 인기순 정렬
        if sort == 'recent':
            post_list = post_list.order_by('-created_at')  # 최신순 정렬

        context = {'post_list': post_list}
        return render(request, 'posts/test.html', context)

def check_location(country_name):
    
    country_name_english = country_names_mapping.get(country_name)

    countries = gc.get_countries()
    for country_code, country_info in countries.items():
        if country_name_english == "South Korea":
            return 0  # 국내인 경우
        
        elif country_info['name'] == country_name_english:
            return 1  # 국외인 경우
        
    return 0# 국내인 경우

country_names_mapping = {
    "안도라": "Andorra",
    "아랍에미리트": "United Arab Emirates",
    "아프가니스탄": "Afghanistan",
    "앤티가 바부다": "Antigua and Barbuda",
    "앵귈라": "Anguilla",
    "알바니아": "Albania",
    "아르메니아": "Armenia",
    "앙골라": "Angola",
    "남극 대륙": "Antarctica",
    "아르헨티나": "Argentina",
    "아메리칸 사모아": "American Samoa",
    "오스트리아": "Austria",
    "오스트레일리아": "Australia",
    "아루바": "Aruba",
    "올란드 제도": "Aland Islands",
    "아제르바이잔": "Azerbaijan",
    "보스니아 헤르체고비나": "Bosnia and Herzegovina",
    "바베이도스": "Barbados",
    "방글라데시": "Bangladesh",
    "벨기에": "Belgium",
    "부르키나파소": "Burkina Faso",
    "불가리아": "Bulgaria",
    "바레인": "Bahrain",
    "부룬디": "Burundi",
    "베냉": "Benin",
    "생바르텔레미": "Saint Barthelemy",
    "버뮤다": "Bermuda",
    "브루나이": "Brunei",
    "볼리비아": "Bolivia",
    "보네르, 산트 유스타시우스 및 사바": "Bonaire, Saint Eustatius and Saba",
    "브라질": "Brazil",
    "바하마": "Bahamas",
    "부탄": "Bhutan",
    "부베 섬": "Bouvet Island",
    "보츠와나": "Botswana",
    "벨라루스": "Belarus",
    "벨리즈": "Belize",
    "캐나다": "Canada",
    "코코스 제도": "Cocos Islands",
    "콩고 민주 공화국": "Democratic Republic of the Congo",
    "중앙 아프리카 공화국": "Central African Republic",
    "콩고 공화국": "Republic of the Congo",
    "스위스": "Switzerland",
    "코트디부아르": "Ivory Coast",
    "쿡 제도": "Cook Islands",
    "칠레": "Chile",
    "카메룬": "Cameroon",
    "중국": "China",
    "콜롬비아": "Colombia",
    "코스타리카": "Costa Rica",
    "쿠바": "Cuba",
    "카보베르데": "Cabo Verde",
    "쿠라사오": "Curacao",
    "크리스마스 섬": "Christmas Island",
    "키프로스": "Cyprus",
    "체코": "Czechia",
    "독일": "Germany",
    "지부티": "Djibouti",
    "덴마크": "Denmark",
    "도미니카": "Dominica",
    "도미니카 공화국": "Dominican Republic",
    "알제리": "Algeria",
    "에콰도르": "Ecuador",
    "에스토니아": "Estonia",
    "이집트": "Egypt",
    "서사하라": "Western Sahara",
    "에리트리아": "Eritrea",
    "스페인": "Spain",
    "에티오피아": "Ethiopia",
    "핀란드": "Finland",
    "피지": "Fiji",
    "포클랜드 제도": "Falkland Islands",
    "미크로네시아 연방": "Micronesia",
    "페로 제도": "Faroe Islands",
    "프랑스": "France",
    "가이아나": "Guyana",
    "영국령 기아나": "French Guiana",
    "건지 섬": "Guernsey",
    "가나": "Ghana",
    "지브롤터": "Gibraltar",
    "그린란드": "Greenland",
    "감비아": "Gambia",
    "기니": "Guinea",
    "과들루프": "Guadeloupe",
    "적도 기니": "Equatorial Guinea",
    "그리스": "Greece",
    "남조지아와 남샌드위치 제도": "South Georgia and the South Sandwich Islands",
    "과테말라": "Guatemala",
    "괌": "Guam",
    "기니비사우": "Guinea-Bissau",
    "가이아나": "Guyana",
    "홍콩": "Hong Kong",
    "허드 섬 및 맥도날드 제도": "Heard Island and McDonald Islands",
    "온두라스": "Honduras",
    "크로아티아": "Croatia",
    "아이티": "Haiti",
    "헝가리": "Hungary",
    "인도네시아": "Indonesia",
    "아일랜드": "Ireland",
    "이스라엘": "Israel",
    "맨 섬": "Isle of Man",
    "인도": "India",
    "영국령 인도양 지역": "British Indian Ocean Territory",
    "이라크": "Iraq",
    "이란": "Iran",
    "아이슬란드": "Iceland",
    "이탈리아": "Italy",
    "저지섬": "Jersey",
    "자메이카": "Jamaica",
    "요르단": "Jordan",
    "일본": "Japan",
    "케냐": "Kenya",
    "키르기스스탄": "Kyrgyzstan",
    "캄보디아": "Cambodia",
    "키리바시": "Kiribati",
    "코모로": "Comoros",
    "세인트키츠 네비스": "Saint Kitts and Nevis",
    "북한": "North Korea",
    "대한민국": "South Korea",
    "코소보": "Kosovo",
    "쿠웨이트": "Kuwait",
    "케이맨 제도": "Cayman Islands",
    "카자흐스탄": "Kazakhstan",
    "라오스": "Laos",
    "레바논": "Lebanon",
    "세인트루시아": "Saint Lucia",
    "리히텐슈타인": "Liechtenstein",
    "스리랑카": "Sri Lanka",
    "라이베리아": "Liberia",
    "레소토": "Lesotho",
    "리투아니아": "Lithuania",
    "룩셈부르크": "Luxembourg",
    "라트비아": "Latvia",
    "리비아": "Libya",
    "모로코": "Morocco",
    "모나코": "Monaco",
    "몰도바": "Moldova",
    "몬테네그로": "Montenegro",
    "세인트 마틴": "Saint Martin",
    "마다가스카르": "Madagascar",
    "마샬 제도": "Marshall Islands",
    "북마케도니아": "North Macedonia",
    "말리": "Mali",
    "미얀마": "Myanmar",
    "몽골": "Mongolia",
    "마카오": "Macao",
    "북마리아나 제도": "Northern Mariana Islands",
    "마르티니크": "Martinique",
    "모리타니아": "Mauritania",
    "몬트세라트": "Montserrat",
    "몰타": "Malta",
    "가나": "Ghana",
    "가봉": "Gabon",
    "가이아나": "Guyana",
    "감비아": "Gambia",
    "과테말라": "Guatemala",
    "그리스": "Greece",
    "그레나다": "Grenada",
    "기니": "Guinea",
    "기니비사우": "Guinea-Bissau",
    "나미비아": "Namibia",
    "나우루": "Nauru",
    "나이지리아": "Nigeria",
    "남수단": "South Sudan",
    "남아프리카 공화국": "South Africa",
    "네덜란드": "Netherlands",
    "네팔": "Nepal",
    "노르웨이": "Norway",
    "뉴질랜드": "New Zealand",
    "니제르": "Niger",
    "니카라과": "Nicaragua",
    "대한민국": "South Korea",
    "덴마크": "Denmark",
    "도미니카 공화국": "Dominican Republic",
    "도미니카 연방": "Dominica",
    "독일": "Germany",
    "동티모르": "Timor-Leste",
    "라오스": "Laos",
    "라이베리아": "Liberia",
    "라트비아": "Latvia",
    "러시아": "Russia",
    "레바논": "Lebanon",
    "레소토": "Lesotho",
    "루마니아": "Romania",
    "룩셈부르크": "Luxembourg",
    "르완다": "Rwanda",
    "리비아": "Libya",
    "리투아니아": "Lithuania",
    "리히텐슈타인": "Liechtenstein",
    "마다가스카르": "Madagascar",
    "마셜 제도": "Marshall Islands",
    "마케도니아": "Macedonia",
    "말라위": "Malawi",
    "말레이시아": "Malaysia",
    "말리": "Mali",
    "멕시코": "Mexico",
    "모나코": "Monaco",
    "모로코": "Morocco",
    "모리셔스": "Mauritius",
    "모리타니": "Mauritania",
    "모잠비크": "Mozambique",
    "몬테네그로": "Montenegro",
    "몰도바": "Moldova",
    "몰디브": "Maldives",
    "몰타": "Malta",
    "몽골": "Mongolia",
    "미국": "United States",
    "미얀마": "Myanmar",
    "미크로네시아 연방": "Micronesia",
    "바누아투": "Vanuatu",
    "바레인": "Bahrain",
    "바베이도스": "Barbados",
    "바티칸 시국": "Vatican City",
    "바하마": "Bahamas",
    "방글라데시": "Bangladesh",
    "베냉": "Benin",
    "베네수엘라": "Venezuela",
    "베트남": "Vietnam",
    "벨기에": "Belgium",
    "벨라루스": "Belarus",
    "벨리즈": "Belize",
    "보스니아 헤르체고비나": "Bosnia and Herzegovina",
    "보츠와나": "Botswana",
    "볼리비아": "Bolivia",
    "부룬디": "Burundi",
    "부르키나파소": "Burkina Faso",
    "북마케도니아": "North Macedonia",
    "북아일랜드": "Northern Ireland",
    "북키프로스": "Northern Cyprus",
    "브라질": "Brazil",
    "브루나이": "Brunei",
    "브루키": "Burundi",
    "사모아": "Samoa",
    "사우디아라비아": "Saudi Arabia",
    "사하라 아랍 민주 공화국": "Western Sahara",
    "산마리노": "San Marino",
    "상투메 프린시페": "Sao Tome and Principe",
    "세네갈": "Senegal",
    "세르비아": "Serbia",
    "세이셸": "Seychelles",
    "세인트루시아": "Saint Lucia",
    "세인트빈센트 그레나딘": "Saint Vincent and the Grenadines",
    "세인트키츠 네비스": "Saint Kitts and Nevis",
    "소말리아": "Somalia",
    "솔로몬 제도": "Solomon Islands",
    "수단": "Sudan",
    "수리남": "Suriname",
    "스리랑카": "Sri Lanka",
    "스와질란드": "Eswatini",
    "스웨덴": "Sweden",
    "스위스": "Switzerland",
    "스페인": "Spain",
    "슬로바키아": "Slovakia",
    "슬로베니아": "Slovenia",
    "시리아": "Syria",
    "시에라리온": "Sierra Leone",
    "신트마르턴": "Sint Maarten",
    "싱가포르": "Singapore",
    "아랍에미리트": "United Arab Emirates",
    "아르메니아": "Armenia",
    "아르헨티나": "Argentina",
    "아이슬란드": "Iceland",
    "아이티": "Haiti",
    "아일랜드": "Ireland",
    "아제르바이잔": "Azerbaijan",
    "아프가니스탄": "Afghanistan",
    "안도라": "Andorra",
    "알바니아": "Albania",
    "알제리": "Algeria",
    "앙골라": "Angola",
    "앤티가 바부다": "Antigua and Barbuda",
    "앵귈라": "Anguilla",
    "에리트리아": "Eritrea",
    "에스와티니": "Eswatini",
    "에스토니아": "Estonia",
    "에콰도르": "Ecuador",
    "에티오피아": "Ethiopia",
    "엘살바도르": "El Salvador",
    "영국": "United Kingdom",
    "예멘": "Yemen",
    "오만": "Oman",
    "오스트레일리아": "Australia",
    "오스트리아": "Austria",
    "온두라스": "Honduras",
    "올란드 제도": "Aland Islands",
    "요르단": "Jordan",
    "우간다": "Uganda",
    "우루과이": "Uruguay",
    "우즈베키스탄": "Uzbekistan",
    "우크라이나": "Ukraine",
    "이라크": "Iraq",
    "이란": "Iran",
    "이스라엘": "Israel",
    "이집트": "Egypt",
    "이탈리아": "Italy",
    "인도": "India",
    "인도네시아": "Indonesia",
    "일본": "Japan",
    "자메이카": "Jamaica",
    "잠비아": "Zambia",
    "적도 기니": "Equatorial Guinea",
    "조선민주주의인민공화국": "North Korea",
    "조지아": "Georgia",
    "중앙아프리카 공화국": "Central African Republic",
    "중화민국": "Taiwan",
    "중화인민공화국": "China",
    "지부티": "Djibouti",
    "짐바브웨": "Zimbabwe",
    "차드": "Chad",
    "체코": "Czech Republic",
    "칠레": "Chile",
    "카메룬": "Cameroon",
    "카보베르데": "Cabo Verde",
    "카자흐스탄": "Kazakhstan",
    "카타르": "Qatar",
    "캄보디아": "Cambodia",
    "캐나다": "Canada",
    "케냐": "Kenya",
    "코모로": "Comoros",
    "코스타리카": "Costa Rica",
    "코코스 제도": "Cocos Islands",
    "코트디부아르": "Cote d'Ivoire",
    "콜롬비아": "Colombia",
    "콩고 공화국": "Republic of the Congo",
    "콩고 민주 공화국": "Democratic Republic of the Congo",
    "쿠바": "Cuba",
    "쿠웨이트": "Kuwait",
    "쿡 제도": "Cook Islands",
    "퀴라소": "Curacao",
    "크로아티아": "Croatia",
    "키르기스스탄": "Kyrgyzstan",
    "키리바시": "Kiribati",
    "키프로스": "Cyprus",
    "타이": "Thailand",
    "타지키스탄": "Tajikistan",
    "탄자니아": "Tanzania",
    "터크메니스탄": "Turkmenistan",
    "터키": "Turkey",
    "토고": "Togo",
    "토켈라우": "Tokelau",
    "통가": "Tonga",
    "투르크메니스탄": "Turkmenistan",
    "투발루": "Tuvalu",
    "튀니지": "Tunisia",
    "트리니다드 토바고": "Trinidad and Tobago",
    "파나마": "Panama",
    "파라과이": "Paraguay",
    "파키스탄": "Pakistan",
    "파푸아뉴기니": "Papua New Guinea",
    "팔라우": "Palau",
    "팔레스타인": "Palestine",
    "페루": "Peru",
    "포르투갈": "Portugal",
    "폴란드": "Poland",
    "프랑스": "France",
    "피지": "Fiji",
    "핀란드": "Finland",
    "필리핀": "Philippines",
    "헝가리": "Hungary",
    "홍콩": "Hong Kong",
    "흑만": "Black Man",
}

