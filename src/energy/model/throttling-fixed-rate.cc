
#include "throttling-fixed-rate.h"

#include "ns3/core-module.h"

#include <iostream>

using namespace ns3;

FixedRateThrottling::FixedRateThrottling(int maxRequestsPerSecond)
    : m_maxRequestsPerSecond(maxRequestsPerSecond),
      m_availableTokens(maxRequestsPerSecond),
      tot_denied(0),
      m_lastCheck(Simulator::Now())
{
}

// Método para verificar se é possível realizar uma requisição
bool
FixedRateThrottling::canProceed()
{
    Time now = Simulator::Now();
    Time elapsed = now - m_lastCheck;

    // Recarrega todos os tokens a cada segundo
    if (elapsed.GetSeconds() >= 1.0)
    {
        m_availableTokens = m_maxRequestsPerSecond;
        m_lastCheck = now;
    }

    // Permite a requisição se há tokens disponíveis
    if (m_availableTokens > 0)
    {
        --m_availableTokens;
        return true;
    }
    tot_denied++;
    return false;
}

int
FixedRateThrottling::getTotalthrottled()
{
    return tot_denied;
}
