import subprocess
import re

def list_used_ports():
    print("[i] 현재 사용 중인 포트 목록:\n")
    try:
        result = subprocess.check_output('netstat -ano', shell=True, encoding='cp949')  # ✅ 인코딩 수정
        lines = result.strip().split('\n')
        port_info = {}

        for line in lines:
            match = re.search(r'TCP\s+[\[\]:.\d]+:(\d+)\s+[\[\]:.\d]+:(\d+|\*)\s+\S+\s+(\d+)', line)
            if match:
                local_port = match.group(1)
                pid = match.group(3)
                port_info[local_port] = pid

        if not port_info:
            print("  [!] 사용 중인 TCP 포트를 찾을 수 없습니다.")
        else:
            for port, pid in sorted(port_info.items(), key=lambda x: int(x[0])):
                print(f"  포트: {port}  →  PID: {pid}")

        return port_info

    except subprocess.CalledProcessError as e:
        print("[-] 포트 정보를 가져오는 데 실패했습니다.")
        return {}
    except UnicodeDecodeError as e:
        print("[-] 인코딩 문제로 netstat 출력 해석에 실패했습니다.")
        return {}

def kill_pid(pid):
    try:
        subprocess.check_call(f'taskkill /PID {pid} /F', shell=True)
        print(f"[+] PID {pid} 종료 성공")
    except subprocess.CalledProcessError:
        print(f"[-] PID {pid} 종료 실패")

def main():
    port_info = list_used_ports()
    if not port_info:
        return

    print("\n[i] 종료할 포트 번호를 입력하세요.")
    port = input("포트 번호: ").strip()

    pid = port_info.get(port)
    if pid:
        confirm = input(f"포트 {port}를 사용 중인 PID {pid}를 종료할까요? (y/n): ").lower()
        if confirm == 'y':
            kill_pid(pid)
        else:
            print("[i] 작업이 취소되었습니다.")
    else:
        print(f"[!] 포트 {port}를 사용 중인 프로세스를 찾을 수 없습니다.")

if __name__ == '__main__':
    main()
