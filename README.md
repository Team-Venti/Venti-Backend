
# VENTI

## 프로젝트 설명

<img src="/img/project_detail.png" width="40%" height="50%"></img>

**이벤트 및 할인 정보 모음 플랫폼**

## 핵심 기능

<img src="/img/func1.png" width="30%" height="20%"></img> <img src="/img/func2.png" width="30%" height="20%"></img> <img src="/img/func3.png" width="30%" height="20%"></img>

- 필터링

    33개의 브랜드와 200개에 달하는 이벤트 중 원하는 브랜드와 이벤트만 골라볼 수 있습니다. 

- 당신을 위한 이벤트

    당신이 좋아할 이벤트를 벤티에서 추천해드려요.

- 알림

    구독한 브랜드들의 알림을 받아보세요!

    새로 이벤트가 등록될 때, 좋아한 이벤트가 마감되기 전 알람이 발송됩니다. 

## Architecture

<img src="/img/architecture.png"></img>

- Django

    > 파이썬으로 작성된 오픈 소스 웹 프레임워크

- Docker

    > 리눅스의 응용 프로그램들을 프로세스 격리 기술들을 사용해 컨테이너로 실행하고 관리하는 오픈 소스 프로젝트

- Database

    **배포 전** : 
    > MySQL

    **배포 후** :
    > Amazon RDS
      : User 정보, 이벤트, 브랜드 정보 저장
    > Amazon S3 
      : 이미지 저장

     

- CI

    > - Travis + Github + Docker hub
      : github 업로드 시 Image Build 후 Docker hub에 자동 업로드

- Deploy

    > - AWS EC2

- Frontend
    > [Frontend](https://github.com/Team-Venti/Venti-Frontend)

## ERD

<img src="/img/erd.png"></img>

## Package

```jsx
Django==3.1.4
django-allauth==0.45.0
django-cors-headers
django-filter==2.4.0
django-rest-auth==0.9.5
djangorestframework==3.12.4
djangorestframework-jwt==1.11.0
drf-yasg==1.20.0
gunicorn==20.0.4
jsonify==0.5
oauthlib==3.1.1
packaging==21.0
Pillow==8.3.1
PyJWT==1.7.1
PyMySQL==1.0.2
pyparsing==2.4.7
requests-oauthlib==1.3.0
sqlparse==0.4.1
boto3
django-storages
```

## Contact Us

* [김현진](https://github.com/gimkuku) - jwt, eventforyou, 마감알림, 도커, CI&CD, AWS

* [이준기](https://github.com/Jun-k0) - ERD, MYVENTI, 검색, 등록알림, 배너, 필터링
