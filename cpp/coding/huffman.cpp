#include <iostream>
#include <algorithm>
#include <vector>
#include <string>
#include <numeric>
#include <iterator>
using namespace std;

template<class T>
struct HuffmanNode {
    float p;
    T sym;
    HuffmanNode *left, *right;

    HuffmanNode(T sym, float p, HuffmanNode *l = nullptr, HuffmanNode *r = nullptr)
        :p(p), sym(sym), left(l), right(r) { }

    ~HuffmanNode() {
        delete left;
        delete right;
    }

};

using NodeType = HuffmanNode<int>;
void getHuffmanCode(vector<pair<int, string>> &result, NodeType *root, string code = "");

int main() {
    vector<float> freq{0.2, 0.19, 0.18, 0.17, 0.15, 0.1, 0.01};// {0.4, 0.18, 0.1, 0.1, 0.07, 0.06, 0.05, 0.04};
    vector<NodeType *> nodes;
    auto cmp = [](NodeType *a, NodeType *b) {
        if (a->p == b->p) {
            if (a->sym == -1) return false;
            if (b->sym == -1) return true;
            return a->sym < b->sym;
        }
        return a->p > b->p;
    };

    transform(freq.begin(), freq.end(), back_inserter(nodes), [](float p){
                static int i = 1;
                return new NodeType(i++, p);
            });

    auto heapEnd = nodes.end();
    make_heap(nodes.begin(), heapEnd, cmp);
    while (heapEnd != next(nodes.begin())) {
        pop_heap(nodes.begin(), heapEnd--, cmp);
        NodeType *right = *heapEnd;
        pop_heap(nodes.begin(), heapEnd--, cmp);
        NodeType *left = *heapEnd;
        NodeType *root = new NodeType(-1, left->p + right->p, left, right);
        nodes.erase(heapEnd, nodes.end());
        nodes.push_back(root);
        heapEnd = nodes.end();
        push_heap(nodes.begin(), heapEnd, cmp);
    }
    vector<pair<int, string>> result;
    getHuffmanCode(result, nodes[0]);
    sort(result.begin(), result.end(), [](auto a, auto b) {return a.first < b.first;});
    for (const auto &line : result) {
        cout << line.first << " " << freq[line.first - 1] << " " << line.second << endl;
    }
    return 0;
}

void getHuffmanCode(vector<pair<int, string>> &result, NodeType *root, string code) {
    if (!root->left && !root->right) {
        result.emplace_back(root->sym, code);
        return;
    }

    getHuffmanCode(result, root->left, code + "0");
    getHuffmanCode(result, root->right, code + "1");
}

