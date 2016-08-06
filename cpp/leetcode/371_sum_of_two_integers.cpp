#include <iostream>
using namespace std;

class Solution {
public:
    int getSum(int a, int b) {
        const int bitcount = 8 * sizeof a;
        int c = 0;
        int r = 0;
        int i = 1;
        while (i) {
            int ta = a & 1;
            int tb = b & 1;
            r >>= 1;
            r &= ~(1 << (bitcount - 1));
            r |= (ta ^ tb ^ c) << (bitcount - 1);
            c = (ta & tb) | (tb & c) | (ta & c);
            a >>= 1;
            b >>= 1;
            i <<= 1;
        }
        return r;
    }
};

int main() {
    Solution s;
    cout << s.getSum(1, 2) << endl;
    cout << s.getSum(10, 345) << endl;
    return 0;
}

