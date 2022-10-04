# Python DB API
 
파이썬에서 데이터베이스에 접근하기 위한 표준 API로 
Python DB API는 기본적으로 PEP249 인터페이스를 따르도록 권장하고 있습니다.

 
## PEP249
 
파이썬에서 명시하는 DBAPI v2.0에 대한 문서로
DB와 연결하는 파이썬 묘듈은 권장하는 내용에 따르도록 설계되어 있습니다.

![img1 daumcdn](https://user-images.githubusercontent.com/96939334/193818910-7e907918-6c98-4777-b094-d4298e1156bd.png)

위에는 PEP 249에 대한 설명입니다.
이를 통해 다양한 DB에대해서 동일하게 조작할 수 있도록 만들었다는 목적을 알 수 있습니다.
간단하게는 가이드라인이라고 생각하면 될 것 같습니다.

---

# SQLite

별도의 서버 필요없이 DB처리를 구현한 파일형DB로
__임베디드 SQL DB엔진을 말합니다.__
서버가 아니라 응용프로그램에 넣어 사용하는 가벼운 데이터베이스 관리 시스템으로 
빠르고, 사용하기 쉽다는 장점이 있습니다.

#SQLite 3

파이썬이 설치됨과 동시에 같이 설치가 되는 모듈로 데이터베이스 관리 모듈 중 하나라고 볼 수 있습니다.
SQLite에 대한 인터페이스를 제공하고 별도의 DB전용 프로그램이 없이 사용할 수 있습니다.
이제 SQLite3 사용법을 알아보도록 하겠습니다.

---

# DB 소통 과정 
 
1. 우선 splite3 모듈을 import 해야합니다.

import sqlite3
 

2. 파이썬에서 DB를 연결하기 위해서 connect()메소드를 활용합니다.

conn = sqlite3.connect('test.db')
conn은 DB와 연결된 하나의 세션을 보관합니다.

 

 

3. 해당 세션을 통해 DB와 소통하기 위한 cursur를 생성합니다.

cur = conn.cursor()
4. 코드 내에서 SQL쿼리로 테이블을 만들어줍니다.

cur.execute("""CREATE TABLE hamburger (
                name VARCHAR(32),
                price INT,
                kcal INT)
            """)
cursur의 excute 메소드를 사용해서 SQL 쿼리문을 넘겨줄 수 있습니다.

 

5. 테이블에 데이터를 추가합니다.

cur.execute("INSERT INTO hamburger VALUES ('버거킹', 13000, 878)")
 

6. 마지막으로 commit을 해주면됩니다.

conn.commit()
SQL 질의가 끝났다면 commit을 해야 DB가 업데이트 됩니다.

commit을 하기 전까진 DB에 데이터가 업데이트된 것이 아닌 임시로만 바뀐 것이므로 

위에서 만들어놓은 connection 객체인 conn을 통해 commit 합니다.

 

전체적인 코드입니다.

import sqlite3

conn = sqlite3.connnect('test.db')
cur = conn.cursor()

cur.execute("""CREATE TABLE hamburger (
                name VARCHAR(32),
                price INT,
                kcal INT)
            """)
cur.execute("INSERT INTO hamburger VALUES ('버거킹', 13000, 878)")

conn.commit()
 


실제로 만들어진 결과물을 확인할 수 있습니다.
