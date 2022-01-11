#include <iostream>

#include "official.h"

std::vector<std::pair<int,int>> make_all_pair(std::vector<int> XN){
    std::vector<std::pair<int,int>> all_pair;
    for(size_t i=0; i<XN.size(); i++)
        for(size_t j=i+1; j<XN.size(); j++){
            std::pair<int,int> match(XN.at(i),XN.at(j));
            all_pair.push_back(match);
        }
    return all_pair;
}

std::vector<std::vector<std::vector<int>>> draw_all_quarter(std::vector<std::pair<int,int>> pair){
    std::vector<std::vector<std::vector<int>>> all_scenario;
    std::vector<std::vector<int>> scenario;
    std::vector<int> X1;
    std::vector<int> X2;
    std::vector<int> player_taken;

    for(size_t i=0; i<pair.size(); i++){
        X1.push_back(pair[i].first);
        X2.push_back(pair[i].second);
        player_taken.push_back(pair[i].first);
        player_taken.push_back(pair[i].second);
        for(size_t j=i+1; j<pair.size(); j++)
            if(std::find(player_taken.begin(), player_taken.end(), pair[j].first) != player_taken.end()
                    || std::find(player_taken.begin(), player_taken.end(), pair[j].second) != player_taken.end())
                continue;
            else{
                X1.push_back(pair[j].first);
                X2.push_back(pair[j].second);
                player_taken.push_back(pair[j].first);
                player_taken.push_back(pair[j].second);
                for(size_t k=j+1; k<pair.size(); k++)
                    if(std::find(player_taken.begin(), player_taken.end(), pair[k].first) != player_taken.end()
                            || std::find(player_taken.begin(), player_taken.end(), pair[k].second) != player_taken.end())
                        continue;
                    else{
                        X1.push_back(pair[k].first);
                        X2.push_back(pair[k].second);
                        player_taken.push_back(pair[k].first);
                        player_taken.push_back(pair[k].second);
                        for(size_t l=k+1; l<pair.size(); l++)
                            if(std::find(player_taken.begin(), player_taken.end(), pair[l].first) != player_taken.end()
                                    || std::find(player_taken.begin(), player_taken.end(), pair[l].second) != player_taken.end())
                                continue;
                            else{
                                X1.push_back(pair[l].first);
                                X2.push_back(pair[l].second);
                                scenario = {X1,X2};
                                all_scenario.push_back(scenario);
                                X1.pop_back();
                                X2.pop_back();
                            }
                        X1.pop_back();
                        X2.pop_back();
                        player_taken.pop_back();
                        player_taken.pop_back();
                    }
                X1.pop_back();
                X2.pop_back();
                player_taken.pop_back();
                player_taken.pop_back();
            }
        X1.pop_back();
        X2.pop_back();
        player_taken.pop_back();
        player_taken.pop_back();
    }
    return all_scenario;
}

std::vector<std::vector<std::vector<int>>> draw_all_semi(std::vector<std::pair<int,int>> pair){
    std::vector<std::vector<std::vector<int>>> all_scenario;
    std::vector<std::vector<int>> scenario;
    std::vector<int> X1;
    std::vector<int> X2;
    std::vector<int> player_taken;

    for(size_t i=0; i<pair.size(); i++){
        X1.push_back(pair[i].first);
        X2.push_back(pair[i].second);
        player_taken.push_back(pair[i].first);
        player_taken.push_back(pair[i].second);
        for(size_t j=i+1; j<pair.size(); j++)
            if(std::find(player_taken.begin(), player_taken.end(), pair[j].first) != player_taken.end()
                    || std::find(player_taken.begin(), player_taken.end(), pair[j].second) != player_taken.end())
                continue;
            else{
                X1.push_back(pair[j].first);
                X2.push_back(pair[j].second);
                scenario = {X1,X2};
                all_scenario.push_back(scenario);
                X1.pop_back();
                X2.pop_back();
            }
        X1.pop_back();
        X2.pop_back();
        player_taken.pop_back();
        player_taken.pop_back();
    }
    return all_scenario;
}




std::vector<std::vector<std::vector<int>>> draw_round(std::vector<int> XN){
    assert(XN.size() == 8 || XN.size() == 4 || XN.size() == 2);
    if(XN.size() == 8)
        return draw_all_quarter(make_all_pair(XN));
    else if(XN.size() == 4)
        return draw_all_semi(make_all_pair(XN));
    else if(XN.size() == 2){
        std::cout << XN.size();
        return {{{XN.at(0)},{XN.at(1)}}};
    }
}




