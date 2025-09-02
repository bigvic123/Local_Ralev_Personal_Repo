#include <iostream>
#include <windows.h>
using namespace std;

int main() {

    int    one_tone = 440;
    string one_name = "Fa";

    Beep(one_tone, 300);
    cout << one_name << endl;


    int    tones[8] = {261,  293,  329,  349,  392,   440,  493,   523};
    string names[8] = {"Do", "Re", "Mi", "Fa", "Sol", "La", "Si", "Do"};
    char     key[8] = {'A',   'S', 'D',   'F',  'H',   'J', 'K',   'L'};


    for (int number = 0; number < 8; number++){
        cout << names[number] << " ";
        Beep(   tones[number], 300);
        Sleep(100);
    }

    for (int number = 7; number >= 0; number--){
        cout << names[number] << " ";
        Beep(   tones[number], 300);
        Sleep(100);
    }

    cout << endl << endl;
    cout << "Play the piano now: ";
    while ('A' == 'A') {
        if (GetAsyncKeyState(VK_ESCAPE)) {
            break;
        }

        for (int number = 0; number < 8; number++) {

            if (GetAsyncKeyState(key[number])) {
                cout <<        names[number] << " ";
                Beep(          tones[number], 200);
            } /// end if

        }/// end for

        Sleep(50);

    }/// end while




    return 0;
}
