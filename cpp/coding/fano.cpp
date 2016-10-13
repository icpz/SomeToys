#include <cstdio>
#include <algorithm>
#include <numeric>
#include <vector>
#include <iterator>
#include <string>
#include <cmath>
#include <map>
using namespace std;

using NodeType = pair<int, float>;
template<class _Iter>
void generateCode(_Iter first, _Iter last, map<int, string> &result);

int main() {
    vector<float> freq{0.2, 0.19, 0.18, 0.17, 0.15, 0.1, 0.01};
    map<int, string> result;
    vector<NodeType> nodes;

    transform(freq.begin(), freq.end(), back_inserter(nodes), [](float p) {
                static int i;
                return make_pair(i++, p);
            });

    sort(nodes.begin(), nodes.end(), [](const auto &a, const auto &b) { return a.second > b.second; });
    generateCode(nodes.begin(), nodes.end(), result);

    float avg = 0.0;
	puts("sig       p(x)     W            K");
    puts("---------------------------------");
    for (const auto &line : result) {
        printf("%-6d    %-6g   %-11s  %-3lu\n", line.first, freq[line.first], line.second.c_str(), line.second.size());
        avg += freq[line.first] * line.second.size();
    }
    puts("---------------------------------");
    printf("avg(K) = %g sym/sig\n", avg);

    return 0;
}

template<class _Iter>
_Iter partitionHalf(_Iter first, _Iter last) {
    auto half = accumulate(first, last, 0.0, [](float a, const auto &b) { return a + b.second; }) / 2;
    _Iter middle = first;
    float tsum = 0.0;
    while (tsum < half) {
        tsum += middle++->second;
    }
    if (fabs(tsum - (middle - 1)->second - half) < fabs(tsum - half)) --middle;
    return middle;
}

template<class _Iter>
void generateCode(_Iter first, _Iter last, map<int, string> &result) {
    if (next(first) == last) return;
    _Iter middle = partitionHalf(first, last);
    for (int i = 0; i < distance(first, last); ++i) {
        result[(first + i)->first].push_back('0' + (i >= distance(first, middle) ? 1 : 0));
    }
    generateCode(first, middle, result);
    generateCode(middle, last, result);
}

