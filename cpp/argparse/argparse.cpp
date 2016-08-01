#include "argparse.h"
#include <algorithm>

ArgParse::ArgParse(int argc, char **argv) {
    for (int i = 1; i < argc; ++i)
        tokens.push_back(argv[i]);
}

bool ArgParse::hasArg(std::string arg) const {
    return std::end(tokens) != std::find(std::begin(tokens), std::end(tokens), arg);
}

const std::string & ArgParse::getArg(std::string arg) const {
    auto itr = std::find(std::begin(tokens), std::end(tokens), arg);
    if (itr != std::end(tokens) && ++itr != std::end(tokens))
        return *itr;
    return emptyArg;
}

