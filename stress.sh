#!/bin/bash

#기본값 설정
#n=${1:-5}
#nn=${2:-1}
#
##요청 URL 설정
#url="http://localhost:8949/"
#
#for ((i=1; i<=n; i++)); do
#        echo "request #$i"
#        curl -I "$url"
#        echo ""
#        sleep "$nn"
#done

#!/bin/bash

# 기본값 설정
nn=${1:-1}

# 요청 URL 설정
url="http://localhost:8949/"

i=1
while true; do
    echo "request #$i"
    curl -I "$url"
    echo ""

    sleep "$nn"
    ((i++))
done

