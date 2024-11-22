
#include "throttling-energy-based.h"
#include "throttling-energy-input-based.h"

#include "ns3/core-module.h"

#include <iostream>

using namespace ns3;

namespace ns3
{

EnergyInputBasedThrottling::EnergyInputBasedThrottling(double bufferSize, double recoveryRate)
    : m_bufferSize(bufferSize),
      m_currentEnergy(bufferSize),
      m_lastTime(Simulator::Now()),
      m_throttlingMode(ThrottlingMode::NORMAL),
      tot_denied(0),
      recoveryRate(recoveryRate),
      m_energyInput(0)
{
    m_availableTokens = getMaxRequestsPerSecond();
}

std::string
EnergyInputBasedThrottling::getThrottleMode()
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
EnergyInputBasedThrottling::updateEnergyLevel(double currentEnergy)
{
    if (currentEnergy > m_currentEnergy){
        m_energyInput = currentEnergy - m_currentEnergy;
    }
    m_currentEnergy = currentEnergy;

    updateThrottlingMode(); // Atualiza o modo de throttling conforme o nível de energia
}


bool
EnergyInputBasedThrottling::canProceed()
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
EnergyInputBasedThrottling::getTotalthrottled()
{
    return tot_denied;
}

void
EnergyInputBasedThrottling::updateThrottlingMode()
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
    else if (energyPercentage >= 0.1 && energyPercentage < 0.3)
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
EnergyInputBasedThrottling::getMaxRequestsPerSecond() const
{
    switch (m_throttlingMode)
    {
    case ThrottlingMode::NORMAL:
        return -1;
    case ThrottlingMode::CONSERVATIVE:
        return 8;
    case ThrottlingMode::CRITICAL:
        return 5;
    case ThrottlingMode::SLEEP:        
        return (m_energyInput / recoveryRate) -1 ;
    default:
        return 0;
    }
}



} // namespace ns3
