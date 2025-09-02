import time
import subprocess
import hashlib

def main():
    startTime = time.time()
    gang = set()
    h2pass = {} #hash password to password
    u2hash = {} #username to hashed passwords

    with open('gang') as myfile2:
        gang.update(line.strip() for line in myfile2)
    
    with open('PwnedPWs100k') as myfile:
        for pwds in myfile:
            pwds = pwds.strip()
            for i in range(100):
                numpswd = f'{pwds}{i:02d}'
                hashedpswd = hashlib.sha256(numpswd.encode("utf-8")).hexdigest()
                h2pass[hashedpswd] = numpswd
                

    with open('HashedPWs') as myfile3:
        for line in myfile3:
            name, namehash = line.strip().split(",")
            if name in gang:
                if namehash != '2ca53f6b9204a9cdd781131f46765514581be0f0a6fccd053aaab3ca8f3a9d5a':
                    #John is in the file twice, this hash is wrong
                    u2hash[name] = namehash
             
    for name, namehash in u2hash.items():
        if namehash in h2pass:
            fpassword = h2pass[namehash]
            myvar = subprocess.run(['python3', 'Login.pyc', name, fpassword], capture_output = True, text = True)
            print(name, fpassword, namehash)
            if "success" in myvar.stdout:
                print('success', name, fpassword, namehash)
                break

    endTime = time.time()
    timeTaken = endTime - startTime
    print("Time Taken: " + str(timeTaken))

if __name__ == "__main__":
    main()
