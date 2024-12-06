# 1. PHP-Apache 기본 이미지 사용
FROM php:8.1-apache

# 2. 작업 디렉터리 설정 (Apache의 루트 디렉터리로)
WORKDIR /var/www/html/

# 3. PHP 파일을 컨테이너로 복사
COPY . .

# 4. 80번 포트 오픈 (Apache 기본 포트)
EXPOSE 80
