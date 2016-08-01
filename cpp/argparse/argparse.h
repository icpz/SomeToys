#ifndef __ARGPARSE_H__
#define __ARGPARSE_H__

#include <string>
#include <vector>

class ArgParse {
private:
    std::vector<std::string> tokens;
    static const std::string emptyArg;

public:
    ArgParse(int argc, char **argv);

    bool hasArg(std::string arg) const;
    const std::string & getArg(std::string arg) const;

};


const std::string ArgParse::emptyArg = std::string("");

#endif

