api_key = "#######################"
GITHUB_TOKEN = "######################"
HOSTNAME = "127.0.0.1"
# Mysql监听的端口号
PORT = 3306
# 连接Mysql的用户名
USERNAME = '####'
# 连接Mysql的密码
PASSWORD = '####'
# Mysql上创建的数据库名称
DATABASE = '####'

DB_URI = f"mysql+pymysql://{USERNAME}:{PASSWORD}@" \
         f"{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"
SQLALCHEMY_DATABASE_URI = DB_URI

test_urls = ['https://discuss.elastic.co/c/security-announcements.rss', 'http://xxlegend.com/atom.xml',
             'https://ethicalhackingguru.com/feed', 'https://awakened1712.github.io/feed.xml',

             'https://blog.binaryedge.io/rss',
             'https://www.contrastsecurity.com/security-influencers/rss.xml', 'https://xz.aliyun.com/feed',
             'https://www.leavesongs.com/feed', 'https://3gstudent.github.io/atom.xml',
             'https://rss.ricterz.me/hacktivity',
             'https://rss.packetstormsecurity.com/news/tags/hacker',
             'https://www.exploit-db.com/rss.xml', 'https://www.zdnet.com/topic/security/rss.xml',
             'https://www.zerodayinitiative.com/blog?format=rss',
             'http://seclists.org/rss/fulldisclosure.rss',
             'https://wechat2rss.xlab.app/feed/1800f529b600474a4cd0434c65654c483739e192.xml',
             'https://wechat2rss.xlab.app/feed/9da87fba8130d0c2dc52cc45b844f045227e06a7.xml',
             'https://wechat2rss.xlab.app/feed/09d2ae436c3aa6166353d53502096e1a957a808a.xml',
             'https://wechat2rss.xlab.app/feed/74ce3507f54a7a5145a4ddd6e4e3407fd76705b5.xml',
             'https://wechat2rss.xlab.app/feed/fd912d34201eea9dbaaa73e22bffee21636c0f9e.xml',
             'https://wechat2rss.xlab.app/feed/63688861efb2362716368e36b7f8b8b61d0394a9.xml',
             'https://wechat2rss.xlab.app/feed/1aa5b8c8e4fb27ccb905694f7563b5529cd12269.xml',
             'https://wechat2rss.xlab.app/feed/059ae07ca76f11c6e9f9fad7698ab205b3b039c8.xml',
             'https://wechat2rss.xlab.app/feed/3051a5bf0ae50996df7d16a2a9880c021a41d02a.xml',
             'https://wechat2rss.xlab.app/feed/4470030205d4d847065a2f0d26219b280b421440.xml',
             'https://wechat2rss.xlab.app/feed/27be924bf0d49a8d3ff45c0a85e9c6e94ba7a93c.xml',
             'https://wechat2rss.xlab.app/feed/f17b52a78a32b532f0d7729e6cf7d94a669c1d53.xml',
             'https://wechat2rss.xlab.app/feed/fb1486a83f41d2b3ab5758c9811936beaa762097.xml',
             'https://wechat2rss.xlab.app/feed/8c5d5f0004e7231abeb01dac49cac5da4ec6933d.xml',
             'https://wechat2rss.xlab.app/feed/9e9c3c70e598266a1ac993e50458a10a6d853eb7.xml',
             'https://wechat2rss.xlab.app/feed/7772ec79ac327394596861ae412fc25a823e09d0.xml',
             'https://wechat2rss.xlab.app/feed/aff52b9db3b57b1fcf24b40668d44baecd3da044.xml',
             'https://wechat2rss.xlab.app/feed/8defbaee147ce6fc812f5d1eedca61ea22ecf168.xml',
             'https://wechat2rss.xlab.app/feed/56ccecd04a64c0459442d07f30325218f8b4f210.xml',
             'https://wechat2rss.xlab.app/feed/a54132c52ec3e562fc896bf803a7fe0aa277bab7.xml',
             'https://wechat2rss.xlab.app/feed/7874947663d806190d77bdca6f8f6855f65a1b20.xml',
             'https://wechat2rss.xlab.app/feed/d5eb8577bf93aacdd7481ad0c3364939096b99a1.xml',
             'https://wechat2rss.xlab.app/feed/84fdb53acad07ab607128a9f387cefdee53809dd.xml',
             'https://wechat2rss.xlab.app/feed/956e0bcbfd7dc0ca5274a3489bd2cc03cda26907.xml',
             'https://wechat2rss.xlab.app/feed/77cfc87fa0e7200d7ef74c8956eca2e44fd6a4ec.xml',
             'https://wechat2rss.xlab.app/feed/b93962f981247c0091dad08df5b7a6864ab888e9.xml',
             'https://wechat2rss.xlab.app/feed/fe0f4b4ed13da1bd9296fe819c5770526ae910b0.xml',
             'https://wechat2rss.xlab.app/feed/1bbe066c89588a1aff71eb8b6a4446c7c422499f.xml',
             'https://wechat2rss.xlab.app/feed/e687678d6fc1dacb25e9191fd361250f538e45a1.xml',
             'https://wechat2rss.xlab.app/feed/792558edf818ce03d377d1d2677afb4d6537853d.xml',
             'https://wechat2rss.xlab.app/feed/7fc9f5344f14228ba49208282d844349f8afdee7.xml',
             'https://wechat2rss.xlab.app/feed/923c0e2f33b6d39c8a826a90f185725f0edb10e8.xml',
             'https://wechat2rss.xlab.app/feed/ac64c385ebcdb17fee8df733eb620a22b979928c.xml',
             'https://wechat2rss.xlab.app/feed/62ba31603ffe26b5a8eca9ddaa434ea612445c10.xml',
             'https://wechat2rss.xlab.app/feed/2f38aa5ec9e067b1d02196f5a50665f8ec23a4e4.xml',
             'https://wechat2rss.xlab.app/feed/ca9e6f3e905e64301c6f00a21f2e3f135df1e691.xml',
             'https://wechat2rss.xlab.app/feed/be2795d741304af2370cbf8d31d1e5d3675f8e85.xml',
             'https://wechat2rss.xlab.app/feed/869b4e387a017fdd76a56b965ee0ab22c2a52dc2.xml',
             'https://wechat2rss.xlab.app/feed/1bbf7fc5fac024226f86a1851c682253a7eae63f.xml',
             'http://russiansecurity.expert/feed/', 'https://hernan.de/feed.xml', 'https://paper.seebug.org/rss',
             'https://www.nextron-systems.com/feed',
             'https://0day.work/rss',
             'https://blog.rapid7.com/rss', 'https://securelist.com/feed',
             'https://www.helpnetsecurity.com/feed', 'https://blog.qualys.com/feed',
             'https://feeds.megaphone.fm/darknetdiaries', 'https://www.gosecure.net/feed',
             'http://blog.pi3.com.pl/?feed=rss2', 'https://security.tencent.com/index.php/feed/blog/0',
             'https://dozer.nz/feed.xml', 'https://blog.redforce.io/feed',
             'https://rss.packetstormsecurity.com/files/tags/exploit',
             'https://securitylab.github.com/advisories/feed.xml', 'https://senzee.net/index.php/feed/',
             'https://eaton-works.com/feed.atom', 'https://blog.assetnote.io/feed.xml', 'https://govuln.com/news/feed/']

