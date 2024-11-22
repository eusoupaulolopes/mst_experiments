#ifndef THROTTLING_FIXED_RATE_H
#define THROTTLING_FIXED_RATE_H

#include "ns3/core-module.h"
#include "ns3/throttling-strategy.h"

using namespace ns3;

class FixedRateThrottling {
private:
    int m_maxRequestsPerSecond; // Número máximo de requisições por segundo
    int m_availableTokens;      // Tokens disponíveis para requisições
    Time m_lastCheck; // Última vez que os tokens foram atualizados
    int tot_denied;
public:
    // Construtor 
    FixedRateThrottling(int maxRequestsPerSecond);

    // Verifica se uma requisição pode prosseguir com base na taxa permitida
    bool canProceed();
    int getTotalthrottled();

};

#endif 


