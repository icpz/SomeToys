#include <cmath>
#include <cstdio>
#include <vector>
#include <numeric>
#include <string>
#include <iterator>
using namespace std;

using NodeType = pair<int, float>;

string getbits(float p, int n);

int main() {
    vector<float> freq{0.2, 0.19, 0.18, 0.17, 0.15, 0.1, 0.01};
    vector<float> pa{0.0};
    vector<NodeType> nodes;

    transform(freq.begin(), freq.end(), back_inserter(nodes), [](float p) {
            static int i;
            return make_pair(i++, p);
        });
    sort(nodes.begin(), nodes.end(), [](const auto &a,  const auto &b) { return a.second > b.second; });
    transform(nodes.begin(), nodes.end(), freq.begin(), [](const auto &p) { return p.second; });
    partial_sum(freq.begin(), freq.end(), back_inserter(pa));

    puts("sig       p(x)     W            K");
    puts("---------------------------------");
    
    float avg = 0.0;
    for (size_t i = 0; i < nodes.size(); ++i) {
        int n = ceil(-log2(nodes[i].second));
        string word = getbits(pa[i], n);
        printf("%-6d    %-6g   %-11s  %-3lu\n", nodes[i].first, freq[nodes[i].first], word.c_str(), word.size());
        avg += word.size() * freq[nodes[i].first];
    }

    puts("---------------------------------");
    printf("avg(K) = %g sym/sig\n", avg);

    return 0;
}

string getbits(float p, int n) {
    string result;

    while (n--) {
        p -= floor(p);
        result.push_back(floor(p * 2) + '0');
        p *= 2;
    }

    return result;
}

