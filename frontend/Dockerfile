# 1. PHP와 Apache가 포함된 공식 이미지 사용
FROM php:8.1-apache

# 2. 로컬 'frontend' 디렉토리의 파일을 Apache의 웹 루트 디렉토리로 복사
COPY . /var/www/html/

# 3. Apache 설정이 변경될 필요가 있으면 추가로 설정
# 예: 특정 .htaccess 파일, PHP.ini 설정 등
# COPY ./php.ini /usr/local/etc/php/

# 4. Apache 서버 실행 (이미지 내에 기본적으로 설정됨)
CMD ["apache2-foreground"]
