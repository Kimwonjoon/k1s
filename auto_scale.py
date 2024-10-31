import subprocess
import json
import time

import yaml
import requests
import os

#import pandas as pd

api_url = 'https://notify-api.line.me/api/notify'
key = os.getenv('LINE_NOTI_PATH')
#file_path = '/home/kimpass189/code/docker/k1s/data/cpu.csv'
#os.makedirs(os.path.dirname(file_path), exist_ok=True)

# yml 파일을 읽어서 임계값 가져오기
with open('docker-compose.yml') as f:
    file = yaml.full_load(f)
lim = file['services']['blog']['deploy']['resources']['limits']['cpus']

start = 0
sca = 1

cpu_list = [] # cpu 사용량 모음집

try:
    while True:
        # cpu % 아래로 곤두박질 치면 scale out : docker container 개수를 늘린다. in : 개수를 줄인다.
        r=subprocess.run(["docker","stats","samdul-blog-1","--no-stream","--format","{{ json .}}"],
                capture_output=True, text=True)
        # {"BlockIO":"0B / 0B","CPUPerc":"0.01%","Container":"samdul-blog-1","ID":"710c301a218e","MemPerc":"0.32%","MemUsage":"24.51MiB / 7.543GiB","Name":"samdul-blog-1","NetIO":"1.32kB / 0B","PIDs":"82"}
        #j = json.loads(r.stdout.decode("utf-8"))
        j = json.loads(r.stdout)
        per = float(j["CPUPerc"][:-1])
        print(f"현재 CPU 사용량은 {per}입니다.")

        cpu_list.append(per) # cpu 사용량 저장

        if per > float(lim): # 만약 cpu % 가 특정 값을 넘어간다면
            if not start:
                start = time.time()
            else: # 넘은 적이 있다면?
                end = time.time()
                if end - start >= 60.00:
                    print(f"Container가 임계값을 넘은지 1분이 지났습니다. 현재 컨테이너 개수 : {sca}")
                    sca += 1
                    start = 0 # scale out이 되면 시간 초기화
                    subprocess.run(["docker", "compose", "scale", f"blog={sca}"])
                    response = requests.post(api_url, headers = {'Authorization':'Bearer ' + key},
                            data = {'message' : 'Container Scale Out'})

        elif per <= float(lim) and sca > 1:
            # 내려간지 1분이 지나면 scale in인데....
            if not start:
                start = time.time()
            else:
                end = time.time()
                if end - start >= 60.00:
                    print(f"Container가 필요 이상으로 많습니다. 현재 컨테이너 개수 : {sca}")
                    sca -= 1
                    start = 0 # scale in이 된다면 시간 초기화
                    subprocess.run(["docker", "compose", "scale", f"blog={sca}"])
                    response = requests.post(api_url, headers = {'Authorization':'Bearer ' + key},
                                    data = {'message' : 'Container Scale In'})

        time.sleep(10)
except KeyboardInterrupt: # ctrl+c 로 종료한 경우
#    if os.path.exists(file_path): # 파일이 이미 있다면?
#        data = pd.read_csv(file_path)
#        new_data = pd.DataFrame({'cpu' : cpu_list})
#        con_data = pd.concat([data, new_data])
#        con_data.to_csv(file_path, index = False)
#    else: # 파일을 처음 만드는 경우
#        data = pd.DataFrame({'cpu' : cpu_list})
#        data.to_csv(file_path, index = False)
    print(f"종료!, 파일 경로는 {file_path} 입니다.")
