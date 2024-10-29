import subprocess
import json
import time

sca = 1
while True:
    # cpu % 아래로 곤두박질 치면 scale out : docker container 개수를 늘린다. in : 개수를 줄인다.
    r=subprocess.run(["docker","stats","samdul-blog-1","--no-stream","--format","{{ json .}}"],
            capture_output=True, text=True)
    # {"BlockIO":"0B / 0B","CPUPerc":"0.01%","Container":"samdul-blog-1","ID":"710c301a218e","MemPerc":"0.32%","MemUsage":"24.51MiB / 7.543GiB","Name":"samdul-blog-1","NetIO":"1.32kB / 0B","PIDs":"82"}
    #j = json.loads(r.stdout.decode("utf-8"))
    j = json.loads(r.stdout)
    print(j)
    per = float(j["CPUPerc"][:-1])

    if per > 50.00: # 만약 cpu % 가 특정 값을 넘어간다면
        print(f"Container가 임계값을 넘었습니다. 현재 컨테이너 개수 : {sca}")
        sca += 1
        subprocess.run(["docker", "compose", "scale", f"blog={sca}"])
    elif per <= 50.00 and sca > 1:
        print(f"Container가 필요 이상으로 많습니다. 현재 컨테이너 개수 : {sca}")
        sca -= 1
        subprocess.run(["docker", "compose", "scale", f"blog={sca}"])

    time.sleep(5)
