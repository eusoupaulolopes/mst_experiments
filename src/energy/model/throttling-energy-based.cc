
#include "throttling-energy-based.h"

#include "ns3/core-module.h"

#include <iostream>

using namespace ns3;

namespace ns3
{

EnergyBasedThrottling::EnergyBasedThrottling(double bufferSize)
    : m_bufferSize(bufferSize),
      m_currentEnergy(bufferSize),
      m_lastTime(Simulator::Now()),
      m_throttlingMode(ThrottlingMode::NORMAL),
      tot_denied(0)
{
    m_availableTokens = getMaxRequestsPerSecond();
}

std::string
EnergyBasedThrottling::getThrottleMode()
{
    if (m_throttlingMode == ThrottlingMode::NORMAL)
        return "NORMAL";
    else if (m_throttlingMode == ThrottlingMode::CONSERVATIVE)
        return "CONSERVATIVE";
    else if (m_throttlingMode == ThrottlingMode::CRITICAL)
        return "CRITICAL";
    return "SLEEP";
}

void
EnergyBasedThrottling::updateEnergyLevel(double currentEnergy)
{
    m_currentEnergy = currentEnergy;
    updateThrottlingMode(); // Atualiza o modo de throttling conforme o nível de energia
}

bool
EnergyBasedThrottling::canProceed()
{
    Time now = Simulator::Now();
    Time elapsed = now - m_lastTime;

    // Recarrega tokens com base na taxa do modo atual
    if (elapsed.GetSeconds() >= 1.0)
    {
        m_availableTokens = getMaxRequestsPerSecond();
        m_lastTime = now;
    }

    if (m_availableTokens > 0 || m_throttlingMode == ThrottlingMode::NORMAL)
    {
        if (m_throttlingMode != ThrottlingMode::NORMAL)
        {
            --m_availableTokens;
        }
        return true;
    }
    tot_denied++;
    return false;
}

int
EnergyBasedThrottling::getTotalthrottled()
{
    return tot_denied;
}

void
EnergyBasedThrottling::updateThrottlingMode()
{
    double energyPercentage = m_currentEnergy / m_bufferSize;
    ThrottlingMode curr = m_throttlingMode;
    if (energyPercentage >= 0.7)
    {
        m_throttlingMode = ThrottlingMode::NORMAL;
    }
    else if (energyPercentage >= 0.3 && energyPercentage < 0.7)
    {
        m_throttlingMode = ThrottlingMode::CONSERVATIVE;
    }
    else if (energyPercentage >= 0.1 && energyPercentage <0.3)
    {
        m_throttlingMode = ThrottlingMode::CRITICAL;
    }
    else
    {
        m_throttlingMode = ThrottlingMode::SLEEP;
    }

    if (curr != m_throttlingMode)
    {
        m_availableTokens = getMaxRequestsPerSecond();
    }
}

int
EnergyBasedThrottling::getMaxRequestsPerSecond() const
{
    switch (m_throttlingMode)
    {
    case ThrottlingMode::NORMAL:
        return -1; 
    case ThrottlingMode::CONSERVATIVE:
        return 8; 
    case ThrottlingMode::CRITICAL:
        return 5; 
    default:
        return 0;
    }
}

} // namespace ns3
