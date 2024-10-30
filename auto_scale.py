import subprocess
import json
import time

import yaml
import requests
import os

api_url = 'https://notify-api.line.me/api/notify'
key = os.getenv('LINE_NOTI_PATH')

# yml 파일을 읽어서 임계값 가져오기
with open('docker-compose.yml') as f:
    file = yaml.full_load(f)
lim = file['services']['blog']['deploy']['resources']['limits']['cpus']

start = 0
sca = 1
while True:
    # cpu % 아래로 곤두박질 치면 scale out : docker container 개수를 늘린다. in : 개수를 줄인다.
    r=subprocess.run(["docker","stats","samdul-blog-1","--no-stream","--format","{{ json .}}"],
            capture_output=True, text=True)
    # {"BlockIO":"0B / 0B","CPUPerc":"0.01%","Container":"samdul-blog-1","ID":"710c301a218e","MemPerc":"0.32%","MemUsage":"24.51MiB / 7.543GiB","Name":"samdul-blog-1","NetIO":"1.32kB / 0B","PIDs":"82"}
    #j = json.loads(r.stdout.decode("utf-8"))
    j = json.loads(r.stdout)
    per = float(j["CPUPerc"][:-1])
    print(f"현재 CPU 사용량은 {per}입니다.")

    if per > float(lim): # 만약 cpu % 가 특정 값을 넘어간다면
        if not start:
            start = time.time()
        else: # 넘은 적이 있다면?
            end = time.time()
            if end - start >= 60.00:
                print(f"Container가 임계값을 넘은지 1분이 지났습니다. 현재 컨테이너 개수 : {sca}")
                sca += 1
                subprocess.run(["docker", "compose", "scale", f"blog={sca}"])

                response = requests.post(api_url, headers = {'Authorization':'Bearer ' + key},
                        data = {'message' : 'Container Scale Out'})

    elif per <= float(lim) and sca > 1:
        start = 0
        print(f"Container가 필요 이상으로 많습니다. 현재 컨테이너 개수 : {sca}")
        sca -= 1
        subprocess.run(["docker", "compose", "scale", f"blog={sca}"])
        response = requests.post(api_url, headers = {'Authorization':'Bearer ' + key},
                        data = {'message' : 'Container Scale In'})

    time.sleep(10)
