#include <iostream>
#include <fstream>
#include <cstring>
#include <string>
#include <algorithm>
#include <iterator>
#include <numeric>

int encode(const std::string &meta, std::string &res);
int decode(const std::string &enc, std::string &meta);
void printUsage();
void printResult(std::ostream &__os, const std::string &ostr, bool crlf);

int main(int argc, char *argv[]){

    if(argc <= 2){
        printUsage();
        return 0;
    }

    std::string inSeq{argv[2]};
    std::string outSeq;
    bool crlf = false;

    if(std::strcmp(argv[2], "-i") == 0){
        std::ifstream ifs(argv[3], std::ios::binary);
        if(!ifs){
            std::cout << "No such file." << std::endl;
            return 0;
        }
        inSeq.clear();
        std::copy(std::istreambuf_iterator<char>(ifs),
                  std::istreambuf_iterator<char>(),
                  std::back_inserter(inSeq));
        ifs.close();
    }

    if(std::strcmp(argv[1], "-d") == 0)
        decode(inSeq, outSeq);
    else if(std::strcmp(argv[1], "-e") == 0){
        encode(inSeq, outSeq);
        crlf = true;
    } else {
        printUsage();
        return 0;
    }

    if(argc >= 5 && std::strcmp(argv[4], "-o") == 0){
        if(std::strlen(argv[5]) <= 0){
            printUsage();
            return 0;
        }
        std::ofstream ofs(argv[5], std::ios::binary);
        printResult(ofs, outSeq, crlf);
    } else
        printResult(std::cout, outSeq, crlf);

    return 0;
}

void printUsage(){
    std::cout << "Usage: program -d|-e metadata|[-i filename] [-o filename]\n" << std::endl;
}

void printResult(std::ostream &__os, const std::string &ostr, bool crlf){
    int c = ostr.size() / 76;
    auto itr = ostr.cbegin();
    std::ostream_iterator<char> oitr{__os, ""};

    for(int i = 0; i < c; ++i){
        std::copy_n(itr, 76, oitr);
        itr += 76;
        if(crlf) __os << std::endl;
    }
    if(itr < ostr.cend())
        std::copy(itr, ostr.cend(), oitr);
}

int encode(const std::string &meta, std::string &res){
    static const std::string table = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
    static const char *tail = "==";
    char buf[4] = "";
    int *p = reinterpret_cast<int *>(&buf[0]);
    size_t len = meta.size();
    size_t commonlen = len - len % 3;
    const char *pmeta = meta.c_str();
    const char *itr = pmeta;

    res.clear();
    while(itr - pmeta < commonlen){
        buf[3] = *itr++;
        buf[2] = *itr++;
        buf[1] = *itr++;
        res.push_back(table[(*p >> 26) & 0x3F]);
        res.push_back(table[(*p >> 20) & 0x3F]);
        res.push_back(table[(*p >> 14) & 0x3F]);
        res.push_back(table[(*p >> 8) & 0x3F]);
    }
    if(commonlen == len)
        return 0;
    *p = 0;
    if(itr - pmeta < len)
        buf[3] = *itr++;
    if(itr - pmeta < len)
        buf[2] = *itr;
    res.push_back(table[(*p >> 26) & 0x3F]);
    res.push_back(table[(*p >> 20) & 0x3F]);
    if(buf[2])
        res.push_back(table[(*p >> 14) & 0x3F]);
    res += tail + (len % 3) - 1;
    return 0;
}

void filtCRLF(std::string &str){
    std::string buf;
    std::copy_if(str.begin(), str.end(), std::back_inserter(buf),
                    [](char c){ return c != '\n' && c != '\r';});
    str.swap(buf);
}

int decode(const std::string &penc, std::string &meta){
    static const auto table = [](int c){
        size_t r = 0;
        switch(c >> 4){
        case 2:
            r = 62 + ((c >> 2) & 1);
            break;
        case 3:
            r = 52 + c - '0';
            break;
        case 6:
        case 7:
            r = 26 - 'a' + 'A';
        case 4:
        case 5:
            r += c - 'A';
            break;
        default:
            r = 0;
            break;
        }
        return r;
    };
    
    std::string enc = penc;
    filtCRLF(enc);

    if(enc.size() % 4)
        return 1;
    
    char buf[4] = "";
    int *p = reinterpret_cast<int *>(&buf[0]);
    
    meta.clear();
    size_t i;
    for(i = 0; i  < enc.size() - 4; i += 4){
        *p = table(enc[i]);
        *p = (*p << 6) | table(enc[i + 1]);
        *p = (*p << 6) | table(enc[i + 2]);
        *p = (*p << 6) | table(enc[i + 3]);
        meta.push_back(buf[2]);
        meta.push_back(buf[1]);
        meta.push_back(buf[0]);
    }
    *p = table(enc[i]);
    *p = (*p << 6) | table(enc[i + 1]);
    *p = (*p << 6) | table(enc[i + 2]);
    *p = (*p << 6) | table(enc[i + 3]);
    meta.push_back(buf[2]);
    if(enc[i + 2] != '=')
        meta.push_back(buf[1]);
    if(enc[i + 3] != '=')
        meta.push_back(buf[0]);
    return 0;
}

