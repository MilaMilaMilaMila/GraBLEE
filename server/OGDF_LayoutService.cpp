#include <ogdf/energybased/FMMMLayout.h>
#include <ogdf/fileformats/GraphIO.h>

#include <string>
#include <fstream>
#include <sstream>
#include <map>

using namespace ogdf;

std::map<std::string, std::string> ParseKeyValuePairs(const std::string& file_path) {
    std::map<std::string, std::string> paramsValue; // итоговый map
    std::ifstream infile(file_path); // открытие файла
    std::string line;

    if (!infile) {
        std::cout << "Unable to open file";
        return paramsValue;
    }

    while (std::getline(infile, line)) // чтение построчно
    {
        std::istringstream iss(line);
        std::string key, value;
        if (std::getline(std::getline(iss, key, ':'), value)) // разбиение на пару ключ-значение
        {
            paramsValue[key] = value; // добавление пары в map
        }
    }
    return paramsValue;
}

int main(int argc, char *argv[])
{
    if(argc != 3) {
        std::cout << "run program with arguments: path to the .gml graph and path to the .txt layout parameters." << std::endl;
        return 0;
    }
    std::string graphFilePath = argv[1];
    std::string paramFilePath = argv[2];

    std::map<std::string, std::string> key_value_pairs = ParseKeyValuePairs(paramFilePath);

    Graph G;
    GraphAttributes GA(G);
    if (!GraphIO::read(G, graphFilePath)) {
        std::cerr << "Could not " << graphFilePath << std::endl;
        return 1;
    }

    for (node v : G.nodes)
        GA.width(v) = GA.height(v) = 5.0;

    FMMMLayout fmmm;

    fmmm.useHighLevelOptions(true);
    fmmm.unitEdgeLength(155.0);
    fmmm.newInitialPlacement(true);
    fmmm.qualityVersusSpeed(FMMMOptions::QualityVsSpeed::GorgeousAndEfficient);

    fmmm.call(GA);
    GraphIO::write(GA, graphFilePath, GraphIO::writeGML);
    GraphIO::write(GA, "../test.svg", GraphIO::drawSVG);

    return 0;
}