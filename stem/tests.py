from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase

from stem.models import Post, Comment


class BasicTests(TestCase):
    def setUp(self):
        author, succeeded = User.objects.get_or_create(username='testie')

        p1 = Post()
        p1.author = author
        p1.created = datetime(2015, 5, 10, 20)
        p1.edited = datetime(2015, 5, 10, 21)
        p1.language = 'pl'
        p1.title = 'Polski bardzo ladny tytul posta'
        p1.content = 'Polska tresc artykulu. Litwo! Ojczyzno moja! Ty jesteś jak zdrowie. Ile cię stracił. Dziś ' \
                     'piękność widziana więc wszyscy ją nudzi rzecz zakonna, to mówiąc, że gotyckiej są nasze spraw ' \
                     'bernardyńskie. cóż by życie uprzyjemnić i jąkał się sprawa. My od płaczącej matki pod ' \
                     'Napoleonem, demokrata przyjechał z ziemi włoskiej stara się w pogody lilia jeziór skroń ' \
                     'ucałowawszy, uprzejmie pozdrowił. A na dole. Ujrzała, zaśmiała się kojarz wspaniały domów ' \
                     'sojusz - mój Tadeuszu, żeś się pan nigdy sługom nie rzuca w nieczynności! a chłopi żegnali się, ' \
                     'toczył zdumione źrenic po '
        p1.blog_post = True
        p1.hidden = False
        p1.comments_closed = False
        p1.number_of_comments = 0
        p1.save()

        p2 = Post()
        p2.author = author
        p2.created = datetime(2016, 5, 10, 20)
        p2.language = 'en'
        p2.title = 'Beautiful english blog post title'
        p2.content = 'Lorem ipsum dolor sit amet, velit sagittis quam nulla, justo aenean. Duis duis dui maecenas ' \
                     'mauris montes nec, non posuere facilisis nunc proin, quam mattis vulputate ut ante, ' \
                     'mi consequat sed sit tempus, erat nullam dolor ut pellentesque arcu. Nunc posuere nam, ' \
                     'tincidunt augue, ridiculus mi consectetuer maecenas, ut nonummy mattis netus suspendisse ' \
                     'bibendum hendrerit, lorem vehicula mollis et maecenas justo. At et dapibus a mattis ' \
                     'pellentesque, semper leo pharetra tempor, elit enim in tellus sed, feugiat elementum wisi ' \
                     'vestibulum faucibus tincidunt mi. Libero quisque justo potenti conubia mollis. Tristique ac sem ' \
                     'omnis. Pulvinar a, in amet nec mauris arcu vitae, augue et sed tristique. Et sed, ' \
                     'eget non diam, nec gravida diam nulla urna, vulputate faucibus quis donec interdum et neque, ' \
                     'luctus etiam laoreet in dolor. Convallis at, bibendum wisi cursus, cursus egestas mi, ' \
                     'a magna quam a ullamcorper pharetra, sapien mollis morbi amet erat. Tempus tellus eros vitae ' \
                     'ligula nascetur diam. Velit nec eget, nec a mi magnis faucibus vestibulum. Sagittis orci eget, ' \
                     'nec quis ante. Pede diam voluptates, nibh est tincidunt est nulla diam consectetuer, ' \
                     'porttitor sed sit nulla augue pulvinar posuere, quam hymenaeos suscipit a luctus, quis felis ' \
                     'gravida fermentum nulla orci id. Justo fringilla nulla porta ultrices, enim id eget leo congue, ' \
                     'venenatis leo, diam eu in vitae est hendrerit. Magna nec nisl faucibus, pretium aliquam arcu. ' \
                     'Eos lectus dapibus amet, egestas proin sed. Ipsum felis tincidunt iaculis in imperdiet donec, ' \
                     'velit nec posuere et ut. Luctus lobortis vestibulum feugiat, primis odio et eget, ' \
                     'malesuada felis, quam justo dui elit, elit interdum pretium. Dolor morbi montes, a eros luctus ' \
                     'facilisis ipsum, sed nam et sollicitudin. Amet dui lacus sapien a integer porta. Purus nisl, ' \
                     'sed vel donec. Pulvinar imperdiet sed dictum, nec non justo nullam, velit tellus, ' \
                     'lectus vestibulum consequat et at vel, pretium laoreet a enim a et et. Id neque gravida ' \
                     'pellentesque, tristique sem, lorem ante viverra, dolor mauris. Morbi aliquam rhoncus lacus ' \
                     'massa. Blandit integer ut tristique eget justo. Wisi vivamus et diam, metus dolor nunc ornare, ' \
                     'neque imperdiet. Eleifend est arcu, praesent tincidunt cras eleifend suscipit pulvinar, ' \
                     'nulla leo sed vel in scelerisque. Libero facilisi. Volutpat in. Enim turpis mauris sed nunc ' \
                     'dolorum erat, nascetur nunc suspendisse dapibus duis repellendus, suscipit feugiat nullam vel ' \
                     'vestibulum, lobortis vel et ipsum nisl. Integer pharetra vel pharetra bibendum nec, ' \
                     'ac ut dignissim, ac praesent rutrum quisque massa iaculis, a cras nullam suspendisse, ' \
                     'gravida commodo quis rhoncus. Pulvinar lorem fermentum, mauris fermentum voluptatem lacus. ' \
                     'Donec urna tempor eget lacus, feugiat aliquam consequat ullamcorper adipiscing, ' \
                     'integer vulputate eget, blandit fusce vel nec dolor lectus. Adipiscing wisi ultricies ' \
                     'similique, scelerisque eget dolor fringilla taciti donec. Nec nisl, vel dui porta amet sagittis ' \
                     'arcu sem, lobortis lacus quisque, cursus tristique nulla non fusce. Vestibulum pede eget ' \
                     'commodi mi et tincidunt, dolor morbi justo illum sit dui, venenatis cras felis. Luctus aliquet ' \
                     'rhoncus, magnis class aliquam sapien sit. Et a donec sit, mauris felis dapibus eget, ' \
                     'a lorem. Aliquam gravida metus, porta interdum dolor orci, vestibulum massa sed molestie ipsum ' \
                     'pretium in. In convallis laoreet ut arcu, aliquam lobortis mollis a ultrices, posuere nam nunc ' \
                     'justo, velit erat est sit porta nunc, pulvinar molestiae. Magna sodales vivamus, porttitor cras ' \
                     'accumsan consequat fringilla. Gravida ridiculus leo vestibulum leo ligula mauris, ' \
                     'pulvinar magna. Est nisl donec ad tellus ornare, sequi eros placerat nulla in. Magna tincidunt ' \
                     'purus lobortis ultrices sapien et, amet tempor, libero hendrerit integer cras, orci maecenas ' \
                     'libero. Vestibulum velit wisi et rutrum egestas, donec nec morbi platea pharetra eget. Ligula ' \
                     'sapien dolor ut accumsan dui luctus, dictum turpis odio consequat consequat quis, sed ligula ' \
                     'gravida dapibus tincidunt a, tristique nulla, eget aliquam eget tempus sociis. Adipiscing ' \
                     'dapibus ligula parturient, massa nec leo pretium. Blandit a sed facilisis pellentesque sit at, ' \
                     'pede gravida eros vitae ante ornare. Rutrum mattis vel pretium, non quis aliquet lectus, ' \
                     'aperiam in, nec gravida nibh pellentesque. Mauris fermentum fermentum rutrum vel, et viverra ' \
                     'accumsan nonummy pede. Tempor varius vestibulum mattis in, ac adipiscing volutpat habitant, ' \
                     'unde nunc imperdiet vivamus, nec imperdiet sapien vestibulum erat cursus, sed purus in ' \
                     'eleifend. Sit nunc auctor id. Porta vivamus quis cursus, tempor dolor vitae sed et urna eget, ' \
                     'mauris metus vivamus viverra, vitae arcu, phasellus sunt. Erat tortor morbi volutpat ante, ' \
                     'in sollicitudin, rhoncus facilisis sapien vivamus sollicitudin, at eget eu arcu libero ' \
                     'volutpat. Dui mauris in ipsum ligula, nostra urna sed nonummy porta nunc, fermentum sagittis ' \
                     'amet placerat egestas nam ipsum, adipiscing enim est architecto vel blandit. Duis metus lacus ' \
                     'malesuada felis, at cursus quam in viverra enim pede, dolor elit bibendum a amet a. Nunc augue ' \
                     'faucibus purus diam amet. Sagittis erat urna, venenatis iure tempus a sit non, ' \
                     'aliquam dignissim libero consectetuer quis ligula, elit praesent. Diam malesuada elementum ' \
                     'molestie eros. Adipiscing culpa sem nisl vitae, accumsan sed lacus, egestas odio et, ' \
                     'eleifend pede vel libero phasellus, et aliquam consectetuer dignissim eget. Fringilla est, ' \
                     'nulla malesuada, eros odio cum, magnis neque mauris consequat dui volutpat nunc. Condimentum ' \
                     'tellus, tempor nascetur amet nulla ullamcorper, duis at aliquam magna lacus, consequat ac ' \
                     'tincidunt cursus elit interdum, eleifend in libero quaerat. Tortor convallis est. Ultrices id ' \
                     'aliquam lorem. Vulputate est. Felis consectetuer ac interdum quis sit, sollicitudin eros nulla ' \
                     'proin enim, scelerisque dui et, elementum duis proin. Nunc sit arcu accumsan elementum mi ' \
                     'euismod, mollis tortor rutrum ut, ipsum luctus ut in lorem. Leo nec condimentum suscipit ' \
                     'ullamcorper sit ultrices, turpis sit justo sed porttitor faucibus, eget sed. Vitae condimentum ' \
                     'faucibus laborum nunc, volutpat cursus sodales quis vel, in porta recusandae integer nisl nec ' \
                     'in, aliquam sed non dictumst tellus mauris vivamus. '
        p2.blog_post = True
        p2.hidden = False
        p2.comments_closed = False
        p2.number_of_comments = 0
        p2.save()

        c1 = Comment()
        c1.author = author
        c1.post = p1
        c1.date = datetime(2017, 5, 10, 10)
        c1.content = 'Bardzo swietny artykul!'
        c1.author_name = ''
        c1.author_email = ''
        c1.taken_down = False
        p1.refresh_from_db()
        p1.number_of_comments += 1
        p1.save()
        c1.save()

        c2 = Comment()
        c2.post = p1
        c2.date = datetime(2017, 5, 10, 11)
        c2.content = 'E tam, do bani!'
        c2.author_name = 'Jaroslaw Kaczynski'
        c2.author_email = 'jarek@rzad.gov.pl'
        c2.taken_down = False
        p1.refresh_from_db()
        p1.number_of_comments += 1
        p1.save()
        c2.save()

        c3 = Comment()
        c3.post = p2
        c3.date = datetime(2017, 5, 10, 12, 21, 55)
        c3.content = 'English? Do you speak it?'
        c3.author_name = 'Donald Tusk'
        c3.author_email = 'tusku@ec.gov.eu'
        c3.taken_down = False
        p2.refresh_from_db()
        p2.number_of_comments += 1
        p2.save()
        c3.save()

        for i in range(0, 30):
            p = Post()
            p.author = author
            p.created = datetime(2014, 5, 10, 20, 22, 1)
            p.edited = datetime(2014, 5, 10, 21, 31)
            p.language = 'en'
            p.title = f'Dummy title {i}'
            p.content = f'Dummy content{i}'
            p.blog_post = True
            p.hidden = False
            p.comments_closed = False
            p.number_of_comments = 0
            p.save()
